{
    'name': 'wms',
    'version': '1.0.0',
    'depends': ['base'],
    'data': ['views/vehicle.xml',
             'views/api_log.xml',
             'views/stock.xml'],
    'assets': {
        'web.assets_backend': [
            '/wms/static/src/css/style.scss',
        ],
    }

}
