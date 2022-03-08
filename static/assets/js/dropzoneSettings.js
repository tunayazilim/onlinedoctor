Dropzone.autoDiscover = false;



const myDropzone = new Dropzone("#my-dropzone",{
    url: "save_clinic_images",
    maxFiles: 5,
    maxFilesize: 2,
    acceptedFiles:'.jpg, .png, .jfif',
  

})

