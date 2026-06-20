"""
simulation_engine.py — The LangGraph-based multi-agent simulation
===================================================================
"""

import uuid
import logging
import time
import json
from typing import Dict, Any, List, TypedDict
from datetime import datetime

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from app.agents.crowd_agents import generate_crowd, TwitterSkeptic
from app.agents.media_agents import generate_media_crowd
from app.agents.base_persona import BasePersona
from app.utils.json_extractor import extract_json_from_text
from app.config import settings

logger = logging.getLogger(__name__)


class SimulationState(TypedDict):
    simulation_id: str
    announcement: str
    industry: str
    parsed_claims: list
    crowd: list
    media: list
    timeline_phase: str
    reactions: list
    sentiment_scores: list
    narratives: list
    crisis_indicators: list
    cascade_detected: bool
    scenarios: list
    iteration: int
    max_iterations: int
    overall_risk_score: float
    sentiment_trajectory: list
    red_flags: list
    overall_sensitivity: float


class SimulationEngine:
    """The main simulation engine using LangGraph."""

    _persona_cache: Dict[str, BasePersona] = {}

    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=2048,
        )
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(SimulationState)

        workflow.add_node("parse_announcement", self._parse_announcement)
        workflow.add_node("generate_crowd", self._generate_crowd_node)
        workflow.add_node("simulate_T0", self._simulate_phase("T0"))
        workflow.add_node("simulate_T1h", self._simulate_phase("T1h"))
        workflow.add_node("simulate_T6h", self._simulate_phase("T6h"))
        workflow.add_node("simulate_T24h", self._simulate_phase("T24h"))
        workflow.add_node("detect_cascades", self._detect_cascades)
        workflow.add_node("generate_scenarios", self._generate_scenarios)
        workflow.add_node("calculate_risk", self._calculate_risk)

        workflow.set_entry_point("parse_announcement")

        workflow.add_edge("parse_announcement", "generate_crowd")
        workflow.add_edge("generate_crowd", "simulate_T0")
        workflow.add_edge("simulate_T0", "simulate_T1h")
        workflow.add_edge("simulate_T1h", "simulate_T6h")
        workflow.add_edge("simulate_T6h", "simulate_T24h")
        workflow.add_edge("simulate_T24h", "detect_cascades")
        workflow.add_edge("detect_cascades", "generate_scenarios")
        workflow.add_edge("generate_scenarios", "calculate_risk")
        workflow.add_edge("calculate_risk", END)

        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)

    async def _parse_announcement(self, state: SimulationState) -> dict:
        logger.info("Parsing announcement...")

        prompt = f"""Analyze this company announcement and extract all claims, promises, and sensitive points.

ANNOUNCEMENT:
---
{state['announcement']}
---

For each claim, assess:
1. The claim itself
2. Sensitivity score (0-1): How likely is this to trigger controversy?
3. Controversy potential: What could go wrong?
4. Fact_checkability: How easy is it to verify this claim? (0-1)

Respond in JSON:
{{
    "claims": [
        {{
            "claim": "The claim text",
            "sensitivity_score": 0.0,
            "controversy_potential": "What could go wrong",
            "fact_checkability": 0.0,
            "trigger_keywords": ["keywords"]
        }}
    ],
    "overall_sensitivity": 0.0,
    "red_flags": ["Major red flags"]
}}"""

        try:
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            parsed = extract_json_from_text(response.content)

            return {
                "parsed_claims": parsed.get("claims", []),
                "overall_sensitivity": parsed.get("overall_sensitivity", 0.5),
                "red_flags": parsed.get("red_flags", []),
            }
        except Exception as e:
            logger.error(f"Parse failed: {e}")
            return {
                "parsed_claims": [],
                "overall_sensitivity": 0.5,
                "red_flags": [],
            }

    async def _generate_crowd_node(self, state: SimulationState) -> dict:
        logger.info("Generating crowd...")

        industry = state.get("industry", "tech")
        crowd_personas = generate_crowd(industry, size=20)
        media_personas = generate_media_crowd(industry)

        crowd_configs = [
            {
                "name": p.name,
                "type": p.PERSONA_TYPE,
                "platform": p.PLATFORM,
                "traits": p.traits,
                "biases": p.biases,
                "followers": p.follower_count,
                "influence": p.influence_score,
            }
            for p in crowd_personas
        ]

        media_configs = [
            {
                "name": p.name,
                "type": p.PERSONA_TYPE,
                "platform": p.PLATFORM,
                "traits": p.traits,
                "biases": p.biases,
                "followers": p.follower_count,
                "influence": p.influence_score,
            }
            for p in media_personas
        ]

        return {
            "crowd": crowd_configs,
            "media": media_configs,
        }

    def _simulate_phase(self, phase: str):
        async def phase_node(state: SimulationState) -> dict:
            logger.info(f"Simulating phase: {phase}")

            crowd = self._recreate_personas(state.get("crowd", []))
            media = self._recreate_personas(state.get("media", []))

            previous_reactions = state.get("reactions", [])
            new_reactions = []

            if phase == "T0":
                for persona in crowd[:10]:
                    reaction = await persona.react_to_announcement(
                        state["announcement"],
                        state.get("parsed_claims", [])
                    )
                    reaction["persona_name"] = persona.name
                    reaction["persona_type"] = persona.PERSONA_TYPE
                    reaction["platform"] = persona.PLATFORM
                    reaction["phase"] = phase
                    new_reactions.append(reaction)

                for persona in media:
                    reaction = await persona.react_to_announcement(
                        state["announcement"],
                        state.get("parsed_claims", [])
                    )
                    reaction["persona_name"] = persona.name
                    reaction["persona_type"] = persona.PERSONA_TYPE
                    reaction["platform"] = persona.PLATFORM
                    reaction["phase"] = phase
                    new_reactions.append(reaction)

            elif phase in ["T1h", "T6h"]:
                for persona in crowd[10:15]:
                    reaction = await persona.react_to_other_reactions(
                        state["announcement"],
                        previous_reactions[-10:]
                    )
                    reaction["persona_name"] = persona.name
                    reaction["persona_type"] = persona.PERSONA_TYPE
                    reaction["platform"] = persona.PLATFORM
                    reaction["phase"] = phase
                    new_reactions.append(reaction)

            elif phase == "T24h":
                for persona in crowd[15:]:
                    reaction = await persona.react_to_other_reactions(
                        state["announcement"],
                        previous_reactions[-15:]
                    )
                    reaction["persona_name"] = persona.name
                    reaction["persona_type"] = persona.PERSONA_TYPE
                    reaction["platform"] = persona.PLATFORM
                    reaction["phase"] = phase
                    new_reactions.append(reaction)

            all_reactions = previous_reactions + new_reactions

            sentiments = [r.get("sentiment", 0) for r in new_reactions]
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0

            sentiment_trajectory = state.get("sentiment_trajectory", [])
            sentiment_trajectory.append({
                "phase": phase,
                "avg_sentiment": avg_sentiment,
                "reaction_count": len(new_reactions),
                "negative_reactions": len([s for s in sentiments if isinstance(s, (int, float)) and s < -3]),
            })

            return {
                "reactions": all_reactions,
                "timeline_phase": phase,
                "sentiment_trajectory": sentiment_trajectory,
                "iteration": state.get("iteration", 0) + 1,
            }

        return phase_node

    async def _detect_cascades(self, state: SimulationState) -> dict:
        logger.info("Detecting cascades...")

        reactions = state.get("reactions", [])
        parsed_claims = state.get("parsed_claims", [])

        prompt = f"""Analyze these social media reactions to detect if a crisis cascade is forming.

ANNOUNCEMENT: {state['announcement'][:500]}

RECENT REACTIONS (last 15):
{json.dumps(reactions[-15:], indent=2, default=str)[:3000]}

KEY CLAIMS WITH SENSITIVITY:
{json.dumps(parsed_claims, indent=2, default=str)[:1000]}

Look for:
1. Outrage cascade: Are negative reactions amplifying each other?
2. Narrative formation: Are people coalescing around a specific negative narrative?
3. Media pickup: Are journalists/analysts amplifying the negativity?
4. Trigger points: Which specific claims are causing the most outrage?
5. Escalation pattern: Is the sentiment getting worse over time?

Respond in JSON:
{{
    "cascade_detected": true,
    "cascade_type": "outrage_cascade",
    "severity": "medium",
    "key_narratives": ["narrative1"],
    "trigger_claims": ["claim1"],
    "amplification_risk": 0.5,
    "peak_prediction_hours": 24,
    "recommended_monitoring": ["monitor1"]
}}"""

        try:
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            cascade_data = extract_json_from_text(response.content)

            return {
                "cascade_detected": cascade_data.get("cascade_detected", False),
                "crisis_indicators": [cascade_data],
                "narratives": cascade_data.get("key_narratives", []),
            }
        except Exception as e:
            logger.error(f"Cascade detection failed: {e}")
            return {
                "cascade_detected": False,
                "crisis_indicators": [],
                "narratives": [],
            }

    async def _generate_scenarios(self, state: SimulationState) -> dict:
        logger.info("Generating crisis scenarios...")

        reactions = state.get("reactions", [])
        narratives = state.get("narratives", [])

        prompt = f"""Based on this crisis simulation, generate 3-5 specific crisis scenarios that could unfold.

SIMULATION SUMMARY:
- Announcement: {state['announcement'][:300]}
- Cascade detected: {state.get('cascade_detected', False)}
- Key narratives: {narratives}
- Sentiment trajectory: {json.dumps(state.get('sentiment_trajectory', []), default=str)}
- Total reactions: {len(reactions)}
- Negative reactions: {len([r for r in reactions if isinstance(r.get('sentiment', 0), (int, float)) and r.get('sentiment', 0) < -3])}

For each scenario, provide:
1. Scenario name and type
2. Probability (0-1)
3. Severity (low/medium/high/critical)
4. Description of how it unfolds
5. Trigger points (what makes it happen)
6. Key narratives that emerge
7. Peak time (hours after announcement)
8. Affected metrics (brand sentiment, stock price, employee morale, etc.)

Respond in JSON:
{{
    "scenarios": [
        {{
            "scenario_name": "Name",
            "scenario_type": "outrage_cascade",
            "probability": 0.5,
            "severity": "medium",
            "description": "How this scenario unfolds",
            "trigger_points": ["trigger1"],
            "key_narratives": ["narrative1"],
            "peak_time_hours": 24,
            "affected_metrics": ["metric1"]
        }}
    ]
}}"""

        try:
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            scenarios_data = extract_json_from_text(response.content)

            return {
                "scenarios": scenarios_data.get("scenarios", []),
            }
        except Exception as e:
            logger.error(f"Scenario generation failed: {e}")
            return {"scenarios": []}

    async def _calculate_risk(self, state: SimulationState) -> dict:
        logger.info("Calculating risk score...")

        scenarios = state.get("scenarios", [])
        sentiment_trajectory = state.get("sentiment_trajectory", [])
        cascade_detected = state.get("cascade_detected", False)

        if not scenarios:
            return {"overall_risk_score": 50.0}

        scenario_risk = 0
        for s in scenarios:
            severity_weight = {"low": 0.2, "medium": 0.4, "high": 0.7, "critical": 1.0}.get(
                s.get("severity", "medium"), 0.4
            )
            probability = s.get("probability", 0.5)
            if isinstance(probability, (int, float)):
                scenario_risk += severity_weight * probability * 100

        scenario_risk = min(100, scenario_risk / max(len(scenarios), 1))

        if sentiment_trajectory:
            sentiments = [s.get("avg_sentiment", 0) for s in sentiment_trajectory]
            numeric_sentiments = [s for s in sentiments if isinstance(s, (int, float))]
            if len(numeric_sentiments) >= 2 and numeric_sentiments[-1] < numeric_sentiments[0]:
                sentiment_decline = (numeric_sentiments[0] - numeric_sentiments[-1]) / 20 * 100
                sentiment_risk = min(100, sentiment_decline)
            else:
                avg = sum(numeric_sentiments) / len(numeric_sentiments) if numeric_sentiments else 0
                sentiment_risk = max(0, 50 - (avg + 10) * 5)
        else:
            sentiment_risk = 50

        cascade_risk = 80 if cascade_detected else 20

        overall_risk = (scenario_risk * 0.5 + sentiment_risk * 0.3 + cascade_risk * 0.2)

        return {
            "overall_risk_score": round(overall_risk, 1),
        }

    def _recreate_personas(self, configs: list) -> List[BasePersona]:
        from app.agents.crowd_agents import (
            TwitterSkeptic, TwitterFanboy, TwitterActivist, TwitterJournalist,
            RedditConspiracist, RedditSnark, RedditExpert,
            TikTokDrama, TikTokLifestyle
        )
        from app.agents.media_agents import (
            TechCrunchJournalist, WallStreetAnalyst, IndustryAnalyst, CompetitorPR
        )

        persona_map = {
            "twitter_skeptic": TwitterSkeptic,
            "twitter_fanboy": TwitterFanboy,
            "twitter_activist": TwitterActivist,
            "twitter_journalist": TwitterJournalist,
            "reddit_conspiracist": RedditConspiracist,
            "reddit_snark": RedditSnark,
            "reddit_expert": RedditExpert,
            "tiktok_drama": TikTokDrama,
            "tiktok_lifestyle": TikTokLifestyle,
            "tech_journalist": TechCrunchJournalist,
            "financial_analyst": WallStreetAnalyst,
            "industry_analyst": IndustryAnalyst,
            "competitor": CompetitorPR,
        }

        personas = []
        for config in configs:
            cache_key = f"{config.get('type')}_{config.get('name')}"
            if cache_key not in self._persona_cache:
                persona_class = persona_map.get(config.get("type"), TwitterSkeptic)
                persona = persona_class(name=config.get("name", "Unknown"))
                self._persona_cache[cache_key] = persona
            personas.append(self._persona_cache[cache_key])

        return personas

    async def run_simulation(
        self,
        simulation_id: str,
        announcement: str,
        industry: str = "tech",
    ) -> Dict[str, Any]:
        logger.info(f"Starting simulation {simulation_id}")
        start_time = time.time()

        initial_state: SimulationState = {
            "simulation_id": simulation_id,
            "announcement": announcement,
            "industry": industry,
            "parsed_claims": [],
            "crowd": [],
            "media": [],
            "timeline_phase": "T0",
            "reactions": [],
            "sentiment_scores": [],
            "narratives": [],
            "crisis_indicators": [],
            "cascade_detected": False,
            "scenarios": [],
            "iteration": 0,
            "max_iterations": 10,
            "overall_risk_score": 0.0,
            "sentiment_trajectory": [],
            "red_flags": [],
            "overall_sensitivity": 0.5,
        }

        config = {"configurable": {"thread_id": simulation_id}}

        try:
            final_state = await self.graph.ainvoke(initial_state, config=config)
            elapsed = int((time.time() - start_time) * 1000)

            return {
                "simulation_id": simulation_id,
                "status": "completed",
                "risk_score": final_state.get("overall_risk_score", 0),
                "scenarios": final_state.get("scenarios", []),
                "sentiment_trajectory": final_state.get("sentiment_trajectory", []),
                "parsed_claims": final_state.get("parsed_claims", []),
                "cascade_detected": final_state.get("cascade_detected", False),
                "narratives": final_state.get("narratives", []),
                "total_reactions": len(final_state.get("reactions", [])),
                "elapsed_ms": elapsed,
                "red_flags": final_state.get("red_flags", []),
            }

        except Exception as e:
            logger.error(f"Simulation failed: {e}", exc_info=True)
            return {
                "simulation_id": simulation_id,
                "status": "failed",
                "error": str(e),
            }
