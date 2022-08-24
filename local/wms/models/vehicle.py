import datetime
import re
from odoo import models, fields
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Vehicle(models.Model):
    _name = "wms.vehicle"

    carrier_plate_number = fields.Char(string="车牌号", required=True, size=32)
    enter_exit_time = fields.Datetime(string="出入时间", required=True)
    enter_exit_type = fields.Selection([('0', '进入'), ('1', '出去')], string='出入类型', required=True)
    carrier_plate_type = fields.Selection([('0', '非危险化学品车'), ('1', '危险化学品车')], string='车辆性质', required=True)

    carrier_driver_name = fields.Char(string="驾驶员姓名", size=32, required=True)
    carrier_driver_idcard = fields.Char(string="驾驶员身份证号", size=32, required=True)

    escort = fields.Char(string="押运员姓名", size=32, required=True)
    escort_idcard = fields.Char(string="押运员身份证号", size=32, required=True)

    report_time = fields.Datetime(string="上报时间")

    def id_check(self, id):
        if id is None:
            return False
        if len(id) != 18:
            return False
        if not (id[0:17].isdigit()):
            return False

        if (int(id[6:10]) % 4 == 0 or (int(id[6:10]) % 100 == 0 and int(id[6:10]) % 4 == 0)):
            # 出生日期闰年时合法性正则表达式
            birthday = re.compile(
                '[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2]              [0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')
        else:
            # 出生日期平年时合法性正则表达式
            birthday = re.compile(
                '[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2]           [0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')
        if not (re.match(birthday, id)):
            return False

        mod = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        jym = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        sum = 0
        for i in range(0, 17):
            sum += int(id[i]) * mod[i]
        sum %= 11
        if (jym[sum]) == id[17]:
            return True
        else:
            return False

    def plate_number_check(self, plate_number):
        pattern_str = "([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼]" \
                      "{1}(([A-HJ-Z]{1}[A-HJ-NP-Z0-9]{5})|([A-HJ-Z]{1}(([DF]{1}[A-HJ-NP-Z0-9]{1}[0-9]{4})|([0-9]{5}[DF]" \
                      "{1})))|([A-HJ-Z]{1}[A-D0-9]{1}[0-9]{3}警)))|([0-9]{6}使)|((([沪粤川云桂鄂陕蒙藏黑辽渝]{1}A)|鲁B|闽D|蒙E|蒙H)" \
                      "[0-9]{4}领)|(WJ[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼·•]{1}[0-9]{4}[TDSHBXJ0-9]{1})" \
                      "|([VKHBSLJNGCE]{1}[A-DJ-PR-TVY]{1}[0-9]{5})"

        # 校验车牌
        if re.findall(pattern_str, plate_number):
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

            if not self.id_check(record.carrier_driver_idcard):
                Errors.append("驾驶员身份证号格式错误")

            if not self.id_check(record.escort_idcard):
                Errors.append("押运员身份证号格式错误")

            if record.enter_exit_time and record.enter_exit_time > datetime.datetime.now():
                Errors.append("出入时间错误")

        if Errors:
            raise models.ValidationError('\n'.join(Errors))
