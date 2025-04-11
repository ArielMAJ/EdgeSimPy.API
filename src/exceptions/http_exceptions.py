from fastapi import HTTPException, status

from src.utils.enums import SimulationInputAlgorithm


class AlgorithmException(HTTPException):
    def __init__(self, algorithm: SimulationInputAlgorithm):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"There was a problem executing {algorithm}. "
            "Please validate your input and try again.",
        )
