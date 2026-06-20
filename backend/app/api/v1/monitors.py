"""monitors.py — Monitor CRUD endpoints"""

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List

from app.database import get_db
from app.models import Monitor, MonitorAlert

router = APIRouter()


class MonitorCreate(BaseModel):
    organization_id: str
    name: str
    keywords: List[str] = []
    sentiment_baseline: float = 0.0
    alert_threshold: float = -5.0


@router.post("/monitors")
async def create_monitor(request: MonitorCreate, db: AsyncSession = Depends(get_db)):
    monitor = Monitor(
        id=uuid.uuid4(),
        organization_id=uuid.UUID(request.organization_id),
        name=request.name,
        keywords=request.keywords,
        sentiment_baseline=request.sentiment_baseline,
        alert_threshold=request.alert_threshold,
    )
    db.add(monitor)
    await db.commit()
    return {
        "id": str(monitor.id),
        "name": monitor.name,
        "is_active": monitor.is_active,
    }


@router.get("/monitors")
async def list_monitors(organization_id: str = None, db: AsyncSession = Depends(get_db)):
    query = select(Monitor).order_by(Monitor.created_at.desc())
    if organization_id:
        query = query.where(Monitor.organization_id == uuid.UUID(organization_id))
    result = await db.execute(query)
    monitors = result.scalars().all()
    return [
        {
            "id": str(m.id),
            "name": m.name,
            "is_active": m.is_active,
            "keywords": m.keywords,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in monitors
    ]


@router.get("/monitors/{monitor_id}/alerts")
async def get_monitor_alerts(monitor_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MonitorAlert)
        .where(MonitorAlert.monitor_id == uuid.UUID(monitor_id))
        .order_by(MonitorAlert.created_at.desc())
    )
    alerts = result.scalars().all()
    return [
        {
            "id": str(a.id),
            "alert_type": a.alert_type,
            "severity": a.severity,
            "title": a.title,
            "description": a.description,
            "is_acknowledged": a.is_acknowledged,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in alerts
    ]
