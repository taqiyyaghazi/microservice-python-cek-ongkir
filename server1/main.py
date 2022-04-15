from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from os import path
import datetime
import json

db = SQLAlchemy()
DB_NAME = 'database.db'

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_history = db.Column(db.Date, default=datetime.datetime.now)
    origin = db.Column(db.String(5))
    destination = db.Column(db.String(5))
    weight = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    courier = db.Column(db.String(10))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'qwertyuiop' #Inisiasi secret key -> Secret key bebas
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    create_database(app)

    return app

def create_database(app):
    if not path.exists('server1/' + DB_NAME):
        db.create_all(app=app)
        print('Database Created!')

app = create_app()

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/get-all-history', methods=['GET'])
def get_history():
    histories = History.query.all()
    all_history, data = [], {}
    for history in histories:
        all_history.append({
            'id': history.id,
            'date_history': str(history.date_history),
            'origin': history.origin,
            'destination': history.destination,
            'weight': history.weight,
            'cost': history.cost,
            'courier': history.courier
        })
    data["data"] = all_history
    data["message"] = "Got All History!"
    
    return json.dumps(data)

@app.route('/add-history', methods=['POST'])
def add_history():
        data = request.get_json()
        if 'origin' in data.keys() and 'destination' in data.keys() and 'cost' in data.keys() and 'courier' in data.keys() and 'weight' in data.keys():
            history = History(origin=data['origin'], destination=data['destination'], cost=data['cost'], courier=data['courier'], weight=data['weight'])
            db.session.add(history)
            db.session.commit()
            return 'History Added!'
        elif 'origin' not in data.keys():
            return 'Origin is required!'
        elif 'destination' not in data.keys():
            return 'Destination is required!'
        elif 'cost' not in data.keys():
            return 'Cost is required!'
        elif 'courier' not in data.keys():
            return 'Courier is required!'
        

if __name__ == '__main__':
    app.run(debug=True, port=1111)