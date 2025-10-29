"""Database models for PyDayflow"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Recording(Base):
    """Model for screen recording chunks"""
    __tablename__ = 'recordings'
    
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    file_path = Column(String(512), nullable=False)
    duration = Column(Float, nullable=False)  # Duration in seconds
    analyzed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class TimelineCard(Base):
    """Model for timeline activity cards"""
    __tablename__ = 'timeline_cards'
    
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    title = Column(String(256), nullable=False)
    summary = Column(Text)
    category = Column(String(64))  # e.g., 'work', 'personal', 'distraction'
    confidence = Column(Float)  # AI confidence score
    thumbnail_path = Column(String(512))
    created_at = Column(DateTime, default=datetime.utcnow)


class AppState(Base):
    """Model for application state"""
    __tablename__ = 'app_state'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(64), unique=True, nullable=False)
    value = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DatabaseManager:
    """Database manager for PyDayflow"""
    
    def __init__(self, database_path):
        """Initialize database manager"""
        self.engine = create_engine(f'sqlite:///{database_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        """Get a new database session"""
        return self.Session()
    
    def close(self):
        """Close database connection"""
        self.engine.dispose()
