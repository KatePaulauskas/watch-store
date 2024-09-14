// Automatically select the standard delivery method on page load
var standardDelivery = document.querySelector('input[name="delivery_method"][data-standard="true"]');
if (standardDelivery) {
    standardDelivery.checked = true;
}

// Function to calculate and update the grand total (delivery cost + add-ons)
function updateGrandTotal() {
    var selectedDeliveryMethod = document.querySelector('input[name="delivery_method"]:checked');

    if (selectedDeliveryMethod) {
        var deliveryRate = parseFloat(selectedDeliveryMethod.dataset.rate);
        var cartWeight = parseFloat(document.getElementById("cart-weight").value);
        var initialTotal = document.getElementById("initial-total");
        var deliveryCost = document.getElementById("delivery-cost");
        var grandTotalSummary = document.getElementById("grand-total-summary");
        var grandTotalPayment = document.getElementById("grand-total-payment");

        if (initialTotal && deliveryCost && grandTotalSummary && grandTotalPayment) {
            var finalInitialTotal = parseFloat(initialTotal.textContent.replace(/[^0-9.-]+/g, ""));
            var finalDeliveryCost = Math.round(deliveryRate * cartWeight);

            // Calculate the add-on total using the data-price attribute
            var addOnTotal = 0;
            var cartQuantity = parseInt(document.getElementById("product-count").value);
            var addOnCheckboxes = document.querySelectorAll('input[name="add_ons"]:checked');
            addOnCheckboxes.forEach(function (addOnCheckbox) {
                var addOnPrice = parseFloat(addOnCheckbox.getAttribute('data-price'));  // Use data-price attribute
                addOnTotal += addOnPrice * cartQuantity;
            });

            // Update the delivery cost and add-ons in the DOM
            deliveryCost.textContent = "€" + finalDeliveryCost.toFixed(2);
            document.getElementById("add-ons").textContent = "€" + addOnTotal.toFixed(2);

            // Calculate the grand total including both delivery cost and add-ons
            var finalGrandTotal = finalInitialTotal + finalDeliveryCost + addOnTotal;

            // Update the grand total in both 'grand-total-summary' and 'grand-total-payment'
            grandTotalSummary.textContent = "€" + finalGrandTotal.toFixed(2);
            grandTotalPayment.textContent = "€" + finalGrandTotal.toFixed(2);
        } else {
            console.error("One or more elements with IDs 'initial-total', 'delivery-cost', or 'grand-total-summary' are missing in the DOM.");
        }
    } else {
        console.error("No delivery method selected.");
    }
}

// Add event listeners to the delivery method radio buttons
var deliveryMethodRadios = document.querySelectorAll('input[name="delivery_method"]');
deliveryMethodRadios.forEach(function (radio) {
    radio.addEventListener('change', updateGrandTotal);
});

// Add event listeners to the add-ons checkboxes
var addOnCheckboxes = document.querySelectorAll('input[name="add_ons"]');
addOnCheckboxes.forEach(function (checkbox) {
    checkbox.addEventListener('change', updateGrandTotal);
});

// Initial calculation on page load
updateGrandTotal();
