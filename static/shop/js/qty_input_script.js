/**
*Source: code adapted from Code Institute Boutique Ado walk-through
*/

    // Disable +/- buttons outside 1-10 range
    function handleEnableDisable(itemId) {
        var currentValue = parseInt($(`#id_qty_${itemId}`).val());
        var minusDisabled = currentValue < 2;
        var plusDisabled = currentValue >= 10;
        $(`#decrement-qty_${itemId}`).prop('disabled', minusDisabled);
        $(`#increment-qty_${itemId}`).prop('disabled', plusDisabled);
    }
    
    // Ensure proper enabling/disabling of all inputs on page load
    var allQtyInputs = $('.qty_input');
    allQtyInputs.each(function() {
        var itemId = $(this).data('item_id');
        handleEnableDisable(itemId);
    });
    
    // Check enable/disable every time the input is changed
    $('.qty_input').change(function() {
        var itemId = $(this).data('item_id');
        handleEnableDisable(itemId);
    });
    
    // Increment quantity
    $('.increment-qty').click(function(e) {
       e.preventDefault();
       var closestInput = $(this).closest('.d-flex').find('.qty_input')[0];
       var currentValue = parseInt($(closestInput).val());
       $(closestInput).val(currentValue + 1);
       var itemId = $(this).data('item_id');
       handleEnableDisable(itemId);
    });
    
    // Decrement quantity
    $('.decrement-qty').click(function(e) {
       e.preventDefault();
       var closestInput = $(this).closest('.d-flex').find('.qty_input')[0];
       var currentValue = parseInt($(closestInput).val());
       $(closestInput).val(currentValue - 1);
       var itemId = $(this).data('item_id');
       handleEnableDisable(itemId);
    });
