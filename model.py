from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable = True)
    password = Column(String(64), nullable = True)
    age = Column(Integer, nullable = True)
    gender = Column(String(64), nullable = True)
    zipcode = Column(String(15), nullable = True)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    title = Column(String(64))
    release_date = Column(DateTime(timezone = False), nullable = True)
    imdb_url = Column(String(64), nullable = True)

class Rating(Base):
### Association object
    __tablename__= "ratings"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    rating = Column(Integer)
    timestamp = Column(String(15), nullable = True)

    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=id))

### End class declarations

def get_user_from_email(email):
    user = User.query.filter_by(email=email).first()
    return user

def get_user_from_id(id):
    user = User.query.filter_by(id=id).first()
    return user

def get_the_eye():
    the_eye = User.query.filter_by(email="theeye@ofjudgment.com").first()
    return the_eye

def get_eye_rating(the_eye, movie_id):
    eye_rating = Rating.query.filter_by(user_id=the_eye.id, movie_id=movie_id).first()
    return eye_rating

def get_movie_from_id(id):
    movie = Movie.query.filter_by(id=id).first()
    return movie

def create_user(email, password, gender, zipcode, age):
    user = User(age = age, gender = gender, zipcode = zipcode, email=email, password= password)
    session.add(user)
    session.commit()

def show_movie_details(id):
    movies = Rating.query.filter_by(movie_id=id).all()
    return movies

def add_rating(movie_id, user_id, rating):
    rating = Rating(movie_id=movie_id, user_id=user_id, rating=rating)
    session.add(rating)
    session.commit()

def is_rating(user_id, movie_id):
    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    return rating

def update_rating(movie_id, user_id, new_rating):
    old_rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    old_rating.rating = new_rating

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
