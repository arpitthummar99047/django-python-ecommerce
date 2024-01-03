function displayImage(){
    const input = document.getElementById("uplode-input");
    const file = input.files[0];
    if(file){
        const render = new FileReander();
        ReadableStream.onload = function(event){
            const ImageDataUrl = event.target.result;
            updateImageSrc(ImageDataUrl);
        };
        render.onerror = function (error){
            console.error("Error reading the file:",error);
        };
        render.readAsDataURL(file);
    }
}

