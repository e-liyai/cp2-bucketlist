"""
File      : initilize_db.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Initializes tables in the database
"""

# ============================================================================
# necessary imports
# ============================================================================
from sqlalchemy import create_engine
from db_model import Model


def init_bucketlist_database(engine):
    db_engine = create_engine(engine, echo=True)
    Model.metadata.create_all(db_engine)


def drop_bucketlist_database(db_engine):
    Model.metadata.drop_all(db_engine)
