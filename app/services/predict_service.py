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
        # try:
            # Evaluate each parameter
        evaluations = {
                "temperature": self.evaluate_suitability("temperature", data.temperature),
                "humidity": self.evaluate_suitability("humidity", data.humidity),
                "rainfall": self.evaluate_suitability("rainfall", data.rainfall),
                "rainfall_days": self.evaluate_suitability("rainfall_days", data.rainfall_days),
                "slope": self.evaluate_suitability("slope", data.slope),
                "ph_top": self.evaluate_suitability("ph_top", data.ph_top)
            }

            # Continue with your existing ML prediction logic
        numeric_scaler = self.transform_num_suitable(data)

        payload = {
                "signature_name": "serving_default",
                "instances": [{"keras_tensor": numeric_scaler[0]}]
            }

        response = self.get_url_predict(url='/v1/models/model_suitability/versions/3:predict', payload=payload)

        response = response['predictions'][0]
        predicted_class_index = int(np.argmax(response))


        class_labels = [0, 1, 2]
        predicted_class_label = class_labels[predicted_class_index]

        predicted_result = {
                    "suitability": predicted_class_label
                }

            # Add evaluations to the response
        predicted_result["evaluations"] = evaluations
        print(predicted_result)
        return predicted_result

        # except Exception as e:
        #     logger.error("Unknown error: %s", e)
        #     raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")

    
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
    
    def evaluate_suitability(self, param_name: str, value) -> dict:
        """
        ประเมินความเหมาะสมของค่าตัวแปรตามเกณฑ์ที่กำหนด
        Args:
            param_name: ชื่อตัวแปรที่ต้องการประเมิน
            value: ค่าที่ต้องการประเมิน (can be number or string)
        Returns:
            dict: ผลการประเมินความเหมาะสม (2: เหมาะสม, 1: เหมาะสมปานกลาง, 0: ไม่เหมาะสม)
        """
        param = self._get_param_config(param_name)
        if not param:
            return {"suitability": 0, "message": "ไม่พบข้อมูลเกณฑ์การประเมิน"}

        # Special handling for ph_top which can be ranges like "4.5-5.0"
        if param_name == "ph_top" and isinstance(value, str):
            return self._evaluate_ph_top(value, param)
        elif "ranges" in param:
            # For numeric parameters with range definitions
            try:
                numeric_value = float(value)
                return self._evaluate_with_ranges(numeric_value, param)
            except ValueError:
                logger.error(f"Invalid numeric value for {param_name}: {value}")
                return {
                    "suitability": 0,
                    "message": f"ค่า {param_name} ({value}) ไม่ถูกต้อง ต้องเป็นตัวเลข"
                }
        else:
            # For simple parameters with min/max values
            try:
                numeric_value = float(value)
                return self._evaluate_simple_param(numeric_value, param, param_name)
            except ValueError:
                logger.error(f"Invalid numeric value for {param_name}: {value}")
                return {
                    "suitability": 0,
                    "message": f"ค่า {param_name} ({value}) ไม่ถูกต้อง ต้องเป็นตัวเลข"
                }

    def _get_param_config(self, param_name: str) -> dict:
        """Returns the configuration for the specified parameter."""
        weather_params = {
            "ph_top": {
                "suitables": ["4.5-5.0", "4.5-5.5", "4.5-6.0", "5.0-5.5"],
                "moderate": ["5.0-6.5", "5.5-6.5"],
                "not_suitable": ["<4.0", "5.5-7.0", "5.5-8.0", "6.0-7.0", "6.0-8.0"],
                "messages": {
                    "not_suitable": "ค่า pH ดินเฉลี่ย {value} ไม่เหมาะสม ควรมีค่า pH ดินระหว่าง {suitable}",
                    "moderate": "ค่า pH ดินเฉลี่ย {value} เหมาะสมปานกลาง ค่าที่เหมาะสมควรอยู่ระหว่าง {suitable}",
                    "suitable": "ค่า pH ดินเฉลี่ย {value} อยู่ในเกณฑ์ที่เหมาะสม"
                }
            },
            "temperature": {
                "ranges": {
                    "suitable": [{"min": 24, "max": 27}],
                    "moderate": [{"min": 20, "max": 24}, {"min": 27, "max": 35}],
                    "not_suitable": [{"max": 20}, {"min": 35}]
                },
                "messages": {
                    "not_suitable": "อุณหภูมิเฉลี่ย {value} °C ไม่เหมาะสม ควรอยู่ระหว่าง 24-27 °C",
                    "moderate": "อุณหภูมิเฉลี่ย {value} °C เหมาะสมปานกลาง ค่าที่เหมาะสมควรอยู่ระหว่าง 24-27 °C",
                    "suitable": "อุณหภูมิเฉลี่ย {value} °C อยู่ในเกณฑ์ที่เหมาะสม"
                }
            },
            "humidity": {
                "ranges": {
                    "suitable": [{"min": 65, "max": 80}],
                    "moderate": [{"min": 50, "max": 65}, {"min": 80, "max": 90}],
                    "not_suitable": [{"max": 50}, {"min": 90}]
                },
                "messages": {
                    "not_suitable": "ความชื้นสัมพัทธ์เฉลี่ย {value} % ไม่เหมาะสม ควรอยู่ระหว่าง 65-80 %",
                    "moderate": "ความชื้นสัมพัทธ์เฉลี่ย {value} % เหมาะสมปานกลาง ค่าที่เหมาะสมควรอยู่ระหว่าง 65-80 %",
                    "suitable": "ความชื้นสัมพัทธ์เฉลี่ย {value} % อยู่ในเกณฑ์ที่เหมาะสม"
                }
            },
            "rainfall": {
                "ranges": {
                    "suitable": [{"min": 1350, "max": 2500}],
                    "moderate": [{"min": 1000, "max": 1350}, {"min": 2500, "max": 3000}],
                    "not_suitable": [{"max": 1000}, {"min": 3000}]
                },
                "messages": {
                    "not_suitable": "ปริมาณน้ำฝนเฉลี่ย {value} มม. ไม่เหมาะสม ควรอยู่ระหว่าง 1350-2500 มม.",
                    "moderate": "ปริมาณน้ำฝนเฉลี่ย {value} มม. เหมาะสมปานกลาง ค่าที่เหมาะสมควรอยู่ระหว่าง 1350-2500 มม.",
                    "suitable": "ปริมาณน้ำฝนเฉลี่ย {value} มม. อยู่ในเกณฑ์ที่เหมาะสม"
                }
            },
            "rainfall_days": {
                "ranges": {
                    "suitable": [{"min": 120, "max": 200}],
                    "moderate": [{"min": 100, "max": 120}, {"min": 200, "max": 250}],
                    "not_suitable": [{"max": 100}, {"min": 250}]
                },
                "messages": {
                    "not_suitable": "จำนวนวันฝนตกเฉลี่ย {value} วัน ไม่เหมาะสม ควรอยู่ระหว่าง 120-200 วัน",
                    "moderate": "จำนวนวันฝนตกเฉลี่ย {value} วัน เหมาะสมปานกลาง ค่าที่เหมาะสมควรอยู่ระหว่าง 120-200 วัน",
                    "suitable": "จำนวนวันฝนตกเฉลี่ย {value} วัน อยู่ในเกณฑ์ที่เหมาะสม"
                }
            },
            "slope": {
                "ranges": {
                    "suitable": [{"min": 15, "max": 16}],
                    "moderate": [{"min": 0, "max": 15}, {"min": 16, "max": 45}],
                    "not_suitable": [{"min": 45}]
                },
                "messages": {
                    "not_suitable": "ความลาดชันเฉลี่ย {value} องศา ไม่เหมาะสม ควรอยู่ระหว่าง 15-16 องศา",
                    "moderate": "ความลาดชันเฉลี่ย {value} องศา เหมาะสมปานกลาง ค่าที่เหมาะสมควรอยู่ระหว่าง 15-16 องศา",
                    "suitable": "ความลาดชันเฉลี่ย {value} องศา อยู่ในเกณฑ์ที่เหมาะสม"
                }
            }
        }
        return weather_params.get(param_name)

    def _evaluate_ph_top(self, value, param: dict) -> dict:
        """Evaluates pH top values against defined ranges."""
        # For pH top, we need to check if the exact string matches any of the ranges
        # rather than converting to float and checking numerical ranges
        
        # If value is already a suitable range, it's suitable
        if value in param["suitables"]:
            return {
                "suitability": 2,
                "message": param["messages"]["suitable"].format(value=value)
            }
        
        # If value is a moderate range, it's moderately suitable
        if value in param["moderate"]:
            return {
                "suitability": 1,
                "message": param["messages"]["moderate"].format(
                    value=value,
                    suitable=" หรือ ".join(param["suitables"])
                )
            }
        
        # If value is in not_suitable list, it's not suitable
        if value in param["not_suitable"]:
            return {
                "suitability": 0,
                "message": param["messages"]["not_suitable"].format(
                    value=value,
                    suitable=" หรือ ".join(param["suitables"])
                )
            }
        
        # If value is a number or unknown range, try to evaluate it numerically
        try:
            value_float = self._convert_to_float(value)
            
            # Check against suitable ranges
            for suitable_range in param["suitables"]:
                if self._is_in_range(value_float, suitable_range):
                    return {
                        "suitability": 2,
                        "message": param["messages"]["suitable"].format(value=value)
                    }
            
            # Check against moderate ranges
            for moderate_range in param["moderate"]:
                if self._is_in_range(value_float, moderate_range):
                    return {
                        "suitability": 1,
                        "message": param["messages"]["moderate"].format(
                            value=value,
                            suitable=" หรือ ".join(param["suitables"])
                        )
                    }
            
            # If neither suitable nor moderate
            return {
                "suitability": 0,
                "message": param["messages"]["not_suitable"].format(
                    value=value,
                    suitable=" หรือ ".join(param["suitables"])
                )
            }
        except ValueError:
            # If we can't convert to float, treat as not suitable
            logger.error(f"Invalid pH value format: {value}")
            return {
                "suitability": 0,
                "message": f"ค่า pH ดิน ({value}) ไม่ถูกต้อง"
            }

    def _convert_to_float(self, value) -> float:
        """Converts string values (including those with < or >) to float."""
        if isinstance(value, str):
            # Handle range values differently - extract first number for comparison
            if "-" in value and not value.startswith("<") and not value.startswith(">"):
                try:
                    # Return the midpoint of the range for comparison
                    min_val, max_val = map(float, value.split("-"))
                    return (min_val + max_val) / 2
                except ValueError:
                    # If can't parse the range, log and return a default
                    logger.warning(f"Could not parse range value: {value}")
                    return 0.0
            
            # Handle < and > values
            if value.startswith('<'):
                return float(value[1:]) - 0.1
            elif value.startswith('>'):
                return float(value[1:]) + 0.1
            
            # Regular numeric string
            return float(value)
        
        # Already a numeric value
        return float(value)

    def _is_in_range(self, value_float: float, range_str: str) -> bool:
        """Checks if a value is within a specified range."""
        try:
            if range_str.startswith("<"):
                max_val = float(range_str[1:])
                return value_float < max_val
            elif range_str.startswith(">"):
                min_val = float(range_str[1:])
                return value_float > min_val
            else:
                min_val, max_val = map(float, range_str.split("-"))
                return min_val <= value_float <= max_val
        except ValueError as e:
            logger.error(f"Invalid range format '{range_str}': {str(e)}")
            return False

    def _evaluate_with_ranges(self, value, param: dict) -> dict:
        """Evaluates values against ranges in the param dictionary."""
        value_float = float(value)
        
        # Check suitable ranges
        for range_obj in param["ranges"]["suitable"]:
            min_val = range_obj.get("min", float("-inf"))
            max_val = range_obj.get("max", float("inf"))
            if min_val <= value_float <= max_val:
                return {
                    "suitability": 2,
                    "message": param["messages"]["suitable"].format(value=value)
                }
        
        # Check moderate ranges
        for range_obj in param["ranges"]["moderate"]:
            min_val = range_obj.get("min", float("-inf"))
            max_val = range_obj.get("max", float("inf"))
            if min_val <= value_float <= max_val:
                return {
                    "suitability": 1,
                    "message": param["messages"]["moderate"].format(value=value)
                }
        
        # If neither suitable nor moderate, it's not suitable
        return {
            "suitability": 0,
            "message": param["messages"]["not_suitable"].format(value=value)
        }

    def _evaluate_simple_param(self, value, param: dict, param_name: str) -> dict:
        """Evaluates parameters with simple min/max values."""
        if "suitable" not in param or "min" not in param["suitable"] or "max" not in param["suitable"]:
            logger.error(f"Parameter structure for {param_name} is incorrect")
            return {
                "suitability": 0, 
                "message": f"ค่า {param_name} ({value}) ไม่สามารถประเมินความเหมาะสมได้"
            }
        
        value_float = float(value)
        
        # Check suitable range
        if param["suitable"]["min"] <= value_float <= param["suitable"]["max"]:
            return {
                "suitability": 2,
                "message": param["messages"]["suitable"].format(value=value)
            }
        
        # Check moderate range if it exists
        if "moderate" in param and "min" in param["moderate"] and "max" in param["moderate"]:
            if param["moderate"]["min"] <= value_float <= param["moderate"]["max"]:
                return {
                    "suitability": 1,
                    "message": param["messages"]["moderate"].format(
                        value=value,
                        min=param["suitable"]["min"],
                        max=param["suitable"]["max"]
                    )
                }
        
        # If neither suitable nor moderate
        return {
            "suitability": 0,
            "message": param["messages"]["not_suitable"].format(
                value=value,
                min=param["suitable"]["min"],
                max=param["suitable"]["max"]
            )
        }
