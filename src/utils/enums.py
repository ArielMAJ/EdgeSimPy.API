from enum import StrEnum, auto


class SimulationInputAlgorithm(StrEnum):
    """
    Enum for simulation input algorithms.
    """

    SMMS = auto()
    THEA = auto()


class SimulationResultOptions(StrEnum):
    """
    Enum for transforming service names.
    """

    SERVICE = auto()
