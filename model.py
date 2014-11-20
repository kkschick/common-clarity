from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Text, Float
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine("postgresql://localhost:5432/dash", echo=False)
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index=True)
    user_type = Column(String(64))
    email = Column(String(128), nullable = True)
    password = Column(String(128), nullable = True)
    first_name = Column(String(64))
    last_name = Column(String(64))

class Cohort(Base):
    __tablename__ = "cohorts"

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String(64))
    teacher_id = Column(Integer, ForeignKey('users.id'))

    teacher = relationship("User", backref=backref("cohorts", order_by=id))

class StudentCohort(Base):
    __tablename__ = "studentcohorts"

    id = Column(Integer, primary_key = True, index=True)
    student_id = Column(Integer, ForeignKey('users.id'))
    cohort_id = Column(Integer, ForeignKey('cohorts.id'))

    student = relationship("User", backref=backref("studentcohorts", order_by=id))
    cohort = relationship("Cohort", backref=backref("studentcohorts", order_by=id))

class Test(Base):

    __tablename__ = "tests"

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String(64))
    test_date = Column(Date)
    cohort_id = Column(Integer, ForeignKey('cohorts.id'))

    cohort = relationship("Cohort", backref=backref("tests", order_by=id))

class Standard(Base):
    __tablename__ = "standards"

    id = Column(Integer, primary_key = True, index=True)
    category = Column(String(64))
    code = Column(String(64))
    description = Column(Text)

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key = True, index=True)
    student_id = Column(Integer, ForeignKey('users.id'))
    test_id = Column(Integer, ForeignKey('tests.id'))
    standard_id = Column(Integer, ForeignKey('standards.id'))
    score = Column(String(20))

    student = relationship("User", backref=backref("scores", order_by=id))
    test = relationship("Test", backref=backref("scores", order_by=id))
    standard = relationship("Standard", backref=backref("scores", order_by=id))

class NormScore(Base):
    __tablename__ = "normscores"

    id = Column(Integer, primary_key = True, index=True)
    cohort_name = Column(String(64))
    test_id = Column(Integer, ForeignKey('tests.id'))
    standard_id = Column(Integer, ForeignKey('standards.id'))
    score = Column(Float)

    test = relationship("Test", backref=backref("normscores", order_by=id))
    standard = relationship("Standard", backref=backref("normscores", order_by=id))


### End class declarations

def create_tables():
    Base.metadata.create_all(engine)

def main():
    create_tables()

if __name__ == "__main__":
    main()