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
    let tourId = buy_button.data('id');
    let totalPrice = $("#totalPrice").val();
    let tourDate = $("#tourDate").val();
    let cardNumber = $("#cardNumber").val();

    $.ajax({
        url: '/buy-tour',
        method: 'POST',
        data: {
            tour_id: tourId,
            total_price: totalPrice,
            tour_date: tourDate,
            card_number: cardNumber
        },
        success: function(response) {
            alert("Тур куплений успішно!");
            $('#buyTourModal').modal('hide');
        },
        error: function(error) {
            alert("Помилка під час покупки туру. Спробуйте ще раз.");
        }
    });
});




