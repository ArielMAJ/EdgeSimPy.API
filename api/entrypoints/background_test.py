from api.services.background_test import TestService
from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
async def test_background_task():
    TestService().test_background()
    return {"status": "ok"}
