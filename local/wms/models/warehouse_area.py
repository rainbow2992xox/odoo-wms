from odoo import models, fields
from random import randint


class WarehouseArea(models.Model):
    _name = "wms.warehouse.area"

    warehouse_code = fields.Char(string="仓库号/罐组号", size=32, required=True)
    warehouse_area_code = fields.Char(string="仓间号/储罐号", size=32, required=True)
    location_code_list = fields.Char(string="仓位号", size=2048, help="仓间下所有仓位号列表")
    # 单选  TODO 同步数据或者接口上报时需二次处理
    fire_risk = fields.Char(string="仓库火灾危险性 类别", size=32,
                            help="甲、甲1、甲2、甲3、甲4、甲5、甲6、乙、乙1、乙2、乙3、乙4、乙5、乙6、丙、丙1、丙2、丁、丁1、丁2、丁3、丁4、丁5、丁6、戊、戊1、戊2、戊3、戊4、戊5、戊6")
    acreage = fields.Float(string="仓间面积", digits=(10, 2), help="单位平方米，2位小数")
    max_volume = fields.Float(string="仓间最大存储量", digits=(10, 2), help="仓间-单位吨，2位小数")

    # 多选 代号英文逗号隔开 TODO 同步数据或者接口上报时需二次处理
    fire_fighting_measures = fields.Char(string="消防措施", size=32, help="1干粉；2黄沙；3水；4大量流水；5泡沫；6二氧化碳；7其它")

    # 多选 代号英文逗号隔开 TODO 同步数据或者接口上报时需二次处理
    risk_ghs_category = fields.Char(string="仓间储存危险化学品危险性类别（GHS）", size=128,
                                help="1爆炸物；2易燃气体；3易燃气溶胶；4氧化性气体；5高压气体；6易燃液体；7易燃固体；")



