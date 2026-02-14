# OpenCV 카테고리 업데이트 가이드

## 📋 개요

이 문서는 OpenCV 테스팅 보드의 함수 카테고리를 **OpenCV 공식 문서 구조**에 맞게 업데이트하는 방법을 설명합니다.

스크립트 실행 시 **각 카테고리별 전체 함수 목록**이 자동으로 표시됩니다.

## 🎯 목적

현재 카테고리 구조를 OpenCV 공식 문서의 계층 구조에 맞춰 재구성:
- **Main modules** → **Sub categories** → **Functions**
- 각 카테고리에 속한 모든 함수를 자동으로 출력

## 📂 현재 구조 vs 목표 구조

### 현재 구조 (23개 카테고리)
```
Image Processing (imgproc) - 17개
├── color - Color Conversions
├── colormap - ColorMaps
├── filter - Basic Filters
├── advanced_filter - Advanced Filters
├── morphology - Morphological Operations
├── edge - Edge Detection
├── derivative - Derivatives
├── threshold - Thresholding
├── transform - Geometric Transforms
├── pyramid - Image Pyramids
├── contour - Contours
├── shape - Shape Analysis
├── feature - Feature Detection
├── histogram - Histograms
├── drawing - Drawing Functions
├── motion - Motion Analysis
└── misc - Miscellaneous

Core (core) - 5개
├── basic - Basic Operations
├── arithmetic - Arithmetic Operations
├── matrix - Matrix Operations
├── statistical - Statistical Operations
└── comparison - Comparison Operations
```

### 목표 구조 (OpenCV 공식 문서 기준)

```
Core Module (core) - 5개 카테고리
├── core_array_arithmetic - Arithmetic Operations
├── core_array_logic - Logical Operations
├── core_array_comparison - Comparison Operations
├── core_array_stats - Statistical Operations
└── core_array_transform - Array Transforms

Image Processing Module (imgproc) - 10개 카테고리
├── imgproc_filter - Image Filtering
├── imgproc_geometric - Geometric Transformations
├── imgproc_misc - Miscellaneous Transformations
├── imgproc_drawing - Drawing Functions
├── imgproc_colormap - ColorMaps in OpenCV
├── imgproc_color - Color Space Conversions
├── imgproc_shape - Structural Analysis and Shape Descriptors
├── imgproc_motion - Motion Analysis and Object Tracking
├── imgproc_feature - Feature Detection
└── imgproc_hist - Histograms
```

## 🔧 카테고리 매핑 테이블

| 현재 카테고리 | OpenCV 공식 카테고리 | 설명 |
|--------------|---------------------|------|
| `color` | `imgproc_color` | Color Space Conversions |
| `colormap` | `imgproc_colormap` | ColorMaps in OpenCV |
| `filter` | `imgproc_filter` | Image Filtering (Basic) |
| `advanced_filter` | `imgproc_filter` | Image Filtering (Advanced) |
| `morphology` | `imgproc_filter` | Morphological Operations → Filtering |
| `edge` | `imgproc_feature` | Edge Detection → Feature Detection |
| `derivative` | `imgproc_filter` | Derivatives → Filtering |
| `threshold` | `imgproc_misc` | Thresholding → Misc Transformations |
| `transform` | `imgproc_geometric` | Geometric Transforms |
| `pyramid` | `imgproc_geometric` | Image Pyramids → Geometric |
| `contour` | `imgproc_shape` | Contours → Shape Descriptors |
| `shape` | `imgproc_shape` | Structural Analysis and Shape Descriptors |
| `feature` | `imgproc_feature` | Feature Detection |
| `histogram` | `imgproc_hist` | Histograms |
| `drawing` | `imgproc_drawing` | Drawing Functions |
| `motion` | `imgproc_motion` | Motion Analysis and Object Tracking |
| `misc` | `imgproc_misc` | Miscellaneous Transformations |
| `basic` | `core_array_arithmetic` | Basic Operations → Arithmetic |
| `arithmetic` | `core_array_arithmetic` | Arithmetic Operations |
| `matrix` | `core_array_transform` | Matrix Operations → Array Transforms |
| `statistical` | `core_array_stats` | Statistical Operations |
| `comparison` | `core_array_comparison` | Comparison Operations |

