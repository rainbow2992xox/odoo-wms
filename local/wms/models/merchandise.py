from odoo import models, fields, api
import os


class Merchandise(models.Model):
    _name = "wms.merchandise"

    # 主键
    merchandise_id = fields.Integer(string="货品ID", required=True)
    merchandise_name = fields.Char(string="货品名称", size=128, required=True)
    owner_id = fields.Char(string="货主ID", size=128, required=True)
    owner_name = fields.Char(string="货主名称", size=128, required=True)
    warehouse_type = fields.Integer(string="货品存储空间类型", required=True, help="0:储罐，1：仓库")
    # 单选
    is_mixture = fields.Integer(string="是否为混合物", required=True, help="0:否，1：是")
    chemical_serial = fields.Integer(string="2828目录序号")

    chemical_name = fields.Char(string="危险化学品名", size=128, required=True)
    # 多选 代号英文逗号隔开
    mix_chemicle_name = fields.Char(string="成分", size=128, help="成分化学品名最少1个，最多5个")
    # 单选
    physical_state = fields.Integer(string="物理状态", required=True, help="1-气体；2-液体；3-固体4-气溶胶")
    # 多选 代号英文逗号隔开
    other_attribute = fields.Char(string="其他属性", size=128, help='''1＜硝化甘油≤10%;2-10%＜含酸≤90%;3-20%≤含量＜60%;闪点4-"23℃≤≤60℃;5-8%≤含量＜20%;6-按质量含水不低于20%;7-非自燃的;8-粉末;9-干的;10-干的，或湿的，按质量含水低于15%;11-干的，或湿的，按质量含水低于20%;12-固态;13-含结晶水≥30%;14-含结晶水不低于25%;15-含结晶水低于25%;16-含量≥60%;17-含酸≥90%;18-甲醛含量不低于25%;19-甲醛溶液，易燃;20-冷冻液态;21-冷冻液态氦;
    22-气态;23-溶液;24-熔融;25-闪点＜23℃和初沸点＞35℃;26-闪点＜23℃和初沸点≤35℃;27-湿的;28-湿的，按质量含水不低于10%;29-湿的，按质量含水不低于15%;30-湿的，按质量含水不低于20%;31-丸状、旋屑或带状;32-无水或含结晶水＜30%;33-无涂层;34-硝化甘油≤1%;35-压缩的;36-液态;37-乙酸溶液[10%＜含量≤25%];38-乙酸溶液[25%＜含量≤80%];39-有涂层;40-自燃的;41-其他;''')

    un_code = fields.Char(string="联合国编号（UN号）", size=32, required=True)
    cas_code = fields.Char(string="CAS号", size=32)
    cas_index = fields.Char(string="CAS索引号", size=32)

    # 多选 代号英文逗号隔开
    risk_ghs_item_category = fields.Char(string="危险性类别 （GHS）", size=128, required=True,
                                         help='''010001-爆炸物,1.1项010002-爆炸物,1.2项010003-爆炸物,1.3项010004-爆炸物,1.4项010005-爆炸物,不稳定爆炸物020001-易燃气体,类别1020002-易燃气体,类别2020003-易燃气体,类别3030001-易燃气溶胶,类别1030002-易燃气溶胶,类别2030003-易燃气溶胶,类别3040001-氧化性气体,类别1040002-氧化性气体,类别2040003-氧化性气体,
    类别3050000-加压气体060001-易燃液体,类别1060002-易燃液体,类别2060003-易燃液体,类别3070001-易燃固体,类别1070002-易燃固体,类别2070003-易燃固体,类别3080001-自反应物质和混合物,A型080002-自反应物质和混合物,B型080003-自反应物质和混合物,C型080004-自反应物质和混合物,D型080005-自反应物质和混合物,E型090001-发火液体,类别1090002-发火液体,类别2
    090003-发火液体,类别3100001-发火固体,类别1100002-发火固体,类别2100003-发火固体,类别2110001-自热物质和混合物,类别1110002-自热物质和混合物,类别2110003-自热物质和混合物,类别3120001-遇水放出易燃气体的物质和混合物,类别1120002-遇水放出易燃气体的物质和混合物,类别2120003-遇水放出易燃气体的物质和混合物,类别3130001-氧化性液体,类别1130002-氧化性液体,类别2130003-氧化性液体,
    类别3140001-氧化性固体,类别1140002-氧化性固体,类别2140003-氧化性固体,类别3150001-有机过氧化物,A型150002-有机过氧化物,B型150003-有机过氧化物,C型150004-有机过氧化物,D型150005-有机过氧化物,E型150006-有机过氧化物,F型160001-金属腐蚀剂,类别1160002-金属腐蚀剂,类别2160003-金属腐蚀剂,类别3170101-急性毒性-经口,类别1170102-急性毒性-经
    口,类别2170103-急性毒性-经口,类别3170201-急性毒性-经皮,类别1170202-急性毒性-经皮,类别2170203-急性毒性-经皮,类别3170301-急性毒性-吸入,类别1170302-急性毒性-吸入,类别2170303-急性毒性-吸入,类别3180101-特异性靶器官毒性-反复接触,类别1180102-特异性靶器官毒性-反复接触,类别2180103-特异性靶器官毒性-反复接触,类别3180201-特异性靶器官毒性-一次接触,类别1180202-特异性靶器
    官毒性-一次接触,类别2180203-特异性靶器官毒性-一次接触,类别3190001-呼吸道致敏物,类别1190002-呼吸道致敏物,类别2190003-呼吸道致敏物,类别3200001-化学不稳定性气体,类别A200002-化学不稳定性气体,类别B200003-化学不稳定性气体,类别C210001-皮肤腐蚀/刺激,类别1210002-皮肤腐蚀/刺激,类别1A210003-皮肤腐蚀/刺激,类别1B210004-皮肤腐蚀/刺激,类别1C210011-皮肤腐蚀/刺激,类别2210012-皮肤腐蚀/刺
    激,类别2A210013-皮肤腐蚀/刺激,类别2B210014-皮肤腐蚀/刺激,类别2C220001-皮肤致敏物,类别1220002-皮肤致敏物,类别2220003-皮肤致敏物,类别3230000-生殖毒性,附加类别230001-生殖毒性,类别1230002-生殖毒性,类别1A230003-生殖毒性,类别1B230011-生殖毒性,类别2230012-生殖毒性,类别2A230013-生殖毒性,类别2B240001-生殖细胞致突变性,类别1240002-生殖细胞致
    突变性,类别1A240003-生殖细胞致突变性,类别1B240011-生殖细胞致突变性,类别2240012-生殖细胞致突变性,类别2A240013-生殖细胞致突变性,类别2B250000-酸性260001-危害臭氧层,类别1260002-危害臭氧层,类别2260003-危害臭氧层,类别3270101-危害水生环境-急性危害,类别1270102-危害水生环境-急性危害,类别2270103-危害水生环境-急性危害,类别3270201-危害水生环境-长期危害,类别1270202-危害水生环境-长期危害,类别2270203-危害水生环境-长期危害,类别3
    280001-吸入危害,类别1280002-吸入危害,类别2280003-吸入危害,类别3290001-严重眼损伤/眼刺激,类别1290002-严重眼损伤/眼刺激,类别1A290003-严重眼损伤/眼刺激,类别1B290011-严重眼损伤/眼刺激,类别2290012-严重眼损伤/眼刺激,类别2A290013-严重眼损伤/眼刺激,类别2B300001-致癌性,类别1300002-致癌性,类别1A300003-致癌性,类别1B300011-致癌性,类别2300012-致癌性,类别2A
    300013-致癌性,类别2B310001-自燃固体,类别1310002-自燃固体,类别2310003-自燃固体,类别3320001-自燃液体,类别1320002-自燃液体,类别2320003-自燃液体,类别3''')

    # 单选
    risk_item_category = fields.Char(string="危险货物类别", size=128, required=True,
                                     help='''1.爆炸品1.1有整体爆炸危险的物质和物品1.2有迸射危险，但无整体爆炸危险的物质和物品1.3有燃烧危险并有局部爆炸危险或局部迸射危险或者这两种危险都有，但无整体爆炸危险的物质和物品1.4不呈现重大危险的物质和物品1.5有整体爆炸危险的非常不敏感物质1.6无整体爆炸危险的极端不敏感物品2.气体2.1易燃气体2.2非易燃无毒气体2.3毒性气体
    3.易燃液体4.易燃固体、易于自然的物质、遇水放出易燃气体的物质4.1易燃固体、易于自然的物质、遇水放出易燃气体的物质4.2易于自然的物质4.3遇水放出易燃气体的物质5.氧化性物质和有机过氧化物5.1氧化性物质5.2有机过氧化物6.毒性物质和感染性物质6.1毒性物质6.2感染性物质7.放射性物质8.腐蚀性物质9.杂项危险物质和物品，包含危害环境物质''')

    # 单选
    fire_risk = fields.Char(string="火灾危险性类别", size=32, required=True,
                            help="甲、甲1、甲2、甲3、甲4、甲5、甲6、乙、乙1、乙2、乙3、乙4、乙5、乙6、丙、丙1、丙2、丁、丁1、丁2、丁3、丁4、丁5、丁6、戊、戊1、戊2、戊3、戊4、戊5、戊6")
    # 单选
    organic = fields.Integer(string="化学结构", required=True, help="0:无机，1：有机")
    # 单选
    deleterious = fields.Integer(string="剧毒品特性", required=True, help="0:否，1：是")

    # 单选
    acid_base = fields.Integer(string="酸碱性", help="0：酸性，1:碱性")

    # 单选
    monitored = fields.Integer(string="监控化学品（禁化武）特性", help="0:否，1：是")
    # 单选
    special_controlled = fields.Integer(string="特别管控危险化学品特性", required=True, help="0:否，1：是")
    # 单选
    regulatory = fields.Integer(string="重点监管危险化学品特性", required=True, help="0:否，1：是")
    # 多选
    prohibited = fields.Integer(string="上海禁限控化学品特性", required=True,
                                help="1-全市禁止2-化工区禁止3-中心城限制和控制4-不限控")
    # 单选
    easy_made_drug = fields.Integer(string="公安易制毒特性", required=True, help="0:否，1：是")
    # 单选
    easy_to_explode = fields.Integer(string="公安易制爆特性", required=True, help="0:否，1：是")
    critical_quantity = fields.Float(string="重大危险源申报临界值", digits=(10, 2), required=True, help="单位吨")
    # 多选
    fire_fighting_measures = fields.Char(string="适用消防措施", size=32, required=True,
                                         help="1干粉；2黄沙；3水；4大量流水；5泡沫；6二氧化碳；7其它")
    mixed_taboo = fields.Char(string="混放禁忌", size=128, help="危险化学品名/联合国编号（UN号）/CAS号")

    # 计算字段页面上传文件调用JAVA上传文件接口保存KEY字段 TODO url是否需要保存？
    chemical_identification_report = fields.Char(string="上传《化学品安全技术说明书》", size=256, required=True,
                                                 help="上传市局系统后获得的路径")
    # 计算字段页面上传文件调用JAVA上传文件接口保存KEY字段 TODO url是否需要保存？
    chemical_classification_report = fields.Char(string="上传《化学品危险性分类报告》", size=256, required=True,
                                                 help="上传市局系统后获得的路径")

    density = fields.Float(string="密度值", digits=(10, 2), help="密度值（保留2位小数）")
    density_unit = fields.Char(string="密度单位", size=32,
                               help="气体：千克/立方米，克/立方米，毫克/立方米液体：千克/升，克/升，毫克/升")
    concentration = fields.Float(string="浓度", digits=(10, 2), required=True, help="百分比，保留2位小数")
    unit_count = fields.Integer(string="规格数量", required=True, help="规格数量")
    unit = fields.Char(string="规格计量单位", size=32, required=True,
                       help="质量：毫克，克，千克，吨体积：微升，毫升，升，立方米")
    specification = fields.Char(string="规格包装单位名称", size=32, required=True, help="包装单位（桶／箱／罐／瓶／包）")

    # 定时任务调用时间
    report_time = fields.Datetime(string="上报时间")

    # 导入数据后更新出入库、库存状态

    def upload_file(self):
        for r in self:
            filepath = os.path.join('/home/reagent/opt/sdspdf', r['cas_index'] + '.pdf')
            move_post_body = {
                "type": "filesync",
                "filepath": filepath,
            }

            res = self.env["wms.api.log"]._post(move_post_body)
            r.chemical_identification_report = res['module']['key']

            if r.chemical_serial <= 2827 or r.chemical_serial >= 1:
                pass
            else:
                r.chemical_classification_report = res['module']['key']

            print(res)
