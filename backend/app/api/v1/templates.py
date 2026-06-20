"""templates.py — Template endpoints"""

from fastapi import APIRouter
from app.templates.industry_profiles import INDUSTRY_PROFILES
from app.templates.persona_library import PERSONA_LIBRARY

router = APIRouter()


@router.get("/templates/industries")
async def get_industries():
    return INDUSTRY_PROFILES


@router.get("/templates/personas")
async def get_personas():
    return PERSONA_LIBRARY
