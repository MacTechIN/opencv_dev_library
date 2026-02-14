# 🖼️ OpenCV 학습용 테스팅 보드

OpenCV의 내장 함수들을 카테고리별로 학습하고 테스트할 수 있는 교육용 웹 애플리케이션입니다.

## ✨ 주요 특징

- 📚 **216개 OpenCV 함수** 완벽 구현
- 🎯 **24개 카테고리**로 체계적 분류
- 🔄 **3단계 워크플로우**: 입력 → 처리 → 출력
- 📖 **한글 인터페이스**와 상세한 파라미터 설명
- 🔗 **OpenCV 공식 문서** 링크 제공
- 💻 **웹 브라우저**에서 즉시 실행

## 🎓 구현된 모듈

### 🔷 Core Module (31개 함수)
- Arithmetic Operations (산술 연산)
- Comparison Operations (비교 연산)
- Statistical Operations (통계 연산)
- Array Transforms (배열 변환)

### 🔶 Image Processing Module (155개 함수)
- Color Space Conversions - 20개
- ColorMaps in OpenCV - 22개
- Basic Filters - 8개
- Advanced Filters - 6개
- Morphological Operations
- Edge Detection
- Derivatives
- Thresholding
- Geometric Transforms
- Image Pyramids
- Contours
- Shape Analysis
- Feature Detection
- Histograms
- Drawing Functions
- Motion Analysis

### 🖥️ High-level GUI Module (21개 함수) ⭐ NEW!
- Window Management (윈도우 관리) - 8개
- Keyboard Input (키보드 입력) - 2개
- Trackbar (트랙바) - 6개
- ROI Selection (ROI 선택) - 2개
- Mouse Events (마우스 이벤트) - 2개
- Image Display (이미지 표시) - 1개

## 🚀 빠른 시작

### 설치
```bash
npm install
```

### 실행
```bash
npm run dev
```

### 카테고리 전환 (OpenCV 공식 구조)
```bash
npm run apply-categories
```

## 📖 문서

- **[CURRENT_STATUS.md](CURRENT_STATUS.md)** - 현재 상태 및 전체 개요
- **[HIGHGUI_FUNCTIONS_ADDED.md](HIGHGUI_FUNCTIONS_ADDED.md)** - High-level GUI 함수 추가 내역
- **[CATEGORY_UPDATE_README.md](CATEGORY_UPDATE_README.md)** - 카테고리 업데이트 상세 가이드
- **[QUICK_START.md](QUICK_START.md)** - 빠른 시작 가이드
- **[SCRIPT_FEATURES.md](SCRIPT_FEATURES.md)** - 스크립트 기능 상세

## 🎯 사용 방법

### 1️⃣ 이미지 업로드
- 이미지 파일을 업로드하거나
- 샘플 이미지 사용

### 2️⃣ 함수 선택
- 카테고리에서 원하는 함수 선택
- 함수 설명 및 문법 확인

### 3️⃣ 파라미터 조정
- 각 파라미터를 슬라이더나 드롭다운으로 조정
- 실시간으로 결과 미리보기

### 4️⃣ 결과 저장
- 처리된 이미지 다운로드
- 다른 함수로 추가 처리

## 📊 전체 통계

| 항목 | 개수 |
|------|------|
| **전체 함수** | **216개** |
| Core 모듈 | 31개 |
| Image Processing 모듈 | 155개 |
| High-level GUI 모듈 | 21개 |
| **Motion Analysis** | **17개** |
| 현재 카테고리 | 24개 |

## 🔧 기술 스택

- **React** + **TypeScript**
- **Tailwind CSS** v4
- **opencv-ts** (OpenCV for Web)
- **Vite**

## 📝 카테고리 구조

### 현재 구조 (24개 - 학습 편의)
세분화된 카테고리로 학습하기 쉬운 구조

### OpenCV 공식 구조 (15개 - 표준 준수)
스크립트로 언제든지 전환 가능:
```bash
npm run apply-categories
```

## 🎨 High-level GUI 기능 ⭐ NEW!

### 윈도우 관리
- namedWindow, destroyWindow, resizeWindow, moveWindow 등

### 사용자 입력
- waitKey, pollKey (키보드)
- setMouseCallback, getMouseWheelDelta (마우스)

### 대화형 컨트롤
- createTrackbar, setTrackbarPos (트랙바)
- selectROI, selectROIs (관심 영역 선택)

### 이미지 표시
- imshow (이미지 표시)

## 💡 예제 함수

### 색상 변환
- `cvtColor` - RGB ↔ Gray, HSV, LAB 등
- `applyColorMap` - 22가지 컬러맵

### 필터링
- `GaussianBlur` - 가우시안 블러
- `medianBlur` - 미디언 블러
- `bilateralFilter` - 양방향 필터

### 엣지 검출
- `Canny` - 캐니 엣지
- `Sobel` - 소벨 필터
- `Laplacian` - 라플라시안

### 형태학 연산
- `erode` - 침식
- `dilate` - 팽창
- `morphologyEx` - 모폴로지 연산

### GUI 컨트롤 ⭐
- `createTrackbar` - 슬라이더 생성
- `selectROI` - 영역 선택
- `setMouseCallback` - 마우스 이벤트

## 🌟 교육적 가치

### 학생들이 배우는 내용

1. **OpenCV 함수 구조**
   - 함수 이름, 파라미터, 반환값
   - 정확한 문법 및 사용법

2. **파라미터의 역할**
   - 각 파라미터가 결과에 미치는 영향
   - 최적 값 찾기

3. **이미지 처리 이론**
   - 색상 공간, 필터링, 형태학, 엣지 검출 등
   - 실시간 결과로 즉각적인 피드백

4. **GUI 프로그래밍** ⭐
   - 윈도우 관리 및 사용자 입력 처리
   - 대화형 애플리케이션 개발

## 🔄 최근 업데이트 (2026-02-13)

### ✅ Motion Analysis 모듈 확장 ⭐ NEW!
- 9개 Optical Flow 및 Motion Estimation 함수 추가
- Lucas-Kanade, Farneback, SimpleFlow 알고리즘
- 아핀 변환 추정, ECC 변환
- 광학 흐름 I/O 기능

### ✅ High-level GUI 모듈 추가
- 21개 GUI 관련 함수 추가
- 윈도우, 트랙바, 마우스, 키보드 제어
- 웹 환경 시뮬레이션 구현

### ✅ 함수 개수 확장
- 186개 → **216개** (+30개)

### ✅ 카테고리 추가
- 23개 → **24개** (+1개)

## 🚀 향후 계획

- [ ] Video I/O 모듈
- [ ] Object Detection 모듈
- [ ] Feature2D 모듈
- [ ] Camera Calibration
- [ ] DNN (Deep Neural Networks)

## 📚 참고 자료

- [OpenCV 공식 문서](https://docs.opencv.org/4.x/)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [opencv-ts GitHub](https://github.com/opencv/opencv)

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

---

**버전**: 2.1.0  
**최종 업데이트**: 2026-02-13  
**함수 개수**: 216개  
**카테고리**: 24개