# OpenCV 카테고리 업데이트 빠른 가이드

## 🚀 빠른 시작

카테고리를 OpenCV 공식 문서 구조로 변경하려면:

```bash
npm run apply-categories
```

✨ **스크립트 실행 시 각 카테고리별 전체 함수 목록이 자동으로 출력됩니다!**

## 📁 생성된 파일

- `CATEGORY_UPDATE_README.md` - 상세 가이드 (이 파일 참조!)
- `apply-categories-now.mjs` - Node.js 스크립트 (메인)
- `update-categories.py` - Python 스크립트
- `update-categories.sh` - Bash 스크립트

## 🔄 실행 방법

### 방법 1: npm 명령어 (권장)
```bash
npm run apply-categories
```

### 방법 2: Node.js 직접 실행
```bash
node apply-categories-now.mjs
```

### 방법 3: Python
```bash
python update-categories.py
```

### 방법 4: Bash
```bash
chmod +x update-categories.sh
./update-categories.sh
```

## 📊 변경 사항

**이전:** 23개 카테고리
```
color, colormap, filter, advanced_filter, morphology, 
edge, derivative, threshold, transform, pyramid, 
contour, shape, feature, histogram, drawing, 
motion, misc, basic, arithmetic, matrix, 
statistical, comparison
```

**이후:** 15개 카테고리 (OpenCV 공식)
```
Core Module:
- core_array_arithmetic
- core_array_logic  
- core_array_comparison
- core_array_stats
- core_array_transform

Image Processing Module:
- imgproc_filter
- imgproc_geometric
- imgproc_misc
- imgproc_drawing
- imgproc_colormap
- imgproc_color
- imgproc_shape
- imgproc_motion
- imgproc_feature
- imgproc_hist
```

## ⚠️ 중요

- 모든 스크립트는 자동으로 백업 파일을 생성합니다
- 백업 위치: `src/app/data/opencv-functions.ts.backup`
- 160개 함수는 그대로 유지됩니다

## 🔙 되돌리기

```bash
cp src/app/data/opencv-functions.ts.backup src/app/data/opencv-functions.ts
```

## 📖 상세 정보

더 자세한 정보는 `CATEGORY_UPDATE_README.md` 파일을 참조하세요!