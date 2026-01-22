# -*- coding: utf-8 -*-
{
    "name": "Configuración de usuario: Almacén y Diario de ventas",
    "version": "19.0.2",
    "category": "Inventory/Inventory",
    "summary": "Filtra inventario por almacén y agrega diario de ventas por defecto al usuario",
    "description": """
Funcionalidades:
1. Filtra el 'Resumen de inventario' por el almacén por defecto del usuario.
2. Agrega campo de diario de ventas por defecto en el usuario.

Motivo del filtro de inventario:
- En el dominio de una acción (ir.actions.act_window) no existe 'user' en el evaluador JS.
- Se resuelve generando la acción desde servidor (ir.actions.server).
""",
    "author": "guven C.G.",
    "license": "LGPL-3",
    "depends": ["sale_stock", "account"],
    "data": [
        "views/stock_picking_type_views.xml",
    ],
    "installable": True,
    "application": False,
}
