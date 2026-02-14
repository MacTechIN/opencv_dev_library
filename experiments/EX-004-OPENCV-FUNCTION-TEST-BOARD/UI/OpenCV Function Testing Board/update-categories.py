#!/usr/bin/env python3
"""
OpenCV 카테고리 업데이트 스크립트 (Python)

현재 카테고리를 OpenCV 공식 문서 구조에 맞게 변경합니다.

사용법:
    python update-categories.py
"""

import re
import os
from pathlib import Path
from collections import defaultdict

FILE_PATH = 'src/app/data/opencv-functions.ts'

# 카테고리 매핑 테이블
CATEGORY_MAPPING = {
    # Image Processing Module
    'color': 'imgproc_color',
    'colormap': 'imgproc_colormap',
    'filter': 'imgproc_filter',
    'advanced_filter': 'imgproc_filter',
    'morphology': 'imgproc_filter',
    'edge': 'imgproc_feature',
    'derivative': 'imgproc_filter',
    'threshold': 'imgproc_misc',
    'transform': 'imgproc_geometric',
    'pyramid': 'imgproc_geometric',
    'contour': 'imgproc_shape',
    'shape': 'imgproc_shape',
    'feature': 'imgproc_feature',
    'histogram': 'imgproc_hist',
    'drawing': 'imgproc_drawing',
    'motion': 'imgproc_motion',
    'misc': 'imgproc_misc',
    
    # Core Module
    'basic': 'core_array_arithmetic',
    'arithmetic': 'core_array_arithmetic',
    'matrix': 'core_array_transform',
    'statistical': 'core_array_stats',
    'comparison': 'core_array_comparison',
}

# 새로운 카테고리 정의
NEW_CATEGORIES = """export const categories = [
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
];"""

# 카테고리 이름 매핑
CATEGORY_NAMES = {
    'core_array_arithmetic': 'Arithmetic Operations',
    'core_array_logic': 'Logical Operations',
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

def extract_functions(content):
    """함수 정보 추출"""
    function_pattern = r"\{\s*id:\s*'([^']+)',\s*name:\s*'([^']+)',\s*category:\s*'([^']+)'"
    functions = []
    for match in re.finditer(function_pattern, content):
        functions.append({
            'id': match.group(1),
            'name': match.group(2),
            'category': match.group(3)
        })
    return functions

def main():
    print('🚀 OpenCV 카테고리 업데이트 시작...\n')
    
    try:
        # 파일 읽기
        print(f'📖 파일 읽는 중: {FILE_PATH}')
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 백업 생성
        backup_path = FILE_PATH + '.backup'
        print(f'💾 백업 생성 중: {backup_path}')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 1. categories 배열 교체
        print('\n📝 categories 배열 업데이트 중...')
        categories_pattern = r'export const categories = \[[\s\S]*?\];'
        content = re.sub(categories_pattern, NEW_CATEGORIES, content)
        
        # 2. 각 함수의 category 필드 업데이트
        print('📝 함수 카테고리 업데이트 중...\n')
        update_count = 0
        
        for old_category, new_category in CATEGORY_MAPPING.items():
            pattern = f"category: '{old_category}'"
            matches = len(re.findall(pattern, content))
            if matches > 0:
                content = content.replace(pattern, f"category: '{new_category}'")
                print(f"  ✓ '{old_category}' → '{new_category}' ({matches}개 함수)")
                update_count += matches
        
        # 파일 저장
        print(f'\n💾 파일 저장 중: {FILE_PATH}')
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 함수 정보 추출 (변경 후)
        functions = extract_functions(content)
        
        # 카테고리별 함수 그룹화
        functions_by_category = defaultdict(list)
        for func in functions:
            functions_by_category[func['category']].append(func)
        
        print('\n✅ 카테고리 업데이트 완료!')
        print(f'   총 {update_count}개 함수의 카테고리가 변경되었습니다.\n')
        print('📋 결과:')
        print('   - 23개 카테고리 → 15개 카테고리')
        print('   - OpenCV 공식 문서 구조 적용 완료\n')
        
        # 카테고리별 함수 목록 출력
        print('=' * 80)
        print('📊 카테고리별 함수 목록\n')
        
        # Core Module
        print('🔷 CORE MODULE - Operations on Arrays\n')
        core_categories = [
            'core_array_arithmetic',
            'core_array_comparison',
            'core_array_stats',
            'core_array_transform'
        ]
        
        for cat_id in core_categories:
            if cat_id in functions_by_category and functions_by_category[cat_id]:
                funcs = functions_by_category[cat_id]
                print(f'\n  {CATEGORY_NAMES[cat_id]} ({len(funcs)}개)')
                print('  ' + '-' * 60)
                for idx, func in enumerate(funcs, 1):
                    print(f"  {idx:2}. {func['name']} ({func['id']})")
        
        # Image Processing Module
        print('\n\n🔶 IMAGE PROCESSING MODULE\n')
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
                print(f'\n  {CATEGORY_NAMES[cat_id]} ({len(funcs)}개)')
                print('  ' + '-' * 60)
                for idx, func in enumerate(funcs, 1):
                    print(f"  {idx:2}. {func['name']} ({func['id']})")
        
        print('\n' + '=' * 80)
        print('\n📈 통계 요약:\n')
        
        total_functions = len(functions)
        core_count = sum(len(functions_by_category.get(cat, [])) for cat in core_categories)
        imgproc_count = sum(len(functions_by_category.get(cat, [])) for cat in imgproc_categories)
        
        print(f'  전체 함수: {total_functions}개')
        print(f'  Core 모듈: {core_count}개')
        print(f'  Image Processing 모듈: {imgproc_count}개')
        
        print('\n🔍 확인 방법:')
        print('   grep "category:" src/app/data/opencv-functions.ts | sort | uniq -c\n')
        print('🔄 되돌리기:')
        print(f'   cp {backup_path} {FILE_PATH}\n')
        
    except Exception as error:
        print(f'❌ 오류 발생: {error}')
        exit(1)

if __name__ == '__main__':
    main()
