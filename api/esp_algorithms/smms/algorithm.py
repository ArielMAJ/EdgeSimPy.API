import edge_sim_py as esp
from api.esp_algorithms.smms.service_management_agent import ServiceManagementAgent
from api.schemas.algorith_parameters import AlgorithmInputParameters
from loguru import logger


def service_management_multiagent_system_runner(parameters: AlgorithmInputParameters):
    """ """
    _validate_simulation_agents_are_set()

    parameters = AlgorithmInputParameters.model_validate(parameters)
    logger.info(f"[SMMS] [STEP {parameters.current_step}]")

    _let_agents_think()


def _let_agents_think():
    [agent.step() for agent in ServiceManagementAgent.all()]


def _validate_simulation_agents_are_set():
    if hasattr(esp.Simulator, "has_agents_set_up"):
        return

    logger.info("[SMMS] Setting up agents")

    services: list[esp.Service] = esp.Service.all()
    for service in services:
        service.agent = ServiceManagementAgent(service)

    esp.Simulator.has_agents_set_up = True
