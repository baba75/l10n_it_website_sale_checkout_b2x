# Copyright 2023 Alberto Carollo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged

from odoo.addons.website.tools import MockRequest

from ..controllers.main import WebsiteSaleCheckoutB2x

BILLING = ("new", "billing")


@tagged("post_install", "-at_install")
class TestEinvoiceValidation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].get_current_website()
        cls.controller = WebsiteSaleCheckoutB2x()
        cls.italy = cls.env.ref("base.it")

    def _form(self, **values):
        """Posted values of an Italian company"""
        form = {
            "name": "B2X Buyer",
            "email": "buyer@example.com",
            "street": "Via Roma 1",
            "city": "Roma",
            "zip": "00100",
            "country_id": str(self.italy.id),
            "state_id": str(self.env.ref("base.state_it_rm").id),
            "company_type": "on",
            "company_name": "B2X Srl",
            "vat": "IT12345670017",
            "codice_destinatario": "0000000",
        }
        form.update(values)
        return {key: value for key, value in form.items() if value is not None}

    def _validate(self, form, mode=BILLING):
        data = dict(form)
        for field in ("country_id", "state_id"):
            data[field] = int(data[field])
        with MockRequest(self.env, website=self.website):
            return self.controller.checkout_form_validate(mode, form, data)

    def _einvoice_values(self, form):
        with MockRequest(self.env, website=self.website):
            return self.controller._b2x_einvoice_values(form, form["country_id"])

    def test_valid_company(self):
        error, messages = self._validate(self._form(pec_destinatario="b2x@pec.it"))
        self.assertFalse(error, messages)

    def test_addressee_code_length(self):
        error, _messages = self._validate(self._form(codice_destinatario="ABC12"))
        self.assertEqual(error.get("codice_destinatario"), "error")

    def test_pec_needs_standard_code(self):
        error, _messages = self._validate(
            self._form(codice_destinatario="ABC1234", pec_destinatario="b2x@pec.it")
        )
        self.assertEqual(error.get("codice_destinatario"), "error")

    def test_invalid_pec(self):
        error, _messages = self._validate(self._form(pec_destinatario="not-an-email"))
        self.assertEqual(error.get("pec_destinatario"), "error")

    def test_person_not_checked(self):
        """Without "I'm a Company" the e-invoice fields are ignored"""
        form = self._form(company_type=None, codice_destinatario="ABC12")
        error, _messages = self._validate(form)
        self.assertNotIn("codice_destinatario", error)

    def test_shipping_not_checked(self):
        form = self._form(codice_destinatario="ABC12")
        error, _messages = self._validate(form, mode=("new", "shipping"))
        self.assertNotIn("codice_destinatario", error)

    def test_einvoice_values_italy(self):
        values = self._einvoice_values(
            self._form(codice_destinatario=" abc1234 ", pec_destinatario="")
        )
        self.assertEqual(
            values,
            {
                "electronic_invoice_subjected": True,
                "codice_destinatario": "ABC1234",
                "pec_destinatario": False,
            },
        )

    def test_einvoice_values_foreign_company(self):
        form = self._form(
            country_id=str(self.env.ref("base.fr").id),
            pec_destinatario="b2x@pec.it",
        )
        values = self._einvoice_values(form)
        self.assertEqual(values["codice_destinatario"], "XXXXXXX")
        self.assertFalse(values["pec_destinatario"])
