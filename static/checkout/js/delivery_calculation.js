// Automatically select the standard delivery method on page load
var standardDelivery = document.querySelector('input[name="delivery_method"][data-standard="true"]');
if (standardDelivery) {
    standardDelivery.checked = true;
}

// Function to calculate the delivery cost
function calculateDeliveryCost() {
    var selectedDeliveryMethod = document.querySelector('input[name="delivery_method"]:checked');

    if (selectedDeliveryMethod) {
        var deliveryRate = parseFloat(selectedDeliveryMethod.dataset.rate);
        var cartWeight = parseFloat(document.getElementById("cart-weight").value);
        var initialTotal = document.getElementById("initial-total");
        var deliveryCost = document.getElementById("delivery-cost");
        var grandTotal = document.getElementById("grand-total");

        if (initialTotal && deliveryCost && grandTotal) {
            var finalInitialTotal = parseFloat(initialTotal.textContent.replace(/[^0-9.-]+/g, ""));
            var finalDeliveryCost = Math.round(deliveryRate * cartWeight);
            var finalGrandTotal = finalInitialTotal + finalDeliveryCost;

            deliveryCost.textContent = "€" + finalDeliveryCost.toFixed(2);
            grandTotal.textContent = "€" + finalGrandTotal.toFixed(2);
        } else {
            console.error("One or more elements with IDs 'initial-total', 'delivery-cost', or 'grand-total' are missing in the DOM.");
        }
    } else {
        console.error("No delivery method selected.");
    }
}

// Add event listeners to the delivery method radio buttons
var deliveryMethodRadios = document.querySelectorAll('input[name="delivery_method"]');
deliveryMethodRadios.forEach(function (radio) {
    radio.addEventListener('change', calculateDeliveryCost);
});

calculateDeliveryCost();