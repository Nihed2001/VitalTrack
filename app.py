from flask import Flask, render_template
import serial
import threading

app = Flask(__name__)
pulse_data = []

def read_serial():
    global pulse_data
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust to your serial port
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(f"Read line: {line}")  # Debug: Print the read line
            pulse_data.append(line)
            if len(pulse_data) > 10:  # Keep only the last 10 readings
                pulse_data.pop(0)

@app.route('/')
def index():
    print(f"Pulse Data: {pulse_data}")  # Debug: Print the pulse data
    return render_template('index.html', data=pulse_data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/view_data')
def view_data():
    return render_template('view_data.html', data=pulse_data)

@app.route('/other')
def other():
    return render_template('other.html')

if __name__ == '__main__':
    threading.Thread(target=read_serial).start()
    app.run(debug=True)
