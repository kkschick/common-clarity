from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


engine = create_engine("postgresql://localhost:5432/loop", echo=False)
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    user_type = Column(String(64))
    username = Column(String(64))
    password = Column(String(64))
    first_name = Column(String(64))
    last_name = Column(String(64))
    email = Column(String(128), nullable = True)

class Cohort(Base):
    __tablename__ = "cohorts"

    id = Column(Integer, primary_key = True)
    name = Column(String(64))
    teacher_id = Column(Integer, ForeignKey('users.id'))

class StudentCohort(Base):
    __tablename__ = "studentcohorts"

    id = Column(Integer, primary_key = True)
    student_id = Column(Integer, ForeignKey('users.id'))
    cohort_id = Column(Integer, ForeignKey('cohorts.id'))

    student = relationship("User", backref=backref("studentcohorts", order_by=id))
    cohort = relationship("Cohort", backref=backref("studentcohorts", order_by=id))

class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key = True)
    name = Column(String(64))
    test_date = Column(Date)
    teacher_id = Column(Integer, ForeignKey('users.id'))

    teacher = relationship("User", backref=backref("tests", order_by=id))

class Standard(Base):
    __tablename__ = "standards"

    id = Column(Integer, primary_key = True)
    category = Column(String(64))
    code = Column(String(64))
    description = Column(Text)

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key = True)
    student_id = Column(Integer, ForeignKey('users.id'))
    test_id = Column(Integer, ForeignKey('tests.id'))
    standard_id = Column(Integer, ForeignKey('standards.id'))
    score = Column(String(20))

    student = relationship("User", backref=backref("scores", order_by=id))
    test = relationship("Test", backref=backref("scores", order_by=id))
    standard = relationship("Standard", backref=backref("scores", order_by=id))

### End class declarations

def create_tables():
    Base.metadata.create_all(engine)

def main():
    create_tables()

if __name__ == "__main__":
    main()