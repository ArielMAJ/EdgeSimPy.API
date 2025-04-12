from pydantic import BaseModel


class LogSchema(BaseModel):
    hash: str
    input_simulation: dict
    agent_metrics: dict
    algorithm: str
