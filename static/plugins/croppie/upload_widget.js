// todo: add formdata is supported, see admin/static/js/web2py.js

function initCroppie(inp) {
    var imageFile;
    var uploadCrop;
    var uploadForm;
    var formData = new FormData();

    console.log('document ready!');

    $('#croppie-modal').on('shown.bs.modal', function (e) {

        uploadForm = inp.closest('form');
        console.log(uploadForm.name);
        imageFile = inp.files[0];
        console.log(imageFile);

        readFile(imageFile);
        formSubmitListen(uploadForm);
    });

    $('#croppie-result').on('click', function (e) {

        uploadCrop.croppie('result', {
            size: 'viewport',
            type: 'blob',
            format: 'jpeg'

        }).then(function (resp) {
            formData = new FormData(uploadForm);

            // file extension must match croppie result file type
            var fileName = imageFile.name.substr(0, imageFile.name.lastIndexOf(".")) + "_cropped.jpg";

            formData.delete(inp.name);
            formData.append(inp.name, resp, fileName);
            $('#upload-file-info').html(fileName);  // set label html to new filename

            console.log(inp.formAction);
        });
    });

    function readFile(input) {

        if (input) {
            var reader = new FileReader();

            uploadCrop = $('#croppie');
            uploadCrop.html('');  // clear <div id='croppie'> if it stores image processed before

            uploadCrop.croppie({
                viewport: {width: 250, height: 250},
                boundary: {width: 300, height: 300},
                enableExif: true
            });


            reader.onload = function (e) {
                $('#croppie').addClass('ready');

                uploadCrop.croppie('bind', {
                    url: e.target.result
                }).then(function () {
                    console.log('jQuery bind complete');
                });
            };

            reader.readAsDataURL(input);
        }
        else {
            console.log("Sorry - Your browser doesn't support the FileReader API");
        }
    }


    function formSubmitListen(f) {
        $(f).on('submit', function (e) {

            e.preventDefault();

            $.ajax('#', {//inp.formAction, {
                method: "POST",
                // contentType: "multipart/form-data",
                data: formData,
                processData: false,
                contentType: false,
                success: function (data, status, xhr) {
                    console.log(status);
                    console.log('Upload success');
                },
                error: function () {
                    console.log('Upload error');
                }
            });

            formData = new FormData();

        });
    }
}



