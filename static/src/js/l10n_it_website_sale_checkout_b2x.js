/** @odoo-module **/
/* Copyright 2023 Alberto Carollo
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import publicWidget from "web.public.widget";

const COMPANY_FIELDS = ["company_name", "vat"];
const PERSON_FIELDS = ["fiscalcode"];
// Electronic invoice fields of Italian companies: field name => required
const EINVOICE_FIELDS = {codice_destinatario: true, pec_destinatario: false};

publicWidget.registry.L10nItWebsiteSaleCheckoutB2x = publicWidget.Widget.extend({
    selector: ".oe_website_sale form.checkout_autoformat",
    events: {
        "change input[name='company_type']": "_onChangeCompanyType",
        "change select[name='country_id']": "_onChangeCountry",
    },

    /**
     * @override
     */
    start() {
        this.b2xInput = this.el.querySelector("input[name='company_type']");
        if (this.b2xInput) {
            this._updateB2xFields();
        }
        return this._super(...arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Show the fields of the selected customer type and make them mandatory;
     * hide the other ones and disable them, so that they are not posted.
     *
     * @private
     */
    _updateB2xFields() {
        const isCompany = this.b2xInput.checked;
        for (const fieldName of COMPANY_FIELDS) {
            this._toggleField(fieldName, isCompany);
        }
        for (const fieldName of PERSON_FIELDS) {
            this._toggleField(fieldName, !isCompany);
        }
        const isItalianCompany = isCompany && this._isItalySelected();
        for (const [fieldName, required] of Object.entries(EINVOICE_FIELDS)) {
            this._toggleField(fieldName, isItalianCompany, isItalianCompany && required);
        }
    },

    /**
     * @private
     * @returns {Boolean}
     */
    _isItalySelected() {
        const select = this.el.querySelector("select[name='country_id']");
        const option = select && select.selectedOptions[0];
        return Boolean(option) && (option.dataset.code || "").toUpperCase() === "IT";
    },

    /**
     * @private
     * @param {String} fieldName
     * @param {Boolean} active
     * @param {Boolean} [required=active]
     */
    _toggleField(fieldName, active, required = active) {
        const input = this.el.querySelector(`[name='${fieldName}']`);
        if (!input) {
            return;
        }
        input.parentElement.classList.toggle("d-none", !active);
        input.disabled = !active;
        const label = this.el.querySelector(`label[for='${fieldName}']`);
        if (label) {
            label.classList.toggle("label-optional", !required);
        }
        this._setRequired(fieldName, required);
    },

    /**
     * Add or remove a field from the comma separated list of
     * mandatory fields checked by website_sale on submit.
     *
     * @private
     * @param {String} fieldName
     * @param {Boolean} required
     */
    _setRequired(fieldName, required) {
        const requiredInput = this.el.querySelector("input[name='field_required']");
        if (!requiredInput) {
            return;
        }
        const fields = new Set(requiredInput.value.split(",").filter(Boolean));
        if (required) {
            fields.add(fieldName);
        } else {
            fields.delete(fieldName);
        }
        requiredInput.value = [...fields].join(",");
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _onChangeCompanyType() {
        this._updateB2xFields();
    },

    /**
     * @private
     */
    _onChangeCountry() {
        if (this.b2xInput) {
            this._updateB2xFields();
        }
    },
});

export default publicWidget.registry.L10nItWebsiteSaleCheckoutB2x;
