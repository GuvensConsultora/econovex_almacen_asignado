# -*- coding: utf-8 -*-
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    sale_journal_id = fields.Many2one(
        "account.journal",
        string="Diario de ventas por defecto",
        domain=[("type", "=", "sale")],
        help="Diario de ventas que se usará por defecto para este usuario.",
    )
