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

from enums.decision import DecisionEnum
from enums.dimension import DimensionEnum
from enums.intensity import IntensityEnum
from enums.usage import UsageEnum
from sql_app.database import Base


class Dimension(Base):
    __tablename__ = "dimension"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Enum(DimensionEnum), nullable=False)

    mean = Column(Float, nullable=False)
    median = Column(Float, nullable=False)
    usage_type = Column(Enum(UsageEnum), index=True, nullable=False)
    intensity = Column(Enum(IntensityEnum), nullable=False)
    decision = Column(Enum(DecisionEnum), index=True, nullable=False)
    collect_date = Column(DateTime, nullable=False)

    resource = relationship("Resource", back_populates="dimensions")
    resource_id = Column(Integer, ForeignKey("resource.id"))


class Resource(Base):
    __tablename__ = "resource"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)

    dimensions = relationship("Dimension", back_populates="resource")

    team = relationship("Team", back_populates="resources")
    team_id = Column(Integer, ForeignKey("team.id"))


class Team(Base):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)

    resources = relationship("Resource", back_populates="team")
