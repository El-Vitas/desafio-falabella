from fastapi import APIRouter

HEALTHY_STATUS = "ok"

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": HEALTHY_STATUS}
