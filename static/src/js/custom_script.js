odoo.define('lims_inventory.custom_script', function (require) {
    "use strict";
    var domReady = require('web.dom_ready'); // Ensure the DOM is loaded before running

    if (!domReady) {
        return;
    }

    console.log('Custom script loaded.');

    // Function to update the total value
    function updateTotal() {
        let total = 0;
        document.querySelectorAll('.line_item').forEach(function (item) {
            const quantity = parseFloat(item.querySelector('.quantity').value) || 0;
            const price = parseFloat(item.querySelector('.price').textContent) || 0;
            total += quantity * price;
        });

        document.getElementById('total_value').textContent = total.toFixed(2); // Update total display
    }

    // Event listener for quantity changes
    document.addEventListener('input', function (event) {
        console.log('Custom loaded.');
        if (event.target.classList.contains('quantity')) {
            console.log('Custom.');
            updateTotal();
        }
    });
});
