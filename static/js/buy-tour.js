document.addEventListener('DOMContentLoaded', () => {
    const buyButtons = document.querySelectorAll('.buy-button');
    const modal = new bootstrap.Modal(document.getElementById('buyTourModal'));
    const modalPrice = document.getElementById('tourPrice');
    const totalPrice = document.getElementById('totalPrice');
    const dateInput = document.getElementById('tourDate');
    const cardInput = document.getElementById('cardNumber');
    const buyForm = document.getElementById('buyTourForm');

    buyButtons.forEach(button => {
        button.addEventListener('click', () => {
            const price = button.dataset.price;
            modalPrice.textContent = `${price} грн`;
            totalPrice.value = price;
            modal.show();
        });
    });

    buyForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const selectedDate = dateInput.value;
        const cardNumber = cardInput.value;

        if (!selectedDate || !cardNumber) {
            alert('Будь ласка, заповніть всі поля!');
            return;
        }

        alert(`Покупка успішна!\nДата туру: ${selectedDate}\nНомер карти: ${cardNumber}\nСума: ${totalPrice.value} грн`);
        modal.hide();
        buyForm.reset();
    });
});
