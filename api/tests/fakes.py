from collections.abc import Callable
from datetime import date
from typing import NoReturn

from app.pokemon.schemas import (
    PokemonDetail,
    PokemonListItem,
    PokemonPage,
    PokemonSummary,
    PokemonType,
    TypeSummary,
)
from app.shared.config import Settings
from app.stats.schemas import (
    LevelClassificationReport,
    MonthlyGrowth,
    MonthlyGrowthReport,
    RankedTrainer,
    RegionTopTrainers,
    TopTrainersReport,
    TypeLevelClassification,
)

TEST_SETTINGS = Settings(
    database_url="postgresql://unused@localhost/unused",
    cors_allowed_origins=("http://localhost:5173",),
)

BULBASAUR = PokemonDetail(
    id=1,
    name="bulbasaur",
    height=7,
    weight=69,
    base_experience=64,
    sprite="https://sprites.example/1.png",
    types=[PokemonType(id=12, name="grass", slot=1), PokemonType(id=4, name="poison", slot=2)],
)

SUMMARY = PokemonSummary(
    total_pokemon=1,
    by_type=[
        TypeSummary(type_id=12, type_name="grass", pokemon_count=1, avg_base_experience=64.0),
        TypeSummary(type_id=4, type_name="poison", pokemon_count=1, avg_base_experience=64.0),
    ],
)


MONTHLY_GROWTH = MonthlyGrowthReport(
    months=[
        MonthlyGrowth(
            month=date(2025, 11, 1), captures=233, previous_captures=None, change_percent=None
        ),
        MonthlyGrowth(
            month=date(2025, 12, 1), captures=244, previous_captures=233, change_percent=4.72
        ),
    ]
)

TOP_TRAINERS = TopTrainersReport(
    regions=[
        RegionTopTrainers(
            region="Kanto",
            trainers=[
                RankedTrainer(position=1, trainer_id=44, trainer_name="Lucas Kukui", captures=544),
                RankedTrainer(position=1, trainer_id=26, trainer_name="Ash Oak", captures=544),
            ],
        ),
        RegionTopTrainers(region="Galar", trainers=[]),
    ]
)

LEVEL_CLASSIFICATION = LevelClassificationReport(
    types=[
        TypeLevelClassification(
            type_id=15,
            type_name="ice",
            high_level_captures=10,
            total_captures=56,
            high_level_percent=17.86,
        ),
        TypeLevelClassification(
            type_id=10,
            type_name="fire",
            high_level_captures=0,
            total_captures=0,
            high_level_percent=None,
        ),
    ]
)


class FakePokemonRepository:
    def __init__(self, details: list[PokemonDetail]) -> None:
        self._details = {detail.id: detail for detail in details}
        self.requested_pages: list[tuple[int, int]] = []

    def list_page(self, limit: int, offset: int) -> PokemonPage:
        self.requested_pages.append((limit, offset))
        ordered = sorted(self._details.values(), key=lambda detail: detail.id)
        return PokemonPage(
            items=[
                PokemonListItem(id=detail.id, name=detail.name, sprite=detail.sprite)
                for detail in ordered[offset : offset + limit]
            ],
            total=len(ordered),
            limit=limit,
            offset=offset,
        )

    def find_detail(self, pokemon_id: int) -> PokemonDetail | None:
        return self._details.get(pokemon_id)

    def summary(self) -> PokemonSummary:
        return SUMMARY


class FakeStatsRepository:
    def monthly_growth(self) -> MonthlyGrowthReport:
        return MONTHLY_GROWTH

    def top_trainers(self) -> TopTrainersReport:
        return TOP_TRAINERS

    def level_classification(self) -> LevelClassificationReport:
        return LEVEL_CLASSIFICATION


class FailingRepository:
    def __init__(self, error: Exception) -> None:
        self._error = error

    def __getattr__(self, _name: str) -> Callable[..., NoReturn]:
        return self._raise

    def _raise(self, *_args: object, **_kwargs: object) -> NoReturn:
        raise self._error
