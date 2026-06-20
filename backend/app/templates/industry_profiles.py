"""Industry profiles for crisis simulation templates."""

INDUSTRY_PROFILES = {
    "tech": {
        "name": "Technology",
        "common_crises": ["data_breach", "AI_ethics", "layoffs", "founder_scandal", "product_failure"],
        "stakeholders": ["users", "investors", "regulators", "employees", "media"],
        "typical_sentiment_baseline": 0.2,
        "risk_multipliers": ["AI_controversy", "privacy_concerns", "monopoly_fears"],
    },
    "fintech": {
        "name": "Fintech",
        "common_crises": ["fraud", "regulatory_action", "data_breach", "outage", "fund_mismanagement"],
        "stakeholders": ["customers", "regulators", "investors", "partners", "media"],
        "typical_sentiment_baseline": 0.0,
        "risk_multipliers": ["financial_loss", "regulatory_scrutiny", "trust_erosion"],
    },
    "food": {
        "name": "Food & Beverage",
        "common_crises": ["contamination", "allergy_incident", "false_advertising", "labor_practices"],
        "stakeholders": ["customers", "health_regulators", "suppliers", "media"],
        "typical_sentiment_baseline": 0.1,
        "risk_multipliers": ["health_safety", "brand_loyalty", "viral_negative_content"],
    },
    "healthcare": {
        "name": "Healthcare",
        "common_crises": ["data_breach", "patient_harm", "pricing_scandal", "regulatory_violation"],
        "stakeholders": ["patients", "regulators", "insurers", "media", "employees"],
        "typical_sentiment_baseline": -0.1,
        "risk_multipliers": ["patient_safety", "privacy", "affordability"],
    },
    "retail": {
        "name": "Retail",
        "common_crises": ["product_recall", "labor_scandal", "data_breach", "boycott"],
        "stakeholders": ["customers", "employees", "suppliers", "media"],
        "typical_sentiment_baseline": 0.1,
        "risk_multipliers": ["consumer_activism", "labor_issues", "supply_chain"],
    },
    "media": {
        "name": "Media & Entertainment",
        "common_crises": ["talent_scandal", "cancellation", "bias_accusation", "copyright"],
        "stakeholders": ["audience", "advertisers", "talent", "regulators"],
        "typical_sentiment_baseline": 0.0,
        "risk_multipliers": ["culture_war", "talent_behavior", "platform_policies"],
    },
    "education": {
        "name": "Education",
        "common_crises": ["data_breach", "safety_incident", "curriculum_controversy", "fraud"],
        "stakeholders": ["students", "parents", "regulators", "media"],
        "typical_sentiment_baseline": 0.1,
        "risk_multipliers": ["child_safety", "academic_integrity", "accessibility"],
    },
    "other": {
        "name": "Other",
        "common_crises": ["generic_crisis"],
        "stakeholders": ["customers", "media", "regulators"],
        "typical_sentiment_baseline": 0.0,
        "risk_multipliers": [],
    },
}
