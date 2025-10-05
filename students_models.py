from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class StudentModel(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    certification = Column(String)
    gender = Column(String)
    address = Column(String)


engine = create_engine('sqlite:///students.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def create_tables():
    Base.metadata.create_all(engine)

