from pydantic import BaseModel


class AlgorithmInputParameters(BaseModel):
    current_step: int
