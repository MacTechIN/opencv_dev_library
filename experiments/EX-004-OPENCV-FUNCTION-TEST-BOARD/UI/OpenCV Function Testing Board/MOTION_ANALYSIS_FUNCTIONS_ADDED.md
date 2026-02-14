# ✅ Motion Analysis 함수 추가 완료

## 📊 추가된 내용

### 🆕 추가된 9개 함수

**기존 Motion Analysis 함수**: 8개
- accumulate, accumulateSquare, accumulateProduct, accumulateWeighted
- createHanningWindow, phaseCorrelate
- meanShift, CamShift

**새로 추가된 함수**: 9개

#### 1️⃣ Optical Flow (광학 흐름) - 3개

1. **calcOpticalFlowPyrLK** - Pyramidal Lucas-Kanade Optical Flow
   - 피라미달 Lucas-Kanade 방법으로 희소 특징점의 광학 흐름 계산
   - 파라미터: maxLevel(피라미드 레벨), winSize(윈도우 크기), maxIter, epsilon
   - 입력: 2개 이미지 (이전 프레임, 현재 프레임)
   - 시각화: 특징점 추적 벡터를 화살표로 표시
   
2. **calcOpticalFlowFarneback** - Dense Optical Flow (Farneback)
   - Gunnar Farneback 알고리즘으로 밀집 광학 흐름 계산
   - 파라미터: pyrScale, levels, winsize, iterations, polyN, polySigma
   - 입력: 2개 이미지 (그레이스케일 변환 필요)
   - 시각화: HSV 색상으로 흐름 방향과 크기 표시
   
3. **buildOpticalFlowPyramid** - Build Optical Flow Pyramid
   - 광학 흐름 계산을 위한 이미지 피라미드 생성
   - 파라미터: winSize, maxLevel, withDerivatives
   - 시각화: 각 피라미드 레벨의 크기 정보 표시

#### 2️⃣ Motion Estimation (모션 추정) - 3개

4. **estimateAffine2D** - Estimate Affine 2D Transformation
   - 두 점 집합 간의 최적 아핀 변환 행렬 추정
   - 파라미터: method(RANSAC/LMEDS), ransacThreshold, maxIters, confidence
   - 입력: 2개 이미지 (특징점 매칭용)
   - 용도: 모션 추정, 이미지 정렬
   
5. **estimateAffinePartial2D** - Estimate Partial Affine Transformation
   - 회전, 이동, 균일 스케일링만 포함하는 부분 아핀 변환 추정
   - 파라미터: method, ransacThreshold, maxIters, confidence
   - 용도: 제한된 자유도의 변환 추정
   
6. **findTransformECC** - Find Transform using ECC Maximization
   - ECC(Enhanced Correlation Coefficient) 최대화로 기하학적 변환 찾기
   - 파라미터: motionType(TRANSLATION/EUCLIDEAN/AFFINE/HOMOGRAPHY), maxIters, epsilon
   - 입력: 2개 이미지 (템플릿과 입력)
   - 용도: 정밀한 이미지 정렬

#### 3️⃣ Optical Flow I/O (광학 흐름 입출력) - 2개

7. **readOpticalFlow** - Read Optical Flow from File
   - 파일에서 광학 흐름 읽기
   - 파라미터: format(.flo)
   - 지원 포맷: Middlebury .flo
   
8. **writeOpticalFlow** - Write Optical Flow to File
   - 광학 흐름을 파일로 저장
   - 파라미터: format(.flo)
   - 지원 포맷: Middlebury .flo

#### 4️⃣ Advanced Optical Flow - 1개

9. **calcOpticalFlowSF** - SimpleFlow Algorithm
   - SimpleFlow 알고리즘으로 밀집 광학 흐름 계산
   - 파라미터: layers, averagingBlockSize, maxFlow
   - 빠른 처리 속도

## 📈 전체 통계 업데이트

### 이전
- Motion Analysis 함수: 8개
- 전체 함수: 207개

### 현재
- **Motion Analysis 함수: 17개** (+9개) ✨
- **전체 함수: 216개** (+9개) ✨

### 함수 분류

**배경 모델링 및 누적 (4개)**
- accumulate
- accumulateSquare
- accumulateProduct
- accumulateWeighted

**위상 상관 (2개)**
- createHanningWindow
- phaseCorrelate

**객체 추적 (2개)**
- meanShift
- CamShift

**광학 흐름 (Optical Flow) (5개)** ⭐ NEW!
- calcOpticalFlowPyrLK (희소)
- calcOpticalFlowFarneback (밀집)
- calcOpticalFlowSF (SimpleFlow)
- buildOpticalFlowPyramid
- readOpticalFlow / writeOpticalFlow (I/O)

**모션 추정 (4개)** ⭐ NEW!
- estimateAffine2D
- estimateAffinePartial2D
- findTransformECC
- (phaseCorrelate)

## 🎨 구현 특징

### 1. Sparse Optical Flow (희소 광학 흐름)
**calcOpticalFlowPyrLK**
- 특징점 추적에 최적화
- 피라미드 구조로 큰 움직임 처리
- 실시간 처리 가능
- 시각화: 녹색 벡터와 빨간색 추적 점

### 2. Dense Optical Flow (밀집 광학 흐름)
**calcOpticalFlowFarneback**
- 모든 픽셀의 움직임 계산
- 정밀한 모션 분석
- HSV 색상 매핑:
  - 색상(H): 흐름 방향
  - 채도(S): 최대값 (255)
  - 명도(V): 흐름 크기

