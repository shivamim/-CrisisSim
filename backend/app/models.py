"""
models.py — Database schema for CrisisSim
==========================================
"""

import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Float, Integer, Boolean,
    DateTime, ForeignKey, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    industry = Column(String(100), nullable=False)
    brand_voice = Column(Text)
    key_executives = Column(JSON)
    past_crises = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    simulations = relationship("Simulation", back_populates="organization")
    monitors = relationship("Monitor", back_populates="organization")


class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    title = Column(String(255), nullable=False)
    announcement_text = Column(Text, nullable=False)
    industry_context = Column(Text)
    status = Column(String(50), default="pending")

    parsed_claims = Column(JSON)
    risk_score = Column(Float)
    crisis_scenarios = Column(JSON)
    timeline_predictions = Column(JSON)
    sentiment_trajectory = Column(JSON)

    agent_count = Column(Integer, default=0)
    iteration_count = Column(Integer, default=0)
    total_time_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    organization = relationship("Organization", back_populates="simulations")
    scenarios = relationship("CrisisScenario", back_populates="simulation", cascade="all, delete-orphan")


class CrisisScenario(Base):
    __tablename__ = "crisis_scenarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    simulation_id = Column(UUID(as_uuid=True), ForeignKey("simulations.id"), nullable=False)
    scenario_name = Column(String(255), nullable=False)
    scenario_type = Column(String(100))
    probability = Column(Float)
    severity = Column(String(50))
    description = Column(Text)
    trigger_points = Column(JSON)
    key_narratives = Column(JSON)
    peak_time_hours = Column(Integer)
    affected_metrics = Column(JSON)

    simulation = relationship("Simulation", back_populates="scenarios")
    playbooks = relationship("Playbook", back_populates="scenario", cascade="all, delete-orphan")


class Playbook(Base):
    __tablename__ = "playbooks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id = Column(UUID(as_uuid=True), ForeignKey("crisis_scenarios.id"), nullable=False)
    playbook_type = Column(String(100))
    strategy_summary = Column(Text)
    response_timeline = Column(JSON)
    key_messages = Column(JSON)
    spokesperson_recommendation = Column(String(255))
    do_not_say = Column(JSON)
    success_metrics = Column(JSON)
    channel_strategy = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    scenario = relationship("CrisisScenario", back_populates="playbooks")


class Monitor(Base):
    __tablename__ = "monitors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    keywords = Column(JSON)
    sentiment_baseline = Column(Float)
    alert_threshold = Column(Float)
    is_active = Column(Boolean, default=True)
    last_check_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="monitors")
    alerts = relationship("MonitorAlert", back_populates="monitor", cascade="all, delete-orphan")


class MonitorAlert(Base):
    __tablename__ = "monitor_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    monitor_id = Column(UUID(as_uuid=True), ForeignKey("monitors.id"), nullable=False)
    alert_type = Column(String(100))
    severity = Column(String(50))
    title = Column(String(255))
    description = Column(Text)
    matched_scenario_id = Column(UUID(as_uuid=True), ForeignKey("crisis_scenarios.id"))
    recommended_action = Column(Text)
    is_acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    monitor = relationship("Monitor", back_populates="alerts")
