from typing import Annotated

from fastapi import APIRouter, Depends

from app.shared.constants.openapi import SERVER_ERROR_RESPONSES
from app.stats.repository import StatsRepository, get_stats_repository
from app.stats.schemas import LevelClassificationReport, MonthlyGrowthReport, TopTrainersReport

router = APIRouter(prefix="/queries", tags=["stats"], responses=SERVER_ERROR_RESPONSES)

Repository = Annotated[StatsRepository, Depends(get_stats_repository)]


@router.get("/monthly-growth")
def monthly_growth(repository: Repository) -> MonthlyGrowthReport:
    return repository.monthly_growth()


@router.get("/top-trainers")
def top_trainers(repository: Repository) -> TopTrainersReport:
    return repository.top_trainers()


@router.get("/level-classification")
def level_classification(repository: Repository) -> LevelClassificationReport:
    return repository.level_classification()
