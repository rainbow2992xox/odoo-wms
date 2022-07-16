from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class Main(http.Controller):
  # 对于auth = 'none'
  # 哪怕是已验证用户在访问路径时用户记录也是空的。使用这一个验证的场
  # 景是所响应的内容对用户不存在依赖，或者是在服务端模块中提供与数据库无关的功能。
  #
  # auth = 'public'的值将未验证用户设置为一个带有XML ID
  # base.public_user的特殊用户，已验证用户设置为用户自己的记录。
  # 对于所提供的功能同时针对未验证和已验证用户而已验证用户又具有一些
  # 额外的功能时应选择它，前面的代码中已经演示。
  #
  # 使用auth = 'user'
  # 来确保仅已验证用户才能访问所提供的内容。通过这个方法，我们可以确保
  # request.env.user指向已有用户。
  #


  @http.route('/javaMock', type='json', auth='none',csrf=False)
  def books_json(self):
    body  = request.jsonrequest
    _logger.info("==========MOCK==========")
    _logger.info(body)
    return {
      'api_address':body['api_address'],
      'status':'0',
      'res':{'test':'test'}
    }



