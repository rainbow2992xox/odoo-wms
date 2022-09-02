import re

from odoo import models, fields, api
import logging
import cx_Oracle as cx
import datetime
import requests
import json
import pandas as pd
import os, sys

_logger = logging.getLogger(__name__)


class ApiLog(models.Model):
    _name = 'wms.api.log'
    api_address = fields.Char('API地址')
    last_idx = fields.Integer(string="最后一条记录ID")
    status = fields.Selection([('0', '成功'), ('1', '失败')], string='状态')
    # body = fields.Text(string='请求结果')
    res = fields.Text(string='返回结果')

    _sql = {
        "stock": '''SELECT si.FACILITY_ALIAS_ID 仓库号
              ,si.LOCN_AREA 仓间号
              ,si.LOCN_BRCD 仓位号
              ,si.ITEM_ID 货品ID
              ,si.ITEM_NAME 商品编码
              ,sum(si.ON_HAND_QTY) 数量
              FROM SEND_INVNTORY_LIST_TO_GOV si WHERE si.FACILITY_ALIAS_ID='HS01' AND si.COMPANY_CODE ='SCRC' --AND si.ITEM_NAME='10000218' 
              AND si.LOCN_AREA in(4,5，6，8，11，12，13，17，18，19，20，21，22，23，24，25，26，27，28，29，30，31，32，33)
              AND TO_CHAR(si.INVN_DATE, 'YYYY-MM-DD')=TO_CHAR(SYSDATE,'YYYY-MM-DD')
              GROUP  BY si.FACILITY_ALIAS_ID
                        ,si.LOCN_AREA
                        ,si.LOCN_BRCD
                        ,si.ITEM_ID
                        ,si.ITEM_NAME
              ORDER BY si.LOCN_AREA
                      ,si.LOCN_BRCD
                      ,si.ITEM_NAME''',
        "in_stock": '''SELECT sr.RECV_DATE_TIME 入库时间
      ,sr.FACILITY_ALIAS_ID 入库仓库号
      ,sr.LOCN_AREA  入库仓间号
      ,sr.LOCN_BRCD  入库仓位号
      ,sr.ITEM_ID 货品ID
      ,sr.ITEM_NAME  商品编码
      ,sr.BATCH_NBR  生产批次号
      ,sr.ON_HAND_QTY  数量
      ,sr.DIRECTION 业务描述
      ,sr.car_nbr   送货车号
      FROM SEND_RECV_LIST_TO_GOV sr
      WHERE sr.COMPANY_CODE ='SCRC' AND sr.FACILITY_ALIAS_ID ='HS01'AND sr.DIRECTION IN ('入库上架')
   --   AND sr.LOCN_AREA in(4,5，6，8，11，12，13，17，18，19，20，21，22，23，24，25，26，27，28，29，30，31，32，33)
      AND TO_CHAR(sr.RECV_DATE_TIME, 'YYYY-MM-DD')=TO_CHAR(SYSDATE,'YYYY-MM-DD')
      ORDER BY sr.RECV_DATE_TIME''',
        "out_stock": '''SELECT sd.DO_DATE_TIME 出库时间
      ,sd.FACILITY_ALIAS_ID 出库仓库号
      ,sd.LOCN_AREA  出库仓间号
      ,sd.LOCN_BRCD  出库仓位号
      ,sd.ITEM_ID 货品ID
      ,sd.ITEM_NAME  商品编码
      ,sd.BATCH_NBR  生产批次号
      ,sd.ON_HAND_QTY  数量
      ,sd.CUSTOMER_NAME 收货方名称
      ,sd.CUSTOMER_ADDR 收货方地址
      ,sd.DIRECTION 业务描述
      --,sd.*
      --,vb.CARRIERNAME AS 运输公司名称
      ,case when vb.TRANSMETHOD ='自车' then '国药试剂' else vb.CARRIERNAME end as 运输公司名称
      --,vb.GOODSCLASSNAME AS 运输车辆类型
      ,case when vb.GOODSCLASSNAME IS NOT NULL THEN '3' else vb.GOODSCLASSNAME end as 运输车辆类型
      ,vb.LICENSENO AS 车牌号
      ,vb.DRIVERNAME AS 驾驶员
      ,vb.DRIVERIDCARDNO AS 驾驶员身份证
      ,vb.SUPERCARGONAME AS 押运员
      ,vb.SUPERCARGOIDCARDNO AS 押运员身份证
      ,vb.TALLYNO AS 状态
      --,vb.* 
      FROM SEND_DO_LIST_TO_GOV sd 
      LEFT JOIN v_boxno_follow@link_tms vb ON sd.CASE_NBR =vb.boxno
      WHERE sd.COMPANY_CODE ='SCRC' AND sd.FACILITY_ALIAS_ID ='HS01'AND sd.DIRECTION IN ('原箱出库','拼箱出库')
      --AND sd.LOCN_AREA in(4,5，6，8，11，12，13，17，18，19，20，21，22，23，24，25，26，27，28，29，30，31，32，33)
      AND TO_CHAR(sd.DO_DATE_TIME, 'YYYY-MM-DD')=TO_CHAR(SYSDATE,'YYYY-MM-DD')
      ORDER BY sd.DO_DATE_TIME
      ''',
        "move_stock": '''select sr.RECV_DATE_TIME as 移库时间,     sd.FACILITY_ALIAS_ID as 移出仓库号,   sd.LOCN_AREA as 移出仓间号,        sd.LOCN_BRCD as 移出仓位号,         
       sd.id   as 出库ID,                 sr.FACILITY_ALIAS_ID as 目标仓库号,   sr.LOCN_AREA as 目标仓间号,        sr.LOCN_BRCD as 目标仓位号,  
       sr.id    as 入库ID,                sr.ITEM_ID AS 货品ID,                 sr.ITEM_NAME as 货品编码,          sr.BATCH_NBR as 生产批次号,  
       sr.on_hand_qty as 数量,            sd.inventory_qty as 移出货位结存,     sr.inventory_qty as 移入货位结存， sr.direction as 业务描述                          
from send_recv_list_to_gov sr inner join  send_do_list_to_gov sd 
on ( sd.direction = sr.direction and sd.LPN_ID = sr.LPN_ID)  
where sr.direction ='库内移动' AND sd.FACILITY_ALIAS_ID='HS01'
--AND sd.LOCN_AREA in(4,5，6，8，11，12，13，17，18，19，20，21，22，23，24，25，26，27，28，29，30，31，32，33)
AND TO_CHAR(sr.RECV_DATE_TIME, 'YYYY-MM-DD')=TO_CHAR(SYSDATE,'YYYY-MM-DD')
union           
select  D.RECV_DATE_TIME as 移库时间,    sd.FACILITY_ALIAS_ID  as 移出仓库号,    sd.LOCN_AREA as 移出仓间号,         sd.LOCN_BRCD as 移出仓位号,     
        sd.id as 出库ID,                 D.wh as 目标仓库号,                      D.LOCN_AREA as 目标仓间号,         D.LOCN_BRCD as 目标仓位号, 
        D.id as 入库ID,                  sd.ITEM_ID AS 货品ID,                    sd.ITEM_NAME as 货品编码,          sd.BATCH_NBR as 生产批次号,   
        sd.on_hand_qty as 数量,          sd.inventory_qty as 移出货位结存,     D.inventory_qty as 移入货位结存，    sd.direction as 业务描述
from send_do_list_to_gov sd  inner join 
    (select  sr.RECV_DATE_TIME, sr.FACILITY_ALIAS_ID as wh,sr.LOCN_AREA,sr.LOCN_BRCD,sr.lpn_id,sr.id,t.source_lpn_id,t.direction,sr.inventory_qty  
     from send_recv_list_to_gov sr inner join
         (select sr1.lpn_id,sr1.source_lpn_id,sr1.direction from send_recv_list_to_gov sr1 where sr1.direction ='库内下架' ) T
     on t.lpn_id = sr.lpn_id where sr.direction = '库内上架' and t.direction ='库内下架' ) D
on D.source_lpn_id = sd.lpn_id 
WHERE sd.FACILITY_ALIAS_ID='HS01'
--AND sd.LOCN_AREA in(4,5，6，8，11，12，13，17，18，19，20，21，22，23，24，25，26，27，28，29，30，31，32，33)
AND TO_CHAR(D.RECV_DATE_TIME, 'YYYY-MM-DD')=TO_CHAR(SYSDATE,'YYYY-MM-DD')
        '''
    }
    _map = {
        "stock": {
            "仓库号": "warehouseCode",
            "仓间号": "warehouseAreaCode",
            "仓位号": "locationCode",
            "货品ID": "merchandiseId",
            "数量": "amount"
        },
        "move_stock": {
            "移库时间": "transferTime",
            "仓储空间类型": "warehouseType",
            "移出仓库号": "fromWarehouseCode",
            "移出仓间号": "fromWarehouseAreaCode",
            "移出仓位号": "fromLocationCode",
            "目标仓库号": "toWarehouseCode",
            "目标仓间号": "toWarehouseAreaCode",
            "目标仓位号": "toLocationCode",
            "货品ID": "merchandiseId",
            "货品编码": "barCode",
            "生产批次号": "batchCode",
            "数量": "amount"
        },
        "warehouse_area": {
            "仓库号": "warehouseCode",
            "仓间号": "warehouseAreaCode",
            "仓位号": "locationCodeList",
            "仓库火灾危险性类别": "fireRisk",
            "仓间面积（㎡）": "acreage",
            "仓间最大存储量（吨）": "maxVolume",
            "消防措施": "fireFightingMeasures",
            "仓间储存危险化学品危险性类别": "riskGhsCategory"
        },
        "merchandise": {"货品ID": "merchandiseId",
                        "货品名称": "merchandiseName",
                        "货主ID": "ownerId",
                        "货主名称": "ownerName",
                        "货品存储空间类型": "warehouseType",
                        "是否为混合物": "isMixture",
                        "危险化学品名": "chemicalName",
                        "成分": "mixChemicleName",
                        "物理状态": "physicalState",
                        "其它属性": "otherAttribute",
                        "联合国编号（UN号）": "unCode",
                        "CAS号": "casCode",
                        "危险性类别（GHS）": "riskGhsItemCategory",
                        "危险货物类别": "riskItemCategory",
                        "火灾危险性类别": "fireRisk",
                        "化学结构": "organic",
                        "剧毒品特性": "deleterious",
                        "监控化学品（禁化武）特性": "monitored",
                        "特别管控危险化学品特性": "specialControlled",
                        "重点监管危险化学品特性": "regulatory",
                        "上海禁限控化学品特性": "prohibited",
                        "公安易制毒特性": "easyMadeDrug",
                        "公安易制爆特性": "easyToExplode",
                        "重大危险源申报临界值": "criticalQuantity",
                        "适用消防措施": "fireFightingMeasures",
                        "混放禁忌": "mixedTaboo",
                        "上传《化学品安全技术说明书》": "chemicalIdentificationReport",
                        "上传《化学品危险性分类报告》": "chemicalClassificationReport",
                        "密度值": "density",
                        "密度单位": "densityUnit",
                        "浓度": "concentration",
                        "规格数量": "unitCount",
                        "规格计量单位": "unit",
                        "规格包装单位名称": "specification",
                        }
    }

    def _trans_res(self, result, cursor):
        list_result = []
        for i in result:
            list_list = list(i)
            des = cursor.description  # 获取表详情，字段名，长度，属性等
            t = ",".join([item[0] for item in des])
            table_head = t.split(',')  # # 查询表列名 用,分割
            dict_result = dict(zip(table_head, list_list))  # 打包为元组的列表 再转换为字典
            list_result.append(dict_result)  # 将字典添加到list_result中
        return list_result

    def _map_list_res(self, list_result, map_dict):
        new_list = []
        for item in list_result:
            new_item = {}
            for key in map_dict:
                if key in item:
                    new_key = map_dict[key]
                    value = item[key]
                    new_item[new_key] = value
            new_list.append(new_item)
        return new_list

    def _post(self, body):
        res = requests.request("POST", "http://10.3.0.150:7673/java/sync", headers={"content-type": "application/json",
                                                                                    "charset": "utf-8"},
                               data=json.dumps(body))
        return res.json()

    def _trans_model_data(self, body):
        pat = re.compile(r"[A-Z]")
        record = {}
        for key in body:
            k_list = pat.findall(key)
            n_key = key
            for k in k_list:
                n_key = n_key.replace(k, "_" + k.lower())
            record[n_key] = body[key]
        return record

    def call(self, key):
        con = cx.connect("MANH_WM", "MANH_WM", "10.3.0.73:1521/orcl")
        cursor = con.cursor()
        logs = []
        if key == "move_stock":
            cursor.execute(self._sql[key])
            result = cursor.fetchall()
            list_result = self._map_list_res(self._trans_res(result, cursor), self._map[key])  # 拼装映射查询结果
            for item in list_result:
                now = datetime.datetime.now()
                if (now - item['transferTime']).seconds < 60 * 200:
                    move_post_body = {
                        "type": "incresync",
                        "data": {},
                        "router": "/report/trans"
                    }
                    item['warehouseType'] = 1
                    move_post_body['transferData'] = item

                    # 查询出仓库位状态
                    inventoryOutData = self.search_stock(item['fromWarehouseCode'], item['fromWarehouseAreaCode'],
                                                         item['fromLocationCode'], item['merchandiseId'])
                    move_post_body['inventoryOutData'] = inventoryOutData

                    # 查询入仓库位状态
                    inventoryInData = self.search_stock(item['toWarehouseCode'], item['toWarehouseAreaCode'],
                                                        item['toLocationCode'], item['merchandiseId'])
                    move_post_body['inventoryInData'] = inventoryInData

                    print(move_post_body, end='\n')

                    res = self._post(move_post_body)
                    logs.append({"api_address": move_post_body["router"],
                                 "status": '0' if res["success"] else '1',
                                 "res": res,
                                 "last_idx": 0
                                 })

        elif key == "stock":
            cursor.execute(self._sql[key])
            result = cursor.fetchall()
            if result:
                list_result = self._map_list_res(self._trans_res(result, cursor), self._map[key])

                # 覆盖更新
                self.env['wms.stock'].search([]).unlink()
                for item in list_result:
                    self.env['wms.stock'].create(self._trans_model_data(item))

                move_post_body = {
                    "type": "fullsync",
                    "data": {"inventoryData": list_result},
                    "router": "/sync/data/inventorySync"
                }
                res = self._post(move_post_body)

                logs.append({"api_address": move_post_body["router"],
                             "status": '0' if res["success"] else '1',
                             "res": res,
                             "last_idx": 0
                             })

        elif key == "warehouse_area":
            df = pd.read_excel("/opt/odoo-wms/local/wms/data/warehouse_area.xlsx")
            new_cols = []
            map_dict = self._map[key]
            for k in df.columns:
                if k in map_dict:
                    new_cols.append(map_dict[k])
                else:
                    new_cols.append(k)
            df.columns = new_cols
            df = df.fillna('')
            move_post_body = {
                "type": "fullsync",
                "data": {"warehouseData": df.to_dict(orient='records')},
                "router": "/sync/data/warehouseSync"
            }

            res = self._post(move_post_body)
            logs.append({"api_address": move_post_body["router"],
                         "status": '0' if res["success"] else '1',
                         "res": res,
                         "last_idx": 0
                         })

        elif key == "merchandise":
            # df = pd.read_excel("/opt/odoo-wms/local/wms/data/merchandise_file.xlsx", dtype={"危险货物类别": str})
            df = pd.read_excel("../data/merchandise_file.xlsx", dtype={"危险货物类别": str})
            df.loc[:, '上传《化学品危险性分类报告》'] = df.loc[:, '上传《化学品安全技术说明书》']
            new_cols = []
            del_cols = []
            map_dict = self._map[key]
            for k in df.columns:
                if k in map_dict:
                    new_cols.append(map_dict[k])
                else:
                    new_cols.append(k)
                    del_cols.append(k)
            df.columns = new_cols
            df.drop(del_cols, axis=1, inplace=True)
            df = df.fillna('')

            merchandise_dict_list = df.to_dict(orient='records')

            self.env['wms.merchandise'].search([]).unlink()
            for item in merchandise_dict_list:
                self.env['wms.merchandise'].create(self._trans_model_data(item))

            move_post_body = {
                "type": "fullsync",
                "data": {"merchandiseData": merchandise_dict_list},
                "router": "/sync/data/merchandiseSync"
            }

            res = self._post(move_post_body)
            logs.append({"api_address": move_post_body["router"],
                         "status": '0' if res["success"] else '1',
                         "res": res,
                         "last_idx": 0
                         })

        elif key == "merchandise_files":
            df = pd.read_excel("/opt/odoo-wms/local/wms/data/merchandise.xlsx", dtype={"危险货物类别": str})
            code_list = list(set(df['CAS索引号']))
            for code in code_list:
                # '/home/reagent/opt/sdspdf'
                filepath = os.path.join('/home/reagent/opt/sdspdf', code + '.pdf')
                print(filepath)
                move_post_body = {
                    "type": "filesync",
                    "filepath": filepath,
                }
                res = self._post(move_post_body)
                print(res)
                if res['success']:
                    print('============success===========')
                    df.loc[df[df['CAS索引号'] == code].index.tolist(), '上传《化学品安全技术说明书》'] = res['module'][
                        'key']
                    print(df[df['CAS索引号'] == code]['上传《化学品安全技术说明书》'])
                else:
                    df.loc[df[df['CAS索引号'] == code].index.tolist(), '上传《化学品安全技术说明书》'] = '上传失败'
            print(df['上传《化学品安全技术说明书》'])
            df.to_excel("/opt/odoo-wms/local/wms/data/merchandise_file.xlsx", index=False)

        for log in logs:
            record = self.env['wms.api.log'].create(log)
        cursor.close()
        con.close()
