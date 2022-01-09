Introduction
=========================
It's an IoT car. You can use your cellphone to control it to pick up a ball.

PREPARE
=======
* Car kit
* DC motor*4
* Camera
* Battery box
* Battery*4
* L298N motor driver
* Dupont Line
* Breadboard
* servo motor*4

BEFORE GETTING START
====================
You needto  install Flask on your Raspberry Pi first. Go to Terminal and enter:
```
sudo apt-get install python3-flask
```
Build up your Car
================
*Click [here](https://www.youtube.com/watch?v=uW8YVcBjPGU) to learn how to build the car kit*

L298N MOTOR DRIVER
============
One L298N motor driver can help us to control our motor in two parts, depending on the way you connect Dupont Lines. In my project, I use one driver, for my car only has two wheels.
*You can click [here]( https://sites.google.com/site/zsgititit/home/arduino/arduino-shi-yongl298n-qu-dong-liang-ge-ma-da) to get more detail*

It's my code for app.py.

 ```
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(23, gpio.OUT)

def setio(p7, p11, p13, p15):
    gpio.output(17, p7)
    gpio.output(18, p11)
    gpio.output(22, p13)
    gpio.output(23, p15)
    
app = Flask(__name__)  
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')
    
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
    setio(True, False, False, True)
    return render_template('index.html')


@app.route('/left')
def left():    
    setio(False, True, True, False)
    return render_template('index.html')
 ```
 
Here is the code for index.html.
```
    <tr>
         <td></td>
         <td>
             <input type="button" value="go" onclick="location.href='/go'"> 
         </td>
         <td></td>
    </tr>
          
    <tr>
         <td>
            <input type="button" value="left" onclick="location.href='/left'"> 
         </td>

         <td>
            <input type="button" value=" stop " onclick="location.href='/stop'"> 
         </td>
         <td>
            <input type="button" value="right" onclick="location.href='/right'"> 
         </td>
     </tr>
		  
		  <tr>
          <td></td>
          <td>
             <input type="button" value="back" onclick="location.href='/back'"> 
          </td>
          <td></td>
      </tr>
 ```
 
 
Servo motor
===========
Servo motor can reach a specific angle. I use it to pick up a ball.

Here is my code.(app.py)
```
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
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

def setud(p11, p8):
    pwm_motorr.ChangeDutyCycle(p11)
    pwm_motorl.ChangeDutyCycle(p8)


def setct(p26, p21):
    pwm_motorfr.ChangeDutyCycle(p26)
    pwm_motorfl.ChangeDutyCycle(p21)
    
app = Flask(__name__)

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
    setct(8.2, 11.1)  
    return render_template('index.html')
    
@app.route('/throw')      
def throw():
    setct(10.5, 7.5)      
    return render_template('index.html')
```
And for index.html
```
<tr>
   <td></td>
   <td>
        <input type="button" value=" up " onclick="location.href='/up'"> 
   </td>
   <td></td>
   <td></td>
   <td>
       <input type="button" value="down" onclick="location.href='/down'"> 
   </td> 
</tr>
         
<tr>
    <td></td>
    <td>
         <input type="button" value="catch" onclick="location.href='/catch'"> 
    </td>
    <td></td>
    <td></td>
    <td>
         <input type="button" value="throw" onclick="location.href='/throw'"> 
    </td>
 </tr>

```


VIDEO STREAMING
===============
*You can click [here]( http://hophd.com/raspberry-pi-python-flask-video-streaming/) to get more detail*

Basically you need to install Flask and picamera by using pip on your RPI  
  ```
  sudo apt-get udpate 
  sudo pip install picamera  
  sudo pip install Flask
  ```
Then copy an open source project
```
git clone https://github.com/miguelgrinberg/flask-video-streaming
```
You need to put a programming attontation on line NO.5, and cancel the attonation on line NO.8.

Here is my code.(app.py)
```
from importlib import import_module
import os
from flask import Flask, render_template, Response
import RPi.GPIO as gpio

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
 ```
 
 It's my code for index.html.
 ``` 
 <div align="center">
    <img src="{{ url_for('video_feed') }}" width="50%" />
 </div>
```

Do streaming & controlling on an html website (by flask webserver)
==================================================================
Write the codes above about app.py into your app.py, and the all codes above about index.html into index.html.
Then you can run the car by enter this into your terminal.
```
sudo python3 app.py
```
Then you may see this.
![image](https://user-images.githubusercontent.com/86145342/148650177-eee5e85b-7dd8-4300-9905-a96caee1f42a.png)

Open a webrower, and enter the url showing on your VNC screen. 

DEMO CLIP
=========
*[https://youtu.be/1jeaqI7l7Lk](https://youtu.be/1jeaqI7l7Lk)*
