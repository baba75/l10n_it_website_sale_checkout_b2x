/** @odoo-module **/
/* Copyright 2023 Alberto Carollo
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import tour from "web_tour.tour";
import tourUtils from "website_sale.tour_utils";

function requiredFields() {
    return $("input[name='field_required']").val().split(",").filter(Boolean);
}

function isShown(fieldName) {
    const $input = $(`.checkout_autoformat [name='${fieldName}']`);
    return !$input.parent().hasClass("d-none") && !$input.prop("disabled");
}

function isItalySelected() {
    const code = $("select[name='country_id'] option:selected").data("code") || "";
    return code.toUpperCase() === "IT";
}

function assertState(isCompany) {
    const required = requiredFields();
    const einvoice = isCompany && isItalySelected();
    // field name => [visible, required]
    const expected = {
        company_name: [isCompany, isCompany],
        vat: [isCompany, isCompany],
        fiscalcode: [!isCompany, !isCompany],
        codice_destinatario: [einvoice, einvoice],
        pec_destinatario: [einvoice, false],
    };
    for (const [fieldName, [visible, mandatory]] of Object.entries(expected)) {
        if (isShown(fieldName) !== visible) {
            throw new Error(`${fieldName} should be ${visible ? "visible" : "hidden"}`);
        }
        if (required.includes(fieldName) !== mandatory) {
            throw new Error(
                `${fieldName} should ${mandatory ? "" : "not "}be required: ${required}`
            );
        }
    }
    if (new Set(required).size !== required.length) {
        throw new Error(`Duplicated required fields: ${required}`);
    }
}

function goToAddressForm() {
    return [
        ...tourUtils.addToCart({productName: "B2X Test Box"}),
        tourUtils.goToCart(),
        {
            content: "Go to the address form",
            trigger: 'a[href="/shop/checkout?express=1"]',
        },
    ];
}

function selectCountry(code) {
    const $country = $("select[name='country_id']");
    $country.val($country.find(`option[data-code='${code}']`).val()).trigger("change");
}

function fillAddress(values) {
    return [
        {
            content: "Fill the address form",
            trigger: "form.checkout_autoformat select[name='country_id']",
            run() {
                for (const [fieldName, value] of Object.entries(values)) {
                    $(`.checkout_autoformat input[name='${fieldName}']`).val(value);
                }
                selectCountry("IT");
            },
        },
        {
            content: "Select a province",
            trigger: "select[name='state_id']:visible:has(option:contains('Roma'))",
            run() {
                const $state = $("select[name='state_id']");
                $state.val($state.find("option:contains('Roma')").first().val());
            },
        },
    ];
}

const ADDRESS = {
    phone: "0123456789",
    street: "Via Roma 1",
    city: "Roma",
    zip: "00100",
};

const clickNext = {
    content: "Submit the address",
    trigger: ".oe_cart .btn:contains('Next')",
};

const onPaymentStep = {
    content: "The address was accepted",
    trigger: "#wizard-step40.active",
    run() {},
};

tour.register(
    "l10n_it_website_sale_checkout_b2x_company",
    {test: true, url: "/shop"},
    [
        ...goToAddressForm(),
        {
            content: "Private customer by default",
            trigger: "input[name='company_type']:not(:checked)",
            run: () => assertState(false),
        },
        {
            content: "Switch to company",
            trigger: "input[name='company_type']",
            run: "click",
        },
        {
            content: "Company fields are shown and required",
            trigger: "input[name='company_type']:checked",
            run: () => assertState(true),
        },
        {
            content: "Switch back to private",
            trigger: "input[name='company_type']",
            run: "click",
        },
        {
            content: "Private fields are shown and required again",
            trigger: "input[name='company_type']:not(:checked)",
            run: () => assertState(false),
        },
        {
            content: "Switch to company again",
            trigger: "input[name='company_type']",
            run: "click",
        },
        {
            content: "Company fields are shown and required again",
            trigger: "input[name='company_type']:checked",
            run: () => assertState(true),
        },
        {
            content: "Select a foreign country",
            trigger: "select[name='country_id']",
            run: () => selectCountry("FR"),
        },
        {
            content: "No electronic invoice fields for a foreign company",
            trigger: "select[name='country_id']:has(option[data-code='FR']:selected)",
            run: () => assertState(true),
        },
        ...fillAddress({
            ...ADDRESS,
            name: "B2X Company Buyer",
            email: "company@example.com",
            company_name: "B2X Company Srl",
            vat: "IT12345670017",
            codice_destinatario: "ABC12",
        }),
        {
            content: "Electronic invoice fields for an Italian company",
            trigger: ".div_codice_destinatario:not(.d-none)",
            run: () => assertState(true),
        },
        clickNext,
        {
            content: "The Addressee Code must be 7 characters long",
            trigger: "input[name='codice_destinatario'].is-invalid",
            run: () => assertState(true),
        },
        {
            content: "Fix the Addressee Code",
            trigger: "input[name='codice_destinatario']",
            run: "text abc1234",
        },
        clickNext,
        onPaymentStep,
    ]
);

tour.register(
    "l10n_it_website_sale_checkout_b2x_person",
    {test: true, url: "/shop"},
    [
        ...goToAddressForm(),
        ...fillAddress({
            ...ADDRESS,
            name: "B2X Private Buyer",
            email: "private@example.com",
        }),
        clickNext,
        {
            content: "The fiscal code is mandatory for a private customer",
            trigger: "input[name='fiscalcode'].is-invalid",
            run: () => assertState(false),
        },
        {
            content: "Fill the fiscal code",
            trigger: "input[name='fiscalcode']",
            run: "text RSSMRA85T10A562S",
        },
        clickNext,
        onPaymentStep,
    ]
);
