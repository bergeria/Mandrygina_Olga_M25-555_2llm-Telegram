"""
Главный агрегатор API-роутеров.

Объединяет все группы endpoint-ов
в единый APIRouter.
"""

from fastapi import APIRouter

from app.api import routes_auth


router = APIRouter()
router.include_router(routes_auth.router)
