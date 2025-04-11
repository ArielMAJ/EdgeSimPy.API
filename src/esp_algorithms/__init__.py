from typing import Callable, Optional

from src.esp_algorithms.smms.algorithm import (
    service_management_multiagent_system_runner,
)
from src.esp_algorithms.thea.algorithm import thea
from src.schemas.algorithm_parameters import AlgorithmInputParameters
from src.utils.enums import SimulationInputAlgorithm

algorithm_options: dict[
    SimulationInputAlgorithm,
    Callable[[Optional[dict | AlgorithmInputParameters]], None],
] = {
    SimulationInputAlgorithm.SMMS: service_management_multiagent_system_runner,
    SimulationInputAlgorithm.THEA: thea,
}
