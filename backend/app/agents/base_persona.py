"""
base_persona.py — Base class for all simulated personas
=========================================================
"""

import json
import logging
from typing import Dict, Any, List

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import settings
from app.utils.json_extractor import extract_json_from_text

logger = logging.getLogger(__name__)


class BasePersona:
    """Base class for all simulated social media personas."""

    PERSONA_TYPE: str = "generic"
    PLATFORM: str = "generic"

    def __init__(
        self,
        name: str,
        traits: Dict[str, float],
        biases: List[str],
        follower_count: int = 0,
        influence_score: float = 0.0,
    ):
        self.name = name
        self.traits = traits
        self.biases = biases
        self.follower_count = follower_count
        self.influence_score = influence_score

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=500,
        )

    def get_system_prompt(self) -> str:
        traits_str = ", ".join([f"{k}: {v}" for k, v in self.traits.items()])
        biases_str = ", ".join(self.biases) if self.biases else "none"

        return f"""You are simulating a {self.PLATFORM} user named "{self.name}".

YOUR PERSONALITY:
- Type: {self.PERSONA_TYPE}
- Traits: {traits_str}
- Biases: {biases_str}
- Followers: {self.follower_count}
- Influence: {self.influence_score}/10

YOUR BEHAVIOR:
- You react to company announcements based on your personality and biases
- You write in the style typical of {self.PLATFORM}
- Your reaction should be authentic to your character
- If something triggers your biases, you react strongly
- You may amplify or dismiss information based on your traits

RESPOND IN CHARACTER. Be realistic, emotional, and authentic."""

    async def react_to_announcement(self, announcement: str, claims: List[Dict]) -> Dict[str, Any]:
        """Generate this persona's reaction to an announcement."""
        user_prompt = f"""A company just made this announcement:

---
{announcement}
---

KEY CLAIMS IN THE ANNOUNCEMENT:
{self._format_claims(claims)}

How do YOU react? Write your response as a {self.PLATFORM} post/comment.

Include:
1. Your immediate reaction (the post/comment itself)
2. Your sentiment score (-10 to +10, where -10 is furious, +10 is ecstatic)
3. Whether you would share/amplify this (yes/no/maybe)
4. What narrative you would push (if any)
5. How likely you are to engage in follow-up arguments (0-1)

Respond in JSON:
{{
    "reaction_text": "Your actual post/comment",
    "sentiment": 0,
    "would_amplify": "yes/no/maybe",
    "narrative_pushed": "What narrative you'd push, or null",
    "follow_up_engagement": 0.5,
    "trigger_points": ["What specifically triggered you"],
    "tags_or_mentions": ["Who you'd tag or mention"]
}}"""

        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=self.get_system_prompt()),
                HumanMessage(content=user_prompt)
            ])
            result = extract_json_from_text(response.content)
            if not result:
                result = {
                    "reaction_text": response.content[:500],
                    "sentiment": 0,
                    "would_amplify": "maybe",
                }
            return result
        except Exception as e:
            logger.error(f"Persona {self.name} reaction failed: {e}")
            return {
                "reaction_text": f"[Simulation error]",
                "sentiment": 0,
                "would_amplify": "maybe",
                "narrative_pushed": None,
                "follow_up_engagement": 0.0,
                "trigger_points": [],
                "tags_or_mentions": [],
            }

    async def react_to_other_reactions(self, announcement: str, other_reactions: List[Dict]) -> Dict[str, Any]:
        """React to how others are reacting (cascade simulation)."""
        reactions_summary = "\n".join([
            f"- @{r.get('persona_name', 'unknown')}: \"{str(r.get('reaction_text', ''))[:100]}\" (sentiment: {r.get('sentiment', 0)})"
            for r in other_reactions[-10:]
        ]) or "No reactions yet."

        user_prompt = f"""Original announcement:
---
{announcement[:500]}
---

Here's how others are reacting:
{reactions_summary}

How do YOU react now, seeing how others are responding?
Do you join in? Push back? Amplify? Ignore?

Respond in JSON:
{{
    "reaction_text": "Your response",
    "sentiment": 0,
    "would_amplify": "yes/no/maybe",
    "responding_to": "Which reaction(s) you're responding to",
    "escalation_level": 0.5
}}"""

        try:
            response = await self.llm.ainvoke([
                SystemMessage(content=self.get_system_prompt()),
                HumanMessage(content=user_prompt)
            ])
            result = extract_json_from_text(response.content)
            if not result:
                result = {
                    "reaction_text": response.content[:500],
                    "sentiment": 0,
                    "would_amplify": "maybe",
                }
            return result
        except Exception as e:
            logger.error(f"Persona {self.name} cascade reaction failed: {e}")
            return {
                "reaction_text": "[Error]",
                "sentiment": 0,
                "would_amplify": "maybe",
                "escalation_level": 0.0,
            }

    def _format_claims(self, claims: List[Dict]) -> str:
        if not claims:
            return "No claims parsed."
        lines = []
        for c in claims:
            sensitivity = c.get("sensitivity_score", 0)
            sens_label = "HIGH" if sensitivity > 0.7 else "MEDIUM" if sensitivity > 0.4 else "LOW"
            lines.append(f"- \"{c.get('claim', '')}\" [{sens_label} sensitivity]")
        return "\n".join(lines)
