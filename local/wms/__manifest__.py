{
    'name': 'wms',
    'version': '1.1.0',
    'depends': ['base'],
    'data': [
        'views/stock.xml',
        'views/in_stock.xml',
        'views/out_stock.xml',
        'views/move_stock.xml',
        'views/vehicle.xml',
        'views/api_log.xml'
    ],
    'assets': {
        'web.assets_backend': [
            '/wms/static/src/css/style.scss',
        ],
    }

}
