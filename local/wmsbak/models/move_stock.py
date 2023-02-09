from odoo import models, fields

class MoveStock(models.Model):
    _name = "wms.move.stock"

    transfer_time = fields.Datetime(string='移库时间')
    warehouse_type = fields.Integer(string="仓储空间类型")
    from_warehouse_code = fields.Char(string="入库仓库号", size=32)
    from_warehouse_area_code = fields.Char(string="入库仓间号", size=32)
    from_location_code = fields.Char(string="入库仓位号", size=128, help="单个仓位号")

    to_warehouse_code = fields.Char(string="出库仓库号", size=32)
    to_warehouse_area_code = fields.Char(string="出库仓间号", size=32)
    to_location_code = fields.Char(string="出库仓位号", size=128, help="单个仓位号")

    in_stock_id = fields.Integer(string="入库ID")
    out_stock_id = fields.Integer(string="出库ID")

    from_amount = fields.Integer(string="移出货位结存")
    to_amount = fields.Integer(string="移入货位结存")

    merchandise_id = fields.Integer(string="货品ID")
    batch_code = fields.Char(string="生产批次号")
    amount = fields.Integer(string="数量")

    report_time = fields.Datetime(string="上报时间")

