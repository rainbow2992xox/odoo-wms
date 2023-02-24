from odoo import models, fields, api
import datetime


class OutStock(models.Model):
    _name = "wms.out.stock"

    outbound_time = fields.Datetime(string='出库时间')
    warehouse_type = fields.Integer(string="仓储空间类型")
    warehouse_code = fields.Char(string="入库仓库号", size=32)
    warehouse_area_code = fields.Char(string="入库仓间号", size=32)
    location_code = fields.Char(string="入库仓位号", size=128, help="单个仓位号")
    merchandise_code = fields.Char(string="商品编码", required=True)
    merchandise_id = fields.Integer(string="货品ID")
    batch_code = fields.Char(string="生产批次号")
    amount = fields.Integer(string="数量")
    carrier_plate_number = fields.Char(string="车牌号", size=32)
    consignee_address = fields.Char(string="收货方地址", size=128)
    consignee_name = fields.Char(string="收货方名称", size=32)
    o_id = fields.Integer(string="原始ID")
    vehicle_id = fields.Many2one("wms.vehicle", string="进出入记录ID")
    report_time = fields.Datetime(string="上报时间")
    if_need_update = fields.Boolean(
        string="是否需要上传",
        compute="_compute_if_need_update",
        readonly=True,
        store=True
    )

    abnormal_reason = fields.Char(
        string="异常原因",
        compute="_compute_abnormal_reason",
        readonly=True,
        store=True
    )

    def check_if_abnormal(self, vals):
        if self.env["wms.merchandise"].search([("merchandise_id", "=", vals["merchandise_id"])]):
            vals["if_need_update"] = True
        else:
            vals["if_need_update"] = False

        if not vals["carrier_plate_number"]:
            vals["abnormal_reason"] = "无车牌号"
        else:
            outbound_time = vals["outbound_time"]
            tomorrow = datetime.datetime(outbound_time.year, outbound_time.month, outbound_time.day, 0, 0, 0)
            vehicle_res = self.env['wms.vehicle'].search(
                ["&",
                 ('carrier_plate_number', '=', vals["carrier_plate_number"]),
                 ('enter_exit_type', '=', "0"),
                 ('enter_exit_time', '<', tomorrow),
                 ('enter_exit_time', '>', outbound_time)
                 ], limit=1, order="enter_exit_time DESC")

            if len(vehicle_res) == 0:
                vals["abnormal_reason"] = "未匹配到%s在%s至%s的出厂记录" % (
                    vals["carrier_plate_number"], outbound_time.strftime('%Y-%m-%d %H:%M'),
                    tomorrow.strftime('%Y-%m-%d %H:%M'))
        return vals

    @api.model
    def create(self, vals):
        vals = self.check_if_abnormal(vals)
        res = super(OutStock, self).create(vals)
        return res
