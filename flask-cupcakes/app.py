"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'keep it secret, keep it safe'

connect_db(app)
db.create_all()


###################################################################################################
# These two routes render the templates for... 
# 1) the HOME page to display ALL cupcakes, 
# 2) the SHOW page to display information and the edit form for a SINGLE cupcake
###################################################################################################

@app.route('/')
def homepage():
    """Display the home page template"""
    return render_template('home.html')


@app.route('/cupcake/<int:cupcake_id>')
def show_cupcake(cupcake_id):
    """Get data about a single cupcake; render details page for that cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return render_template('show_cupcake.html', cupcake=cupcake)


###################################################################################################
# These routes are API endpoints, following RESTful architecture as best as possible
###################################################################################################

@app.route('/api/cupcakes')
def get_cupcakes():
    """Return JSON for each cupcake in db"""
    cupcakes = Cupcake.query.all()
    serialized = [c.serialize_cupcake() for c in cupcakes]
    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/find', methods=['POST'])
def search_cupcakes():
    """Search the db for cupcakes matching the search term input value;
    This route will return JSON results that closely match either the FLAVOR, SIZE, or RATING of the search term"""
    data = request.json
    search_term = data['searchTerm']
    search_results = Cupcake.query.filter((Cupcake.flavor.ilike(f'%{search_term}%')) 
        | (Cupcake.size.ilike(f'%{search_term}%')) 
        | (Cupcake.rating.ilike(f'%{search_term}%'))).all()
    cupcakes = [c.serialize_cupcake() for c in search_results]
    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes', methods=['POST'])
def add_cupcake():
    """Add a new cupcake to the db and return the JSON for that cupcake"""
    data = request.json
    cupcake = Cupcake(
        flavor = data['flavor'],
        size = data['size'],
        rating = data['rating'],
        image = data['image']
        )
    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake = cupcake.serialize_cupcake()), 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['POST'])
def update_cupcake(cupcake_id):
    """Update a cupcake's info in the db and return the JSON for that cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json
    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize_cupcake())


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a cupcake from the db"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")

