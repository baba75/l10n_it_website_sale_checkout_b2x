odoo.define("l10n_it_website_sale_checkout_b2x", function(require) {
    "use strict";
    require("web.core");

    $(document).ready(function() {
        var $container_div = $(".oe_website_sale");
        var $b2x_input = $container_div.find(
            "input[name='company_type'][type='checkbox']"
        );
        var $div_fiscalcode = $container_div.find("#div_fiscalcode");
        var $div_company_name = $container_div.find("input[name='company_name']").parent();
        var $div_vat = $container_div.find(".div_vat");
        var $field_required = $container_div.find("input[name='field_required']");

        var compute_b2x_fields_visibility = function() {
            if (
                $b2x_input[0] !== null &&
                $b2x_input[0] !== undefined
            ) {
                if ($b2x_input[0].checked) {
                    /* set the fiscal code as optional */
                    if($field_required[0].value.includes("fiscalcode")){
                        $field_required[0].value = $field_required[0].value.replace(",fiscalcode","")
                    }
                    /* set vat id as mandatory */
                    $field_required[0].value = $field_required[0].value.concat(",vat");

                    $div_fiscalcode.hide();
                    $div_company_name.show();
                    $div_vat.show();
                } else {
                    $div_fiscalcode.show();
                    /* Set the fiscal code as mandatory */
                    $field_required[0].value = $field_required[0].value.concat(",fiscalcode");
                    /* set vat id as optional */
                    if($field_required[0].value.includes("vat")){
                        $field_required[0].value = $field_required[0].value.replace(",vat","")
                    }
                    $div_company_name.hide();
                    $div_vat.hide();
                }
            }
        };
        compute_b2x_fields_visibility();
        $b2x_input.change(compute_b2x_fields_visibility);
    });
});