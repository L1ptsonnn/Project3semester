document.addEventListener('DOMContentLoaded', () => {
    const buyButtons = document.querySelectorAll('.buy-button');
    const modal = new bootstrap.Modal(document.getElementById('buyTourModal'));
    const modalPrice = document.getElementById('tourPrice');
    const totalPrice = document.getElementById('totalPrice');
    const dateInput = document.getElementById('tourDate');
    const cardInput = document.getElementById('cardNumber');
    const buyForm = document.getElementById('buyTourForm');

    let selectedTourId = null;

    buyButtons.forEach(button => {
        button.addEventListener('click', () => {
            const price = button.dataset.price;
            selectedTourId = button.dataset.tourId;
            modalPrice.textContent = `${price} грн`;
            totalPrice.value = price;
            modal.show();
        });
    });

    buyForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const selectedDate = dateInput.value;
        const cardNumber = cardInput.value;

        if (!selectedDate || !cardNumber) {
            alert('Будь ласка, заповніть всі поля!');
            return;
        }

        try {
            const response = await fetch('/book-tour/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    tour_id: selectedTourId,
                    date: selectedDate,
                    card_number: cardNumber,
                }),
            });

            if (response.ok) {
                const result = await response.json();
                alert(`Покупка успішна!\nДата туру: ${selectedDate}\nНомер карти: ${cardNumber}\nСума: ${totalPrice.value} грн`);
                modal.hide();
                buyForm.reset();
            } else {
                alert('Сталася помилка при бронюванні туру.');
            }
        } catch (error) {
            console.error('Помилка:', error);
            alert('Сталася помилка при бронюванні туру.');
        }
    });
});
