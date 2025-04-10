from api.services.background_test import TestService
from fastapi import APIRouter, BackgroundTasks

router = APIRouter()


@router.get("/test")
async def test_background_task(background_task: BackgroundTasks):
    await TestService().test_background(background_task)
    return {"status": "ok"}
