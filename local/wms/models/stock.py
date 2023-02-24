from odoo import models, fields, api

class Stock(models.Model):
    _name = "wms.stock"

    warehouse_code = fields.Char(string="仓库号", size=32, required=True)
    warehouse_area_code = fields.Char(string="仓间号", size=32, required=True)
    location_code = fields.Char(string="仓位号", size=128, help="单个仓位号")
    merchandise_code = fields.Char(string="商品编码", required=True)
    merchandise_id = fields.Integer(string="货品ID", required=True)
    amount = fields.Integer(string="数量", required=True)
    report_time = fields.Datetime(string="上报时间")

    if_need_update = fields.Boolean(
        string="是否需要上传",
        compute="_compute_if_need_update",
        readonly=True,
        store=True
    )

    def check_if_abnormal(self, vals):
        if self.env["wms.merchandise"].search([("merchandise_id", "=", vals["merchandise_id"])]):
            vals["if_need_update"] = True
        else:
            vals["if_need_update"] = False

        return vals

    @api.model
    def create(self, vals):

        vals = self.check_if_abnormal(vals)
        res = super(Stock, self).create(vals)
        return res