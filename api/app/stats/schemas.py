from datetime import date

from pydantic import BaseModel


class MonthlyGrowth(BaseModel):
    month: date
    captures: int
    previous_captures: int | None
    change_percent: float | None


class MonthlyGrowthReport(BaseModel):
    months: list[MonthlyGrowth]


class RankedTrainer(BaseModel):
    position: int
    trainer_id: int
    trainer_name: str
    captures: int


class RegionTopTrainers(BaseModel):
    region: str
    trainers: list[RankedTrainer]


class TopTrainersReport(BaseModel):
    regions: list[RegionTopTrainers]


class TypeLevelClassification(BaseModel):
    type_id: int
    type_name: str
    high_level_captures: int
    total_captures: int
    high_level_percent: float | None


class LevelClassificationReport(BaseModel):
    types: list[TypeLevelClassification]
