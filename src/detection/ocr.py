# Este archivo tendra como objetivo almacenar la configuracion y la inicializacion del modelo de OCR, 
# para ser utilizado por detector.py

'''
## CODIGO PARA SILENCIAR EL LOG DEL OCR, PARA QUE NO APAREZCA EN LA CONSOLA

from config import DEBUG, OCR_LANG, OCR_ENABLE_MKLDNN

from contextlib import redirect_stdout, redirect_stderr
from paddleocr import PaddleOCR
import logging
import os

_ocr_instance = None

def get_ocr():
    global _ocr_instance

    if _ocr_instance is None:
        def create_model():
            return PaddleOCR(
                lang=OCR_LANG,
                enable_mkldnn=OCR_ENABLE_MKLDNN,      
            )

        if DEBUG:
            _ocr_instance = create_model()
        else:         
            os.environ["GLOG_minloglevel"] = "2"
            os.environ["FLAGS_log_level"] = "2"

            logging.getLogger().setLevel(logging.ERROR)
            logging.getLogger("paddlex").setLevel(logging.ERROR)
            logging.getLogger("paddle").setLevel(logging.ERROR)
            logging.getLogger("ppocr").setLevel(logging.ERROR)

            with open(os.devnull, "w") as f:
                with redirect_stdout(f), redirect_stderr(f):
                    _ocr_instance = create_model()

    return _ocr_instance'''

from paddleocr import PaddleOCR

_ocr_instance = None

def get_ocr():
    global _ocr_instance
    
    if _ocr_instance is None:
        _ocr_instance = PaddleOCR(
            lang="en",
            enable_mkldnn=False
        )
    
    return _ocr_instance