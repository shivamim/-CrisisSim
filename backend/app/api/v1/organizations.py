"""organizations.py — Organization CRUD endpoints"""

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.models import Organization

router = APIRouter()


class OrganizationCreate(BaseModel):
    name: str
    industry: str
    brand_voice: str = ""


@router.post("/organizations")
async def create_organization(request: OrganizationCreate, db: AsyncSession = Depends(get_db)):
    org = Organization(
        id=uuid.uuid4(),
        name=request.name,
        industry=request.industry,
        brand_voice=request.brand_voice,
    )
    db.add(org)
    await db.commit()
    return {
        "id": str(org.id),
        "name": org.name,
        "industry": org.industry,
        "brand_voice": org.brand_voice or "",
    }


@router.get("/organizations")
async def list_organizations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Organization).order_by(Organization.created_at.desc()))
    orgs = result.scalars().all()
    return [
        {
            "id": str(o.id),
            "name": o.name,
            "industry": o.industry,
            "brand_voice": o.brand_voice or "",
            "created_at": o.created_at.isoformat() if o.created_at else None,
        }
        for o in orgs
    ]


@router.get("/organizations/{org_id}")
async def get_organization(org_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Organization).where(Organization.id == uuid.UUID(org_id))
    )
    org = result.scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return {
        "id": str(org.id),
        "name": org.name,
        "industry": org.industry,
        "brand_voice": org.brand_voice or "",
        "created_at": org.created_at.isoformat() if org.created_at else None,
    }
