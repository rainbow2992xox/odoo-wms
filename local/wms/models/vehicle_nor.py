import datetime
import re
from odoo import models, fields
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import requests
import pytz

class Vehicle(models.Model):
    _name = "wms.vehicle.nor"

    carrier_plate_number = fields.Char(string="车牌号", required=True, size=32)
    enter_exit_time = fields.Datetime(string="进出入时间", required=True)
    enter_exit_type = fields.Selection([('0', '进入'), ('1', '出去')], string='出入类型', required=True, default='0',
                                       readonly=True)
    carrier_name = fields.Char(string="企业名称", required=True, size=32)
    visit_reason = fields.Char(string="访客事由", required=True, size=32)

    visitors = fields.One2many(
        'wms.vistor', 'vehicle_id',
        string='访客人员', copy=True)

    vehicle_out_id = fields.Integer(string="出厂记录ID", default=0)

    def id_check(self, id):
        r = requests.get("https://www.haoshudi.com/api/id/query/?userid=" + id)
        res = r.json()

        if not res['status']:
            return (res['status'], res['msg'])
        else:
            return (res['data']['isIdCard'], "请核对")

    def plate_number_check(self, plate_number):
        pattern_str = '([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]{1}[A-Z]{1}(([A-HJ-NP-Z0-9]{5}[DF]{1})|([DF]{1}[A-HJ-NP-Z0-9]{5})))|([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]{1}[A-Z]{1}[A-HJ-NP-Z0-9]{4}[A-HJ-NP-Z0-9挂学警港澳]{1})'

        # 校验车牌
        if re.findall(pattern_str, plate_number) and len(plate_number) <= 8 and len(plate_number) >= 7:
            return True
        else:
            return False

    # 字段约束
    @api.constrains('carrier_plate_number', 'enter_exit_time')
    def _check_release_date(self):
        Errors = []
        # 支持校验多条 如何选择多条
        for record in self:
            if not self.plate_number_check(record.carrier_plate_number):
                Errors.append("车牌号格式错误")

            # print(record.enter_exit_time)
            # print(datetime.datetime.now() + datetime.timedelta(hours=8))
            # if record.enter_exit_time and record.enter_exit_time > datetime.datetime.now() + datetime.timedelta(hours=8):
            #
            #     Errors.append("出入时间错误")

        if Errors:
            raise models.ValidationError('\n'.join(Errors))

    def open_vehicle_copy_view(self):
        for select_records in self:
            record = {
                "default_carrier_plate_number": select_records.carrier_plate_number,
                "default_enter_exit_time": datetime.datetime.now() + datetime.timedelta(hours=8),
                "default_enter_exit_type": '0',
                "default_carrier_name": select_records.carrier_name,
                "default_visit_reason": select_records.visit_reason,
                "default_visitors": None,
                "default_vehicle_out_id": None,
            }

            form_id = self.env.ref('wms.wms_vehicle_nor_view_form_simplified_copy').id
            return {
                'name': "访客车辆出厂",
                'res_model': 'wms.vehicle.nor',
                "view_mode": "form",
                'views': [[form_id, "form"]],
                "context": record,
                "target": "new",
                "flags": {"form": {"action_buttons": False, "options": {"mode": "edit"}}},
                'type': 'ir.actions.act_window',
            }

    def copy_vehicle_in(self):
        for select_records in self:
            return {
                'name': "访客车辆出厂",
                'res_model': 'wms.vehicle.nor',
                'view_mode': 'tree,form',
                'type': 'ir.actions.act_window',
            }

    def create_vehicle_out(self):
        for select_records in self:
            if select_records.vehicle_out_id == 0 and select_records.enter_exit_type == '0':
                enter_exit_time = datetime.datetime.now() + datetime.timedelta(hours=8)
                record = {
                    "carrier_plate_number": select_records.carrier_plate_number,
                    "enter_exit_time": enter_exit_time,
                    "enter_exit_type": '1',
                    "carrier_name": select_records.carrier_name,
                    "visit_reason": select_records.visit_reason,
                    "visitors": select_records.visitors,
                    "vehicle_out_id": None,
                }

                create_record = self.env['wms.vehicle.nor'].create(record)
                select_records.write({"vehicle_out_id": create_record.id})

                return {
                    'name': "访客车辆出厂",
                    'view_mode': 'tree,form',
                    'res_model': 'wms.vehicle.nor',
                    'context': {'search_default_out': 1},
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                }

            else:
                raise models.ValidationError("该车已出厂")
