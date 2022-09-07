import datetime
import re
from odoo import models, fields
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Vehicle(models.Model):
    _name = "wms.vehicle"

    carrier_plate_number = fields.Char(string="车牌号", required=True, size=32)
    enter_exit_time = fields.Datetime(string="出入时间", required=True)
    enter_exit_type = fields.Selection([('0', '进入'), ('1', '出去')], string='出入类型', required=True, default='0',
                                       readonly=True)
    carrier_plate_type = fields.Selection([('0', '非危险化学品车'), ('1', '危险化学品车')], string='车辆性质', default='1',
                                          required=True)

    carrier_name = fields.Char(string="承运企业名称", required=True, size=32)

    carrier_driver_name = fields.Char(string="驾驶员姓名", size=32, required=True)
    carrier_driver_idcard = fields.Char(string="驾驶员身份证号", size=32, required=True)

    escort = fields.Char(string="押运员姓名", size=32, required=True)
    escort_idcard = fields.Char(string="押运员身份证号", size=32, required=True)

    in_stock_id = fields.One2many(
        'wms.in.stock', 'vehicle_id',
        string='入库关联ID')

    out_stock_id = fields.One2many(
        'wms.out.stock', 'vehicle_id',
        string='出库关联ID')

    vehicle_out_id = fields.Integer(string="出厂记录ID")

    report_time = fields.Datetime(string="上报时间")

    def id_check(self, idcard):
        Errors = ['验证通过!', '身份证号码位数不对!', '身份证号码出生日期超出范围或含有非法字符!',
                  '身份证号码校验码错误!', '身份证地区非法!']
        area = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林",
                "23": "黑龙江",
                "31": "上海", "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东",
                "41": "河南", "42": "湖北",
                "43": "湖南", "44": "广东", "45": "广西", "46": "海南", "50": "重庆", "51": "四川", "52": "贵州",
                "53": "云南", "54": "西藏",
                "61": "陕西", "62": "甘肃", "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港",
                "82": "澳门", "91": "国外"}
        idcard = str(idcard)
        idcard = idcard.strip()
        idcard_list = list(idcard)


        # 15位身份号码检测
        if len(idcard) == 15:
            if ((int(idcard[6:8]) + 1900) % 4 == 0 or (
                    (int(idcard[6:8]) + 1900) % 100 == 0 and (int(idcard[6:8]) + 1900) % 4 == 0)):
                erg = re.compile(
                    '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')  # //测试出生日期的合法性
            else:
                ereg = re.compile(
                    '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')  # //测试出生日期的合法性
            if re.match(ereg, idcard):
                return (True, "验证通过")
            else:
                return (False, Errors[2])
        # 18位身份号码检测
        elif len(idcard) == 18:
            # 出生日期的合法性检查
            # 闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
            # 平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
            if (int(idcard[6:10]) % 4 == 0 or (int(idcard[6:10]) % 100 == 0 and int(idcard[6:10]) % 4 == 0)):
                # 闰年出生日期的合法性正则表达式
                ereg = re.compile(
                    '[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')
            else:
                # 平年出生日期的合法性正则表达式
                ereg = re.compile(
                    '[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')
            # 测试出生日期的合法性
            if re.match(ereg, idcard):
                # 计算校验位
                S = (int(idcard_list[0]) + int(idcard_list[10])) * 7 + (
                        int(idcard_list[1]) + int(idcard_list[11])) * 9 + (
                            int(idcard_list[2]) + int(idcard_list[12])) * 10 + (
                            int(idcard_list[3]) + int(idcard_list[13])) * 5 + (
                            int(idcard_list[4]) + int(idcard_list[14])) * 8 + (
                            int(idcard_list[5]) + int(idcard_list[15])) * 4 + (
                            int(idcard_list[6]) + int(idcard_list[16])) * 2 + int(idcard_list[7]) * 1 + int(
                    idcard_list[8]) * 6 + int(idcard_list[9]) * 3
                Y = S % 11
                M = "F"
                JYM = "10X98765432"
                M = JYM[Y]  # 判断校验位
                if M == idcard_list[17]:  # 检测ID的校验位
                    return (True, "验证通过")
                else:
                    return (False, Errors[3])
            else:
                return (False, Errors[2])
        else:
            return (False, Errors[1])

        # 地区校验
        if not area[(idcard)[0:2]]:
            return (False, Errors[4])

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

            if not self.id_check(record.carrier_driver_idcard)[0]:
                Errors.append("驾驶员身份证号格式错误:%s" % (self.id_check(record.carrier_driver_idcard)[1]))

            if not self.id_check(record.escort_idcard)[0]:
                Errors.append("押运员身份证号格式错误:%s" % (self.id_check(record.carrier_driver_idcard)[1]))

            if record.enter_exit_time and record.enter_exit_time > datetime.datetime.now():
                Errors.append("出入时间错误")

        if Errors:
            raise models.ValidationError('\n'.join(Errors))

    def copy_vehicle_in(self):
        for select_records in self:
            record = {
                "carrier_plate_number": select_records.carrier_plate_number,
                "enter_exit_time": select_records.enter_exit_time,
                "enter_exit_type": '0',
                "carrier_name": select_records.carrier_name,
                "carrier_plate_type": select_records.carrier_plate_type,
                "carrier_driver_name": select_records.carrier_driver_name,
                "carrier_driver_idcard": select_records.carrier_driver_idcard,
                "escort": select_records.escort,
                "escort_idcard": select_records.escort_idcard,
                "in_stock_id": None,
                "out_stock_id": None,
                "vehicle_out_id": None,
                "report_time": None
            }
            create_record = self.env['wms.vehicle'].create(record)

            return {
                'name': "车辆出入记录",
                'view_mode': 'tree,form',
                'res_model': 'wms.vehicle',
                'view_id': False,
                'type': 'ir.actions.act_window',
            }

    def create_vehicle_out(self):
        for select_records in self:
            if select_records.vehicle_out_id == 0 and select_records.enter_exit_type == '0':
                enter_exit_time = datetime.datetime.now()
                record = {
                    "carrier_plate_number": select_records.carrier_plate_number,
                    "enter_exit_time": enter_exit_time,
                    "enter_exit_type": '1',
                    "carrier_name": select_records.carrier_name,
                    "carrier_plate_type": select_records.carrier_plate_type,
                    "carrier_driver_name": select_records.carrier_driver_name,
                    "carrier_driver_idcard": select_records.carrier_driver_idcard,
                    "escort": select_records.escort,
                    "escort_idcard": select_records.escort_idcard,
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
                    'context': {'search_default_out':1},
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                }
            else:
                raise models.ValidationError("该车已出厂")

