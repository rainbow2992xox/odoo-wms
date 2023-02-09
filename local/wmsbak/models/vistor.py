from odoo import models, fields

class Vistor(models.Model):
    _name = "wms.vistor"

    name = fields.Char(string="姓名", size=32, required=True)
    phone = fields.Char(string="联系方式", size=32, required=True)
    idcard = fields.Char(string="身份证号", size=32, required=True)

    nuclear_acid_time = fields.Date(string="驾驶员核酸检测时间", required=True)
    nuclear_acid_result = fields.Selection([('0', '阴性'), ('1', '阳性')], string='驾驶员核酸检测结果',
                                                          required=True, default='0')
    antigen_test_time = fields.Date(string="驾驶员抗原检测时间", required=True)
    antigen_test_result = fields.Selection([('0', '阴性'), ('1', '阳性')], string='驾驶员抗原检测结果',
                                                          required=True, default='0')
    temperature = fields.Integer(string="驾驶员体温℃", size=32, required=True)

    vehicle_id = fields.Many2one("wms.vehicle.nor", string="进出入记录ID")

