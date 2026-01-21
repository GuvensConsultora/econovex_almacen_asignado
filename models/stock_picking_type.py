# -*- coding: utf-8 -*-
from odoo import api, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    @api.model
    def action_inventory_overview_my_wh(self):
        """
        Devuelve la misma acción del 'Resumen de inventario' (stock.stock_picking_type_action),
        pero filtrada por el almacén por defecto del usuario (res.users.property_warehouse_id).

        Por qué así:
        - En 'Valor del dominio' del act_window el evaluador del cliente NO conoce 'user'.
        - Desde servidor sí podemos leer env.user y armar domain real.
        """
        # Leemos la acción base como dict (estructura que el cliente entiende).
        action = self.env.ref("stock.stock_picking_type_action").read()[0]

        # Tomamos el almacén por defecto del usuario (campo estándar de stock en res.users).
        wh = self.env.user.property_warehouse_id

        # Si el usuario tiene warehouse, filtramos por ese.
        # Si no tiene, dejamos la acción sin filtro (muestra todo).
        if wh:
            action["domain"] = [("warehouse_id", "=", wh.id)]

        return action
