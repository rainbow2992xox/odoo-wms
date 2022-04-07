from odoo import models, fields

class Stock(models.Model):
    _name = "wms.stock"

    warehouse_id = fields.Integer(string="仓库/罐组ID")
    warehouse_code = fields.Char(string="仓库号/罐组号", size=32, required=True)
    warehouse_area_id = fields.Many2one("wms.warehouse_area", string="仓间/储罐ID")
    warehouse_area_code = fields.Char(string="仓间号/储罐号", size=32, required=True)

    # TODO 同步数据时转换
    warehouse_area_type = fields.Integer(string="仓储空间类型", required=True, help="(单选)：仓间：1，储罐：2")

    location_code = fields.Char(string="仓位号", size=128, help="单个仓位号")
    merchandise_id = fields.Many2one("wms.merchandise", string="货品ID", required=True)
    bar_code = fields.Char(string="电子标签号", size=128, help="非必填项，如有电子标签则必填")
    batch_code = fields.Char(string="电子标签号", size=128, help="必填", required=True)

    # 仓库货物数量或者储罐吨数  TODO 同步数据时转换
    amount = fields.Float(string="数量/储罐交易吨数", digits=(10, 2), required=True)
