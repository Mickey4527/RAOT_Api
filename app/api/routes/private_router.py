from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.services.private_service import PrivateService

router = APIRouter(prefix="/test", tags=["private"])

@router.post("/")
async def endpoint(session: SessionDep):
    try:
        result = await PrivateService.add_private(session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/avg")
async def avg_test(session: SessionDep):
    try:
        result = await PrivateService.avg_test(session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/count")
async def count_test(session: SessionDep):
    try:
        result = await PrivateService.count_test(session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))