# -*- coding: utf-8 -*-
from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

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
