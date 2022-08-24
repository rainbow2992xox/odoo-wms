from odoo import models, fields



class Address(models.Model):
    _name = 'wms.address'
    organization_id = fields.Many2many('wms.organization', 'wms_address_organization_rel', 'address_id',
                                       'organization_id', string='所属机构')
    province_id = fields.Many2one('wms.region', '省', store=True)
    city_id = fields.Many2one('wms.region', '市', store=True)
    county_id = fields.Many2one('wms.region', '县/区', store=True)
    street_id = fields.Many2one('wms.region', '街道', store=True)

    address_detail = fields.Char('详细地址')
    postcode = fields.Char('邮编')
    contacts = fields.Char('联系人')
    contacts_phone = fields.Char('联系电话')
    type = fields.Selection([('0', '办公地址'), ('1', '库存地址'), ('2', '供应商地址')], string='类型')
    is_active = fields.Boolean()
