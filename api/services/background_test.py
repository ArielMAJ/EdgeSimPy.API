import multiprocessing

from loguru import logger


class TestService:
    async def test_background(self):
        simulation_process = multiprocessing.Process(
            target=lambda: logger.info("Background process ran")
        )
        simulation_process.start()
        simulation_process.join()
