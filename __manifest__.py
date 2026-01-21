# -*- coding: utf-8 -*-
{
    "name": "Inventory Overview: My Default Warehouse",
    "version": "19.0.1",
    "category": "Inventory/Inventory",
    "summary": "Filtra el Resumen de inventario por el almacén por defecto del usuario",
    "description": """
Mostrar el  'Resumen de inventario que abre el dashboard estándar
(stock.picking.type, vista kanban) filtrando por el almacén por defecto del usuario
(res.users.property_warehouse_id).

Motivo:
- En el dominio de una acción (ir.actions.act_window) no existe 'user' en el evaluador JS.
- Se resuelve correctamente generando la acción desde servidor (ir.actions.server).
""",
    "author": "guven C.G.",
    "license": "LGPL-3",
    "depends": ["stock"],
    "data": [
       # "data/inventory_overview_action.xml",
    ],
    "installable": True,
    "application": False,
}
