import telebot
from flask import Flask, render_template, request, redirect, session, url_for
import RPi.GPIO as GPIO
import time
import io
from picamera import PiCamera

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "fcuc"

# Set up GPIO pins for ultrasonic sensor
GPIO.setmode(GPIO.BOARD)
TRIG = 7
ECHO = 11
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


reference_distance = 0


TOKEN = '6254032034:AAEc9zXMd_f3FOuWFSn1PGyGz9hOv6tdEMw'
CHAT_ID = '-1001848432375'
bot = telebot.TeleBot(TOKEN)


@app.route("/distance")
def distance():
    global reference_distance
    
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    pulse_end = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    if distance <= reference_distance:
        with PiCamera() as camera:
            bot.send_message(chat_id=CHAT_ID, text="Water level at {}cm.". format(distance))
            time.sleep(1)
            with io.BytesIO() as stream:
                camera.capture(stream, format='jpeg')
                stream.seek(0)
                bot.send_photo(chat_id=CHAT_ID, photo=stream)
    time.sleep(3)
    return str(distance)

@app.route("/set_distance", methods=["GET", "POST"])
def set_distance():
    global reference_distance
    
    if request.method == "POST":
        # Get the distance value from the form data
        reference_distance = int(request.form["distance"])

        # Store the distance value in a session variable
        session["distance"] = reference_distance

        # Redirect back to the home page
        return redirect(url_for("index"))
    else:
        return render_template("set_distance.html")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
   
    # Start the Flask app
    app.run(debug=True, host="0.0.0.0")

    

