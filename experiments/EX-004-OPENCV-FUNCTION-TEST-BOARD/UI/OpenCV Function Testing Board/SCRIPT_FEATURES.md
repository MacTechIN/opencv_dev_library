# 📋 카테고리 업데이트 스크립트 기능 상세

## ✨ 새로운 기능

모든 스크립트에 **카테고리별 함수 목록 자동 출력 기능**이 추가되었습니다!

## 🎯 스크립트가 하는 일

### 1️⃣ 카테고리 업데이트
- 23개 → 15개 카테고리로 통합
- OpenCV 공식 문서 구조 적용
- 160개 함수 자동 재배치

### 2️⃣ 자동 백업
- 원본 파일 백업 생성
- 안전한 복구 가능

### 3️⃣ 카테고리별 함수 목록 출력 ⭐ NEW!
스크립트 실행 시 다음 정보가 자동으로 출력됩니다:

```
📊 카테고리별 함수 목록

🔷 CORE MODULE - Operations on Arrays

  Arithmetic Operations (12개)
  ------------------------------------------------------------
   1. Add (add)
   2. Subtract (subtract)
   3. Multiply (multiply)
   4. Divide (divide)
   5. Absolute Difference (absdiff)
   6. Bitwise AND (bitwiseAnd)
   7. Bitwise OR (bitwiseOr)
   8. Bitwise XOR (bitwiseXor)
   9. Bitwise NOT (bitwiseNot)
  10. Add Weighted (addWeighted)
  11. Convert Scale Abs (convertScaleAbs)
  12. Magnitude (magnitude)

  Comparison Operations (4개)
  ------------------------------------------------------------
   1. Compare (compare)
   2. In Range (inRange)
   3. Min (min)
   4. Max (max)

  Statistical Operations (7개)
  ------------------------------------------------------------
   1. Mean (mean)
   2. Standard Deviation (meanStdDev)
   3. Count Non Zero (countNonZero)
   4. Min Max Loc (minMaxLoc)
   5. Normalize (normalize)
   6. Sum (sum)
   7. Reduce (reduce)

  Array Transforms (8개)
  ------------------------------------------------------------
   1. Transpose (transpose)
   2. Flip (flip)
   3. Rotate (rotate)
   4. Split (split)
   5. Merge (merge)
   6. Mix Channels (mixChannels)
   7. Extract Channel (extractChannel)
   8. Insert Channel (insertChannel)


🔶 IMAGE PROCESSING MODULE

  Color Space Conversions (20개)
  ------------------------------------------------------------
   1. Convert Color (cvtColor)
   2. RGB to Gray (cvtColorRGBToGray)
   ... (20개 모두 나열)

  ColorMaps in OpenCV (22개)
  ------------------------------------------------------------
   1. Apply ColorMap - Autumn (applyColorMapAutumn)
   2. Apply ColorMap - Bone (applyColorMapBone)
   ... (22개 모두 나열)

  Image Filtering (14개)
  ------------------------------------------------------------
   1. Blur (blur)
   2. Gaussian Blur (GaussianBlur)
   ... (14개 모두 나열)

  ... (기타 모든 카테고리)

================================================================================

📈 통계 요약:

  전체 함수: 160개
  Core 모듈: 31개
  Image Processing 모듈: 129개
```

## 🔍 출력되는 정보

### 각 카테고리별로:
- ✅ 카테고리 이름 (한글)
- ✅ 함수 개수
- ✅ 모든 함수 목록
  - 순번
  - 함수 이름 (한글)
  - 함수 ID (영문)

### 전체 통계:
- ✅ 전체 함수 개수
- ✅ Core 모듈 함수 개수
- ✅ Image Processing 모듈 함수 개수

## 📝 스크립트별 구현

### 1. apply-categories-now.mjs (Node.js)
```javascript
// 함수 정보 추출
const functionRegex = /\{\s*id:\s*'([^']+)',\s*name:\s*'([^']+)',\s*category:\s*'([^']+)'/g;

// 카테고리별 그룹화
const functionsByCategory = {};
functionsAfterUpdate.forEach(func => {
  if (!functionsByCategory[func.category]) {
    functionsByCategory[func.category] = [];
  }
  functionsByCategory[func.category].push(func);
});

// 출력
console.log('📊 카테고리별 함수 목록\n');
...
```

### 2. update-categories.py (Python)
```python
# 함수 정보 추출
function_pattern = r"\{\s*id:\s*'([^']+)',\s*name:\s*'([^']+)',\s*category:\s*'([^']+)'"
functions = extract_functions(content)

# 카테고리별 그룹화
from collections import defaultdict
functions_by_category = defaultdict(list)

# 출력
print('📊 카테고리별 함수 목록\n')
...
```

### 3. update-categories.sh (Bash + Python)
```bash
# Python을 사용하여 함수 목록 추출 ��� 출력
python3 << 'PYTHON_SCRIPT'
import re
from collections import defaultdict

# 함수 추출 및 카테고리별 그룹화
...
PYTHON_SCRIPT
```

## 🎨 출력 포맷

### 헤더 섹션
```
================================================================================
📊 카테고리별 함수 목록
```

### 카테고리 헤더
```
🔷 CORE MODULE - Operations on Arrays
```

### 개별 카테고리
```
  Arithmetic Operations (12개)
  ------------------------------------------------------------
```

### 함수 목록
```
   1. Add (add)
   2. Subtract (subtract)
  ...
```

### 통계 요약
```
================================================================================

📈 통계 요약:

  전체 함수: 160개
  Core 모듈: 31개
  Image Processing 모듈: 129개
```

## 💡 활용 방법

### 1. 카테고리 검증
스크립트 출력을 통해 각 함수가 올바른 카테고리로 이동했는지 즉시 확인

### 2. 함수 목록 참조
출력된 목록을 복사하여 문서화에 활용

### 3. 통계 확인
카테고리별 함수 분포를 한눈에 파악

### 4. 교육 자료
학생들에게 OpenCV 함수 구조를 설명할 때 활용

## 🔧 커스터마이징

원하는 경우 스크립트를 수정하여:
- 출력 포맷 변경
- 특정 카테고리만 출력
- CSV/JSON 형식으로 저장
- 함수 설명 추가

## 📊 예상 출력 크기

- 전체 출력 라인: 약 200-250줄
- Core Module: 약 40줄
- Image Processing Module: 약 160줄
- 통계 및 헤더: 약 30줄

## 🎓 교육적 가치

이 기능으로:
1. ✅ 학생들이 함수 분류를 이해
2. ✅ OpenCV 구조를 학습
3. ✅ 카테고리별 함수 개수 파악
4. ✅ 실습 계획 수립

---

**버전**: 2.0.0  
**업데이트**: 2026-02-13  
**새로운 기능**: 카테고리별 함수 목록 자동 출력
