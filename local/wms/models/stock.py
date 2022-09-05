from odoo import models, fields

class Stock(models.Model):
    _name = "wms.stock"

    warehouse_code = fields.Char(string="仓库号", size=32, required=True)
    warehouse_area_code = fields.Char(string="仓间号", size=32, required=True)
    location_code = fields.Char(string="仓位号", size=128, help="单个仓位号")
    merchandise_id = fields.Integer(string="货品ID", required=True)
    amount = fields.Integer(string="数量", required=True)
