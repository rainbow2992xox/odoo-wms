#!/bin/sh
ROOT=$(dirname $0)/..
PYTHON=/root/anaconda3/bin/python
ODOO=$ROOT/src/odoo/odoo-bin
$PYTHON $ODOO -c $ROOT/odoo-pro.cfg --update=wms "$@"
exit $?
