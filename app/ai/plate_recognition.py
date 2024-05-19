from PIL import Image
from .darknet_lib.darknet import detect, load_net, load_meta
from .darknet_lib.utils.label import dknet_label_conversion
from .darknet_lib.utils.utils import nms


class PlateRecognizer:
    def __init__(self, ocr_weights, ocr_netcfg, ocr_dataset):
        self.ocr_net = load_net(ocr_netcfg, ocr_weights, 0)
        self.ocr_meta = load_meta(ocr_dataset)
        self.ocr_threshold = 0.4

    def recognize_plate(self, image_path):
        try:
            R, _ = detect(self.ocr_net, self.ocr_meta, image_path, thresh=self.ocr_threshold, nms=None)
            if len(R):
                width, height = Image.open(image_path).size
                L = dknet_label_conversion(R, width, height)
                L = nms(L, 0.45)
                L.sort(key=lambda x: x.tl()[0])
                plate_text = ''.join([chr(l.cl()) for l in L])
                return plate_text
            else:
                return "No characters found"
        except Exception as e:
            print("Error occurred during plate recognition:", e)
            return None
