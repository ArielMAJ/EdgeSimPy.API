from fastapi import APIRouter
from pydantic import HttpUrl

from src.esp_algorithms import algorithm_options
from src.schemas.simulation_schema import SimulationInput, SimulationServiceOutput
from src.services.simulation_service import SimulationService

router = APIRouter()


@router.post("/services", response_model=SimulationServiceOutput | None)
async def simulation_entrypoint(
    simulation_input: SimulationInput,
) -> SimulationServiceOutput | None:
    """
    Endpoint/controller to run the simulation.
    """
    input_file = simulation_input.url_or_json
    if isinstance(input_file, HttpUrl):
        input_file = str(input_file)
    return {
        "Service": await SimulationService.run(
            algorithm=algorithm_options[simulation_input.algorithm],
            input_file=input_file,
            metrics_from="Service",
        )
    }
