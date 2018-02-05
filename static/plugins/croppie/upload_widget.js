// todo: add formdata is supported, see admin/static/js/web2py.js

function initCroppie(inp) {

    var uploadForm = inp.closest('form');
    var imageFile = inp.files[0];
    var uploadCrop = $('#croppie');
    var formData = new FormData();
    var croppedImage;
    var croppedImageName;

    $('#croppie-modal').on('shown.bs.modal', function (e) {

        readFile(imageFile);
        formSubmitListen(uploadForm);
    });

    $('#croppie-modal').on('hide.bs.modal', function (e) {

        uploadCrop.croppie('result', {
            size: 'viewport',
            type: 'blob',
            format: 'jpeg'
        }).then(function (resp) {
            // file extension must match croppie result file type
            croppedImageName = imageFile.name.substr(0, imageFile.name.lastIndexOf(".")) + "_cropped.jpg";
            croppedImage = resp;

            $('#upload-file-info').html(croppedImageName);  // set label html to new filename
            // $(inp).remove();
        });
    });

    function readFile(input) {

        if (input) {
            var reader = new FileReader();

            uploadCrop.html('');  // clear <div id='croppie'> if it stores image processed before

            uploadCrop.croppie({
                viewport: {width: 263, height: 263},
                boundary: {width: 350, height: 350},
                enableExif: true
            });


            reader.onload = function (e) {
                $('#croppie').addClass('ready');

                uploadCrop.croppie('bind', {
                    url: e.target.result,
                }).then(function () {
                    // console.log('jQuery bind complete');
                });
            };
            reader.readAsDataURL(input);
        }
        else {
            console.log("Sorry - your browser doesn't support the FileReader API");
        }
    }


    function formSubmitListen(f) {
        $(f).on('submit', function (e, done) {

            done = done || false;

            if (!done) {
                $(inp).remove();
                formData = new FormData(uploadForm);
                formData.append(inp.name, croppedImage, croppedImageName);
                $.ajax(inp.formAction, {
                    method: "POST",
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function (data, status, xhr) {
                        console.log('Upload success'); // todo
                    },
                    error: function (data, status, xhr) {
                        console.log('Upload error'); // todo
                    }
                }).then(function () {
                    $(e.currentTarget).trigger(e.type, true);
                });
            } else {
                // todo: check for possible error (missing <input> if the form is not reloaded (?)
            }
        });
    }


    // Show Croppie modal window
    $('#croppie-modal').modal('show');

}



