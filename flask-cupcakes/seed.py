from app import app
from models import db, Cupcake


db.drop_all()
db.create_all()

c1 = Cupcake(
    flavor="cherry",
    size="large",
    rating=5,
    image="https://images.media-allrecipes.com/userphotos/8246912.jpg"
)

c2 = Cupcake(
    flavor="chocolate",
    size="small",
    rating=9,
    image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
)

c3 = Cupcake(
    flavor="banana",
    size="medium",
    rating=7,
    image="https://cdn.cupcakeproject.com/wp-content/uploads/2007/10/Banana-Cupcakes-04.jpg"
)

c4 = Cupcake(
    flavor="strawberry",
    size="medium",
    rating=9,
    image="https://grandbaby-cakes.com/wp-content/uploads/2019/07/Strawberry-cupcakes-04.jpg"
)

c5 = Cupcake(
    flavor="lavender",
    size="large",
    rating=10,
    image="https://www.barleyandsage.com/wp-content/uploads/2021/04/blackberry-lavender-cupcakes-1200x1200-1.jpg"
)

c6 = Cupcake(
    flavor="funfetti",
    size="medium",
    rating=7,
    image="https://www.the-girl-who-ate-everything.com/wp-content/uploads/2018/09/funfetti-cupcakes-14.jpg"
)

c7 = Cupcake(
    flavor="pistachio",
    size="small",
    rating=7,
    image="https://greedyeats.com/wp-content/uploads/2019/09/Pistachio-cupcakes.jpg"
)

db.session.add_all([c1, c2, c3, c4, c5, c6, c7])
db.session.commit()