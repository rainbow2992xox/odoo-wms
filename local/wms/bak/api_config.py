from odoo import models, fields, api
import requests, json
import logging

_logger = logging.getLogger(__name__)


class ApiConfig(models.Model):
    _name = 'wms.api.config'
    api_address = fields.Char('API地址')
    api_type = fields.Selection([('0', '批量'), ('1', '增量')], string='接口类型')
    maser_model = fields.Selection(selection='fetch_model', string='主模型')
    db_field = fields.Selection(selection='fetch_db_field', string='模型字段')
    api_keyword = fields.Char('关键词')
    api_field = fields.Char(string='API字段')

    @api.model
    def map_fields(self, o_dict, map_dict):
        n_dict = {}
        for key in map_dict:
            n_dict[map_dict[key]] = o_dict[key]
        return n_dict

    @api.model
    def create_map_dict(self, config):
        map_dict = {}
        for item in config:
            map_dict[item["db_field"].split(".")[-1]] = item["api_field"]
        return map_dict

    @api.model
    def create_body(self, config, records):
        master_model = config[0]["maser_model"]
        select_text = ",".join([x["db_field"] for x in config])
        map_dict = self.create_map_dict(config)

        # body_sql = '''SELECT %s FROM %s''' % (select_text, master_model)
        # self.env.cr.execute(body_sql)
        body = [self.map_fields(record, map_dict) for record in records]
        return body

    @api.model
    def fetch_model(self):
        sql = '''SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE "table_name" like 'wms_%' '''
        self.env.cr.execute(sql)
        result = self.env.cr.dictfetchall()
        selections = [(x["table_name"], x["table_name"]) for x in result]
        _logger.info(selections)
        return selections

    @api.model
    def fetch_db_field(self):
        sql = '''SELECT a.table_name,b.COLUMN_NAME  FROM information_schema.TABLES a LEFT JOIN information_schema.COLUMNS b ON a.table_name = b.TABLE_NAME WHERE a.table_name like 'wms_%' ORDER BY a.table_name '''
        self.env.cr.execute(sql)
        result = self.env.cr.dictfetchall()
        selections = [(x['table_name'] + '.' + x["column_name"], x['table_name'] + '.' + x["column_name"]) for x in
                      result]

        return selections

    # 监听是否需要调用接口
    @api.model
    def scan_db(self):
        api_list = []
        api_sql = '''SELECT DISTINCT(api_address,maser_model) FROM wms_api_config'''
        self.env.cr.execute(api_sql)
        api_res = self.env.cr.dictfetchall()
        for item in api_res:
            item = item['row']
            item = item.replace('(', '')
            item = item.replace(')', '')
            item = item.split(',')
            api_list.append({"api_address": item[0], "api_view": item[1]})
        _logger.info("======================")
        _logger.info(api_list)

        for api in api_list:
            # 查询最新调用记录
            log_sql = '''
                   SELECT * FROM wms_api_log WHERE api_address='%s' AND status = '0' ORDER BY create_date DESC LIMIT 1
                   ''' % (api["api_address"])
            self.env.cr.execute(log_sql)
            log_res = self.env.cr.dictfetchall()

            # 确定是否有更新
            if log_res:
                last_idx = log_res[0]['last_idx']
                view_sql = '''SELECT * FROM %s WHERE "id" > %s ORDER BY "id" DESC''' % (api["api_view"], last_idx)
            else:
                view_sql = '''SELECT * FROM %s ORDER BY "id" DESC''' % (api["api_view"])

            self.env.cr.execute(view_sql)
            records = self.env.cr.dictfetchall()

            if records:
                self.call_java_api(api["api_address"], records)

        # 监听数据库变化
        # self.call_java_api("/report/vehicle",(1,2))
        # self.call_java_api("/sync/data/inventorySync")
        # pass

    @api.model
    def save_api_log(self, vals):
        other_object = self.env['wms.api.log']
        return other_object.create(vals)

    @api.model
    def call_java_api(self, api_address, records):

        # 载入字段映射
        config_sql = '''
        SELECT * FROM wms_api_config WHERE api_address='%s'
        ''' % (api_address)
        self.env.cr.execute(config_sql)
        config = self.env.cr.dictfetchall()

        # 按API一级字段分组
        body = {}
        for item in config:
            if item["api_keyword"]:
                if item["api_keyword"] in body:
                    body[item["api_keyword"]].append(item)
                else:
                    body[item["api_keyword"]] = [item]

        if body:
            for api_keyword in body:
                field_list = body[api_keyword]
                result = self.create_body(field_list, records)
                if field_list[0]["api_type"] == "0":
                    body[api_keyword] = result
                else:
                    body[api_keyword] = result[0]

        else:
            result = self.create_body(config, records)
            if config[0]["api_type"] == "0":
                body = result
            else:
                body = result[0]

        url = 'http://localhost:8081/javaMock'
        res = requests.post(url, data=json.dumps({'data': body, 'api_address': api_address}),
                            headers={'Content-Type': 'application/json'})

        log_dict = {'api_address': api_address,
                    'last_idx': records[0]['id'],
                    'status': '0',
                    "res": res.json()['result']}

        if res.json()['result']['status'] == '0':
            log_dict['status'] = '0'
        else:
            log_dict['status'] = '1'

        self.save_api_log(log_dict)

    # 组装接口数据
    # for api_address in api_dict:
    #     postJson ={
    #         "api_address":"",
    #         "body":{},
    #         "type":None
    #     }
    #
    #
    #
    # #获取主模型
    # master_model = config[0]["maser_model"]
    #
    # #组装接口字段
    # select_text = ",".join([x["db_field"] + " as " + x["api_field"] for x in config])
    #
    #
    #
    #
    # body_sql= '''SELECT %s FROM %s'''%(select_text,master_model)
    #
    #
    #
    # #判断批量接口还是增量接口
    #
    # self.env.cr.execute(body_sql)
    # body = self.env.cr.dictfetchall()
    #
    # _logger.info("========TEST==========")
    # _logger.info(body)
