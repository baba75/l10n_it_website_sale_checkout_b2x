# -*- coding: utf-8 -*-
{
    'name': "E-commerce Checkout b2x",

    'summary': """
        Let the user choose between B2C and B2B mode at checkout 
        and set the appropriate mandatory fields
        """,

    'description': """
        [ENG]
        
        This module lets the user decide during checkout if they buy as a private person or company. 
        In the first case, the input of the Fiscal Code is enforced; if buying as a company, 
        fields "Company Name" and "VAT" are displayed and set to mandatory.
        
        [ITA]
        
        Questo modulo permette all'utente di decidere in fase di checkout se 
        acquistare come privato o azienda. Nel primo caso viene imposto 
        l'inserimento del Codice Fiscale; in caso di acquisto come azienda, 
        i campi "Ragione Sociale" e "IVA" vengono visualizzati e impostati come obbligatori.
    """,

    'author': "Alberto Carollo",
    'website': "https://github.com/baba75",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localization/Italy',
    'version': '14.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['l10n_it_website_sale_fiscalcode',
                'l10n_it_website_sale_fatturapa'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
    ],
}
