// static/scripts/encode.js
document.addEventListener('DOMContentLoaded', function() {
    const encodeForm = document.getElementById('encode-form');
    if (encodeForm) {
        encodeForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission
            
            const recipientEmail = document.getElementById('receiver-email').value;
            const message = document.getElementById('message').value;
            const password = document.getElementById('password').value;
            const key = document.getElementById('key').value;

            if (recipientEmail && message && password && key) {
                // Simulate sending data to a server
                console.log('Encoding message with:', { recipientEmail, message, password, key });
                // Ideally, here you would make an AJAX request to your server
                alert('Message encoded successfully!');
            } else {
                alert('Please fill all the fields.');
            }
        });
    }
});
