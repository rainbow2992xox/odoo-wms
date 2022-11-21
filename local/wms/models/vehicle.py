import datetime
import re
from odoo import models, fields
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import requests
import pytz

class Vehicle(models.Model):
    _name = "wms.vehicle"

    carrier_plate_number = fields.Char(string="车牌号", required=True, size=32)
    enter_exit_time = fields.Datetime(string="出入时间", required=True)
    enter_exit_type = fields.Selection([('0', '进入'), ('1', '出去')], string='出入类型', required=True, default='0',
                                       readonly=True)
    carrier_plate_type = fields.Selection([('0', '非危险化学品车'), ('1', '危险化学品车')], string='车辆性质',
                                          default='1',
                                          required=True)

    carrier_name = fields.Char(string="承运企业名称", required=True, size=32)

    carrier_driver_name = fields.Char(string="驾驶员姓名", size=32, required=True)
    carrier_driver_idcard = fields.Char(string="驾驶员身份证号", size=32, required=True)

    carrier_driver_phone = fields.Char(string="驾驶员联系电话", size=32, required=True)
    carrier_driver_certificate = fields.Char(string="驾驶员从业资格证", size=32, required=True)
    carrier_driver_nuclear_acid_time = fields.Date(string="驾驶员核酸检测时间", required=True)
    carrier_driver_nuclear_acid_result = fields.Selection([('0', '阴性'), ('1', '阳性')], string='驾驶员核酸检测结果',
                                                          required=True, default='0')
    carrier_driver_antigen_test_time = fields.Date(string="驾驶员抗原检测时间", required=True)
    carrier_driver_antigen_test_result = fields.Selection([('0', '阴性'), ('1', '阳性')], string='驾驶员抗原检测结果',
                                                          required=True, default='0')
    carrier_driver_temperature = fields.Integer(string="驾驶员体温℃", size=32, required=True)

    escort = fields.Char(string="押运员姓名", size=32, required=True)
    escort_idcard = fields.Char(string="押运员身份证号", size=32, required=True)
    escort_phone = fields.Char(string="押运员联系电话", size=32, required=True)
    escort_driver_certificate = fields.Char(string="押运员从业资格证", size=32, required=True)
    escort_driver_nuclear_acid_time = fields.Date(string="押运员核酸检测时间", required=True)
    escort_driver_nuclear_acid_result = fields.Selection([('0', '阴性'), ('1', '阳性')], string='押运员核酸检测结果',
                                                         required=True, default='0')
    escort_driver_antigen_test_time = fields.Date(string="押运员抗原检测时间", required=True)
    escort_driver_antigen_test_result = fields.Selection([('0', '阴性'), ('1', '阳性')], string='押运员抗原检测结果',
                                                         required=True, default='0')
    escort_driver_temperature = fields.Integer(string="押运员体温℃", size=32, required=True)

    registrar = fields.Char(string="登记人员姓名", required=True, size=32)

    in_stock_id = fields.One2many(
        'wms.in.stock', 'vehicle_id',
        string='入库关联ID')

    out_stock_id = fields.One2many(
        'wms.out.stock', 'vehicle_id',
        string='出库关联ID')

    vehicle_out_id = fields.Integer(string="出厂记录ID", default=0)

    report_time = fields.Datetime(string="上报时间")

    # def id_check(self, id):
    #     # r = requests.get("https://www.haoshudi.com/api/id/query/?userid=" + id)
    #     # res = r.json()
    #     #
    #     # if not res['status']:
    #     #     return (res['status'], res['msg'])
    #     # else:
    #     #     return (res['data']['isIdCard'], "请核对")
    #     return (True,"Success")

    def plate_number_check(self, plate_number):
        pattern_str = '([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]{1}[A-Z]{1}(([A-HJ-NP-Z0-9]{5}[DF]{1})|([DF]{1}[A-HJ-NP-Z0-9]{5})))|([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领]{1}[A-Z]{1}[A-HJ-NP-Z0-9]{4}[A-HJ-NP-Z0-9挂学警港澳]{1})'

        # 校验车牌
        if re.findall(pattern_str, plate_number) and len(plate_number) <= 8 and len(plate_number) >= 7:
            return True
        else:
            return False

    # 字段约束
    @api.constrains('carrier_plate_number', 'enter_exit_time', 'carrier_driver_idcard', 'escort_idcard')
    def _check_release_date(self):
        Errors = []
        # 支持校验多条 如何选择多条
        for record in self:
            if not self.plate_number_check(record.carrier_plate_number):
                Errors.append("车牌号格式错误")

            # if not self.id_check(record.carrier_driver_idcard)[0]:
            #     Errors.append("驾驶员身份证号格式错误:%s" % (self.id_check(record.carrier_driver_idcard)[1]))
            #
            # if not self.id_check(record.escort_idcard)[0]:
            #     Errors.append("押运员身份证号格式错误:%s" % (self.id_check(record.carrier_driver_idcard)[1]))
            print(record.enter_exit_time)
            print(datetime.datetime.now(pytz.timezone('Asia/Shanghai')))
            if record.enter_exit_time and record.enter_exit_time.replace(tzinfo=pytz.timezone('Asia/Shanghai')) > datetime.datetime.now(pytz.timezone('Asia/Shanghai')):
                Errors.append("出入时间错误")

        if Errors:
            raise models.ValidationError('\n'.join(Errors))

    def open_vehicle_copy_view(self):
        for select_records in self:
            record = {
                "default_carrier_plate_number": select_records.carrier_plate_number,
                "default_enter_exit_time": datetime.datetime.now(pytz.timezone('Asia/Shanghai')),
                "default_enter_exit_type": '0',
                "default_carrier_name": select_records.carrier_name,
                "default_carrier_plate_type": select_records.carrier_plate_type,
                "default_carrier_driver_name": select_records.carrier_driver_name,
                "default_carrier_driver_idcard": select_records.carrier_driver_idcard,
                "default_carrier_driver_phone": select_records.carrier_driver_phone,
                "default_carrier_driver_certificate": select_records.carrier_driver_certificate,
                "default_escort": select_records.escort,
                "default_escort_idcard": select_records.escort_idcard,
                "default_escort_phone": select_records.escort_phone,
                "default_escort_driver_certificate": select_records.escort_driver_certificate,
                "default_in_stock_id": None,
                "default_out_stock_id": None,
                "default_vehicle_out_id": None,
                "default_report_time": None
            }

            form_id = self.env.ref('wms.wms_vehicle_view_form_simplified_copy').id
            return {
                'name': "危险品车辆出厂",
                'res_model': 'wms.vehicle',
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
                'name': "危险品车辆出厂",
                'res_model': 'wms.vehicle',
                'view_mode': 'tree,form',
                'type': 'ir.actions.act_window',
            }
            # record = {
            #     "carrier_plate_number": select_records.carrier_plate_number,
            #     "enter_exit_time": select_records.enter_exit_time,
            #     "enter_exit_type": '0',
            #     "carrier_name": select_records.carrier_name,
            #     "carrier_plate_type": select_records.carrier_plate_type,
            #     "carrier_driver_name": select_records.carrier_driver_name,
            #     "carrier_driver_idcard": select_records.carrier_driver_idcard,
            #     "escort": select_records.escort,
            #     "escort_idcard": select_records.escort_idcard,
            #     "in_stock_id": None,
            #     "out_stock_id": None,
            #     "vehicle_out_id": None,
            #     "report_time": None
            # }
            # create_record = self.env['wms.vehicle'].create(record)

    def create_vehicle_out(self):
        for select_records in self:
            if select_records.vehicle_out_id == 0 and select_records.enter_exit_type == '0':
                enter_exit_time = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
                record = {
                    "carrier_plate_number": select_records.carrier_plate_number,
                    "enter_exit_time": enter_exit_time,
                    "enter_exit_type": '1',
                    "carrier_name": select_records.carrier_name,
                    "carrier_plate_type": select_records.carrier_plate_type,
                    "carrier_driver_name": select_records.carrier_driver_name,
                    "carrier_driver_idcard": select_records.carrier_driver_idcard,
                    "carrier_driver_phone": select_records.carrier_driver_phone,
                    "carrier_driver_certificate": select_records.carrier_driver_certificate,
                    "carrier_driver_nuclear_acid_time": select_records.carrier_driver_nuclear_acid_time,
                    "carrier_driver_nuclear_acid_result": select_records.carrier_driver_nuclear_acid_result,

                    "carrier_driver_antigen_test_time": select_records.carrier_driver_antigen_test_time,
                    "carrier_driver_antigen_test_result": select_records.carrier_driver_antigen_test_result,
                    "carrier_driver_temperature": select_records.carrier_driver_temperature,

                    "escort": select_records.escort,
                    "escort_idcard": select_records.escort_idcard,
                    "escort_phone": select_records.escort_phone,

                    "escort_driver_certificate": select_records.escort_driver_certificate,
                    "escort_driver_nuclear_acid_time": select_records.escort_driver_nuclear_acid_time,
                    "escort_driver_nuclear_acid_result": select_records.escort_driver_nuclear_acid_result,

                    "escort_driver_antigen_test_time": select_records.escort_driver_antigen_test_time,
                    "escort_driver_antigen_test_result": select_records.escort_driver_antigen_test_result,
                    "escort_driver_temperature": select_records.escort_driver_temperature,

                    "registrar": select_records.registrar,

                    "in_stock_id": select_records.in_stock_id,
                    "out_stock_id": select_records.out_stock_id,
                    "vehicle_out_id": None,
                    "report_time": None
                }

                create_record = self.env['wms.vehicle'].create(record)
                select_records.write({"vehicle_out_id": create_record.id})

                return {
                    'name': "危险品车辆出厂",
                    'view_mode': 'tree,form',
                    'res_model': 'wms.vehicle',
                    'context': {'search_default_out': 1},
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                }
            else:
                raise models.ValidationError("该车已出厂")
