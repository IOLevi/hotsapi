"User module for DB/sqlalchemy integration"
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, DateTime
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from dbs import storage
import dbs
from herotemplate import Base
from flask_login import UserMixin


class User(Base, UserMixin):
    "User for login"
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))
    hotslogs = Column(String(120), nullable=True)

    def set_password(self, password):
        "generates a hashed password for storage"
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        "checks whether password input resolves to same hashed password"
        return check_password_hash(self.password_hash, password)

    def save(self):
        '''
            Update the updated_at attribute with new.
        '''
        dbs.storage.new(self)
        dbs.storage.save()

    def delete(self):
        '''
            Deletes an object
        '''
        dbs.storage.delete(self)