## 🚀 사용 방법

### 방법 1: npm 스크립트 사용 (권장)

```bash
npm run apply-categories
```

이 명령어는 자동으로:
1. 카테고리 매핑 적용
2. `/src/app/data/opencv-functions.ts` 파일 업데이트
3. 백업 파일 생성 (`.backup` 확장자)

### 방법 2: Node.js 스크립트 직접 실행

```bash
node apply-categories-now.mjs
```

### 방법 3: Python 스크립트 사용

```bash
python update-categories.py
```

### 방법 4: Bash 스크립트 사용

```bash
chmod +x update-categories.sh
./update-categories.sh
```

## 📝 스크립트 파일 설명

### 1. `apply-categories-now.mjs` (Node.js)
- **언어**: JavaScript (ES Module)
- **용도**: 메인 업데이트 스크립트
- **특징**: 
  - 자동 백업 생성
  - 파일 읽기/쓰기
  - 정규식 기반 카테고리 교체

### 2. `update-categories.py` (Python)
- **언어**: Python 3
- **용도**: Python 환경에서 실행
- **특징**:
  - 백업 파일 생성
  - 간단한 문자열 교체

### 3. `update-categories.sh` (Bash)
- **언어**: Bash Shell
- **용도**: Unix/Linux 환경에서 실행
- **특징**:
  - `sed` 명령어 사용
  - 빠른 일괄 교체

## ⚠️ 주의사항

1. **백업 생성**: 모든 스크립트는 자동으로 백업 파일을 생성합니다
   - 백업 위치: `/src/app/data/opencv-functions.ts.backup`

2. **되돌리기**: 문제 발생 시 백업 파일로 복구
   ```bash
   cp /src/app/data/opencv-functions.ts.backup /src/app/data/opencv-functions.ts
   ```

3. **검증**: 업데이트 후 반드시 애플리케이션 테스트
   ```bash
   # 카테고리 확인
   grep "category:" /src/app/data/opencv-functions.ts | sort | uniq -c
   ```

## 📊 예상 결과

업데이트 후:
- **23개 카테고리** → **15개 카테고리**로 통합
- **160개 함수**는 그대로 유지
- OpenCV 공식 문서 구조와 일치
- **각 카테고리별 전체 함수 목록이 자동으로 출력됨**

### 스크립트 실행 시 출력 예시

```
🚀 OpenCV 카테고리 업데이트 시작...

📖 파일 읽는 중: src/app/data/opencv-functions.ts
💾 백업 생성 중: src/app/data/opencv-functions.ts.backup

📝 categories 배열 업데이트 중...
📝 함수 카테고리 업데이트 중...

  ✓ 'color' → 'imgproc_color' (20개 함수)
  ✓ 'colormap' → 'imgproc_colormap' (22개 함수)
  ✓ 'filter' → 'imgproc_filter' (8개 함수)
  ...

💾 파일 저장 중: src/app/data/opencv-functions.ts

✅ 카테고리 업데이트 완료!
   총 160개 함수의 카테고리가 변경되었습니다.

📋 결과:
   - 23개 카테고리 → 15개 카테고리
   - OpenCV 공식 문서 구조 적용 완료

================================================================================
📊 카테고리별 함수 목록

🔷 CORE MODULE - Operations on Arrays

  Arithmetic Operations (12개)
  ------------------------------------------------------------
   1. Add (add)
   2. Subtract (subtract)
   3. Multiply (multiply)
   ...

  Comparison Operations (4개)
  ------------------------------------------------------------
   1. Compare (compare)
   2. In Range (inRange)
   ...

  Statistical Operations (7개)
  ------------------------------------------------------------
   1. Mean (mean)
   2. Standard Deviation (meanStdDev)
   ...

  Array Transforms (8개)
  ------------------------------------------------------------
   1. Transpose (transpose)
   2. Flip (flip)
   ...


🔶 IMAGE PROCESSING MODULE

  Color Space Conversions (20개)
  ------------------------------------------------------------
   1. Convert Color (cvtColor)
   2. RGB to Gray (cvtColorRGBToGray)
   ...

  ColorMaps in OpenCV (22개)
  ------------------------------------------------------------
   1. Apply ColorMap - Autumn (applyColorMapAutumn)
   2. Apply ColorMap - Bone (applyColorMapBone)
   ...

  Image Filtering (14개)
  ------------------------------------------------------------
   1. Blur (blur)
   2. Gaussian Blur (GaussianBlur)
   ...

  ... (기타 모든 카테고리와 함수들)

================================================================================

📈 통계 요약:

  전체 함수: 160개
  Core 모듈: 31개
  Image Processing 모듈: 129개
```

