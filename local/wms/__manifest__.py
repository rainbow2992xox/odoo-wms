{
    'name': 'wms',
    'version': '1.0.0',
    'depends': ['base'],
    'data': [
        'views/stock.xml',
        'views/in_stock.xml',
        'views/out_stock.xml',
        'views/move_stock.xml',
        'views/vehicle.xml',
        'views/vehicle_nor.xml',
        'views/driver.xml',
        'views/api_log.xml',
        'views/merchandise.xml',
        'views/warehouse_area.xml',
        'data/wms_actions_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/wms/static/src/css/style.scss',
        ],
    }

}
