from uuid import UUID

import httpx
from fastapi_cache.decorator import cache
from loguru import logger

from src.configs.env import Config
from src.schemas.log_schema import LogSchema
from src.utils.json_processor import replace_inf_values


class LoggingService:
    @staticmethod
    @cache(expire=60 * 5)
    async def get_log(hash: str) -> dict:
        """
        Get the log from the logger service.
        """
        logger.info(f"Fetching log with hash: {hash}")
        async with httpx.AsyncClient(timeout=11) as client:
            response = await client.get(
                f"{Config.LOGGER_API_URL}/log/{hash}/metrics",
                headers={"API-KEY": Config.LOGGER_API_KEY},
            )
            if not response.status_code == 200:
                logger.error(f"Error fetching log: {response.text}")
                response.raise_for_status()
            return response.json()

    @staticmethod
    def save_log(
        request_uuid: str | UUID,
        input_file: dict,
        agent_metrics: dict,
        algorithm_name: str,
    ):
        """
        Save the log to the logger service.
        """
        if isinstance(request_uuid, UUID):
            request_uuid = str(request_uuid)
        logger.warning(f"Saving log with hash: {request_uuid}")

        input_file: dict = replace_inf_values(input_file)
        agent_metrics: dict = replace_inf_values(agent_metrics)

        log: LogSchema = LogSchema(
            hash=request_uuid,
            input_simulation=input_file,
            agent_metrics=agent_metrics,
            algorithm=algorithm_name,
        )
        with httpx.Client(timeout=11) as client:
            response = client.post(
                f"{Config.LOGGER_API_URL}/log/",
                json=log.model_dump(),
                headers={"API-KEY": Config.LOGGER_API_KEY},
            )
            if not response.status_code == 201:
                logger.error(f"Error saving log: {response.text}")
                response.raise_for_status()

        logger.info(f"Log saved successfully: {response.json()}")
