import multiprocessing
from random import seed
from typing import Callable

import edge_sim_py as esp
import numpy as np
from api.esp_algorithms.smms.algorithm import (
    service_management_multiagent_system_runner,
)
from loguru import logger


def stopping_criterion(model):
    remaining_services_awaiting_placement_in_an_edge_server: list[esp.Service] = [
        service for service in esp.Service.all() if not service.server
    ]
    return (
        model.schedule.steps == 100
        or not remaining_services_awaiting_placement_in_an_edge_server  # noqa
    )


def run_simulation_in_background():
    simulator = esp.Simulator(
        tick_duration=1,
        tick_unit="seconds",
        stopping_criterion=stopping_criterion,
        resource_management_algorithm=service_management_multiagent_system_runner,
        dump_interval=float("inf"),
    )

    simulator.initialize(
        input_file="https://raw.githubusercontent.com/ArielMAJ/service-management-multiagent-system/refs/heads/main/datasets/sample1.json"  # noqa
    )

    logger.warning("Inside thread logs start")

    for user in esp.User.all():
        logger.info(user)
    for server in esp.EdgeServer.all():
        logger.info(server)
    simulator.run_model()

    for user in esp.User.all():
        logger.info(user)
    for server in esp.EdgeServer.all():
        logger.info(server)
    for service in esp.Service.all():
        logger.info(service.agent)
    logger.warning("Inside thread logs end")


class Simulation:
    def __init__(self, algorithm: Callable[[dict], None]):
        self.algorithm = algorithm

    def run(self):
        logger.info(f">>>>>> [{self.algo_name}] <<<<<<")
        seed_value = 428956419
        seed(seed_value)
        np.random.seed(seed_value)

        simulation_process = multiprocessing.Process(
            target=run_simulation_in_background
        )
        simulation_process.start()
        simulation_process.join()

        simulation_process = multiprocessing.Process(
            target=run_simulation_in_background
        )
        simulation_process.start()
        simulation_process.join()

        logger.warning("Outside thread logs start")
        for user in esp.User.all():
            logger.info(user)
        for server in esp.EdgeServer.all():
            logger.info(server)
        for service in esp.Service.all():
            logger.info(service.agent)
        logger.warning("Outside thread logs end")

    @property
    def algo_name(self):
        return self._algo_name

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        self._algorithm = value
        self._algo_name = value.__name__
