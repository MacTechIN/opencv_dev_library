#!/bin/bash

###############################################################################
# OpenCV 카테고리 업데이트 스크립트 (Bash)
#
# 현재 카테고리를 OpenCV 공식 문서 구조에 맞게 변경합니다.
#
# 사용법:
#   chmod +x update-categories.sh
#   ./update-categories.sh
###############################################################################

FILE_PATH="src/app/data/opencv-functions.ts"
BACKUP_PATH="${FILE_PATH}.backup"

echo "🚀 OpenCV 카테고리 업데이트 시작..."
echo ""

# 파일 존재 확인
if [ ! -f "$FILE_PATH" ]; then
    echo "❌ 오류: 파일을 찾을 수 없습니다: $FILE_PATH"
    exit 1
fi

# 백업 생성
echo "📖 파일 읽는 중: $FILE_PATH"
echo "💾 백업 생성 중: $BACKUP_PATH"
cp "$FILE_PATH" "$BACKUP_PATH"

echo ""
echo "📝 함수 카테고리 업데이트 중..."
echo ""

# 카테고리 매핑 적용
declare -A CATEGORY_MAPPING=(
    # Image Processing Module
    ["color"]="imgproc_color"
    ["colormap"]="imgproc_colormap"
    ["filter"]="imgproc_filter"
    ["advanced_filter"]="imgproc_filter"
    ["morphology"]="imgproc_filter"
    ["edge"]="imgproc_feature"
    ["derivative"]="imgproc_filter"
    ["threshold"]="imgproc_misc"
    ["transform"]="imgproc_geometric"
    ["pyramid"]="imgproc_geometric"
    ["contour"]="imgproc_shape"
    ["shape"]="imgproc_shape"
    ["feature"]="imgproc_feature"
    ["histogram"]="imgproc_hist"
    ["drawing"]="imgproc_drawing"
    ["motion"]="imgproc_motion"
    ["misc"]="imgproc_misc"
    
    # Core Module
    ["basic"]="core_array_arithmetic"
    ["arithmetic"]="core_array_arithmetic"
    ["matrix"]="core_array_transform"
    ["statistical"]="core_array_stats"
    ["comparison"]="core_array_comparison"
)

# 각 카테고리 변경
for old_cat in "${!CATEGORY_MAPPING[@]}"; do
    new_cat="${CATEGORY_MAPPING[$old_cat]}"
    count=$(grep -c "category: '$old_cat'" "$FILE_PATH" 2>/dev/null || echo 0)
    
    if [ "$count" -gt 0 ]; then
        sed -i.tmp "s/category: '$old_cat'/category: '$new_cat'/g" "$FILE_PATH"
        echo "  ✓ '$old_cat' → '$new_cat' ($count개 함수)"
    fi
done

# 임시 파일 삭제
rm -f "${FILE_PATH}.tmp"

# categories 배열 업데이트
echo ""
echo "📝 categories 배열 업데이트 중..."

# categories 배열을 새로운 구조로 교체
cat > /tmp/new_categories.txt << 'EOF'
export const categories = [
  // Core Module - Operations on Arrays
  { id: 'core_array_arithmetic', name: 'Arithmetic Operations', icon: '➕', parent: 'core' },
  { id: 'core_array_logic', name: 'Logical Operations', icon: '🔀', parent: 'core' },
  { id: 'core_array_comparison', name: 'Comparison Operations', icon: '⚖️', parent: 'core' },
  { id: 'core_array_stats', name: 'Statistical Operations', icon: '📊', parent: 'core' },
  { id: 'core_array_transform', name: 'Array Transforms', icon: '🔄', parent: 'core' },
  
  // Image Processing Module
  { id: 'imgproc_filter', name: 'Image Filtering', icon: '🔍', parent: 'imgproc' },
  { id: 'imgproc_geometric', name: 'Geometric Transformations', icon: '🔁', parent: 'imgproc' },
  { id: 'imgproc_misc', name: 'Miscellaneous Transformations', icon: '🔧', parent: 'imgproc' },
  { id: 'imgproc_drawing', name: 'Drawing Functions', icon: '✏️', parent: 'imgproc' },
  { id: 'imgproc_colormap', name: 'ColorMaps in OpenCV', icon: '🌈', parent: 'imgproc' },
  { id: 'imgproc_color', name: 'Color Space Conversions', icon: '🎨', parent: 'imgproc' },
  { id: 'imgproc_shape', name: 'Structural Analysis and Shape Descriptors', icon: '🔶', parent: 'imgproc' },
  { id: 'imgproc_motion', name: 'Motion Analysis and Object Tracking', icon: '🎬', parent: 'imgproc' },
  { id: 'imgproc_feature', name: 'Feature Detection', icon: '⭐', parent: 'imgproc' },
  { id: 'imgproc_hist', name: 'Histograms', icon: '📈', parent: 'imgproc' },
];
EOF

