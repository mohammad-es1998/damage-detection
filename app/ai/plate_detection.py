import cv2
from app.ai.darknet_lib.utils.keras_utils import load_model, detect_lp
from app.ai.darknet_lib.utils.utils import im2single


class PlateDetector:
    detection_net = None

    def __init__(self, weight_path):
        self.weight_path = weight_path
        self.lp_threshold = .5

    def load_model(self):
        if PlateDetector.detection_net is None:
            PlateDetector.detection_net = load_model(self.weight_path)
            print("Detection model loaded")

    def detect_plate(self, image_path):
        self.load_model()

        Ivehicle = cv2.imread(image_path)
        ratio = float(max(Ivehicle.shape[:2])) / min(Ivehicle.shape[:2])
        side = int(ratio * 288.)
        bound_dim = min(side + (side % (2 ** 4)), 608)
        print("\t\tBound dim: %d, ratio: %f" % (bound_dim, ratio))

        Llp, LlpImgs, _ = detect_lp(PlateDetector.detection_net, im2single(Ivehicle), bound_dim, 2 ** 4, (240, 80),
                                    self.lp_threshold)

        if len(LlpImgs):
            Ilp = LlpImgs[0]
            Ilp = cv2.cvtColor(Ilp, cv2.COLOR_BGR2GRAY)
            Ilp = cv2.cvtColor(Ilp, cv2.COLOR_GRAY2BGR)

            detected_plate_path = b'detected_plate.png'
            cv2.imwrite(detected_plate_path.decode('utf-8'), Ilp * 255.)
            return detected_plate_path
        return None
