from fastapi import APIRouter

from app.shared.constants.http import HEALTHY_STATUS

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": HEALTHY_STATUS}
