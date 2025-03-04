from fastapi import APIRouter, Depends, Request, status

from app.schemas import ProductPredictSchema, SuitablePredictSchema, Result
from app.services.district_service import DistrictService
from app.services.predict_service import PredictService
from app.api.deps import SessionDep, get_current_user, get_trace_id
from app.services.province_service import ProvinceService
from app.services.sub_district_service import SubDistrictService
from app.utilities.app_exceptions import APIException, DuplicateResourceException, ResourceNotFoundException, SQLProcessException, ServerProcessException

router = APIRouter(prefix="/predict", tags=["predict"], dependencies=[Depends(get_current_user)])
result = Result()

@router.post("/product", response_model=Result)
async def predict_product(
    req: Request, 
    session: SessionDep, 
    user_input: ProductPredictSchema
):
    province_service = ProvinceService(session)
    district_service = DistrictService(session)
    sub_district_service = SubDistrictService(session)
    predict_service = PredictService(session)

    trace_id = get_trace_id(req)

    try:

        province = await province_service._get_province_by_code(user_input.province)
        district = await district_service._get_district_by_code(user_input.district)
        subdistrict = await sub_district_service._get_sub_district_by_code(user_input.subdistrict)

        if not province or not district or not subdistrict:
            raise APIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="กรุณากรอกข้อมูลให้ถูกต้อง",
                trace_id=trace_id
            )
        
        user_input.district = district.name_th
        user_input.province = province.name_th
        user_input.subdistrict = subdistrict.name_th

        payload = predict_service.get_product(user_input)

        return Result(
            success=True,
            data=payload,
            trace_id=trace_id
        )
    
    except (ServerProcessException, SQLProcessException) as e:
        raise APIException(status_code=e.status_code, message=e.message, trace_id=trace_id, data=e.data)
    

@router.post("/suitability", response_model=Result)
def predict_suitability(
    session: SessionDep,
    req: Request, 
    user_input: SuitablePredictSchema):

    predict_service = PredictService(session)
    trace_id = get_trace_id(req)

    try:
        payload = predict_service.get_suitable(user_input)

        return Result(
            success=True,
            data=payload,
            trace_id=trace_id
        )
     
    except (ServerProcessException, SQLProcessException) as e:
        raise APIException(status_code=e.status_code, message=e.message, trace_id=trace_id, data=e.data)