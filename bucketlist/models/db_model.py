"""
File      : db_model.py
Date      : April, 2017
Author    : eugene liyai
Desc      : creates instance of SQLAlchemy declarative_base which all models instances inherit
"""

# ============================================================================
# necessary imports
# ============================================================================
from sqlalchemy.ext.declarative import declarative_base
Model = declarative_base()
