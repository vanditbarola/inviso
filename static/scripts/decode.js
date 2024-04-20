document.getElementById("decode-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    fetch('/decode', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'decoded_message.txt';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        alert('Your message has been decoded and downloaded!');
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById("select-image-decode").addEventListener("change", function() {
    const fileReader = new FileReader();
    fileReader.onload = function(event) {
        document.getElementById("image-preview-decode").src = event.target.result;
    };
    fileReader.readAsDataURL(this.files[0]);
});
