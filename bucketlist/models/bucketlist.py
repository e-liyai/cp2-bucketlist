"""
File      : bucketlist.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Model class that creates bucketlists and connects to database
"""

# ============================================================================
# necessary imports
# ============================================================================
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from datetime import datetime
from sqlalchemy.orm import relationship

from db_model import Model


class Bucketlist(Model):
    __tablename__ = 'Bucketlist'
    bucketlist_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    bucketlist_name = Column(String(100), nullable=False)
    date = Column(Date, default=datetime.utcnow)
    user = Column(Integer, ForeignKey('Users.user_id'))
    bucketlist_items = relationship('BucketlistItems')

    @staticmethod
    def return_all_bucketlist():
        pass

    @staticmethod
    def get_by_bucketlist_id(bucketlist_id):
        pass

    def serialize(self):
        """
        The method returns a dictionary of key value pair
        :return: Object property in a dictionary 
        """
        return{
            "bucketlist_id": self.bucketlist_id,
            "bucketlist_name": self.bucketlist_name,
            "date": self.date.isoformat() if self.date else "",
            "user": self.user,
            "bucketlist_items": [item.serialize() for item in self.bucketlist_items]
        }
