
#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
import RPi.GPIO as gpio



gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(23, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(8,  gpio.OUT)
gpio.setup(26, gpio.OUT)
gpio.setup(21, gpio.OUT)

pwm_motorfr = gpio.PWM(26, 50)
pwm_motorfl = gpio.PWM(21, 50)
pwm_motorr = gpio.PWM(11, 50)
pwm_motorl = gpio.PWM(8, 50)
pwm_motorr.start(0)
pwm_motorl.start(0)
pwm_motorfr.start(0)
pwm_motorfl.start(0)

def setio(p7, p11, p13, p15):
    gpio.output(17, p7)
    gpio.output(18, p11)
    gpio.output(22, p13)
    gpio.output(23, p15)

def setud(p11, p8):
    pwm_motorr.ChangeDutyCycle(p11)
    pwm_motorl.ChangeDutyCycle(p8)


def setct(p26, p21):
    pwm_motorfr.ChangeDutyCycle(p26)
    pwm_motorfl.ChangeDutyCycle(p21)
# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    #from camera import Camera

# Raspberry Pi camera module (requires picamera package)
 from camera_pi import Camera
 
 


app = Flask(__name__)

   
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')



def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop')
def stop():    
    setio(False, False, False, False)
    return render_template('index.html' )


@app.route('/go')
def go():  
    setio(False, True, False, True)
    return render_template('index.html')   
        

@app.route('/back')
def back():   
    setio(True, False, True, False)
    return render_template('index.html')


@app.route('/right')
def right():   
    setio(False, True, True, False)
    return render_template('index.html')


@app.route('/left')
def left():        
    setio(True, False, False, True)
    return render_template('index.html')

@app.route('/up')
def up():
   
    setud(4, 11)  
   
    return render_template('index.html')
    
@app.route('/down')      
def down(): 
    setud(9, 5.5)   
    return render_template('index.html')

@app.route('/catch')
def catch():
    setct(8, 11.2)  
    return render_template('index.html')
    
@app.route('/throw')      
def throw():
    setct(10.2, 7.3)       
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
   
