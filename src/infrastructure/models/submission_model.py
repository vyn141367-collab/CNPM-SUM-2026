from sqlalchemy import Column, Integer, String, Text

from infrastructure.databases.base import Base 

class SubmissionModel(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True, default='N/A') 
    title = Column(String(200), nullable=False)
    image_url = Column(String(500), nullable=True)
    film_stock = Column(String(100), nullable=True)
    camera = Column(String(100), nullable=True)
    lens = Column(String(100), nullable=True)
    iso = Column(String(20), nullable=True)
    film_format = Column(String(50), nullable=True)
    developing_lab = Column(String(100), nullable=True)
    scanning_specs = Column(String(100), nullable=True)
    score = Column(Integer, nullable=True)                    
    comment = Column(Text, nullable=True)                     
