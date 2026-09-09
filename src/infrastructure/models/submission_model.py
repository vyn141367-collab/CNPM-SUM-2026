from sqlalchemy import Column, Integer, String
from infrastructure.databases import Base

class SubmissionModel(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=True)
    image_url = Column(String(500), nullable=False)
    film_stock = Column(String(100), nullable=False)
    camera = Column(String(100), nullable=False)
    lens = Column(String(100), nullable=True)
    iso = Column(Integer, nullable=True)
    film_format = Column(String(50), nullable=True)
    developing_lab = Column(String(100), nullable=True)
    scanning_specs = Column(String(100), nullable=True)