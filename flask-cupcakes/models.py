from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database; call this function in app.py"""
    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    """Model for cupcakes"""
    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    flavor = db.Column(db.String, nullable=False)

    size = db.Column(db.String, nullable=False)

    rating = db.Column(db.String, nullable=False)

    image = db.Column(db.String, nullable = False, default='https://thestayathomechef.com/wp-content/uploads/2017/12/Most-Amazing-Chocolate-Cupcakes-1-small.jpg')

    def serialize_cupcake(self):
        """Serialize a cupcake SQLAlchemy obj to dictionary"""
        return {
             "id": self.id,
             "flavor": self.flavor,
             "size": self.size,
             "rating": self.rating,
             "image": self.image
        }
