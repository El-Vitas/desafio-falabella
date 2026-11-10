from fastapi import Depends
from psycopg import Connection
from psycopg.rows import DictRow

from app.shared.database import get_connection
from app.stats import queries
from app.stats.schemas import (
    LevelClassificationReport,
    MonthlyGrowth,
    MonthlyGrowthReport,
    RegionTopTrainers,
    TopTrainersReport,
    TypeLevelClassification,
)


class StatsRepository:
    def __init__(self, connection: Connection[DictRow]) -> None:
        self._connection = connection

    def monthly_growth(self) -> MonthlyGrowthReport:
        rows = self._connection.execute(queries.MONTHLY_GROWTH).fetchall()
        return MonthlyGrowthReport(months=[MonthlyGrowth.model_validate(row) for row in rows])

    def top_trainers(self) -> TopTrainersReport:
        rows = self._connection.execute(queries.TOP_TRAINERS).fetchall()
        return TopTrainersReport(regions=[RegionTopTrainers.model_validate(row) for row in rows])

    def level_classification(self) -> LevelClassificationReport:
        rows = self._connection.execute(queries.LEVEL_CLASSIFICATION).fetchall()
        return LevelClassificationReport(
            types=[TypeLevelClassification.model_validate(row) for row in rows]
        )


def get_stats_repository(
    connection: Connection[DictRow] = Depends(get_connection),
) -> StatsRepository:
    return StatsRepository(connection)
