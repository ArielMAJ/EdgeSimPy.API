from api.services.simulation import Simulation
from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def run_simulation():
    Simulation(lambda: None).run()
    return {"status": "ok"}
