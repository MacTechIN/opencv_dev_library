# VisionAI-Platform 🚀

본 플랫폼은 OpenCV와 Deep Learning 기술을 체계적으로 실험, 보관 및 재사용하기 위한 모듈형 개발 환경입니다. 신규 프로젝트에 기술을 신속하게 도입할 수 있도록 **확장성, 개방성, 재사용성**을 핵심 가치로 설계되었습니다. 
본 라이브러리는 OpenCV 기본 함수 라이브러리 와 함께 실제 Application 개발시 필요한 여러 기능들을 별도로 모아 라이브러리고 구축하는 것을 목적으로 제작 되었습니다. 
---

## 🌟 핵심 가치 (Core Values)
- **확장성 (Scalability)**: 새로운 알고리즘과 엔진(YOLOv8, MediaPipe 등)을 유연하게 추가.
- **개방성 (Openness)**: 표준 인터페이스를 통해 다양한 라이브러리와 원활한 연동.
- **재사용성 (Reusability)**: 핵심 기능을 라이브러리화하여 다른 프로젝트에 즉시 이식 가능.

## 🛠 핵심 설계 원칙
1. **모듈화 (Modularization)**: 기능별로 코드를 분리하여 독립성과 이식성 확보.
2. **추적성 (Traceability)**: 모든 실험 환경, 데이터, 메트릭 및 변경 사항을 체계적으로 기록.

---

## 📂 프로젝트 디렉토리 구조
```text
VisionAI-Platform/
├── core/                # 재사용 가능한 핵심 모듈 (Library)
│   ├── base/            # 인터페이스 및 추상 클래스 (processor.py 등)
│   ├── processing/      # 전처리 및 후처리 (Filter, ROI, Augmentation)
│   └── models/          # 개별 엔진 래퍼 (YOLOv8, MediaPipe, etc.)
├── experiments/         # 기술 검증 및 실험 로깅 (EX-000-NAME 형식)
│   ├── EX-001-FACE/     # 얼굴 인식 테스트 예시
│   │   ├── main.py      # 실험 실행 코드
│   │   ├── results/     # 로그, 스크린샷, 벤치마킹 데이터
│   │   └── report.md    # 실험 결과 분석 보고서
├── assets/              # 공유 자원
│   ├── weights/         # 모델 가중치 파일 (.onnx, .pt, .pb)
│   └── configs/         # 모델 설정 파일 (.yaml, .json)
├── examples/            # 신규 프로젝트 적용을 위한 레퍼런스 코드
├── docs/                # 기술 검색 및 유지보수를 위한 문서화 (Tags, How-to)
└── README.md            # 프로젝트 개요 메인 문서
```

---

## 📝 변경 이력 관리 규칙 (History Tracking)
각 주요 디렉토리에는 `{directory_name}+history.md` 파일이 존재하며, 모든 변경 사항은 아래 형식에 맞춰 기록합니다.

**기록 형식:**
`[날짜][시간] : "변경 사항 요약 정리" , [깃허브 푸쉬 버전]`

**대상 디렉토리:**
- `core/`, `experiments/`, `assets/`, `examples/`, `docs/`

---

## 🚀 시작하기 (Quick Start)
1. `core/base/processor.py`를 상속받아 새로운 영상 처리 프로세서를 구현하세요.
2. `experiments/` 폴더 내에 실험 폴더를 생성하고 기술을 검증하세요.
3. 실험 결과는 각 실험 폴더의 `results/`와 `report.md`에 상세히 기록하세요.

## 본 라이브라리의 운영 규칙 
docs 아래 Library-Guide.md에 상세히 기술되어 있습니다. 
Git 버전 관리 규정은 docs/Git-Version-Control-Guide.md에 상세히 기술되어 있습니다. 
Qwen-VL 모델 사용법은 docs/Qwen-VL-Usage.md에 상세히 기술되어 있습니다. 


본 프로젝트의 소유권은 Sam LEE (Hotnewton@kore.ac.kr)에게 있습니다.  다만 라이브러리 사용에 있어서는 자유롭게 업데이트 및 사용하셔도 좋습니다
출처만 밝혀 주시기 바랍니다. 

2026년 2월13일  13일의 금요일 오후 3시 58분  케나다 윈저에서...Sam LEE 드림

