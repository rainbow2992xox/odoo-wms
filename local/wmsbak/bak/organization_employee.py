from odoo import models, fields
from random import randint


class OrganizationEmployee(models.Model):
    _name = "wms.organization.employee"

    organization_id = fields.Many2one('wms.organization', '机构', store=True)
    name = fields.Char(string="姓名", required=True)
    sex = fields.Selection([('0', '男'), ('1', '女')], string='性别', required=True)
    phone = fields.Char(string="手机号", required=True)
    idcard = fields.Char(string="身份证号", required=True)
    sex = fields.Selection([('0', '驾驶员'), ('1', '押运员')], string='类型', required=True)
    is_active = fields.Boolean()


