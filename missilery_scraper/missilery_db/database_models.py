"""
SQLAlchemy models for Missilery Database
Comprehensive relational database schema for missile data
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import json

Base = declarative_base()

class Country(Base):
    """Countries table"""
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    code = Column(String(3), unique=True, nullable=True)  # ISO country code

    # Relationships
    missiles = relationship("Missile", back_populates="country_rel")

class Purpose(Base):
    """Missile purposes table"""
    __tablename__ = 'purposes'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    missiles = relationship("Missile", back_populates="purpose_rel")

class BaseType(Base):
    """Base types table (launch platforms)"""
    __tablename__ = 'base_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    missiles = relationship("Missile", back_populates="base_type_rel")

class WarheadType(Base):
    """Warhead types table"""
    __tablename__ = 'warhead_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    missiles = relationship("Missile", back_populates="warhead_type_rel")

class GuidanceSystem(Base):
    """Guidance systems table"""
    __tablename__ = 'guidance_systems'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    missiles = relationship("Missile", back_populates="guidance_system_rel")

class Missile(Base):
    """Main missiles table"""
    __tablename__ = 'missiles'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, index=True)
    detail_page_url = Column(String(500), unique=True, nullable=False)
    index_page_url = Column(String(500), nullable=False)
    page_number = Column(Integer, nullable=False)

    # Basic characteristics
    range_km = Column(Integer, nullable=True)
    year_developed = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)

    # Foreign keys
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=True)
    purpose_id = Column(Integer, ForeignKey('purposes.id'), nullable=True)
    base_type_id = Column(Integer, ForeignKey('base_types.id'), nullable=True)
    warhead_type_id = Column(Integer, ForeignKey('warhead_types.id'), nullable=True)
    guidance_system_id = Column(Integer, ForeignKey('guidance_systems.id'), nullable=True)

    # Metadata
    scraped_at = Column(DateTime, default=datetime.utcnow)
    is_detailed = Column(Boolean, default=False)

    # Relationships
    country_rel = relationship("Country", back_populates="missiles")
    purpose_rel = relationship("Purpose", back_populates="missiles")
    base_type_rel = relationship("BaseType", back_populates="missiles")
    warhead_type_rel = relationship("WarheadType", back_populates="missiles")
    guidance_system_rel = relationship("GuidanceSystem", back_populates="missiles")

    # Detailed data relationships
    detailed_data = relationship("MissileDetailedData", back_populates="missile", uselist=False)
    structured_content = relationship("StructuredContent", back_populates="missile")
    characteristics = relationship("Characteristic", back_populates="missile")
    images = relationship("MissileImage", back_populates="missile")

    # Indexes
    __table_args__ = (
        Index('idx_missile_name', 'name'),
        Index('idx_missile_country', 'country_id'),
        Index('idx_missile_purpose', 'purpose_id'),
        Index('idx_missile_range', 'range_km'),
        Index('idx_missile_year', 'year_developed'),
    )

class MissileDetailedData(Base):
    """Detailed missile data table"""
    __tablename__ = 'missile_detailed_data'

    id = Column(Integer, primary_key=True)
    missile_id = Column(Integer, ForeignKey('missiles.id'), unique=True, nullable=False)
    detailed_filename = Column(String(200), nullable=True)

    # Detailed characteristics
    range_detailed = Column(String(100), nullable=True)
    speed = Column(String(100), nullable=True)
    weight = Column(String(100), nullable=True)
    length = Column(String(100), nullable=True)
    diameter = Column(String(100), nullable=True)
    wingspan = Column(String(100), nullable=True)
    height = Column(String(100), nullable=True)
    accuracy = Column(String(100), nullable=True)
    flight_time = Column(String(100), nullable=True)
    flight_altitude = Column(String(100), nullable=True)
    engine_type = Column(String(100), nullable=True)
    thrust = Column(String(100), nullable=True)
    burn_time = Column(String(100), nullable=True)
    fuel_type = Column(String(100), nullable=True)
    guidance_system_detailed = Column(String(200), nullable=True)
    warhead_detailed = Column(String(200), nullable=True)
    fuse_type = Column(String(100), nullable=True)
    country_detailed = Column(String(100), nullable=True)
    developer = Column(String(200), nullable=True)
    manufacturer = Column(String(200), nullable=True)
    year_developed_detailed = Column(String(100), nullable=True)
    adoption_year = Column(String(100), nullable=True)
    status = Column(String(100), nullable=True)
    quantity = Column(String(100), nullable=True)
    other_characteristics = Column(Text, nullable=True)

    # Metadata
    scraped_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    missile = relationship("Missile", back_populates="detailed_data")

class StructuredContent(Base):
    """Structured content from detailed pages"""
    __tablename__ = 'structured_content'

    id = Column(Integer, primary_key=True)
    missile_id = Column(Integer, ForeignKey('missiles.id'), nullable=False)
    field_name = Column(String(100), nullable=False)
    field_label = Column(String(200), nullable=True)
    field_text = Column(Text, nullable=True)

    # Relationships
    missile = relationship("Missile", back_populates="structured_content")

    # Indexes
    __table_args__ = (
        Index('idx_structured_content_missile', 'missile_id'),
        Index('idx_structured_content_field', 'field_name'),
    )

class StructuredContentLink(Base):
    """Links within structured content"""
    __tablename__ = 'structured_content_links'

    id = Column(Integer, primary_key=True)
    structured_content_id = Column(Integer, ForeignKey('structured_content.id'), nullable=False)
    link_url = Column(String(500), nullable=False)
    link_text = Column(String(200), nullable=True)

    # Relationships
    structured_content = relationship("StructuredContent")

class Characteristic(Base):
    """Characteristics table for detailed technical specs"""
    __tablename__ = 'characteristics'

    id = Column(Integer, primary_key=True)
    missile_id = Column(Integer, ForeignKey('missiles.id'), nullable=False)
    field_name = Column(String(200), nullable=False)
    field_value = Column(Text, nullable=False)

    # Relationships
    missile = relationship("Missile", back_populates="characteristics")

    # Indexes
    __table_args__ = (
        Index('idx_characteristics_missile', 'missile_id'),
        Index('idx_characteristics_field', 'field_name'),
    )

class MissileImage(Base):
    """Images associated with missiles"""
    __tablename__ = 'missile_images'

    id = Column(Integer, primary_key=True)
    missile_id = Column(Integer, ForeignKey('missiles.id'), nullable=False)
    image_url = Column(String(500), nullable=False)
    image_type = Column(String(50), nullable=True)  # 'main', 'gallery', 'diagram', etc.
    alt_text = Column(String(200), nullable=True)

    # Relationships
    missile = relationship("Missile", back_populates="images")

    # Indexes
    __table_args__ = (
        Index('idx_missile_images_missile', 'missile_id'),
        Index('idx_missile_images_type', 'image_type'),
    )

class ScrapingSession(Base):
    """Scraping sessions metadata"""
    __tablename__ = 'scraping_sessions'

    id = Column(Integer, primary_key=True)
    session_name = Column(String(100), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    total_pages = Column(Integer, nullable=True)
    total_missiles = Column(Integer, nullable=True)
    total_detailed = Column(Integer, nullable=True)
    status = Column(String(50), default='running')  # 'running', 'completed', 'failed'
    notes = Column(Text, nullable=True)

# Database connection and session management
class DatabaseManager:
    def __init__(self, database_url="sqlite:///missilery.db"):
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        """Get database session"""
        return self.SessionLocal()

    def close(self):
        """Close database connection"""
        self.engine.dispose()

# Utility functions
def get_or_create(session, model, **kwargs):
    """Get or create a model instance"""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
        return instance

def parse_comma_separated_values(value_string):
    """Parse comma-separated values and return list of cleaned values"""
    if not value_string:
        return []
    return [v.strip() for v in value_string.split(',') if v.strip()]

def create_database_schema():
    """Create the complete database schema"""
    db_manager = DatabaseManager()
    db_manager.create_tables()
    print("Database schema created successfully!")
    return db_manager
