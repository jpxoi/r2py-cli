import logging
import os
from datetime import datetime

class Logger:
    _instance = None

    def __new__(cls, action='action', log_dir='logs'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup(action, log_dir)
        return cls._instance

    def _setup(self, action, log_dir):
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        log_filename = f'{action}-{timestamp}.log'
        log_path = os.path.join(log_dir, log_filename)
        self.logger = logging.getLogger(action)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        file_handler = logging.FileHandler(log_path, mode='w')
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger