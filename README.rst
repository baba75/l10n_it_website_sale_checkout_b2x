ENG
===
This module lets the user decide during checkout if they buy as a private person or company. 
In the first case, the input of the Fiscal Code is enforced; if buying as a company, 
fields "Company Name" and "VAT" are displayed and set to mandatory.
        
ITA
===
Questo modulo permette all'utente di decidere in fase di checkout se 
acquistare come privato o azienda. Nel primo caso viene imposto 
l'inserimento del Codice Fiscale; in caso di acquisto come azienda, 
i campi "Ragione Sociale" e "IVA" vengono visualizzati e impostati come obbligatori.

Odoo 16.0
=========
Depends on ``website_sale``, ``l10n_it_website_sale_fiscalcode`` and
``l10n_it_fatturapa`` (OCA l10n-italy).
The "Company Name" and "VAT" fields are always displayed in the checkout
address form, so the "Show b2b fields" option doesn't need to be enabled.

Italian companies also enter the electronic invoice Addressee Code (SDI),
default 0000000, or their PEC. The customer is then enabled to electronic
invoicing; foreign companies get the Addressee Code XXXXXXX.
