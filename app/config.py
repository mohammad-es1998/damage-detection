import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)


class DevelopmentConfig(Config):
    DEBUG = os.getenv('DEBUG', True)


class ProductionConfig(Config):
    DEBUG = os.getenv('DEBUG', False)


class AI(Config):
    DETECTION_WEIGHT_PATH = os.getenv('DETECTION_WEIGHT_PATH',
                                      '/home/mohammad/Desktop/chal/app/ai/weights/lp-detector/wpod-net_update1')
    OCR_DATASET = os.getenv('OCR_DATASET', b'/home/mohammad/Desktop/chal/app/ai/weights/ocr/ocr-net.data')
    OCR_NETCFG = os.getenv('OCR_NETCFG', b'/home/mohammad/Desktop/chal/app/ai/weights/ocr/ocr-net.cfg')
    OCR_WEIGHT = os.getenv('OCR_WEIGHT', b'/home/mohammad/Desktop/chal/app/ai/weights/ocr/ocr-net.weights')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'ai': AI,
}
