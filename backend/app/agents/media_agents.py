"""
media_agents.py — Media & analyst agents
==========================================
"""

from app.agents.base_persona import BasePersona
from typing import List


class TechCrunchJournalist(BasePersona):
    PERSONA_TYPE = "tech_journalist"
    PLATFORM = "News Article"

    def __init__(self, name="TechCrunchReporter", **kwargs):
        super().__init__(
            name=name,
            traits={"skepticism": 0.7, "speed": 0.9, "fact_checking": 0.8, "sensationalism": 0.5},
            biases=["pro_innovation", "anti_pr_spin", "pro_startup"],
            follower_count=100000,
            influence_score=9.0,
        )


class WallStreetAnalyst(BasePersona):
    PERSONA_TYPE = "financial_analyst"
    PLATFORM = "Research Note"

    def __init__(self, name="BullishAnalyst", **kwargs):
        super().__init__(
            name=name,
            traits={"financial_focus": 0.95, "skepticism": 0.6, "risk_assessment": 0.8, "hype_resistance": 0.7},
            biases=["pro_shareholder_value", "anti_overvaluation"],
            follower_count=50000,
            influence_score=8.5,
        )


class IndustryAnalyst(BasePersona):
    PERSONA_TYPE = "industry_analyst"
    PLATFORM = "Industry Report"

    def __init__(self, name="GartnerAnalyst", **kwargs):
        super().__init__(
            name=name,
            traits={"expertise": 0.95, "skepticism": 0.8, "trend_analysis": 0.9, "caution": 0.7},
            biases=["pro_market_reality", "anti_hype"],
            follower_count=30000,
            influence_score=8.0,
        )


class CompetitorPR(BasePersona):
    PERSONA_TYPE = "competitor"
    PLATFORM = "Statement"

    def __init__(self, name="CompetitorPR", **kwargs):
        super().__init__(
            name=name,
            traits={"opportunism": 0.9, "subtlety": 0.7, "aggression": 0.5, "brand_protection": 0.9},
            biases=["pro_own_brand", "anti_competitor"],
            follower_count=0,
            influence_score=5.0,
        )


def generate_media_crowd(industry: str) -> List[BasePersona]:
    """Generate media agents for the simulation."""
    return [
        TechCrunchJournalist(name="TechCrunch_Main"),
        TechCrunchJournalist(name="VergeReporter"),
        WallStreetAnalyst(name="GoldmanAnalyst"),
        WallStreetAnalyst(name="MorganStanleyAnalyst"),
        IndustryAnalyst(name="GartnerAnalyst"),
        CompetitorPR(name="Competitor_Alpha"),
        CompetitorPR(name="Competitor_Beta"),
    ]
