# -*- coding: utf-8 -*-
{
    "name": "Configuración de usuario: Almacén y Diario de ventas",
    "version": "19.0.4",
    "category": "Inventory/Inventory",
    "summary": "Filtra inventario por almacén y facturas de venta por diario del usuario",
    "description": """
Funcionalidades:
1. Filtra el 'Resumen de inventario' por el almacén por defecto del usuario.
2. Filtra las 'Facturas de cliente' por el diario de ventas asignado al usuario.
3. Agrega campo de diario de ventas por defecto en el usuario.
4. Al crear facturas de venta, usa automáticamente el diario asignado al usuario.
5. Valida que solo se puedan confirmar facturas del diario asignado.

Motivo del patrón ir.actions.server:
- En el dominio de una acción (ir.actions.act_window) no existe 'user' en el evaluador JS.
- Se resuelve generando la acción desde servidor (ir.actions.server).
""",
    "author": "guven C.G.",
    "license": "LGPL-3",
    "depends": ["sale_stock", "account"],
    "data": [
        "views/account_move_views.xml",
        "views/stock_picking_type_views.xml",
        "views/res_users_views.xml",
    ],
    "installable": True,
    "application": False,
}
