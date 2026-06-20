"""
crowd_agents.py — The "crowd" agents (Twitter, Reddit, TikTok users)
======================================================================
"""

from app.agents.base_persona import BasePersona
from typing import List


class TwitterSkeptic(BasePersona):
    PERSONA_TYPE = "twitter_skeptic"
    PLATFORM = "Twitter/X"

    def __init__(self, name="SkepticalTechBro", followers=15000, **kwargs):
        super().__init__(
            name=name,
            traits={"skepticism": 0.9, "outrage_prone": 0.6, "snark": 0.8, "nuance": 0.3},
            biases=["anti_corporate", "anti_hype", "pro_transparency"],
            follower_count=followers,
            influence_score=6.0,
        )


class TwitterFanboy(BasePersona):
    PERSONA_TYPE = "twitter_fanboy"
    PLATFORM = "Twitter/X"

    def __init__(self, name="HypeTrainConductor", followers=8000, **kwargs):
        super().__init__(
            name=name,
            traits={"enthusiasm": 0.9, "skepticism": 0.1, "outrage_prone": 0.2, "loyalty": 0.8},
            biases=["pro_innovation", "brand_loyal"],
            follower_count=followers,
            influence_score=4.0,
        )


class TwitterActivist(BasePersona):
    PERSONA_TYPE = "twitter_activist"
    PLATFORM = "Twitter/X"

    def __init__(self, name="SocialJusticeWarrior", followers=25000, **kwargs):
        super().__init__(
            name=name,
            traits={"outrage_prone": 0.95, "moral_certainty": 0.9, "amplification": 0.9, "nuance": 0.1},
            biases=["social_justice", "anti_corporate", "pro_accountability"],
            follower_count=followers,
            influence_score=7.5,
        )


class TwitterJournalist(BasePersona):
    PERSONA_TYPE = "twitter_journalist"
    PLATFORM = "Twitter/X"

    def __init__(self, name="TechReporter", followers=50000, **kwargs):
        super().__init__(
            name=name,
            traits={"skepticism": 0.7, "fact_checking": 0.9, "speed": 0.8, "sensationalism": 0.4},
            biases=["pro_truth", "anti_pr_spin"],
            follower_count=followers,
            influence_score=8.5,
        )


class RedditConspiracist(BasePersona):
    PERSONA_TYPE = "reddit_conspiracist"
    PLATFORM = "Reddit"

    def __init__(self, name="DeepDiveDetector", followers=5000, **kwargs):
        super().__init__(
            name=name,
            traits={"skepticism": 0.95, "conspiracy_minded": 0.8, "research_depth": 0.7, "outrage": 0.6},
            biases=["anti_corporate", "anti_mainstream", "pro_transparency"],
            follower_count=followers,
            influence_score=5.0,
        )


class RedditSnark(BasePersona):
    PERSONA_TYPE = "reddit_snark"
    PLATFORM = "Reddit"

    def __init__(self, name="ShitposterSupreme", followers=2000, **kwargs):
        super().__init__(
            name=name,
            traits={"humor": 0.95, "snark": 0.95, "outrage_prone": 0.3, "creativity": 0.8},
            biases=["anti_authority", "pro_memes"],
            follower_count=followers,
            influence_score=3.5,
        )


class RedditExpert(BasePersona):
    PERSONA_TYPE = "reddit_expert"
    PLATFORM = "Reddit"

    def __init__(self, name="ActuallyAnExpert", followers=12000, **kwargs):
        super().__init__(
            name=name,
            traits={"expertise": 0.9, "pedantry": 0.8, "skepticism": 0.7, "helpfulness": 0.6},
            biases=["pro_accuracy", "anti_hype"],
            follower_count=followers,
            influence_score=6.5,
        )


class TikTokDrama(BasePersona):
    PERSONA_TYPE = "tiktok_drama"
    PLATFORM = "TikTok"

    def __init__(self, name="DramaAlertCreator", followers=500000, **kwargs):
        super().__init__(
            name=name,
            traits={"sensationalism": 0.95, "speed": 0.9, "emotional_intensity": 0.9, "nuance": 0.05},
            biases=["pro_drama", "anti_corporate", "pro_entertainment"],
            follower_count=followers,
            influence_score=9.0,
        )


class TikTokLifestyle(BasePersona):
    PERSONA_TYPE = "tiktok_lifestyle"
    PLATFORM = "TikTok"

    def __init__(self, name="AestheticInfluencer", followers=200000, **kwargs):
        super().__init__(
            name=name,
            traits={"brand_sensitivity": 0.8, "aesthetic_focus": 0.9, "outrage_prone": 0.5, "loyalty": 0.6},
            biases=["pro_aesthetics", "brand_conscious"],
            follower_count=followers,
            influence_score=7.0,
        )


def generate_crowd(industry: str, size: int = 20) -> List[BasePersona]:
    """Generate a crowd of agents appropriate for the industry."""
    crowd_templates = [
        (TwitterSkeptic, 3),
        (TwitterFanboy, 2),
        (TwitterActivist, 2),
        (TwitterJournalist, 1),
        (RedditConspiracist, 3),
        (RedditSnark, 3),
        (RedditExpert, 2),
        (TikTokDrama, 2),
        (TikTokLifestyle, 2),
    ]

    crowd = []
    for persona_class, count in crowd_templates:
        for i in range(count):
            name_suffix = f"_{i+1}" if i > 0 else ""
            persona = persona_class(name=f"{persona_class.PERSONA_TYPE}{name_suffix}")
            crowd.append(persona)

    return crowd[:size]
