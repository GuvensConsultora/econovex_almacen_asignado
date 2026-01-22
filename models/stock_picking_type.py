# -*- coding: utf-8 -*-
import logging
from odoo import api, models

_logger = logging.getLogger(__name__)


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    @api.model
    def action_inventory_overview_my_wh(self):
        """
        Devuelve la misma acción del 'Resumen de inventario' (stock.stock_picking_type_action),
        pero filtrada por el almacén por defecto del usuario (res.users.property_warehouse_id).
        """
        action = self.env["ir.actions.act_window"]._for_xml_id("stock.stock_picking_type_action")

        # Leemos el usuario con sudo para asegurar acceso al property field
        user = self.env.user
        wh = user.property_warehouse_id

        _logger.info(
            "=== FILTRO ALMACEN === Usuario: %s (ID: %s), Almacén: %s (ID: %s)",
            user.name, user.id,
            wh.name if wh else "SIN ALMACEN",
            wh.id if wh else None
        )

        if wh:
            # Forzamos el dominio como string para evitar problemas de evaluación
            action["domain"] = [("warehouse_id", "=", wh.id)]
            # También limpiamos contexto que pueda interferir
            ctx = dict(self.env.context)
            ctx["default_warehouse_id"] = wh.id
            action["context"] = ctx

        _logger.info("=== FILTRO ALMACEN === Domain aplicado: %s", action.get("domain"))

        return action
