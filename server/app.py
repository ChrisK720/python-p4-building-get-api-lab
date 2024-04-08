#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

engine = create_engine('sqlite:///app.db')

# Create session
Session = sessionmaker(bind=engine)
session = Session()




migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

# GET /bakeries: returns a list of JSON objects for all bakeries in the database.
@app.route('/bakeries')

def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all() if isinstance(bakery,Bakery)]
    if not bakeries:
        return make_response({'message': 'No backeries'}, 404)
    return make_response(bakeries,200)
    
    

# GET /bakeries/<int:id>: returns a single bakery as JSON with its baked goods nested in a list. Use the
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id ==id).first()
    if not bakery:
        return  make_response({'message': f'No bakery with an id of {id}'}, 404)
    bakery_dict = bakery.to_dict()
    return make_response(bakery_dict, 200)
    
    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    if not baked_goods:
        return  make_response({'message':'No Baked Goods'}, 404)
    else:
        goods_to_return = [baked_good.to_dict() for baked_good in baked_goods if isinstance(baked_good, BakedGood)]
        return make_response(goods_to_return,200)



# GET /baked_goods/most_expensive: returns the single most expensive baked good as JSON.
# (HINT: how can you use SQLAlchemy to sort the baked goods in descending order and limit the number of results?)
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_exp_good = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    if most_exp_good:
        return make_response(most_exp_good.to_dict(), 200)
    else:
        return make_response({'message':'There is no Baked Good'}, 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)


