from odoo import models, fields

class OrganizationCar(models.Model):
    _name = "wms.organization.car"

    organization_id = fields.Many2one('wms.organization', '机构', store=True)
    license_num = fields.Char(string="车牌号", required=True)
    kind = fields.Integer(string="车辆性质", help="危险化学品车:1 非危险化学品车:0", required=True)
    type = fields.Integer(string="车辆型号", help="", required=True)
    is_active = fields.Boolean()
