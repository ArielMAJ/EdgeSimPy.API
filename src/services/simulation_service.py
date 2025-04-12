import uuid
from concurrent.futures import ProcessPoolExecutor
from random import seed
from typing import Callable, Optional

import edge_sim_py as esp
import numpy as np
from fastapi_cache.decorator import cache
from loguru import logger

from src.config.loguru import logger_config
from src.exceptions.http_exceptions import AlgorithmException
from src.middleware.logger_middleware import REQUEST_UUID
from src.schemas.algorithm_parameters import AlgorithmInputParameters
from src.schemas.simulation_schema import SimulationServiceOutput
from src.utils.enums import SimulationResultOptions


class SimulationService:
    @staticmethod
    @cache(expire=60 * 5)
    async def run(
        algorithm: Callable[[Optional[dict | AlgorithmInputParameters]], None],
        input_file: str | dict,
        metrics_from: SimulationResultOptions,
    ) -> SimulationServiceOutput | None:
        logger.info(f">>>>>> [{algorithm.__name__}] <<<<<<")
        seed_value = 428956419
        seed(seed_value)
        np.random.seed(seed_value)
        logger.warning("Starting simulation process")

        try:
            with ProcessPoolExecutor() as executor:
                future = executor.submit(
                    SimulationService._run_and_process_simulation_in_the_background,
                    input_file,
                    algorithm,
                    REQUEST_UUID.get(),
                    metrics_from,
                )
                logger.warning("Waiting for simulation process to finish")
                results = future.result()
        except Exception:
            logger.error(
                f"There was an error in the simulation process for {algorithm.__name__}"
            )
            raise AlgorithmException(algorithm.__name__)

        logger.warning(f"Simulation results: {type(results)}")
        return results

    @staticmethod
    def stopping_criterion(model):
        remaining_services_awaiting_placement_in_an_edge_server: list[esp.Service] = [
            service for service in esp.Service.all() if not service.server
        ]
        return (
            model.schedule.steps == 100
            or not remaining_services_awaiting_placement_in_an_edge_server  # noqa
        )

    @staticmethod
    def _run_and_process_simulation_in_the_background(
        input_file: str | dict,
        algorithm: Callable[[Optional[dict | AlgorithmInputParameters]], None],
        request_uuid: uuid.UUID | None = None,
        metrics_from: SimulationResultOptions = SimulationResultOptions.SERVICE,
    ) -> SimulationServiceOutput:
        REQUEST_UUID.set(request_uuid)
        logger.configure(**logger_config())
        logger.warning("Start logs inside new proccess.")

        agent_metrics: dict = SimulationService._run_simulation_in_background(
            input_file, algorithm
        )

        # queue.put(simulator.agent_metrics[metrics_from])
        logger.warning("End logs inside new proccess.")
        return agent_metrics[metrics_from]

    @staticmethod
    def _run_simulation_in_background(
        input_file: str | dict,
        algorithm: Callable[[Optional[dict | AlgorithmInputParameters]], None],
    ) -> dict:
        simulator: esp.Simulator = esp.Simulator(
            tick_duration=1,
            tick_unit="seconds",
            stopping_criterion=SimulationService.stopping_criterion,
            resource_management_algorithm=algorithm,
            dump_interval=float("inf"),
        )

        simulator.initialize(input_file=input_file)

        simulator.run_model()
        return simulator.agent_metrics
