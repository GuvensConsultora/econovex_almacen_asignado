# -*- coding: utf-8 -*-
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_sale_journal_id = fields.Many2one(
        "account.journal",
        string="Diario de ventas por defecto",
        domain="[('type', '=', 'sale')]",
        company_dependent=True,
        help="Diario de ventas que se usará por defecto para este usuario.",
    )
