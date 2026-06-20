"""
simulations.py — API endpoints for crisis simulations
=======================================================
"""

import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import select, update

from app.database import get_db, async_session
from app.models import Simulation, CrisisScenario, Playbook, Organization
from app.core.simulation_engine import SimulationEngine
from app.core.playbook_engine import PlaybookEngine

logger = logging.getLogger(__name__)
router = APIRouter()

simulation_engine = SimulationEngine()
playbook_engine = PlaybookEngine()


class SimulationCreate(BaseModel):
    organization_id: str
    title: str
    announcement_text: str
    industry_context: str = ""


@router.post("/simulations")
async def create_simulation(
    request: SimulationCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    org_result = await db.execute(
        select(Organization).where(Organization.id == uuid.UUID(request.organization_id))
    )
    org = org_result.scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    sim_id = uuid.uuid4()
    simulation = Simulation(
        id=sim_id,
        organization_id=uuid.UUID(request.organization_id),
        title=request.title,
        announcement_text=request.announcement_text,
        industry_context=request.industry_context,
        status="running",
    )
    db.add(simulation)
    await db.commit()

    background_tasks.add_task(
        run_simulation_task,
        str(sim_id),
        request.announcement_text,
        org.industry,
        org.name,
        org.brand_voice or "",
    )

    return {
        "id": str(sim_id),
        "title": request.title,
        "status": "running",
        "message": "Simulation started. Check back in 2-3 minutes for results.",
    }


async def run_simulation_task(
    sim_id: str,
    announcement: str,
    industry: str,
    org_name: str,
    brand_voice: str,
):
    async with async_session() as db:
        try:
            result = await simulation_engine.run_simulation(
                simulation_id=sim_id,
                announcement=announcement,
                industry=industry,
            )

            if result.get("status") == "failed":
                await db.execute(
                    update(Simulation)
                    .where(Simulation.id == uuid.UUID(sim_id))
                    .values(status="failed")
                )
                await db.commit()
                return

            await db.execute(
                update(Simulation)
                .where(Simulation.id == uuid.UUID(sim_id))
                .values(
                    status="completed",
                    risk_score=result.get("risk_score", 0),
                    parsed_claims=result.get("parsed_claims", []),
                    crisis_scenarios=result.get("scenarios", []),
                    sentiment_trajectory=result.get("sentiment_trajectory", []),
                    agent_count=result.get("total_reactions", 0),
                    completed_at=datetime.utcnow(),
                )
            )

            for scenario_data in result.get("scenarios", []):
                scenario = CrisisScenario(
                    id=uuid.uuid4(),
                    simulation_id=uuid.UUID(sim_id),
                    scenario_name=scenario_data.get("scenario_name", "Unknown"),
                    scenario_type=scenario_data.get("scenario_type", "unknown"),
                    probability=scenario_data.get("probability", 0.5),
                    severity=scenario_data.get("severity", "medium"),
                    description=scenario_data.get("description", ""),
                    trigger_points=scenario_data.get("trigger_points", []),
                    key_narratives=scenario_data.get("key_narratives", []),
                    peak_time_hours=scenario_data.get("peak_time_hours", 24),
                    affected_metrics=scenario_data.get("affected_metrics", []),
                )
                db.add(scenario)
                await db.flush()

                playbook_data = await playbook_engine.generate_playbook(
                    announcement=announcement,
                    scenario=scenario_data,
                    organization_name=org_name,
                    industry=industry,
                    brand_voice=brand_voice,
                )

                playbook = Playbook(
                    id=uuid.uuid4(),
                    scenario_id=scenario.id,
                    playbook_type=playbook_data.get("playbook_type", "reactive"),
                    strategy_summary=playbook_data.get("strategy_summary", ""),
                    response_timeline=playbook_data.get("response_timeline", []),
                    key_messages=playbook_data.get("key_messages", []),
                    spokesperson_recommendation=playbook_data.get("spokesperson_recommendation", ""),
                    do_not_say=playbook_data.get("do_not_say", []),
                    channel_strategy=playbook_data.get("channel_strategy", {}),
                    success_metrics=playbook_data.get("success_metrics", []),
                )
                db.add(playbook)

            await db.commit()

        except Exception as e:
            logger.error(f"Simulation task failed: {e}", exc_info=True)
            await db.execute(
                update(Simulation)
                .where(Simulation.id == uuid.UUID(sim_id))
                .values(status="failed")
            )
            await db.commit()


@router.get("/simulations/{sim_id}")
async def get_simulation(sim_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Simulation).where(Simulation.id == uuid.UUID(sim_id))
    )
    sim = result.scalar_one_or_none()
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")

    scenarios_result = await db.execute(
        select(CrisisScenario).where(CrisisScenario.simulation_id == uuid.UUID(sim_id))
    )
    scenarios = scenarios_result.scalars().all()

    scenarios_with_playbooks = []
    for scenario in scenarios:
        playbooks_result = await db.execute(
            select(Playbook).where(Playbook.scenario_id == scenario.id)
        )
        playbooks = playbooks_result.scalars().all()

        scenarios_with_playbooks.append({
            "id": str(scenario.id),
            "scenario_name": scenario.scenario_name,
            "scenario_type": scenario.scenario_type,
            "probability": scenario.probability,
            "severity": scenario.severity,
            "description": scenario.description,
            "trigger_points": scenario.trigger_points,
            "key_narratives": scenario.key_narratives,
            "peak_time_hours": scenario.peak_time_hours,
            "playbooks": [
                {
                    "strategy_summary": p.strategy_summary,
                    "response_timeline": p.response_timeline,
                    "key_messages": p.key_messages,
                    "spokesperson_recommendation": p.spokesperson_recommendation,
                    "do_not_say": p.do_not_say,
                    "success_metrics": p.success_metrics,
                }
                for p in playbooks
            ],
        })

    return {
        "id": str(sim.id),
        "title": sim.title,
        "status": sim.status,
        "risk_score": sim.risk_score,
        "parsed_claims": sim.parsed_claims,
        "sentiment_trajectory": sim.sentiment_trajectory,
        "scenarios": scenarios_with_playbooks,
        "agent_count": sim.agent_count,
        "created_at": sim.created_at.isoformat() if sim.created_at else None,
        "completed_at": sim.completed_at.isoformat() if sim.completed_at else None,
    }


@router.get("/simulations")
async def list_simulations(
    organization_id: str = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    query = select(Simulation).order_by(Simulation.created_at.desc()).limit(limit)
    if organization_id:
        query = query.where(Simulation.organization_id == uuid.UUID(organization_id))

    result = await db.execute(query)
    sims = result.scalars().all()

    return [
        {
            "id": str(s.id),
            "title": s.title,
            "status": s.status,
            "risk_score": s.risk_score,
            "created_at": s.created_at.isoformat() if s.created_at else None,
        }
        for s in sims
    ]
