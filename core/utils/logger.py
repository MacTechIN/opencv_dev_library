import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class VisionLogger:
    """
    High-efficiency unified logging system.
    Provides simultaneous console output and file recording, 
    managing disk space through log rotation.
    """
    _instances = {}

    def __new__(cls, name="VisionAI"):
        if name not in cls._instances:
            instance = super(VisionLogger, cls).__new__(cls)
            instance._setup_logger(name)
            cls._instances[name] = instance.logger
        return cls._instances[name]

    def _setup_logger(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        if self.logger.handlers:
            return

        # Create log directory
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Formatter configuration
        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # File handler (Rotate every 5MB, maintain up to 5 backups)
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, "vision_ai.log"),
            maxBytes=5*1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Check terminal live streaming bit (enabled only if VISION_LIVE_LOG=1)
        live_log_bit = os.getenv("VISION_LIVE_LOG", "0").lower()
        if live_log_bit in ("1", "true", "on"):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

def get_logger(name="VisionAI"):
    """Convenience function to return module-specific logger instances"""
    return VisionLogger(name)