### 카테고리별 함수 개수 (예상)

**Core Module:**
- `core_array_arithmetic`: 12개 (basic + arithmetic)
- `core_array_logic`: 0개
- `core_array_comparison`: 4개
- `core_array_stats`: 7개
- `core_array_transform`: 8개 (matrix)

**Image Processing Module:**
- `imgproc_filter`: 14개 (filter + advanced_filter + morphology + derivative)
- `imgproc_geometric`: 9개 (transform + pyramid)
- `imgproc_misc`: 7개 (misc + threshold)
- `imgproc_drawing`: 15개
- `imgproc_colormap`: 22개
- `imgproc_color`: 20개
- `imgproc_shape`: 17개 (shape + contour)
- `imgproc_motion`: 8개
- `imgproc_feature`: 12개 (feature + edge)
- `imgproc_hist`: 11개

## 🔍 검증 방법

### 1. 카테고리 개수 확인
```bash
grep "{ id:" /src/app/data/opencv-functions.ts | grep -E "(core_|imgproc_)" | wc -l
```
예상 결과: 15

### 2. 함수 카테고리 확인
```bash
grep "category:" /src/app/data/opencv-functions.ts | sort | uniq -c | sort -rn
```

### 3. 변경된 라인 수 확인
```bash
diff /src/app/data/opencv-functions.ts.backup /src/app/data/opencv-functions.ts | grep "category:" | wc -l
```

## 🔄 되돌리기 방법

### 전체 되돌리기
```bash
# 백업에서 복구
cp /src/app/data/opencv-functions.ts.backup /src/app/data/opencv-functions.ts
```

### 수동 되돌리기
1. categories 배열 교체
2. 각 함수의 category 필드 수동 변경

## 📚 참고 자료

- [OpenCV Documentation](https://docs.opencv.org/)
- [OpenCV Core Module](https://docs.opencv.org/4.x/d0/de1/group__core.html)
- [OpenCV Image Processing](https://docs.opencv.org/4.x/d7/dbd/group__imgproc.html)

## 💡 추가 정보

### 카테고리 구조 선택 기준

OpenCV 공식 문서는 다음과 같은 계층 구조를 가집니다:
1. **Main modules** (예: core, imgproc, video, etc.)
2. **Sub categories** (예: Operations on arrays, Image Filtering, etc.)
3. **Functions** (예: cv.add(), cv.blur(), etc.)

이 업데이트는 함수들을 OpenCV 공식 문서의 **Sub categories** 수준으로 재분류합니다.

### 왜 카테고리를 통합하나요?

1. **일관성**: OpenCV 공식 문서와 동일한 구조
2. **학습 효율**: 공식 문서 참조가 쉬워짐
3. **관리 용이**: 카테고리 수 감소로 유지보수 개선

## 🤝 기여

카테고리 매핑에 오류가 있거나 개선 제안이 있다면:
1. 이슈 생성
2. 매핑 테이블 검토
3. 스크립트 수정 제안

---

**마지막 업데이트**: 2026-02-13  
**버전**: 1.0.0  
**상태**: 준비 완료