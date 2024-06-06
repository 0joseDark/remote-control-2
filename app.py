#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pip install flask

from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Configuração dos pinos GPIO
GPIO.setmode(GPIO.BCM)
pins = {
    'up': 17,
    'down': 18,
    'left': 27,
    'right': 22,
    'saltar': 23,
    'baixar': 24,
    'extra1': 5,
    'extra2': 6,
    'extra3': 13,
    'extra4': 19,
    'extra5': 26,
    'extra6': 12,
    'extra7': 16,
    'extra8': 20
}

for pin in pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    data = request.json
    command = data.get('command')
    
    if command in pins:
        pin = pins[command]
        GPIO.output(pin, not GPIO.input(pin))  # Toggle the pin state
        state = GPIO.input(pin)
        return jsonify({'status': 'success', 'command': command, 'state': state})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid command'}), 400

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        GPIO.cleanup()
