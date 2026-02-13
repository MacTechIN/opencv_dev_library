import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class VisionLogger:
    """
    고효율 통합 로깅 시스템.
    콘솔 출력과 파일 기록을 동시에 제공하며, 로그 로테이션을 통해 디스크 공간을 관리합니다.
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

        # 로그 디렉토리 생성
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 포맷 설정
        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 파일 핸들러 (5MB 단위로 로테이션, 최대 5개 유지)
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, "vision_ai.log"),
            maxBytes=5*1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)

        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

def get_logger(name="VisionAI"):
    """모듈별 로거 인스턴스를 반환하는 편의 함수"""
    return VisionLogger(name)
