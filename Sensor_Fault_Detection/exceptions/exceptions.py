import traceback2 as traceback
import sys, os
class SensorException(Exception):
    def __init__(self):
        super().__init__()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        self.line_no = exc_tb.tb_lineno
        self.message = str(exc_obj)
        self.filename = os.path.basename(exc_tb.tb_frame.f_code.co_filename)

    def __str__(self):
        return f"\nError occured in [{self.filename}], at line no [{self.line_no}], error message [{self.message}]"