from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool
import random
import string

Base = declarative_base()

class Person(Base):
    __tablename__ = 'people'

    id = Column("id", String, primary_key=True)
    email = Column("Email", String)
    parentname = Column("ParentName", String)
    childname = Column("ChildName", String)
    registeredlesson = Column("RegisteredLesson", String)
    date = Column("Date", String)
    amount = Column("Amount", Integer)


    def __init__(self,id, email, parentname, childname, registeredlesson, date, amount):
        self.id = id
        self.email = email
        self.parentname = parentname
        self.childname = childname
        self.registeredlesson = registeredlesson
        self.date = date
        self.amount = amount

    def __repr__(self):
        return f"{self.id}, {self.email}, {self.parentname}, {self.childname}, {self.registeredlesson}, {self.date}, {self.amount}"
    
engine = create_engine("sqlite:///people.db")
Base.metadata.create_all(bind=engine)

def addPerson(email, parentName, childName, lessonName, date, amount):
    generatedID = (''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=40)))
    person = Person(generatedID, email, parentName, childName, lessonName, date, amount)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(person)
    session.commit()


def queryPeople():
    Session = sessionmaker(bind=engine)
    session = Session()
    results = session.query(Person).all()
    return results


#addUser("stellan.lindrud@gmail.com","Stellan Lindrud","Ally Lindrud","Young Beginners")