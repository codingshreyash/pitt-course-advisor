
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import datetime

Base = declarative_base()

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    title = Column(String)
    sci_href = Column(String)
    description = Column(Text)
    prerequisites = Column(Text)
    credits_min = Column(Integer)
    credits_max = Column(Integer)
    wiki_difficulty_rating = Column(Float)
    wiki_reviews = Column(Text)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    sources = relationship('CourseSource', back_populates='course')
    conflicts = relationship('DataConflict', back_populates='course')
    prerequisite_for = relationship('PrerequisiteRelationship', foreign_keys='PrerequisiteRelationship.prerequisite_id', back_populates='prerequisite_course')
    has_prerequisites = relationship('PrerequisiteRelationship', foreign_keys='PrerequisiteRelationship.course_id', back_populates='main_course')

class CourseSource(Base):
    __tablename__ = 'course_sources'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    field_name = Column(String, nullable=False)
    source = Column(String, nullable=False)

    course = relationship('Course', back_populates='sources')

class DataConflict(Base):
    __tablename__ = 'data_conflicts'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    field_name = Column(String, nullable=False)
    wiki_value = Column(Text)
    official_value = Column(Text)
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime)

    course = relationship('Course', back_populates='conflicts')

class ScrapeMetadata(Base):
    __tablename__ = 'scrape_metadata'

    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False) # "wiki" or "official"
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime)
    status = Column(String, nullable=False) # "success" or "failure"
    rows_processed = Column(Integer)
    error_message = Column(Text)

class PrerequisiteRelationship(Base):
    __tablename__ = 'prerequisite_relationships'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False) # Course that has the prerequisite
    prerequisite_id = Column(Integer, ForeignKey('courses.id'), nullable=False) # The prerequisite course

    main_course = relationship('Course', foreign_keys=[course_id], back_populates='has_prerequisites')
    prerequisite_course = relationship('Course', foreign_keys=[prerequisite_id], back_populates='prerequisite_for')
