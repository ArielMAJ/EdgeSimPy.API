import multiprocessing
import uuid
from random import seed
from typing import Callable, Optional

import edge_sim_py as esp
import numpy as np
from fastapi_cache.decorator import cache
from loguru import logger

from src.configs.loguru import logger_config
from src.exceptions.http_exceptions import AlgorithmException
from src.middleware.logger_middleware import REQUEST_UUID
from src.schemas.algorithm_parameters import AlgorithmInputParameters
from src.schemas.simulation_schema import SimulationServiceOutput
from src.services.logging_service import LoggingService
from src.utils.enums import SimulationResultOptions


class SimulationService:
    @staticmethod
    @cache(expire=60 * 5)
    async def run(
        algorithm: Callable[[Optional[dict | AlgorithmInputParameters]], None],
        input_file: dict,
        metrics_from: SimulationResultOptions,
    ) -> SimulationServiceOutput | None:
        logger.info(f">>>>>> [{algorithm.__name__}] <<<<<<")
        seed_value = 428956419
        seed(seed_value)
        np.random.seed(seed_value)
        logger.warning("Starting simulation process")

        request_uuid = REQUEST_UUID.get()

        process = multiprocessing.Process(
            target=SimulationService._run_and_process_simulation_in_the_background,
            args=(input_file, algorithm, request_uuid),
        )
        logger.warning("Starting simulation process in the background")
        process.start()
        logger.warning("Waiting for simulation process to finish")
        process.join()
        logger.warning("Simulation process finished")
        if process.exitcode != 0:
            logger.error(
                f"There was an error in the simulation process for {algorithm.__name__}"
            )
            raise AlgorithmException(algorithm.__name__)

        logger.warning("Fetching simulation results")
        results = await LoggingService.get_log(request_uuid)
        logger.warning(f"Simulation results: {type(results)}")

        if results is None:
            return None

        return results.get(metrics_from, [])

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
        input_file: dict,
        algorithm: Callable[[Optional[dict | AlgorithmInputParameters]], None],
        request_uuid: uuid.UUID | None = None,
    ) -> SimulationServiceOutput:
        REQUEST_UUID.set(request_uuid)
        logger.configure(**logger_config())
        logger.warning("Start logs inside new proccess.")

        simulator: esp.Simulator = esp.Simulator(
            tick_duration=1,
            tick_unit="seconds",
            stopping_criterion=SimulationService.stopping_criterion,
            resource_management_algorithm=algorithm,
            dump_interval=float("inf"),
        )

        simulator.initialize(input_file=input_file)
        logger.info(f"Starting simulation with algorithm: {algorithm.__name__}")

        simulator.run_model()

        LoggingService.save_log(
            request_uuid,
            input_file,
            simulator.agent_metrics,
            algorithm.__name__,
        )

        logger.warning("End logs inside new proccess.")
