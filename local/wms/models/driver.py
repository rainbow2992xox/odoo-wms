from odoo import models, fields

class Driver(models.Model):
    _name = "wms.driver"
    _sql_constraints = [
        ('idcard_key', 'UNIQUE (idcard)', '该司机已存在')
    ]
    name = fields.Char(string="姓名", size=32, required=True)
    idcard = fields.Char(string="身份证号", size=32, required=True)
    phone = fields.Char(string="联系电话", size=32)
    driver_certificate = fields.Char(string="从业资格证", size=32)

