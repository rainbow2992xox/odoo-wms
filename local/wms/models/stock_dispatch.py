from odoo import models, fields


class StockDispatch(models.Model):
    _name = "wms.stock.dispatch"

    organization_id = fields.Many2one("wms.organization", string="货主机构ID")
    organization_tran_id = fields.Many2one("wms.organization", string="承运机构ID")

    organization_car_id = fields.Many2one("wms.organization.car", string="车辆ID")
    organization_employee_driver_id = fields.Many2one("wms.organization.employee", string="驾驶员ID")
    organization_employee_supercargo_id = fields.Many2one("wms.organization.employee", string="押运员ID")

    stock_loading_id = fields.Many2many("wms.stock.loading","wms_stock_dispatch_loading_rel","stock_dispatch_id","stock_loading_id",string="关联装载单")

    # TODO 待确认
    dispatch_type = fields.Char(string="派车单类型", size=32, help="IN、OUT、MOVE")
    operation_time = fields.Datetime()
    source_id = fields.Char(string="送货单据信息", size=128, required=True)
