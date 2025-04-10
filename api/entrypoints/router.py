from api.entrypoints import simulation
from fastapi.routing import APIRouter

router = APIRouter()
router.include_router(simulation.router, prefix="/simulation", tags=["Simulation"])
