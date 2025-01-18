import pickle
import numpy as np
from app.schemas import ProductPredictSchema, SuitabilityPredictSchema

class PredictService:
    # scaler = None
    # encoders = None

    # @classmethod
    # def load_encoders(cls):
    #     if cls.scaler is None or cls.encoders is None:
    #         scaler_path = r'../models/encoder_files/model_product/scaler_numeric.pkl'
    #         encode_path = r'../models/encoder_files/model_product/labelencoders.pkl'
            
    #         # โหลด scaler
    #         with open(scaler_path, 'rb') as f:
    #             cls.scaler = pickle.load(f)

    #         # โหลด encoders
    #         with open(encode_path, 'rb') as f:
    #             cls.encoders = pickle.load(f)

    @staticmethod
    async def transform_categorical_product(user_input: ProductPredictSchema):
        # โหลดโมเดลและ encoders
 
        encode_path = r'D:\DataSet_Project\seed_api\app\services\encoder_files\model_product\labelencoders.pkl'

        with open(encode_path, 'rb') as f:
            encoders = pickle.load(f)
        
        # ตัวแปลง LabelEncoder
        province_encoder = encoders['province']
        district_encoder = encoders['district']
        subdistrict_encoder = encoders['subdistrict']
        rubbertype_encoder = encoders['rubbertype']
        fer_top_encoder = encoders['fer_top']
        soilgroup_encoder = encoders['soilgroup']
        ph_top_encoder = encoders['pH_top']
        ph_low_encoder = encoders['pH_low']

        # แปลงข้อมูลหมวดหมู่แล้วคืนค่าในรูปแบบของ user_categorical
        user_categorical = {
            "province_input": province_encoder.transform([user_input.province])[0],
            "district_input": district_encoder.transform([user_input.district])[0],
            "subdistrict_input": subdistrict_encoder.transform([user_input.subdistrict])[0],
            "rubbertype_input": rubbertype_encoder.transform([user_input.rubbertype])[0],
            "fer_top_input": fer_top_encoder.transform([user_input.fer_top])[0],
            "soilgroup_input": soilgroup_encoder.transform([user_input.soilgroup])[0],
            "pH_top_input": ph_top_encoder.transform([user_input.pH_top])[0],
            "pH_low_input": ph_low_encoder.transform([user_input.pH_low])[0]
        }
        return user_categorical
    

    @staticmethod
    # ฟังก์ชันแปลงข้อมูลเชิงตัวเลข
    async def transform_numeric_product(user_input: ProductPredictSchema):


        scaler_path = r'D:\DataSet_Project\seed_api\app\services\encoder_files\model_product\scaler_numeric.pkl'
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)


        # แปลงข้อมูลเชิงตัวเลข
        user_numeric = np.array([[user_input.rubberarea,
                                user_input.rubbertreecount,
                                user_input.rubbertreeage,
                                user_input.rainfall,
                                user_input.avg_temperature,
                                user_input.rainy_days,
                                user_input.avg_humidity]])

        # ทำการปรับสเกลข้อมูล
        user_numeric_scaler = scaler.transform(user_numeric)

        # คืนค่าข้อมูลที่ปรับสเกลแล้วเป็น list
        return user_numeric_scaler


    @staticmethod
    async def data_predict_product(user_input: ProductPredictSchema):
        # แปลงข้อมูลหมวดหมู่
        user_categorical = await PredictService.transform_categorical_product(user_input)

        # แปลงข้อมูลเชิงตัวเลข
        user_numeric = await PredictService.transform_numeric_product(user_input)

        # แปลงข้อมูลจาก numpy เป็นชนิดข้อมูลที่ JSON รองรับ
        user_categorical = {key: [int(value)] for key, value in user_categorical.items()}  # แปลงเป็น list ของ int
        user_numeric = user_numeric.tolist()  # แปลง numpy array เป็น list

        # สร้าง payload สำหรับส่งไปยัง API
        data = {
            "signature_name": "serving_default",
            "instances": [
                {
                    "district_input": [user_categorical["district_input"]],
                    "soilgroup_input": [user_categorical["soilgroup_input"]],
                    "fer_top_input": [user_categorical["fer_top_input"]],
                    "subdistrict_input": [user_categorical["subdistrict_input"]],
                    "pH_low_input": [user_categorical["pH_low_input"]],
                    "rubbertype_input": [user_categorical["rubbertype_input"]],
                    "province_input": [user_categorical["province_input"]],
                    "pH_top_input": [user_categorical["pH_top_input"]],
                    "numeric_input": user_numeric[0]  # ใส่ข้อมูลเชิงตัวเลข
                }
            ]
        }

        return data
    


    @staticmethod
    async def transform_categorical_suitability(user_input: SuitabilityPredictSchema):
        # โหลดโมเดลและ encoders
 
        encode_path = r'D:\DataSet_Project\seed_api\app\services\encoder_files\model_classify\labelencoders.pkl'

        with open(encode_path, 'rb') as f:
            encoders = pickle.load(f)
        
        # ตัวแปลง LabelEncoder
        ph_top_encoder = encoders['pH_top']

        # แปลงข้อมูลหมวดหมู่แล้วคืนค่าในรูปแบบของ user_categorical
        user_pH_top_encoded = ph_top_encoder.transform([user_input.ph_top])[0]

        return user_pH_top_encoded
    

    @staticmethod
    # ฟังก์ชันแปลงข้อมูลเชิงตัวเลข
    async def transform_numeric_suitability(user_input: SuitabilityPredictSchema):

        user_pH_top_encoded = await PredictService.transform_categorical_suitability(user_input)

        scaler_path = r'D:\DataSet_Project\seed_api\app\services\encoder_files\model_classify\scaler_numeric.pkl'
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)


        user_numeric = np.array([[
                                    user_pH_top_encoded, 
                                    user_input.rainfall, 
                                    user_input.temperature,
                                    user_input.humidity,
                                    user_input.rainfall_days
                                ]])

        # ทำการปรับสเกลข้อมูล
        user_numeric_scaler = scaler.transform(user_numeric).tolist()

        # คืนค่าข้อมูลที่ปรับสเกลแล้วเป็น list
        return user_numeric_scaler
    

    @staticmethod
    async def data_predict_suitability(user_input: SuitabilityPredictSchema):
        # แปลงข้อมูลหมวดหมู่
        user_numeric_scaler = await PredictService.transform_numeric_suitability(user_input)

        # สร้าง payload สำหรับส่งไปยัง API
        data = {
            "signature_name": "serving_default",
            "instances": [{"keras_tensor_28": user_numeric_scaler[0]}]
            
        }

        return data