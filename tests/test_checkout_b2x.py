# Copyright 2023 Alberto Carollo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import html

from odoo.http import root
from odoo.tests import HttpCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestCheckoutB2x(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].get_current_website()
        cls.product = cls.env["product.product"].create(
            {
                "name": "B2X Test Box",
                "list_price": 10.0,
                "website_published": True,
            }
        )
        cls.portal_user = new_test_user(
            cls.env,
            login="b2x_portal",
            groups="base.group_portal",
            name="B2X Portal",
            email="b2x_portal@example.com",
            street="Via Roma 1",
            city="Roma",
            zip="00100",
            country_id=cls.env.ref("base.it").id,
            state_id=cls.env.ref("base.state_it_rm").id,
        )
        cls.partner = cls.portal_user.partner_id

    def test_b2b_fields_always_displayed(self):
        self.assertTrue(self.website._display_partner_b2b_fields())

    def test_tour_company(self):
        self.start_tour("/shop", "l10n_it_website_sale_checkout_b2x_company")
        partner = self.env["res.partner"].search(
            [("email", "=", "company@example.com")]
        )
        self.assertEqual(len(partner), 1)
        self.assertEqual(partner.company_name, "B2X Company Srl")
        self.assertEqual(partner.vat, "IT12345670017")
        self.assertFalse(partner.fiscalcode)
        self.assertTrue(partner.electronic_invoice_subjected)
        self.assertEqual(partner.codice_destinatario, "ABC1234")
        self.assertFalse(partner.pec_destinatario)

    def test_tour_person(self):
        self.start_tour("/shop", "l10n_it_website_sale_checkout_b2x_person")
        partner = self.env["res.partner"].search(
            [("email", "=", "private@example.com")]
        )
        self.assertEqual(len(partner), 1)
        self.assertEqual(partner.fiscalcode, "RSSMRA85T10A562S")
        self.assertFalse(partner.company_name)
        self.assertFalse(partner.vat)
        self.assertFalse(partner.electronic_invoice_subjected)

    def _get_billing_checkbox(self):
        """Open the billing address of the portal user and return the checkbox"""
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "website_id": self.website.id,
                "order_line": [(0, 0, {"product_id": self.product.id})],
            }
        )
        session = self.authenticate("b2x_portal", "b2x_portal")
        session["sale_order_id"] = order.id
        root.session_store.save(session)
        response = self.url_open("/shop/address?partner_id=%d" % self.partner.id)
        self.assertEqual(response.status_code, 200)
        checkboxes = html.fromstring(response.content).xpath(
            "//input[@name='company_type']"
        )
        self.assertEqual(len(checkboxes), 1)
        return checkboxes[0]

    def test_edit_address_person(self):
        """A private customer is not shown as a company when editing"""
        checkbox = self._get_billing_checkbox()
        self.assertIsNone(checkbox.get("checked"))
        self.assertIsNone(checkbox.get("disabled"))

    def test_edit_address_company(self):
        """A customer with company name and VAT is shown as a company"""
        self.partner.write({"company_name": "B2X Srl", "vat": "IT12345670017"})
        checkbox = self._get_billing_checkbox()
        self.assertEqual(checkbox.get("checked"), "checked")
        self.assertIsNone(checkbox.get("disabled"))
