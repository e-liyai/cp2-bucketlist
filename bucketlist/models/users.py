"""
File      : users.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Model class that creates users and connects to database
"""

# ============================================================================
# necessary imports
# ============================================================================
from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Numeric, Date, desc
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship

from db_model import Model


class Users(Model, UserMixin):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(200), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    hash_password = Column(String(1000))
    bucketlists = relationship('Bucketlist', backref="Users")

    def get_id(self):
        return self.user_id

    def check_user_password(self, _password):
        return check_password_hash(self.hash_password, _password)

    @property
    def password(self, password):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def serialize(self):
        """
        The method returns a dictionary of key value pair
        :return: Object property in a dictionary 
        """
        return{
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "bucketlists": [bucketlist.serialize() for bucketlist in self.bucketlists]
        }
