from flask import Flask, render_template, request, jsonify,  redirect, url_for, session
from flask_pymongo import PyMongo
import math
from flask_mail import Mail, Message
import random
import os
import bson
from PIL import Image
from encode import encrypt, convertToRGB, getPixelCount, calculate_pattern_size, encodeImage
from decode import decrypt, decodeImage

app = Flask(__name__)
app.secret_key = "abcd"

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://inviso76:inviso1234@inviso.3yy4alc.mongodb.net/?retryWrites=true&w=majority&appName=Inviso"
connection_string = "mongodb+srv://inviso76:<password>@inviso.3yy4alc.mongodb.net/"
# Create a new client and connect to the server
mongo = MongoClient(uri, server_api=ServerApi('1'))

try:
    mongo.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    

# Configuring app to send otp through mail
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'e22cseu1486@bennett.edu.in'  # Your Outlook email username
app.config['MAIL_PASSWORD'] = 'Bennett@#947938032'  # Your Outlook email password
app.config['MAIL_DEFAULT_SENDER'] = 'e22cseu1486@bennett.edu.in'


mail = Mail(app)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/services')
def services_page():
    return render_template('services.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')


@app.route('/purchase')
def purchase():
    return render_template('purchase.html')


@app.route('/dashboard')
def dashboard():
    return render_template('main.html', user='Vandit')

# Functions on buttons
@app.route('/login', methods=['POST'])
def login():
    # Get form data from the request
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    aadhar = request.form.get('aadhar')

    # Check if email/mobile exists in the collection
    user_data = mongo.db.Accounts.find_one({'$or': [{'email': email}, {'mobile_no': mobile}]})

    if user_data:
        if user_data.get('password') == password and user_data.get('aadhar') == aadhar:
            # Set session data to store user details
            session['user'] = {
                'name': user_data['name'],
                'email': user_data['email'],
                'mobile_no': user_data['mobile_no']
            }
            
            from datetime import datetime
            current_time = datetime.now()

            login_history = {
                'email': user_data['email'],
                'name': user_data['name'],
                'aadhar': aadhar,
                'login_time': current_time,
                'activity':'login'
            }
            mongo.db.History.insert_one(login_history)
            
            return redirect(url_for('dashboard'))  # Redirect to dashboard or home page
        else:
            alert_message = "Incorrect password or Aadhar card number"
            return f"<script>alert('{alert_message}'); window.location.replace('/login');</script>"
    else:
        alert_message = "User does not exist"
        return f"<script>alert('{alert_message}'); window.location.replace('/login');</script>"
    
@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    dob = request.form.get('DOB')
    mobile_no = request.form.get('MobileNo')
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Get form data from second form
    aadhar = request.form.get('aadhar')
    pan = request.form.get('pan')
    gst = request.form.get('gst')
    reason = request.form.get('message')

    # Create a dictionary with the form data
    user_data = {
        'name': name,
        'dob': dob,
        'mobile_no': mobile_no,
        'email': email,
        'password': password,
        'aadhar': aadhar,
        'pan': pan,
        'gst': gst,
        'reason' : reason
    }
    
    if not all([name, dob, mobile_no, email, password, aadhar, pan, gst, reason]):
        alert_message = "Make sure all the fields are filled."
        return f"<script>alert('{alert_message}'); window.location.replace('/signup');</script>"
    
    if mongo.db.Pending_Requests.find_one({'email': email}):
        alert_message = "Email already exists. Please use a different email address."
        return f"<script>alert('{alert_message}'); window.location.replace('/signup');</script>"
    
    mongo.db.Pending_Requests.insert_one(user_data)
    
    return redirect(url_for("home_page"))

@app.route('/send-otp', methods=['POST'])
def send_otp():
    try:
        email = request.json.get('email')
        otp = ''.join(random.choices('0123456789', k=6))

        # Send OTP via email
        msg = Message(subject='Verification OTP', recipients=[email])
        msg.body = f'Your OTP for signup is: {otp}'
        mail.send(msg)
        
        return jsonify({'success': True, 'message': 'OTP sent successfully', 'otp': otp})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})



