from app.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, DateTime,func
from sqlalchemy.orm import relationship


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(String,default="pending")
    start_date = Column(DateTime,default=func.now())
    end_date = Column(DateTime,default=func.now())