import multiprocessing
import time

from fastapi import BackgroundTasks
from loguru import logger


def test_background_task():
    logger.info("Starting background task")
    time.sleep(2)
    logger.info("Background task completed")


class TestService:
    async def test_background(self, background_task: BackgroundTasks):
        simulation_process = multiprocessing.Process(target=test_background_task)
        simulation_process.start()

        background_task.add_task(simulation_process.join)
