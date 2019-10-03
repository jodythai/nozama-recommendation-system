$.ajaxSetup({
    beforeSend: function() {
       $('.loading').removeClass('hidden');
    },
    complete: function(){
       $('.loading').addClass('hidden');
    },
    success: function() {
      $('.loading').addClass('hidden');
    }
});

function submitUploadForm() {
    let image = document.getElementById('image').value;
    if (!name || !description || !price || !parseFloat(price) || !image) {
      return alert(`Some fields might be empty or incorrect. Please make ` + 
                   `sure that all the required fields have been completed ` + 
                   `correctly, and an image has been uploaded.`);
    }

    document.getElementById('upload-form').submit();
};

PREVIEW_IMAGE_HEIGHT = 400
// Show the selected image to the UI before uploading
function readURL(input) {

    var reader = new FileReader();

    if ( imageCropper.data('cropper') ) {
        imageCropper.cropper('destroy');
    }

    reader.addEventListener("load", function (e) {
        $('#img-preview-container').removeClass('hidden');
        $('#preview-image').attr('src', e.target.result).css('height', PREVIEW_IMAGE_HEIGHT);
        initImageCropper();
    }, false);
    
    reader.readAsDataURL(input.files[0]);
}

var imageCropper = $('#preview-image');
function initImageCropper() {
    
    var cropperOptions = {
        crop: function (e) {
        }
    };

    imageCropper.on({
        'ready': function(e) {
            // console.log(e.type);
            $('#btn-select-image').addClass('hidden');
            $('.section-main-buttons').removeClass('hidden');
            $('.container-main-wrapper').removeClass('fixed-height');
            $(window).scrollTo('#img-preview-container', 600);
        }
    }).cropper(cropperOptions);
}

$(function () {
    'use strict';
    let uploadedImageType = ''

    $("#file").on('change', function() {
        if (this.files && this.files[0]) {
            uploadedImageType = this.files[0].type; 
            readURL(this);
        }
    });

    $('#btn-select-image, .btn-select-new-image').on('click', function (e) {
        e.preventDefault();
        
        $('#file').trigger('click')
    });

    $('#btn-upload-image').on('click', function (e) {
        e.preventDefault();

        // Crop the input image
        let cropper = imageCropper.data('cropper');

        if (uploadedImageType === 'image/jpeg') {
            // imageCropperData.option.fillColor = '#fff';
        }

        let result = imageCropper.cropper('getCroppedCanvas', {
            maxWidth: 500,
            maxHeight: 500,
            fillColor: '#fff'
        });

        let croppedImage = result.toDataURL(uploadedImageType)

        let fileSelected = document.getElementById('file').files;

        if (fileSelected.length > 0) {

            let jsonData = {'data-uri': croppedImage }
            
            $.ajax({
                type: 'POST',
                url: '/recommend',
                processData: false,
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                data: JSON.stringify(jsonData),
                success: function(data) {
                    $('#img-preview-container').addClass('hidden');
                    $('#products_html').html(data['products_html']);
                    $('#recommendation-results').removeClass('hidden');
                    $('.section-main-buttons').addClass('hidden');
                    $('.section-recommendation-results-buttons').removeClass('hidden');
                    $('.section-recommendation-results-buttons .your-photo img').attr('src', croppedImage);
                }
            });
        }
    });
});