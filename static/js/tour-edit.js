document.addEventListener("DOMContentLoaded", function () {
    var editTourModal = document.getElementById('editTourModal');

    editTourModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;
        var tourId = button.getAttribute('data-id');
        var tourCountry = button.getAttribute('data-country');
        var tourContent = button.getAttribute('data-content');
        var tourGroupSize = button.getAttribute('data-group_size');
        var tourPrice = button.getAttribute('data-price');
        var tourImage = button.getAttribute('data-image');

        document.getElementById('country').value = tourCountry;
        document.getElementById('content').value = tourContent;
        document.getElementById('group_size').value = tourGroupSize;
        document.getElementById('price').value = tourPrice;
        document.getElementById('tourImage').src = tourImage;

        document.getElementById('editTourForm').action = '/edit-tour/' + tourId;
    });
});
