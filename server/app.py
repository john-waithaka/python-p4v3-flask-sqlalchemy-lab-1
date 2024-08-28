# server/app.py
#!/usr/bin/env python3

#added the import jsonify

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate


from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)



# Add views here

@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake is None:
    
        return jsonify({'message': f'Earthquake {id} not found.'}), 404
    
    else:
        return jsonify({
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        })
        


#OR VIEW 2

# @app.route('/earthquakes/<int:id>', methods=['GET'])
# def get_earthquake(id):
#     try:
#         earthquake = Earthquake.query.get(id)
#         if earthquake:
#             body = {
#                 'id': earthquake.id,
#                 'location': earthquake.location,
#                 'magnitude': earthquake.magnitude,
#                 'year': earthquake.year
#             }
#             status = 200
#         else:
#             body = {'message': f'Earthquake {id} not found.'}
#             status = 404

#         return jsonify(body), status

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500




@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    data = [{'id': eq.id, 'location': eq.location, 'magnitude': eq.magnitude, 'year': eq.year} for eq in earthquakes]
    return jsonify({'count': len(earthquakes), 'quakes': data})


if __name__ == '__main__':
    app.run(port=5555, debug=True)






