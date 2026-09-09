from abc import ABC, abstractmethod
from config import FactoryConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class AbstractDatabase(ABC):
    def __init__(self):
        # Lấy URI từ file config, tự động dùng SQLite nếu URI bị None
        self.database_uri = FactoryConfig.get_config("development").DATABASE_URI
        self.engine = create_engine(self.database_uri or 'sqlite:///app.db')
        
        # Chỉ khởi tạo Session Factory (bản thiết kế), KHÔNG tạo sẵn session thực tế ở đây
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @abstractmethod
    def init_database(self, app):
        """Phương thức trừu tượng để khởi tạo DB với Flask App"""
        pass

    def get_session(self):
        """Hàm hỗ trợ lấy Session MỚI cho từng Request"""
        return self.SessionLocal()