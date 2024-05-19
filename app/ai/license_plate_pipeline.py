from app.ai.plate_detection import PlateDetector
from app.ai.plate_recognition import PlateRecognizer
from app.config import config


class LicensePlatePipeline:
    def __init__(self):
        self.config = config['ai']
        self.detector_weight_path = self.config.DETECTION_WEIGHT_PATH
        self.ocr_weight_path = self.config.OCR_WEIGHT
        self.ocr_net_cfg = self.config.OCR_NETCFG
        self.ocr_dataset = self.config.OCR_DATASET

        self.detector = PlateDetector(self.detector_weight_path)
        self.recognizer = PlateRecognizer(self.ocr_weight_path, self.ocr_net_cfg, self.ocr_dataset)

    def process(self, image_path):
        detected_plate_path = self.detector.detect_plate(image_path)
        if detected_plate_path:
            plate_text = self.recognizer.recognize_plate(detected_plate_path)
            return plate_text
        else:
            return "No plate detected"
