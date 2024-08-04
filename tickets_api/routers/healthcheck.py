from fastapi import APIRouter

router = APIRouter()


@router.get("")
def dumb_healthcheck():
    return {"status": "ok"}
