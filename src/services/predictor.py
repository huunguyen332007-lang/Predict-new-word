import os
import joblib
from src.core.config import settings

class PredictorService:
    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        """Tải mô hình dự đoán từ file cấu hình"""
        model_path = settings.MODEL_PATH
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
            except Exception as e:
                print(f"Lỗi khi load model: {e}")

    def predict(self, text: str) -> tuple[str, float]:
        """Thực hiện dự đoán từ tiếp theo"""
        if not self.model:
            # Fallback/Mock kết quả nếu chưa có file model thực tế
            return "kết_quả_dự_đoán", 0.95
        
        # TODO: Đặt logic tiền xử lý và gọi self.model.predict() tại đây
        predicted_word = "tương_lai"
        confidence = 0.92
        return predicted_word, confidence

predictor_service = PredictorService()