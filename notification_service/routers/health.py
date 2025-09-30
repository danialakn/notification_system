from fastapi import APIRouter


router = APIRouter()


@router.get("/notification/health")
def health():
    return {"status": "ok"}