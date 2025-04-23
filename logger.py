import logging
import os
from datetime import datetime
from typing import Optional

class Logger:
    _instances = {}

    def __new__(cls, action: str = 'action', log_dir: Optional[str] = None):
        key = (action, log_dir)
        if key not in cls._instances:
            instance = super().__new__(cls)
            instance._setup(action, log_dir)
            cls._instances[key] = instance
        return cls._instances[key]

    def _setup(self, action: str, log_dir: Optional[str]):
        if log_dir is None:
            log_dir = os.path.join(os.getcwd(), "logs")

        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        log_filename = f'{action}-{timestamp}.log'
        log_path = os.path.join(log_dir, log_filename)
        self.logger = logging.getLogger(action)
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_path, mode='w')
        file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)

        # Colored formatter for stream handler
        class ColoredFormatter(logging.Formatter):
            COLORS = {
                'WARNING': '\033[33m',  # yellow
                'ERROR': '\033[31m',    # red
                'CRITICAL': '\033[1;31m', # bold red
                'RESET': '\033[0m',
            }
            def format(self, record):
                msg = super().format(record)
                color = self.COLORS.get(record.levelname, '')
                reset = self.COLORS['RESET'] if color else ''
                return f"{color}{msg}{reset}"

        stream_handler = logging.StreamHandler()
        stream_formatter = ColoredFormatter('%(message)s')
        stream_handler.setFormatter(stream_formatter)
        stream_handler.setLevel(logging.WARNING)  # Only print WARNING and above to console

        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)
        self.logger.propagate = False

    def get_logger(self):
        return self.logger