@app.route("/encode")
def encode():
  image_files = os.listdir('static/images/Encode_Images')  # Assuming your images are in static/images folder
  return render_template('encode.html', image_files=image_files)

@app.route("/encode", methods=['POST'])
def encode_message():
    try:
        recipient_email = request.form['recipient_email']
        selected_image = request.form['select-image']
        message = request.form['message']
        header_text = "M6nMjy5THr2J"
        message = header_text + message
        passkey = request.form['key']
        image_path = os.path.join('static', 'images', 'Encode_Images', selected_image)

        cipher = ""
        if passkey != "":
            cipher = encrypt(key=passkey.encode(), source=message.encode())
            cipher = header_text + cipher
        else:
            cipher = message

        image = Image.open(image_path)
        print("[yellow]Image Mode: [/yellow]%s" % image.mode)
        if image.mode != 'RGB':
            image = convertToRGB(image)
        newimg = image.copy()

        encoded_filename = encodeImage(image=newimg, message=cipher, filename=image_path)

        msg = Message(subject="Encoded Image", recipients=[recipient_email])
        msg.body = "Here is your encoded image."
        with app.open_resource(encoded_filename) as fp:
            msg.attach(encoded_filename, "image/png", fp.read())

        mail.send(msg)
        
        user_data = session['user']
        
        from datetime import datetime
        current_time = datetime.now()

        encode_history = {
            'email': user_data['email'],
            'name': user_data['name'],
            'image': selected_image,
            'login_time': current_time,
            'activity':'encode'
        }
        mongo.db.History.insert_one(encode_history)

        return render_template('success.html')
    except Exception as e:
        print("[red]An error occurred - [/red]%s" % e)
        return render_template(
            'error.html',
            message="An error occurred during encoding. Please try again.")
        
        
@app.route("/decode")
def decode_page():
  return render_template('decode.html')


@app.route('/decode', methods=['POST'])
def decode():
    header_text = "M6nMjy5THr2J"

    # Check if the image file is present in the request

    # Get the image file from the request
    image_file = request.files['select-image']
    password = request.form['key']
    # Check if the image file is provided
    if image_file.filename == '':
        return jsonify(message='No image selected')


    UPLOAD_FOLDER = 'uploads'  # Define the uploads folder

# Check if the uploads folder exists, if not, create it
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Modify the app configuration to set the uploads folder
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Use the configured uploads folder in the file save path
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(image_path)

    # Open the image file using PIL
    image = Image.open(image_path)
    cipher = decodeImage(image)
    print(cipher)

    header = cipher[:len(header_text)]

    if header.strip() != header_text:
        return jsonify(message_text ='Invalid data')
        

    decrypted = ""

    if password != "":
        cipher = cipher[len(header_text):]
        try:
            decrypted = decrypt(key=password.encode(), source=cipher)
        except Exception as e:
            return jsonify(message_text='Wrong password')
            

    else:
        decrypted = cipher

    header = decrypted.decode()[:len(header_text)]

    if header != header_text:
        return jsonify(message_text ='Wrong password')
        

    decrypted = decrypted[len(header_text):]
# Decode the message from the image
    
    
    # Delete the uploaded image file
    os.remove(image_path)
    serialized_data = decrypted.decode('utf-8')  # Convert bytes to string
    
    # Return the serialized data in a JSON response
   

# Check if the decoding was successful
    if decrypted:
        user_data = session['user']
        
        from datetime import datetime
        current_time = datetime.now()

        decode_history = {
            'email': user_data['email'],
            'name': user_data['name'],
            'login_time': current_time,
            'activity':'decode'
        }
        mongo.db.History.insert_one(decode_history)
        return render_template('decode.html', decoded_message=serialized_data)
    else:
        return render_template('decode.html', decoded_message='Error decoding message')

if __name__ == "__main__":
      app.run(host='0.0.0.0', debug=True)
