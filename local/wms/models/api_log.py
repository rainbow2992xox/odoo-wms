from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class ApiLog(models.Model):
    _name = 'wms.api.log'
    api_address = fields.Char('API地址')
    last_idx = fields.Integer(string="最后一条记录ID")
    status = fields.Selection([('0', '成功'), ('1', '失败')], string='状态')
    res = fields.Char(string='返回结果')




