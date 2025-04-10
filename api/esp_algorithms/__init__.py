from typing import Callable, Optional

from api.esp_algorithms.smms.algorithm import (
    service_management_multiagent_system_runner,
)

options: dict[str, Callable[[Optional[dict]], None]] = {
    "smms": service_management_multiagent_system_runner,
}
