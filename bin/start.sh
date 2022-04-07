#!/bin/sh
ROOT=$(dirname $0)/..
PYTHON=$ROOT/env/bin/python3
ODOO=$ROOT/src/odoo/odoo-bin
$PYTHON $ODOO -c $ROOT/odoo.cfg "$@"
exit $?