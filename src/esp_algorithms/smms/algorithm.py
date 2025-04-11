from typing import Optional

import edge_sim_py as esp
from loguru import logger

from src.esp_algorithms.smms.constants import LOGGING_IDENTIFIER
from src.esp_algorithms.smms.service_management_agent import ServiceManagementAgent
from src.schemas.algorithm_parameters import AlgorithmInputParameters


def service_management_multiagent_system_runner(
    parameters: Optional[dict | AlgorithmInputParameters] = {},
):
    """
    Service management multi-agent system.
    """
    _validate_simulation_agents_are_set()

    parameters = AlgorithmInputParameters.model_validate(parameters)
    logger.info(f"{LOGGING_IDENTIFIER} [STEP {parameters.current_step}]")

    _let_agents_think()


def _let_agents_think():
    [agent.step() for agent in ServiceManagementAgent.all()]


def _validate_simulation_agents_are_set():
    if hasattr(esp.Simulator, "has_agents_set_up"):
        return

    logger.info(f"{LOGGING_IDENTIFIER} Setting up agents")

    services: list[esp.Service] = esp.Service.all()
    for service in services:
        service.agent = ServiceManagementAgent(service)

    esp.Simulator.has_agents_set_up = True
    logger.info(f"{LOGGING_IDENTIFIER} Agents set up")
