// Set up the ajax loading behaviour
$.ajaxSetup({
    beforeSend: function() {
        $('.loading').removeClass('hidden');
    },
    complete: function() {
        $('.loading').addClass('hidden');
    },
    success: function() {
        $('.loading').addClass('hidden');
    }
});

PREVIEW_IMAGE_HEIGHT = 400
    // Show the selected image to the UI before uploading
function readURL(input) {

    var reader = new FileReader();

    if (imageCropper.data('cropper')) {
        imageCropper.cropper('destroy');
    }

    reader.addEventListener("load", function(e) {
        $('.box-img-cropper').removeClass('hidden');
        $('#preview-image').attr('src', e.target.result).css({ height: PREVIEW_IMAGE_HEIGHT });
        initImageCropper();
    }, false);

    reader.readAsDataURL(input.files[0]);
}

// Setup Image Cropper
var imageCropper = $('#preview-image');

function initImageCropper() {

    var cropperOptions = {
        // preview: '.img-preview',
        initialAspectRatio: 3 / 2,
        viewMode: 2,
        minContainerWidth: 300,
        crop: function(e) {}
    };

    imageCropper.on({
        'ready': function(e) {
            // console.log(e.type);
            $('#btn-select-image').addClass('hidden');
            $('.section-main-buttons').removeClass('hidden');
            $('.container-main-wrapper').removeClass('fixed-height');
            mainNavHeight = $('.main-nav').height();
            $(window).scrollTo('.box-img-cropper', 400, { interrupt: true, offset: { top: -(mainNavHeight + 50) } });
        }
    }).cropper(cropperOptions);
}

$(function() {
    'use strict';
    let uploadedImageType = '';
    let modelHowToUse = $('#modal-how-to-use');
    let modelHowItWorks = $('#modal-how-it-works');

    // Handle behaviour of input file
    $("#file").on('change', function() {
        if (this.files && this.files[0]) {
            uploadedImageType = this.files[0].type;
            readURL(this);
        }
    });

    $('#btn-select-image, .btn-select-new-image').on('click', function(e) {
        e.preventDefault();

        $('#file').trigger('click')
    });

    $('.btn-how-to-use').on('click', function() {
        modelHowToUse.modal('show');
    });

    $('.btn-how-it-works').on('click', function() {
        modelHowItWorks.modal('show');
    });

    // Handle upload file for recommendation task
    $('#btn-upload-image').on('click', function(e) {
        e.preventDefault();

        // Crop the input image
        let cropper = imageCropper.data('cropper');

        if (uploadedImageType === 'image/jpeg') {
            // imageCropperData.option.fillColor = '#fff';
        }

        let result = imageCropper.cropper('getCroppedCanvas', {
            // maxWidth: 1024,
            // maxHeight: 1024,
            minWidth: 224,
            minHeight: 224,
            imageSmoothingEnabled: false,
            fillColor: '#fff'
        });

        let croppedImage = result.toDataURL(uploadedImageType)

        let fileSelected = document.getElementById('file').files;

        if (fileSelected.length > 0) {

            let jsonData = { 'data-uri': croppedImage }

            $.ajax({
                type: 'POST',
                url: '/recommend',
                processData: false,
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                data: JSON.stringify(jsonData),
                success: function(data) {
                    $('.box-img-cropper').addClass('hidden');
                    $('#products_html').html(data['products_html']);
                    $('#recommendation-results').removeClass('hidden');
                    $('.section-main-buttons').addClass('hidden');
                    $('.section-recommendation-results-buttons').removeClass('hidden');
                    $('.section-recommendation-results-buttons .your-photo img').attr('src', croppedImage);

                    // Setting Stars Ratings
                    $('.rating').raty({
                        readOnly: true,
                        score: function() {
                            return $(this).attr('data-score');
                        },
                        path: 'static/js/vendor/raty/images'
                    });
                }
            });
        }
    });
});