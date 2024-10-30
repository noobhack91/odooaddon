odoo.define('lims_inventory.custom_script', function (require) {
    "use strict";

    var $ = require('jquery');

    $(document).ready(function () {
        // Your custom JavaScript code here
        console.log('Custom script loaded.');

        // Example: Updating a total value based on inputs
        function updateTotal() {
            let total = 0;
            $('.line_item').each(function () {
                const quantity = parseFloat($(this).find('.quantity').val()) || 0;
                const price = parseFloat($(this).find('.price').text()) || 0;
                total += quantity * price;
            });
            $('#total_value').text(total.toFixed(2)); // Update total value
        }

        // Event listener for quantity changes
        $(document).on('input', '.quantity', function () {
            updateTotal();
        });
    });
});