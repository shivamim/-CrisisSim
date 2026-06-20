"""playbooks.py — Playbook endpoints"""

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import Playbook

router = APIRouter()


@router.get("/playbooks/{scenario_id}")
async def get_playbooks(scenario_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Playbook).where(Playbook.scenario_id == uuid.UUID(scenario_id))
    )
    playbooks = result.scalars().all()

    if not playbooks:
        raise HTTPException(status_code=404, detail="No playbooks found for this scenario")

    return [
        {
            "id": str(p.id),
            "playbook_type": p.playbook_type,
            "strategy_summary": p.strategy_summary,
            "response_timeline": p.response_timeline,
            "key_messages": p.key_messages,
            "spokesperson_recommendation": p.spokesperson_recommendation,
            "do_not_say": p.do_not_say,
            "success_metrics": p.success_metrics,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in playbooks
    ]
