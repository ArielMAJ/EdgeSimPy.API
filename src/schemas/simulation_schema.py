from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl

from src.utils.enums import SimulationInputAlgorithm


class SimulationInput(BaseModel):
    algorithm: SimulationInputAlgorithm
    url_or_json: HttpUrl | dict


class MigrationData(BaseModel):
    status: str
    origin: Optional[str]
    target: Optional[str]
    start: Optional[int]
    end: Optional[int]
    waiting: Optional[int]
    pulling: Optional[int]
    migr_state: Optional[int]


class ServiceState(BaseModel):
    Object: str
    Time_Step: int = Field(alias="Time Step")
    Instance_ID: int = Field(alias="Instance ID")
    Available: bool
    Server: Optional[int]
    Being_Provisioned: bool = Field(alias="Being Provisioned")
    Last_Migration: Optional[MigrationData] = Field(alias="Last Migration")

    class Config:
        allow_population_by_field_name = True


class SimulationServiceOutput(BaseModel):
    Service: List[ServiceState]
