from odoo import models, fields, api,tools
import logging
_logger = logging.getLogger(__name__)

class StockDispatchView(models.Model):
    _name = 'wms.stock.dispatch.view'
    _auto = False

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        wms_stock_dispatch_view = """
        CREATE OR REPLACE VIEW wms_stock_dispatch_view AS (
        SELECT 
            wsd."id",
            woc.license_num as carrierPlateNumber,
            wsd.operation_time as enterExitTime,
            wsd.dispatch_type as enterExitType,
            woc.kind as carrierPlateType,
            wo1.full_name as carrierName,
            woe1."name" as carrierDriverName,
            woe1.idcard as carrierDriverIdcard,
            woe2."name" as escort,
            woe2.idcard as escortIdcard
        FROM wms_stock_dispatch wsd
        LEFT JOIN wms_organization_employee woe1 ON (wsd.organization_employee_driver_id = woe1."id")
        LEFT JOIN wms_organization_employee woe2 ON (wsd.organization_employee_supercargo_id = woe2."id")
        LEFT JOIN wms_organization wo1 ON (wsd.organization_id = wo1."id") 
        LEFT JOIN wms_organization_car woc ON (wsd.organization_car_id = woc."id")  
        );
        """
        self.env.cr.execute(wms_stock_dispatch_view)






class StockTransactionMoveView(models.Model):
    _name = 'wms.stock.transaction.move.view'
    _auto = False
    def init(self):
        wms_stock_transaction_move_view = '''
        CREATE OR REPLACE VIEW wms_stock_transaction_move_view AS (
            SELECT
                p1."id",
                p1.transfertime,
                p1.warehouse_area_type,
                p1.fromwarehousecode,
                p1.fromwarehouseareacode,
                p1.fromlocationcode,
                p1.towarehousecode,
                p1.towarehouseareacode,
                p1.tolocationcode,
                p1.merchandise_id,
                p1.bar_code,
                p1.batch_code,
                p1.amount,
                w1.warehouse_code as in_warehouse_code,
                w1.warehouse_area_code as in_warehouse_area_code,
                w1.location_code as in_location_code,
                w1.merchandise_id as in_merchandise_id,
                w1.amount as in_amount,
                w2.warehouse_code as out_warehouse_code,
                w2.warehouse_area_code as out_warehouse_area_code,
                w2.location_code as out_location_code,
                w2.merchandise_id as out_merchandise_id,
                w2.amount as out_amount
                FROM 
                (SELECT
				t1."id" as "id",
				t1.create_date as transferTime,
				t1.warehouse_area_type,
				t1.warehouse_code as fromWarehouseCode,
				t1.warehouse_area_code as fromWarehouseAreaCode,
				t1.location_code as fromLocationCode,
				(
				SELECT
						t2.warehouse_code
				FROM
						wms_stock_transaction t2
				WHERE
						t2.merchandise_id = t1.merchandise_id
										AND t2.create_date > t1.create_date
				ORDER BY
						t2.warehouse_code
						LIMIT 1
				) AS toWarehouseCode,
				(
				SELECT
						t2.warehouse_area_code
				FROM
						wms_stock_transaction t2
				WHERE
						t2.merchandise_id = t1.merchandise_id
										AND t2.create_date > t1.create_date
				ORDER BY
						t2.warehouse_code
						LIMIT 1
				) AS toWarehouseAreaCode,
				(
				SELECT
						t2.location_code
				FROM
						wms_stock_transaction t2
				WHERE
						t2.merchandise_id = t1.merchandise_id
						AND t2.create_date > t1.create_date
				ORDER BY
						t2.warehouse_code
						LIMIT 1
				) AS toLocationCode,
				t1.merchandise_id,
				t1.bar_code,
				t1.batch_code,
				t1.amount

		FROM 
				wms_stock_transaction t1
		WHERE
				t1.transaction_type = 'MOVE'
				AND t1.amount < 0
		ORDER BY
				t1.create_date ASC,
				t1.id ASC) as  p1
				
        LEFT JOIN wms_stock w1 
        ON p1.fromwarehousecode = w1.warehouse_code
        AND p1.fromwarehouseareacode = w1.warehouse_area_code
        AND p1.fromlocationcode = w1.location_code
        AND p1.merchandise_id = w1.merchandise_id
        
        LEFT JOIN wms_stock w2 
        ON p1.towarehousecode = w2.warehouse_code
        AND p1.towarehouseareacode = w2.warehouse_area_code
        AND p1.tolocationcode = w2.location_code
        AND p1.merchandise_id = w2.merchandise_id

        );
              '''
        self.env.cr.execute(wms_stock_transaction_move_view)

