# -*- coding: utf-8 -*-
import logging
from odoo import api, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def action_invoices_my_journal(self):
        """
        Por qué: Filtra facturas de venta por el diario asignado al usuario
        Patrón: Server action (mismo que inventario) - evita limitaciones de domain evaluation en JS
        Tip: ir.actions.act_window no puede evaluar 'user' en JS, se resuelve en Python
        """
        action = self.env["ir.actions.act_window"]._for_xml_id("account.action_move_out_invoice_type")

        user_journal = self.env.user.sale_journal_id

        _logger.info(
            "=== FILTRO DIARIO === Usuario: %s (ID: %s), Diario: %s (ID: %s)",
            self.env.user.name, self.env.user.id,
            user_journal.name if user_journal else "SIN DIARIO",
            user_journal.id if user_journal else None
        )

        # Solo filtrar si el usuario tiene diario asignado
        if user_journal:
            action["domain"] = [("journal_id", "=", user_journal.id)]
            # Contexto por defecto al crear
            ctx = dict(self.env.context or {})
            ctx["default_journal_id"] = user_journal.id
            action["context"] = ctx

        _logger.info("=== FILTRO DIARIO === Domain aplicado: %s", action.get("domain"))

        return action

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)

        # move_type puede venir del contexto o de defaults
        move_type = self.env.context.get("default_move_type") or defaults.get("move_type")

        # Solo aplicar para facturas de venta
        if move_type in ("out_invoice", "out_refund"):
            user_journal = self.env.user.sale_journal_id
            if user_journal:
                defaults["journal_id"] = user_journal.id

        return defaults

    def action_post(self):
        """
        Por qué: Validar que el usuario solo confirme facturas de su diario asignado
        Patrón: Constraint en acción crítica (confirmación)
        Tip: Validaciones de negocio van en acciones, no en write/create
        """
        user_journal = self.env.user.sale_journal_id

        # Solo validar si el usuario tiene un diario asignado
        if user_journal:
            for move in self:
                # Solo validar facturas de venta
                if move.move_type in ("out_invoice", "out_refund"):
                    if move.journal_id != user_journal:
                        raise UserError(_(
                            "No puede confirmar facturas del diario '%s'.\n"
                            "Su diario asignado es: '%s'"
                        ) % (move.journal_id.name, user_journal.name))

        return super().action_post()
