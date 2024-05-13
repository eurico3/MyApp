from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
import sqlite3
import requests
"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins='*')

global binance_best_bid
"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

"""
Generate random sequence of dummy sensor values and send it to our clients
"""
def background_thread():
    global binance_best_bid
    print("Connecting to Projeto3/data.db")
    while True:
        conn = sqlite3.connect("MyApp_Upgrade1/data.db")
        cursor = conn.cursor()

        data = cursor.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 10").fetchall()

        binance_best_bid = data[0][1]
        binance_best_ask = data[0][2]

        conn2 = sqlite3.connect("MyApp_Upgrade1/coindata.db")
        cursor2 = conn2.cursor()

        data2 = cursor2.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 10").fetchall()

        coin_best_bid = data2[0][1]
        coin_best_ask = data2[0][2]
       
       
        socketio.emit('updateSensorData', {'value': binance_best_bid, 'value2': coin_best_ask, "date": get_current_datetime()})

        socketio.sleep(0.1)

"""
Serve root index file
"""
@app.route('/')
def index():
    teste = 128
    return render_template('index.html',teste=teste)

"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app)