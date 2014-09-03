from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from zope.sqlalchemy import ZopeTransactionExtension


Base = declarative_base()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

class MyModel(Base):
    __tablename__ = 'my_models'
    id = Column(Integer, primary_key=True)
    name = Column(Text, index=True)
    value = Column(Integer)
    
