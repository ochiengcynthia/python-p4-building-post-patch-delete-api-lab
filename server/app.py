#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(jsonify(bakeries_serialized), 200)
    return response

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)
    name = request.form.get('name')
    if name is not None:
        bakery.name = name
    db.session.commit()
    
    response = make_response(jsonify(bakery.to_dict()), 200)
    return response

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form['name']
    price = request.form['price']
    bakery_id = request.form['bakery_id']
    baked_good = BakedGood(name, price, bakery_id)
    db.session.add(baked_good)
    db.session.commit()

    response = make_response(jsonify(baked_good.to_dict()), 201)
    return response

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    db.session.delete(baked_good)
    db.session.commit()

    response = jsonify({'message': 'Baked good deleted successfully'})
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
