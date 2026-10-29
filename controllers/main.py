# Copyright 2023 Alberto Carollo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.tools import single_email_re

from odoo.addons.l10n_it_fatturapa.models.partner import STANDARD_ADDRESSEE_CODE
from odoo.addons.website_sale.controllers.main import WebsiteSale

# Addressee code used by l10n_it_fatturapa for foreign partners
FOREIGN_ADDRESSEE_CODE = "XXXXXXX"


class WebsiteSaleCheckoutB2x(WebsiteSale):
    def _b2x_is_company(self, mode, form_values):
        """The customer checked "I'm a Company" in the billing address"""
        return mode[1] == "billing" and bool(form_values.get("company_type"))

    def _b2x_einvoice_values(self, form_values, country_id):
        """Electronic invoice values of a company customer"""
        country = request.env["res.country"].browse(int(country_id or 0))
        if country.code != "IT":
            return {
                "electronic_invoice_subjected": True,
                "codice_destinatario": FOREIGN_ADDRESSEE_CODE,
                "pec_destinatario": False,
            }
        code = (form_values.get("codice_destinatario") or "").strip().upper()
        pec = (form_values.get("pec_destinatario") or "").strip()
        return {
            "electronic_invoice_subjected": True,
            "codice_destinatario": code or False,
            "pec_destinatario": pec or False,
        }

    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super().checkout_form_validate(
            mode, all_form_values, data
        )
        if not self._b2x_is_company(mode, all_form_values):
            return error, error_message

        einvoice = self._b2x_einvoice_values(all_form_values, data.get("country_id"))
        code = einvoice["codice_destinatario"]
        pec = einvoice["pec_destinatario"]
        if code and len(code) != 7:
            error["codice_destinatario"] = "error"
            error_message.append(
                _("The Addressee Code (SDI) must be 7 characters long.")
            )
        if pec and not single_email_re.match(pec):
            error["pec_destinatario"] = "error"
            error_message.append(_("Invalid PEC! Please enter a valid email address."))
        elif pec and code and code != STANDARD_ADDRESSEE_CODE:
            error["codice_destinatario"] = "error"
            error_message.append(
                _(
                    "To receive the invoice by PEC, the Addressee Code (SDI) "
                    "must be %s.",
                    STANDARD_ADDRESSEE_CODE,
                )
            )
        if error:
            # The missing fields are already reported by website_sale
            return error, error_message

        # Same check done by l10n_it_fatturapa when the partner is saved
        partner_values = {
            field: data.get(field)
            for field in (
                "company_name",
                "vat",
                "street",
                "zip",
                "city",
                "state_id",
                "country_id",
            )
        }
        partner_values.update(einvoice)
        partner_dummy = request.env["res.partner"].new(partner_values)
        try:
            partner_dummy._check_ftpa_partner_data()
        except ValidationError as e:
            error["codice_destinatario"] = "error"
            error_message.append(e.args[0])
        return error, error_message

    def _checkout_form_save(self, mode, checkout, all_values):
        if self._b2x_is_company(mode, all_values):
            checkout.update(
                self._b2x_einvoice_values(all_values, checkout.get("country_id"))
            )
        return super()._checkout_form_save(mode, checkout, all_values)
