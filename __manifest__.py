# Copyright 2023 Alberto Carollo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "E-commerce Checkout b2x",
    "summary": """
        Let the user choose between B2C and B2B mode at checkout
        and set the appropriate mandatory fields
        """,
    "description": """
        [ENG]

        This module lets the user decide during checkout if they buy as a private person or company.
        In the first case, the input of the Fiscal Code is enforced; if buying as a company,
        fields "Company Name" and "VAT" are displayed and set to mandatory.
        Italian companies also enter the electronic invoice Addressee Code (SDI)
        or PEC, and the customer is enabled to electronic invoicing.

        [ITA]

        Questo modulo permette all'utente di decidere in fase di checkout se
        acquistare come privato o azienda. Nel primo caso viene imposto
        l'inserimento del Codice Fiscale; in caso di acquisto come azienda,
        i campi "Ragione Sociale" e "IVA" vengono visualizzati e impostati come obbligatori.
        Le aziende italiane inseriscono anche il Codice Destinatario (SDI) o la PEC
        e il cliente viene abilitato alla fatturazione elettronica.
    """,
    "author": "Alberto Carollo",
    "website": "https://github.com/baba75/l10n_it_website_sale_checkout_b2x",
    "category": "Localization/Italy",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "website_sale",
        "l10n_it_website_sale_fiscalcode",
        "l10n_it_fatturapa",
    ],
    "data": [
        "views/templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "l10n_it_website_sale_checkout_b2x/static/src/js/l10n_it_website_sale_checkout_b2x.js",
        ],
        "web.assets_tests": [
            "l10n_it_website_sale_checkout_b2x/static/tests/tours/*.js",
        ],
    },
    "installable": True,
}
