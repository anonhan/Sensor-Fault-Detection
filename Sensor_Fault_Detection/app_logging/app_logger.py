import logging
class AppLogger:
    def __init__(self, file_object=None):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # If a file object is provided, create a file handler and set the formatter
        if file_object:
            file_handler = logging.StreamHandler(file_object)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Create a console handler and set the formatter
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, message, level=logging.INFO):
        # Log with the specified log level
        if level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.INFO:
            self.logger.info(message)
        elif level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.CRITICAL:
            self.logger.critical(message)
        else:
            self.logger.info(message)