# Python을 사용하여 categories 배열 교체 및 함수 목록 출력
python3 << 'PYTHON_SCRIPT'
import re
from collections import defaultdict

FILE_PATH = "src/app/data/opencv-functions.ts"

with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

with open('/tmp/new_categories.txt', 'r', encoding='utf-8') as f:
    new_categories = f.read()

# categories 배열 교체
pattern = r'export const categories = \[[\s\S]*?\];'
content = re.sub(pattern, new_categories, content)

with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

# 함수 정보 추출
function_pattern = r"\{\s*id:\s*'([^']+)',\s*name:\s*'([^']+)',\s*category:\s*'([^']+)'"
functions = []
for match in re.finditer(function_pattern, content):
    functions.append({
        'id': match.group(1),
        'name': match.group(2),
        'category': match.group(3)
    })

# 카테고리별 함수 그룹화
functions_by_category = defaultdict(list)
for func in functions:
    functions_by_category[func['category']].append(func)

# 카테고리 이름 매핑
category_names = {
    'core_array_arithmetic': 'Arithmetic Operations',
    'core_array_comparison': 'Comparison Operations',
    'core_array_stats': 'Statistical Operations',
    'core_array_transform': 'Array Transforms',
    'imgproc_filter': 'Image Filtering',
    'imgproc_geometric': 'Geometric Transformations',
    'imgproc_misc': 'Miscellaneous Transformations',
    'imgproc_drawing': 'Drawing Functions',
    'imgproc_colormap': 'ColorMaps in OpenCV',
    'imgproc_color': 'Color Space Conversions',
    'imgproc_shape': 'Structural Analysis and Shape Descriptors',
    'imgproc_motion': 'Motion Analysis and Object Tracking',
    'imgproc_feature': 'Feature Detection',
    'imgproc_hist': 'Histograms',
}

print("\n" + "=" * 80)
print("📊 카테고리별 함수 목록\n")

# Core Module
print("🔷 CORE MODULE - Operations on Arrays\n")
core_categories = [
    'core_array_arithmetic',
    'core_array_comparison',
    'core_array_stats',
    'core_array_transform'
]

for cat_id in core_categories:
    if cat_id in functions_by_category and functions_by_category[cat_id]:
        funcs = functions_by_category[cat_id]
        print(f'\n  {category_names[cat_id]} ({len(funcs)}개)')
        print('  ' + '-' * 60)
        for idx, func in enumerate(funcs, 1):
            print(f"  {idx:2}. {func['name']} ({func['id']})")

# Image Processing Module
print("\n\n🔶 IMAGE PROCESSING MODULE\n")
imgproc_categories = [
    'imgproc_color',
    'imgproc_colormap',
    'imgproc_filter',
    'imgproc_geometric',
    'imgproc_misc',
    'imgproc_drawing',
    'imgproc_shape',
    'imgproc_motion',
    'imgproc_feature',
    'imgproc_hist'
]

for cat_id in imgproc_categories:
    if cat_id in functions_by_category and functions_by_category[cat_id]:
        funcs = functions_by_category[cat_id]
        print(f'\n  {category_names[cat_id]} ({len(funcs)}개)')
        print('  ' + '-' * 60)
        for idx, func in enumerate(funcs, 1):
            print(f"  {idx:2}. {func['name']} ({func['id']})")

print("\n" + "=" * 80)
print("\n📈 통계 요약:\n")

total_functions = len(functions)
core_count = sum(len(functions_by_category.get(cat, [])) for cat in core_categories)
imgproc_count = sum(len(functions_by_category.get(cat, [])) for cat in imgproc_categories)

print(f"  전체 함수: {total_functions}개")
print(f"  Core 모듈: {core_count}개")
print(f"  Image Processing 모듈: {imgproc_count}개")
PYTHON_SCRIPT

# 임시 파일 삭제
rm -f /tmp/new_categories.txt

echo ""
echo "✅ 카테고리 업데이트 완료!"
echo "   OpenCV 공식 문서 구조 적용 완료"
echo ""
echo "🔍 확인 방법:"
echo "   grep \"category:\" $FILE_PATH | sort | uniq -c"
echo ""
echo "🔄 되돌리기:"
echo "   cp $BACKUP_PATH $FILE_PATH"
echo ""
