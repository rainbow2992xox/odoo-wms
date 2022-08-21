from odoo import models, fields, api
import logging
from ..lib import until

_logger = logging.getLogger(__name__)
api = until.Api()

class ApiLog(models.Model):
    _name = 'wms.api.log'
    api_address = fields.Char('API地址')
    last_idx = fields.Integer(string="最后一条记录ID")
    status = fields.Selection([('0', '成功'), ('1', '失败')], string='状态')
    body = fields.Text(string='请求结果')
    res = fields.Text(string='返回结果')


    def call(self,key):
        res = api.call_java_api(key)
        for item in res:
            record = self.env['wms.api.log'].create(item)


