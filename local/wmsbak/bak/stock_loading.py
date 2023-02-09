from odoo import models, fields


class StockLoading(models.Model):
    _name = "wms.stock.loading"

    # 非主键可重复
    loading_id = fields.Integer(string="装载单ID", required=True)
    loading_code = fields.Char(string="装载单编号", size=32, required=True)
    transaction_id = fields.Many2one("wms.stock.transaction",string="库存交易ID", store=True)
    stock_dispatch_id = fields.Many2many("wms.stock.dispatch", "wms_stock_dispatch_loading_rel", "stock_loading_id",
                                        "stock_dispatch_id", string="关联派车单")
    # TODO 待确认
    operation_time = fields.Datetime()
    recipient = fields.Char(string="收货方", size=128, required=True)


