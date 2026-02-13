# EX-002-QWEN-VL: Qwen-2.5-VL Experiment Environment

이 폴더는 Qwen-2.5-VL 모델을 활용한 시각 언어 분석 실험을 위한 환경입니다.

## 📁 구조
- `test_bench.py`: 모델 연동 및 결과 저장을 위한 메인 실험 스크립트
- `main.py`: 간단한 추론 테스트용 스크립트
- `requirements.txt`: 필요한 라이브러리 목록
- `results/`: 실험 결과(텍스트 등)가 저장되는 폴더

## 🚀 시작하기

### 1. 환경 설정
`venv`를 활성화하거나 필요한 패키지를 설치합니다.
```bash
pip install -r requirements.txt
```

### 2. 실험 실행
분석하고 싶은 이미지 경로를 인자로 주어 실행합니다.
```bash
# 기본 샘플 테스트
python test_bench.py sample.jpg

# 복합 시나리오 최종 검증 (공항 터미널)
python test_bench.py final_verification.jpg
```

## 📝 실험 노트
- `final_verification.jpg`는 얼굴, 다수 객체, 텍스트(전광판), 복잡한 배경이 포함된 고난도 테스트용 이미지입니다.
- Qwen-2.5-VL 모델은 약 7B 파라미터 규모이므로 16GB 이상의 VRAM(GPU)이 권장됩니다.
- 첫 실행 시 Hugging Face에서 모델 가중치를 다운로드하므로 시간이 소요될 수 있습니다.
- `core/models/qwen_vl.py`의 구현체를 사용하여 프로젝트 전체와 일관된 인터페이스를 유지합니다.
