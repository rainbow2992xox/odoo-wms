from odoo import models, fields

class OutStock(models.Model):
    _name = "wms.out.stock"

    outbound_time = fields.Datetime(string='入库时间')
    warehouse_type = fields.Integer(string="仓储空间类型")
    warehouse_code = fields.Char(string="入库仓库号", size=32)
    warehouse_area_code = fields.Char(string="入库仓间号", size=32)
    location_code = fields.Char(string="入库仓位号", size=128, help="单个仓位号")
    merchandise_id = fields.Integer(string="货品ID")
    batch_code = fields.Char(string="生产批次号")
    amount = fields.Integer(string="数量")
    carrier_plate_number = fields.Char(string="车牌号", size=32)
    consignee_address = fields.Char(string="收货方地址", size=128)
    consignee_name = fields.Char(string="收货方名称", size=32)
    o_id = fields.Integer(string="原始ID")
    vehicle_id = fields.Many2one("wms.vehicle", string="进出入记录ID")
    report_time = fields.Datetime(string="上报时间")

