from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import dbs

Base = declarative_base()

class HeroTemplate(Base):

    __tablename__ = 'heroes'
    id = Column(String(60), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    # should i have a UUID as primary key ID?
    heroName = Column(String(60), nullable=False, primary_key=True)    
    gamesPlayed = Column(Integer, nullable=False, default=0) # should i set defaults?
    gamesBanned = Column(Integer, nullable=False, default=0) # should i set defaults?
    participation = Column(Float, nullable=False, default=0) # should i set defaults?
    winRate = Column(Float, nullable=False, default=0) # should i set defaults?
    change = Column(Float, nullable=False, default=0) # should i set defaults?
    heroClass = Column(String(60), nullable=False, default=0) # should i set defaults?
    heroSubclass = Column(String(60), nullable=False, default=0) # should i set defaults?

    def __init__(self, *args, **kwargs):
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        for key, val in kwargs.items():
            setattr(self, key, val)

    def __str__(self):
        '''
            Return string representation of BaseModel class
        '''
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                    self.id, self.__dict__))

    def __repr__(self):
        '''
            Return string representation of BaseModel class
        '''
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def save(self):
        '''
            Update the updated_at attribute with new.
        '''
        self.updated_at = datetime.now()
        dbs.storage.new(self)
        dbs.storage.save()

    def to_dict(self):
        '''
            Return dictionary representation of BaseModel class.
        '''
        cp_dct = dict(self.__dict__)
        cp_dct['__class__'] = self.__class__.__name__
        cp_dct['updated_at'] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        cp_dct['created_at'] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        if hasattr(self, "_sa_instance_state"):
            del cp_dct["_sa_instance_state"]
        return (cp_dct)

    def delete(self):
        '''
            Deletes an object
        '''
        dbs.storage.delete(self)