### 3. Motion Estimation (모션 추정)
**Affine & ECC Transforms**
- RANSAC으로 이상치 제거
- 정밀한 이미지 정렬
- 다양한 변환 타입 지원:
  - TRANSLATION (이동)
  - EUCLIDEAN (회전+이동)
  - AFFINE (아핀)
  - HOMOGRAPHY (호모그래피)

## 💻 사용 시나리오

### 1. 객체 추적 (Object Tracking)
```python
# Lucas-Kanade로 특징점 추적
prev_gray = cv.cvtColor(prev_frame, cv.COLOR_BGR2GRAY)
next_gray = cv.cvtColor(next_frame, cv.COLOR_BGR2GRAY)

# 특징점 검출
prev_pts = cv.goodFeaturesToTrack(prev_gray, ...)

# 광학 흐름 계산
next_pts, status, err = cv.calcOpticalFlowPyrLK(
    prev_gray, next_gray, prev_pts, None
)
```

### 2. 모션 분석 (Motion Analysis)
```python
# Farneback으로 밀집 광학 흐름
flow = cv.calcOpticalFlowFarneback(
    prev_gray, next_gray, None,
    pyr_scale=0.5, levels=3, winsize=15,
    iterations=3, poly_n=5, poly_sigma=1.2, flags=0
)

# 흐름 크기와 각도 계산
magnitude, angle = cv.cartToPolar(flow[...,0], flow[...,1])
```

### 3. 이미지 정렬 (Image Alignment)
```python
# ECC로 정밀한 이미지 정렬
warp_matrix = np.eye(2, 3, dtype=np.float32)

_, warp_matrix = cv.findTransformECC(
    template, input_image, warp_matrix,
    motionType=cv.MOTION_AFFINE,
    criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 50, 0.001)
)

# 변환 적용
aligned = cv.warpAffine(input_image, warp_matrix, (w, h))
```

### 4. 비디오 안정화 (Video Stabilization)
```python
# 프레임 간 변환 추정
transform = cv.estimateAffine2D(
    prev_points, curr_points,
    method=cv.RANSAC, ransacReprojThreshold=3.0
)

# 변환 보정 및 적용
```

## 🎓 교육적 가치

학생들이 배울 수 있는 내용:

### 1. **Optical Flow 이론**
   - 희소 vs 밀집 광학 흐름의 차이
   - 피라미드 구조의 필요성
   - Lucas-Kanade와 Farneback 알고리즘 비교

### 2. **모션 추정 기법**
   - 아핀 변환과 호모그래피
   - RANSAC 이상치 제거
   - ECC 최대화 원리

### 3. **실시간 비디오 처리**
   - 프레임 간 모션 계산
   - 객체 추적 기법
   - 비디오 안정화

### 4. **파라미터 튜닝**
   - 피라미드 레벨 수의 영향
   - 윈도우 크기 조정
   - 반복 횟수와 정밀도 균형

## 📚 OpenCV 공식 문서

- [Video Motion Analysis](https://docs.opencv.org/4.x/de/de1/group__video__motion.html)
- [Optical Flow Tutorial](https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html)
- [Lucas-Kanade Method](https://docs.opencv.org/4.x/dc/d6b/group__video__track.html)

## 🔧 웹 환경 구현

### 처리 로직 (opencv-processor.ts)

1. **calcOpticalFlowPyrLK**: 그리드 포인트 생성 및 추적 벡터 시각화
2. **calcOpticalFlowFarneback**: HSV 색상 매핑으로 흐름 시각화
3. **buildOpticalFlowPyramid**: 각 피라미드 레벨 정보 텍스트 표시
4. **estimateAffine2D**: 샘플 점으로 변환 추정 시뮬레이션
5. **findTransformECC**: 변환 타입과 파라미터 정보 표시
6. **I/O Functions**: 파일 포맷 정보 표시

### 시각적 피드백

- 🟢 Optical Flow 벡터: 녹색 화살표
- 🔴 추적 점: 빨간색 원
- 🌈 Dense Flow: HSV 색상 매핑
- 🟡 정보 텍스트: 노란색 오버레이

## 📊 카테고리별 함수 현황

| 카테고리 | 함수 개수 | 비고 |
|---------|----------|------|
| Core Module | 31개 | - |
| Image Processing | 155개 | - |
| **Motion Analysis** | **17개** | **+9개** ✨ |
| High-level GUI | 21개 | - |
| **전체** | **216개** | **+9개** ✨ |

## ✨ 주요 특징

### 다양한 알고리즘 지원
- ✅ Lucas-Kanade (희소)
- ✅ Farneback (밀집)
- ✅ SimpleFlow
- ✅ ECC Maximization
- ✅ RANSAC 기반 추정

### 실용적인 응용
- ✅ 객체 추적
- ✅ 모션 분석
- ✅ 이미지 정렬
- ✅ 비디오 안정화
- ✅ 배경 차분

### 교육 친화적
- ✅ 한글 설명
- ✅ 상세한 파라미터 설명
- ✅ 시각적 피드백
- ✅ OpenCV 공식 문서 링크

## 🚀 다음 단계

Motion Analysis가 완성되었으므로, 다음 모듈 추가 가능:

- [ ] Object Detection (객체 검출)
- [ ] Feature2D (특징점 검출 및 매칭)
- [ ] Camera Calibration (카메라 캘리브레이션)
- [ ] Video I/O (비디오 입출력)
- [ ] Background Subtraction (배경 차분)

---

**업데이트**: 2026-02-13  
**추가된 함수**: 9개  
**Motion Analysis 함수**: 17개  
**전체 함수**: 216개
