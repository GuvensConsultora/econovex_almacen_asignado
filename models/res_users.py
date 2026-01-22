# -*- coding: utf-8 -*-
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_sale_journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Diario de ventas por defecto",
        domain="[('type', '=', 'sale'), ('company_id', '=', current_company_id)]",
        company_dependent=True,
        help="Diario de ventas que se usará por defecto para este usuario.",
    )
