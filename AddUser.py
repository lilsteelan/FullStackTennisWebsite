from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
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

    def __init__(self,id, email, parentname, childname, registeredlesson):
        self.id = id
        self.email = email
        self.parentname = parentname
        self.childname = childname
        self.registeredlesson = registeredlesson

    def __repr__(self):
        return f"{self.id}, {self.email}, {self.parentname}, {self.childname}, {self.registeredlesson})"
    
engine = create_engine("sqlite:///people.db")
Base.metadata.create_all(bind=engine)


def addUser():
    generatedID = (''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=40)))
    person = Person(generatedID, "stellan.lindrud@gmail.com","Stellan Lindrud","Ally Lindrud","Young Beginners")
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(person)
    session.commit()
    results = session.query(Person).all()
    print(results)

def addUser(email,parentName,childName,lessonName):
    generatedID = (''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=40)))
    person = Person(generatedID, email,parentName,childName,lessonName)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(person)
    session.commit()
    results = session.query(Person).all()
    print(results)

addUser("stellan.lindrud@gmail.com","Stellan Lindrud","Ally Lindrud","Young Beginners")
