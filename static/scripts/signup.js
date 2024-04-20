const { errorMonitor } = require("nodemailer/lib/xoauth2");

var otpValue;

function showFrame(frameNumber) {
    if (frameNumber === 1) {
        document.getElementById('frame1').style.display = 'block';
        document.getElementById('frame2').style.display = 'none';
    } else if (frameNumber === 2) {
        document.getElementById('frame1').style.display = 'none';
        document.getElementById('frame2').style.display = 'block';
    }
}


function sendOTP() {
    var email = document.getElementById("email").value;
    var errorMessage = document.getElementById("error-message")
    if (email==""){
        errorMessage.textContent = "Please enter valid email."
        return
    }
     
    fetch('/send-otp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email })
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Parse JSON response
        } else {
            errorMessage.textContent = "Failed to send OTP. Please try again."
        }
    })
    .then(data => {
        otpValue = data.otp;
        errorMessage.textContent = 'OTP has been sent to your email. ' // Display the OTP to the user
    })
    .catch(error => {
        console.error('Error:', error);
        errorMessage.textContent = 'Error: ' + error.message;
    });
}


function verifyOTP() {
    var inputOtp = document.getElementById("otp").value;
    var errorMessage = document.getElementById("error-message");
    if (inputOtp === otpValue) {
        document.getElementById("continue-btn").disabled = false;
        errorMessage.textContent = "Email verified successfully.";
    } else {
        errorMessage.textContent = "Incorrect OTP. Please enter again.";
    }
    
}

function sendForm() {
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var otp = document.getElementById("otp").value;
    var aadhar = document.getElementById("aadhar").value;

    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password,
            otp: otp,
            aadhar: aadhar
        })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Display response message
        })
        .catch(error => console.error('Error:', error));
}
