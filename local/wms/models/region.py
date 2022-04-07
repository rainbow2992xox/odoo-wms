from odoo import models, fields, api


class Region(models.Model):
    _name = 'wms.region'
    _parent_store = True
    p_id = fields.Many2one(
        'wms.region',
        string='上级区域',
        ondelete='restrict',
        index=True
    )
    child_ids = fields.One2many(
        'wms.region', 'p_id',
        string='下级区域')
    name = fields.Char('区域名称')
    level = fields.Selection([('0', '省'), ('1', '市'), ('2', '区'), ('3', '街道')], string='地区级别')
    is_active = fields.Boolean()

    # 防止循环应用 #TODO
    @api.constrains('p_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')
