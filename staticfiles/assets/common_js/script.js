

function changeImage(imageId, colorSpan) {
    alert()
    const imgElement = document.getElementById(imageId);
    const newImageUrl = colorSpan.getAttribute('data-img');
    if (imgElement && newImageUrl) {
        imgElement.src = newImageUrl;
    }
}