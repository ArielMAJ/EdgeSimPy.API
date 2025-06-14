import multiprocessing

import uvicorn

from src.configs.env import Config


def main() -> None:
    """Entrypoint of the application."""
    multiprocessing.set_start_method("spawn")
    uvicorn.run(
        "src.app:get_app",
        workers=Config.WORKERS_COUNT,
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.RELOAD,
        log_level=Config.LOG_LEVEL.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
