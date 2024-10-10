// Helper function to add comma formatting to numbers. Source: Stack Overflow
function formatWithCommas(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Automatically select the standard delivery method on page load
const standardDelivery = document.querySelector('input[name="delivery_method"][data-standard="true"]');
if (standardDelivery) {
    // If a standard delivery option is available, set it as the default checked option
    standardDelivery.checked = true;
}

// Function to calculate and update the grand total (delivery cost + add-ons)
function updateGrandTotal() {
    // Get the currently selected delivery method (radio button)
    const selectedDeliveryMethod = document.querySelector('input[name="delivery_method"]:checked');

    // Proceed if a delivery method is selected
    if (selectedDeliveryMethod) {
        // Extract the delivery rate from the data attribute of the selected delivery method
        const deliveryRate = parseFloat(selectedDeliveryMethod.dataset.rate);
        
        // Get the total weight of items in the cart from the hidden input field
        const cartWeight = parseFloat(document.getElementById("cart-weight").value);
        
        // Get references to various DOM elements that will display the calculated totals
        const initialTotal = document.getElementById("initial-total");
        const deliveryCost = document.getElementById("delivery-cost");
        const grandTotalSummary = document.getElementById("grand-total-summary");
        const grandTotalPayment = document.getElementById("grand-total-payment");

        // Ensure all necessary DOM elements exist before proceeding
        if (initialTotal && deliveryCost && grandTotalSummary && grandTotalPayment) {
            // Parse the initial total amount from the text content (removing currency symbols or non-numeric characters)
            const finalInitialTotal = parseFloat(initialTotal.textContent.replace(/[^0-9.-]+/g, ""));
            
            // Calculate the delivery cost based on the delivery rate and cart weight
            const finalDeliveryCost = Math.round(deliveryRate * cartWeight);

            // Initialize add-ons total
            let addOnTotal = 0;
            
            // Get the number of products in the cart from the hidden input field
            const cartQuantity = parseInt(document.getElementById("product-count").value);
            
            // Find all checked add-ons and calculate their total price
            const addOnCheckboxes = document.querySelectorAll('input[name="add_ons"]:checked');
            addOnCheckboxes.forEach(function (addOnCheckbox) {
                // Get the price of each checked add-on from its data attribute
                const addOnPrice = parseFloat(addOnCheckbox.getAttribute('data-price'));
                
                // Multiply the add-on price by the quantity of products in the cart
                addOnTotal += addOnPrice * cartQuantity;
            });

            // Update the delivery cost and add-ons total in the DOM
            deliveryCost.textContent = "€" + formatWithCommas(finalDeliveryCost.toFixed(2));
            document.getElementById("add-ons").textContent = "€" + formatWithCommas(addOnTotal.toFixed(2));

            // Calculate the grand total by summing the initial total, delivery cost, and add-ons total
            const finalGrandTotal = finalInitialTotal + finalDeliveryCost + addOnTotal;

            // Update the grand total in both the summary and payment sections of the DOM
            grandTotalSummary.textContent = "€" + formatWithCommas(finalGrandTotal.toFixed(2));
            grandTotalPayment.textContent = "€" + formatWithCommas(finalGrandTotal.toFixed(2));
        } else {
            // Log an error if any of the required DOM elements are missing
            console.error("One or more elements with IDs 'initial-total', 'delivery-cost', or 'grand-total-summary' are missing in the DOM.");
        }
    } else {
        // Log an error if no delivery method is selected
        console.error("No delivery method selected.");
    }
}

// Add event listeners to the delivery method radio buttons
const deliveryMethodRadios = document.querySelectorAll('input[name="delivery_method"]');
deliveryMethodRadios.forEach(function (radio) {
    // Update the grand total whenever the user selects a different delivery method
    radio.addEventListener('change', updateGrandTotal);
});

// Add event listeners to the add-ons checkboxes
const addOnCheckboxes = document.querySelectorAll('input[name="add_ons"]');
addOnCheckboxes.forEach(function (checkbox) {
    // Update the grand total whenever the user selects or deselects an add-on
    checkbox.addEventListener('change', updateGrandTotal);
});

// Perform an initial grand total calculation when the page first loads
updateGrandTotal();
