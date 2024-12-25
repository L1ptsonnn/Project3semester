$('#postSave').click(function () {
    let formData = new FormData();
    formData.append('country', $('#country').val());
    formData.append('content', $('#content').val());
    formData.append('group_size', $('#group_size').val());
    formData.append('price', $('#price').val());

    $.ajax({
        url: '/tour-create',  // Заміна на правильний шлях
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            alert('Тур створено успішно!');
            window.location.href = '/';
        },
        error: function () {
            alert('Сталася помилка. Спробуйте ще раз.');
        }
    });
});
