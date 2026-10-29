# Copyright 2023 Alberto Carollo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class Website(models.Model):
    _inherit = "website"

    def _display_partner_b2b_fields(self):
        # The B2B/B2C switch needs the "Company Name" and "VAT" fields
        # in the checkout address form, so they are always displayed.
        return True
