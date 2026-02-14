# OpenCV Function Testing Board (EX-004)

## 📌 Project Overview
"OpenCV 학습용 테스팅 보드를 만들어드리겠습니다. 먼저 OpenCV.js의 구조를 파악하고, 학생들이 쉽게 배울 수 있는 직관적인 UI를 설계하겠습니다."

### 🎯 Objective
- 카테고리별로 함수 분류 (이미지 처리, 기하학 변환, 필터링, 엣지 검출 등)
- 각 함수의 파라미터를 자동으로 분석하여 입력 UI 생성
- 실시간 미리보기 및 결과 저장 기능
- 이미지와 비디오 모두 지원

## 🏗️ Design Direction
1. **OpenCV.js Core Analysis**: 브라우저에서 동작하는 OpenCV.js의 주요 모듈 및 함수 매핑.
2. **Dynamic UI Generation**: 함수의 인자(Type, Range, Default)를 분석하여 슬라이더, 체크박스 등 자동 생성.
3. **Real-time Pipeline**: WebWorker를 활용하여 메인 스레드 차단 없이 실시간 필터링 적용.
4. **Universal Media Support**: HTML5 Canvas 및 Video 요소를 활용한 범용 입력 인터페이스.

## 💻 Environment Setup (Pre-analysis)
- **Virtual Environment**:
    - **Python**: 이미지 데이터셋 관리나 서버 사이드 전처리가 필요할 경우 필요. (`.venv` 추천)
    - **Node.js**: 웹 어플리케이션 개발 환경(Vite, React 등) 구축을 위해 **필수**. (`npm` 사용)
- **Framework Choice**: 빠른 프로토타이핑을 위해 **React + Vite** 조합을 추천합니다.

## 🗂️ OpenCV.js Function Categories (Draft)
1. **Core Operations**: Image I/O (`imread`, `imshow`), ROI, Arithmetic.
2. **Image Processing**: Color conversions (`cvtColor`), Thresholding (`threshold`, `adaptiveThreshold`).
3. **Filtering**: Blurring (`GaussianBlur`, `medianBlur`), Morpological (`erode`, `dilate`, `morphologyEx`).
4. **Transformations**: Geometric (`resize`, `warpAffine`, `warpPerspective`), Pyramids.
5. **Feature Detection**: Edge detection (`Canny`), Gradients (`Sobel`).
6. **Object Detection**: Haar Cascades (Face, Eyes).
- [ ] [Phase 1] OpenCV.js API 구조 분석 및 분류
- [ ] [Phase 2] 동적 UI 생성 엔진 설계
- [ ] [Phase 3] 실시간 미리보기 시스템 구현
- [ ] [Phase 4] 이미지/비디오 입출력 모듈 통합
