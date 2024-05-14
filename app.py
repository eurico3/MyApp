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
#app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')
coinbase_url = 'https://api.coinbase.com/v2/prices/btc-usd/spot'
binance_url = "wss://stream.binance.com:9443/ws/btcusdt@aggTrade"
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
    print("Connecting to Projeto3/data.db")
    while True:
        conn = sqlite3.connect("MyApp/data.db")
        cursor = conn.cursor()

        data = cursor.execute("SELECT * FROM trades ORDER BY time DESC LIMIT 10").fetchall()

        valor = data[0][3]
        coinbase_price = ((requests.get(coinbase_url)).json())['data']['amount']
       
        #coinbase_price2 = float(coinbase_price)+10
       
        socketio.emit('updateSensorData', {'value': coinbase_price, 'value2': valor, "date": get_current_datetime()})
        #socketio.emit('updateSensorData2', {'value': coinbase_price2, "date": get_current_datetime()})

        socketio.sleep(0.1)

"""
Serve root index file
"""
@app.route('/')
def index():
    return render_template('index.html')

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