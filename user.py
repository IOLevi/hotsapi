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

# ...

class User(Base, UserMixin):
    # ...
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
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
    # is_authenticated()
    # is_active()
    # is_anonymous()
    # get_id()

# if __name__ == "__main__":
#     a = User()
#     a.set_password("hi")

#     print(a.password_hash)
#     print(a.check_password("hi"))