$(document).ready(function () {
    $('.buy-button').on('click', function () {
        const tourPrice = $(this).data('price');
        const tourId = $(this).data('id');
        const tourCountry = $(this).closest('.tour-details').find('.tour-title').text(); // Назва країни


        $('#tourPrice').text(tourPrice + ' грн');
        $('#totalPrice').val(tourPrice);
        $('#buyTourModal').data('tour-country', tourCountry);
    });


    $('#buyTourForm').on('submit', function (e) {
        e.preventDefault();


        const tourCountry = $('#buyTourModal').data('tour-country');
        const cardNumber = $('#cardNumber').val();
        const totalPrice = $('#totalPrice').val();

        if (!cardNumber) {
            alert('Будь ласка, введіть номер картки!');
            return;
        }
        alert(`Купівля успішна!\nКраїна: ${tourCountry}\nНомер картки: ${cardNumber}\nДо сплати: ${totalPrice} грн`);
        $('#buyTourModal').modal('hide');
        $('#buyTourForm')[0].reset();
    });
});
