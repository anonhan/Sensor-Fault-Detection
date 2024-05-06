import sys
import traceback2 as traceback
import os

class SensorException(Exception):
    def __init__(self):
        tb = traceback.extract_tb(sys.exc_info()[2])[-1]
        self.line_no = tb[1]
        self.file_name = os.path.basename(tb[0])
        self.error_message = str(sys.exc_info()[1])

    def __str__(self):
        return f"Error in file [{self.file_name}], line no [{self.line_no}], Error [{self.error_message}]"
