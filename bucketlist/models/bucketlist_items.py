"""
File      : bucketlist_items.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Model class that creates bucketlists items and connects to database
"""

# ============================================================================
# necessary imports
# ============================================================================
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Boolean, Date, desc
from datetime import datetime
from sqlalchemy.orm import relationship

from db_model import Model


class BucketlistItems(Model):
    __tablename__ = 'BucketlistItems'
    item_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    item_name = Column(String(100), nullable=False)
    date_created = Column(Date, default=datetime.utcnow)
    done = Column(Boolean, default=False, nullable=False)
    date_completed = Column(Date)
    description = Column(String(500))
    bucketlist = Column(Integer, ForeignKey('Bucketlist.bucketlist_id'))

    @staticmethod
    def get_by_item_id(cardid):
        pass

    @staticmethod
    def return_all():
        pass

    def serialize(self):
        """
        The method returns a dictionary of key value pair
        :return: Object property in a dictionary 
        """
        return{
            "item_id": self.item_id,
            "item_name": self.item_name,
            "date_created": self.date_created.isoformat() if self.date_created else "",
            "date_completed": self.date_completed.isoformat() if self.date_completed else "",
            "description": self.description,
            "bucketlist": self.bucketlist
        }