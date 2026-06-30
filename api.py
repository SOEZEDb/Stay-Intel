from flask import Flask, jsonify, request
from models import db,Intel,Category
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'StayIntel.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def intel_to_dict(intel):
    return{
        'id': intel.id,
        'name': intel.name,
        'link': intel.link,
        'provisions': ' | '.join([p.strip() for p in intel.provisions.split('\n') if p.strip()]),
        'rating': intel.rating,
    }

@app.route('/list')
def get_rows():
    name = request.args.get('name')
    page = request.args.get('page',  1, type=int)
    per_page = 50
    query =  Intel.query
    if name:
        query = query.filter_by(name=name)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    intels = pagination.items

    return jsonify([intel_to_dict(intel) for intel in intels])

@app.route('/hotels/provision/<provision_name>')
def get_hotel_provision(provision_name):
    intels = Intel.query.filter(Intel.provisions.contains(provision_name)).all()
    return jsonify([intel_to_dict(intel) for intel in intels])

@app.route('/top rated')
def get_top_rated_hotels():
    limit = request.args.get('limit', 10, type=int)
    hotels = Intel.query.filter(Intel.rating is not None).order_by(Intel.rating.desc()).limit(limit).all()
    return jsonify([intel_to_dict(intel) for intel in hotels])

@app.route('/least rated')
def get_least_rated_hotels():
    limit = request.args.get('limit', 10, type=int)
    hotels = Intel.query.filter(Intel.rating is not None).order_by(Intel.rating.asc()).limit(limit).all()
    return jsonify([intel_to_dict(intel) for intel in hotels])

if __name__ == '__main__':
    app.run(debug=True)