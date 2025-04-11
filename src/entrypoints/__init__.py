from fastapi.routing import APIRouter

from src.entrypoints import simulation_entrypoint

router = APIRouter()
router.include_router(
    simulation_entrypoint.router, prefix="/simulation", tags=["Simulation"]
)

__all__ = ["router"]
