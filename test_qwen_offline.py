import os
import sys

# 프로젝트 루트를 경로에 추가
sys.path.append(os.getcwd())

from core.models.qwen_vl import QwenVLProcessor
from core.utils.logger import get_logger

logger = get_logger("TestOffline")

def test_load():
    logger.info("🧪 Testing Qwen-2.5-VL Offline Loading...")
    
    # QwenVLProcessor 인스턴스 생성 (내부적으로 _initialize_model 호출)
    try:
        processor = QwenVLProcessor()
        
        if processor.model is not None and processor.processor is not None:
            logger.info("✅ Success: Model and Processor loaded from local path.")
        else:
            logger.error("❌ Failure: Model or Processor is None.")
            
    except Exception as e:
        logger.error(f"❌ Exception occurred: {e}")

if __name__ == "__main__":
    test_load()
