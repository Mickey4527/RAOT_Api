import logging
import os
import pickle
import requests
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import SuitablePredictSchema
from app.core.config import settings
from app.schemas.predict_schema import ProductPredictSchema
from app.utilities.app_exceptions import ServerProcessException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
class PredictService:

    def __init__(self, session: AsyncSession):
        self.session = session

    def get_url_predict(self, url, payload, headers = {"Content-Type": "application/json"}):
        """
        รับ url และ payload จากผู้ใช้และส่งไปยัง API ทำนายผลผลิต \n
        Get the url and payload from the user and send it to the prediction API.
        """
        payload = requests.post(url=f'{settings.PREDICT_API_URL}{url}', json=payload, headers=headers)
        return payload.json()
    
    def load_encoder(self, encode_path: str):
        """
        โหลดไฟล์ encoder จากไดเรกทอรี \n
        Load the encoder file from the directory.
        """
        
        encode_path = os.path.join(os.path.dirname(__file__), 'encoder_files/', encode_path)
        
        with open(encode_path, 'rb') as f:
            encoders = pickle.load(f)
        return encoders
    
    def get_product(self, data: ProductPredictSchema):
        
        """
        บริการทำนายผลผลิตของพืชที่ต้องการปลูก
        """

        try:

            user_cat = self.transform_cat_product(data)
            user_numeric = self.transform_num_product(data)

            user_cat = { key: [int(value)] for key, value in user_cat.items()}
            user_numeric = user_numeric.tolist()

            payload = {
                "signature_name": "serving_default",
                "instances": [
                    {
                        "district_input": [user_cat["district_input"]],
                        "soilgroup_input": [user_cat["soilgroup_input"]],
                        "subdistrict_input": [user_cat["subdistrict_input"]],
                        "rubbertype_input": [user_cat["rubbertype_input"]],
                        "province_input": [user_cat["province_input"]],
                        "pH_top_input": [user_cat["pH_top_input"]],
                        "numeric_input": user_numeric[0]
                    }
                ]
            }
            response = self.get_url_predict(url='/v1/models/model_product/versions/3:predict', payload=payload)

            return response
        
        except Exception:
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")
        
    def get_suitable(self, data: SuitablePredictSchema):
        """
        บริการทำนายความเหมาะสมของพืชที่ต้องการปลูก
        """

        try:

            numeric_scaler = self.transform_num_suitable(data)

            payload = {
                "signature_name": "serving_default",
                "instances": [{"keras_tensor": numeric_scaler[0]}]
            }

            response = self.get_url_predict(url='/v1/models/model_suitability/versions/3:predict', payload=payload)

            response = response['predictions'][0]
            predicted_class_index = int(np.argmax(response))


            class_labels = [1, 2, 0]
            predicted_class_label = class_labels[predicted_class_index]

            predicted_result = {
                    "suitability": predicted_class_label
                }

            return predicted_result
            
        except Exception as e:
            logger.error("Unknown error: %s", e)
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")


    
    def transform_cat_suitable(self, data: SuitablePredictSchema):
        """
        แปลงข้อมูลที่ได้ให้อยู่ในรูปแบบการทำนายความเหมาะสม และส่งค่ากลับ
        """
        encoders = self.load_encoder('model_classify/labelencoders_3.pkl')
        
        ph_top_encoder = encoders['pH_top']
        user_pH_top_encoded = ph_top_encoder.transform([data.ph_top])[0]

        return user_pH_top_encoded
    
    def transform_num_suitable(self, data: SuitablePredictSchema):
        """
        แปลงข้อมูลที่ได้ให้อยู่ในรูปแบบของข้อมูลที่เป็นตัวเลข และส่งค่ากลับ
        """

        user_pH_top_encoded = self.transform_cat_suitable(data)

        scaler = self.load_encoder('model_classify/scaler_numeric_3.pkl')

        user_numeric = np.array([[
                                    user_pH_top_encoded, 
                                    data.rainfall, 
                                    data.temperature,
                                    data.humidity,
                                    data.rainfall_days,
                                    data.slope,
                                ]])
        
        numeric_scaler = scaler.transform(user_numeric).tolist()

        return numeric_scaler
    
    def transform_cat_product(self, data: ProductPredictSchema):
        """
        แปลงข้อมูลที่ได้ให้อยู่ในรูปแบบการทำนายผลผลิต และส่งค่ากลับ
        """
        encoders = self.load_encoder('model_product/labelencoders_3.pkl')
        
        province_encoder = encoders['province']
        district_encoder = encoders['district']
        subdistrict_encoder = encoders['subdistrict']
        rubbertype_encoder = encoders['rubbertype']
        soilgroup_encoder = encoders['soilgroup']
        ph_top_encoder = encoders['pH_top']

        user_cat = {
            "province_input": province_encoder.transform([data.province])[0],
            "district_input": district_encoder.transform([data.district])[0],
            "subdistrict_input": subdistrict_encoder.transform([data.subdistrict])[0],
            "rubbertype_input": rubbertype_encoder.transform([data.rubber_type])[0],
            "soilgroup_input": soilgroup_encoder.transform([data.soil_group])[0],
            "pH_top_input": ph_top_encoder.transform([data.ph_top])[0],
        }

        return user_cat
    
    def transform_num_product(self, data: ProductPredictSchema):
        """
        แปลงข้อมูลที่ได้ให้อยู่ในรูปแบบของข้อมูลที่เป็นตัวเลข และส่งค่ากลับ
        """

        user_numeric = np.array([[data.rubber_area,
                                data.rubber_tree_count,
                                data.rubber_tree_age,
                                data.rainfall,
                                data.temperature,
                                data.rainfall_days,
                                data.humidity]])

        return user_numeric