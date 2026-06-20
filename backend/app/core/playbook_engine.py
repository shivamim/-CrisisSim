"""
playbook_engine.py — Generates response playbooks for each scenario
=====================================================================
"""

import logging
from typing import Dict, Any, List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from app.utils.json_extractor import extract_json_from_text

logger = logging.getLogger(__name__)


class PlaybookEngine:
    """Generates actionable response playbooks for crisis scenarios."""

    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=3000,
        )

    async def generate_playbook(
        self,
        announcement: str,
        scenario: Dict[str, Any],
        organization_name: str,
        industry: str,
        brand_voice: str = "",
    ) -> Dict[str, Any]:
        prompt = f"""You are a world-class crisis PR strategist. Generate a detailed response playbook for this crisis scenario.

COMPANY: {organization_name}
INDUSTRY: {industry}
BRAND VOICE: {brand_voice or "Professional, transparent, empathetic"}

ORIGINAL ANNOUNCEMENT:
---
{announcement[:1000]}
---

CRISIS SCENARIO:
- Name: {scenario.get('scenario_name', 'Unknown')}
- Type: {scenario.get('scenario_type', 'Unknown')}
- Severity: {scenario.get('severity', 'Unknown')}
- Description: {scenario.get('description', 'N/A')}
- Trigger Points: {scenario.get('trigger_points', [])}
- Key Narratives: {scenario.get('key_narratives', [])}
- Peak Time: {scenario.get('peak_time_hours', 'N/A')} hours after announcement

GENERATE A COMPLETE PLAYBOOK WITH:

1. STRATEGY SUMMARY (2-3 sentences): The overall approach

2. RESPONSE TIMELINE: Exact actions at each time point
   - T+0 (Immediate, first 30 minutes)
   - T+1h (First hour)
   - T+6h (First 6 hours)
   - T+24h (First day)
   - T+72h (First 3 days)

3. KEY MESSAGES: 3-5 core messages to communicate

4. SPOKESPERSON RECOMMENDATION: Who should speak and why

5. DO NOT SAY: Specific phrases/frames to avoid

6. CHANNEL STRATEGY: Which channels to use for what

7. SUCCESS METRICS: How to measure if the response is working

Respond in JSON:
{{
    "strategy_summary": "Overall approach",
    "response_timeline": [
        {{
            "time": "T+0 (0-30 min)",
            "actions": ["Action 1", "Action 2"],
            "channels": ["Twitter", "Internal"],
            "sample_message": "Example of what to say",
            "spokesperson": "CEO / PR Team / etc."
        }}
    ],
    "key_messages": ["Message 1", "Message 2"],
    "spokesperson_recommendation": "Who and why",
    "do_not_say": ["Phrase to avoid 1"],
    "channel_strategy": {{
        "twitter": "What to do on Twitter",
        "internal": "What to communicate internally",
        "media": "How to handle media inquiries"
    }},
    "success_metrics": ["Metric 1"]
}}"""

        try:
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            playbook = extract_json_from_text(response.content)

            return {
                "playbook_type": "reactive",
                "strategy_summary": playbook.get("strategy_summary", ""),
                "response_timeline": playbook.get("response_timeline", []),
                "key_messages": playbook.get("key_messages", []),
                "spokesperson_recommendation": playbook.get("spokesperson_recommendation", ""),
                "do_not_say": playbook.get("do_not_say", []),
                "channel_strategy": playbook.get("channel_strategy", {}),
                "success_metrics": playbook.get("success_metrics", []),
            }
        except Exception as e:
            logger.error(f"Playbook generation failed: {e}")
            return {
                "playbook_type": "reactive",
                "strategy_summary": f"Playbook generation failed. Manual intervention required.",
                "response_timeline": [],
                "key_messages": [],
                "spokesperson_recommendation": "",
                "do_not_say": [],
                "channel_strategy": {},
                "success_metrics": [],
            }

    async def generate_playbooks_for_all_scenarios(
        self,
        announcement: str,
        scenarios: List[Dict[str, Any]],
        organization_name: str,
        industry: str,
        brand_voice: str = "",
    ) -> List[Dict[str, Any]]:
        playbooks = []
        for scenario in scenarios:
            playbook = await self.generate_playbook(
                announcement=announcement,
                scenario=scenario,
                organization_name=organization_name,
                industry=industry,
                brand_voice=brand_voice,
            )
            playbook["scenario_name"] = scenario.get("scenario_name", "Unknown")
            playbook["scenario_type"] = scenario.get("scenario_type", "Unknown")
            playbooks.append(playbook)
        return playbooks
