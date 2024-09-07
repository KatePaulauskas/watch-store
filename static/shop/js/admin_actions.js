const deleteModal = new bootstrap.Modal(document.getElementByClassName("deleteModal"));
const deleteButtons = document.getElementsByClassName("product-delete");
const deleteConfirm = document.getElementByClassName("deleteConfirm");

for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
        e.preventDefault();
        let productId = e.target.getAttribute("product-id");
        if (productId) {
            deleteConfirm.href = `/shop/delete/${productId}/`;
            deleteModal.show();
        } else {
            console.error('Product ID not found');
        }
    });
}