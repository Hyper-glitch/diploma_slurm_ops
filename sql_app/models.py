from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    Enum,
    DateTime,
)
from sqlalchemy.orm import relationship

from enums.analyzer import UsageEnum, DecisionEnum, IntensityEnum, DimensionEnum
from sql_app.database import Base


class Dimension(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Enum(DimensionEnum), nullable=False)
    mean = Column(Float, nullable=False)
    median = Column(Float, nullable=False)
    usage_type = Column(Enum(UsageEnum), index=True, nullable=False)
    intensity = Column(Enum(IntensityEnum), nullable=False)
    decision = Column(Enum(DecisionEnum), index=True, nullable=False)
    collect_date = Column(DateTime, nullable=False)


class Resource(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    dimension_id = Column(Integer, ForeignKey("dimension.id"))
    dimensions = relationship("Dimension", back_populates="resource")


class Team(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    resource_id = Column(Integer, ForeignKey("resource.id"))
    resources = relationship("Resource", back_populates="team")
