document.addEventListener('DOMContentLoaded', () => {
    const buyButtons = document.querySelectorAll('.buy-button');
    const modal = new bootstrap.Modal(document.getElementById('buyTourModal'));
    const modalPrice = document.getElementById('tourPrice');
    const totalPrice = document.getElementById('totalPrice');
    const dateInput = document.getElementById('tourDate');
    const cardInput = document.getElementById('cardNumber');
    const buyForm = document.getElementById('buyTourForm');
    const buyButton = document.getElementById('buy-tour');

    buyButtons.forEach(button => {
        button.addEventListener('click', () => {
            const price = button.dataset.price;
            modalPrice.textContent = `${price} грн`;
            totalPrice.value = price;
            buyButton.dataset.id = button.dataset.id
            modal.show();
        });
    }
});

$("#buy-tour").click(function(){
    let buy_button = $(this);
    $.ajax
})




