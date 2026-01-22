# -*- coding: utf-8 -*-
from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)

        # Solo aplicar para facturas de venta
        if defaults.get("move_type") in ("out_invoice", "out_refund"):
            user_journal = self.env.user.sale_journal_id
            if user_journal:
                defaults["journal_id"] = user_journal.id

        return defaults
