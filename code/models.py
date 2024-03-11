from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()
def connect_db(app):
    """Connect this database to provided Flask app.
    """
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)
    #email?????
    #image?????
    password = db.Column(db.Text)
    reviews = db.Relationship('Review', backref='user')
    favorties = db.Relationship('Favorite', backref='user')

    @classmethod
    def signup(cls, username, firstname, lastname, password):
        hashedpw = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(username=username, firstname=firstname, lastname=lastname, password=hashedpw)
        db.session.add(user)
        return user
    
    @classmethod
    def login(cls, username, password):
        user = cls.query.filter_by(username=username).first()
#################################################
        if user:
            authenticate = bcrypt.check_password_hash(user.password, password)
            if authenticate:
                return user
        return False


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    review = db.Column(db.Text)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    drinkid = db.Column(db.Integer)
    drinkname = db.Column(db.Text)

    # @classmethod
    # def save_review(cls, title, review, userid):
    #     review=Review(title=title, review=review, userid=user_id)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    drinkid = db.Column(db.Integer)
    drinkname = db.Column(db.Text)

# class CreateOwnDrink(db.Model):


    

