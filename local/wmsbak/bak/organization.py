from odoo import models, fields

class Organization(models.Model):
    _name = 'wms.organization'
    full_name = fields.Char(string='机构名称')
    short_name = fields.Char(string='简称')
    code = fields.Integer(string='编码')
    tax_code = fields.Integer(string='税务登记号')
    address_id = fields.Many2many('wms.address', 'wms_address_organization_rel', 'organization_id', 'address_id',
                                  string='地址')

