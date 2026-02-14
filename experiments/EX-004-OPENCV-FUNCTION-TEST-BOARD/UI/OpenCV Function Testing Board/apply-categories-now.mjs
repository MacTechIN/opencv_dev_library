#!/usr/bin/env node

/**
 * OpenCV 카테고리 업데이트 스크립트
 * 
 * 현재 카테고리를 OpenCV 공식 문서 구조에 맞게 변경합니다.
 * 
 * 사용법:
 *   node apply-categories-now.mjs
 *   또는
 *   npm run apply-categories
 */

import { readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const FILE_PATH = join(__dirname, 'src/app/data/opencv-functions.ts');

console.log('🚀 OpenCV 카테고리 업데이트 시작...\n');

// 카테고리 매핑 테이블
const categoryMapping = {
  // Image Processing Module
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
  
  // Core Module
  'basic': 'core_array_arithmetic',
  'arithmetic': 'core_array_arithmetic',
  'matrix': 'core_array_transform',
  'statistical': 'core_array_stats',
  'comparison': 'core_array_comparison',
};

// 새로운 카테고리 정의
const newCategories = `export const categories = [
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
];`;

// 카테고리 이름 매핑
const categoryNames = {
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
};

try {
  // 파일 읽기
  console.log('📖 파일 읽는 중:', FILE_PATH);
  let content = readFileSync(FILE_PATH, 'utf-8');
  const originalContent = content;
  
  // 백업 생성
  const backupPath = FILE_PATH + '.backup';
  console.log('💾 백업 생성 중:', backupPath);
  writeFileSync(backupPath, content, 'utf-8');
  
  // 함수 정보 추출 (변경 전)
  const functionRegex = /\{\s*id:\s*'([^']+)',\s*name:\s*'([^']+)',\s*category:\s*'([^']+)'/g;
  const functionsBeforeUpdate = [];
  let match;
  while ((match = functionRegex.exec(originalContent)) !== null) {
    functionsBeforeUpdate.push({
      id: match[1],
      name: match[2],
      category: match[3]
    });
  }
  
  // 1. categories 배열 교체
  console.log('\n📝 categories 배열 업데이트 중...');
  const categoriesRegex = /export const categories = \[[\s\S]*?\];/;
  content = content.replace(categoriesRegex, newCategories);
  
  // 2. 각 함수의 category 필드 업데이트
  console.log('📝 함수 카테고리 업데이트 중...\n');
  let updateCount = 0;
  const categoryChanges = {};
  
  for (const [oldCategory, newCategory] of Object.entries(categoryMapping)) {
    const regex = new RegExp(`category: '${oldCategory}'`, 'g');
    const matches = content.match(regex);
    if (matches) {
      content = content.replace(regex, `category: '${newCategory}'`);
      console.log(`  ✓ '${oldCategory}' → '${newCategory}' (${matches.length}개 함수)`);
      
      if (!categoryChanges[newCategory]) {
        categoryChanges[newCategory] = [];
      }
      categoryChanges[newCategory].push({ oldCategory, count: matches.length });
      updateCount += matches.length;
    }
  }
  
  // 파일 저장
  console.log('\n💾 파일 저장 중:', FILE_PATH);
  writeFileSync(FILE_PATH, content, 'utf-8');
  
  // 함수 정보 추출 (변경 후)
  const updatedContent = content;
  const functionsAfterUpdate = [];
  const functionRegex2 = /\{\s*id:\s*'([^']+)',\s*name:\s*'([^']+)',\s*category:\s*'([^']+)'/g;
  while ((match = functionRegex2.exec(updatedContent)) !== null) {
    functionsAfterUpdate.push({
      id: match[1],
      name: match[2],
      category: match[3]
    });
  }
  
  // 카테고리별 함수 그룹화
  const functionsByCategory = {};
  functionsAfterUpdate.forEach(func => {
    if (!functionsByCategory[func.category]) {
      functionsByCategory[func.category] = [];
    }
    functionsByCategory[func.category].push(func);
  });
  
  console.log('\n✅ 카테고리 업데이트 완료!');
  console.log(`   총 ${updateCount}개 함수의 카테고리가 변경되었습니다.\n`);
  console.log('📋 결과:');
  console.log('   - 23개 카테고리 → 15개 카테고리');
  console.log('   - OpenCV 공식 문서 구조 적용 완료\n');
  
  // 카테고리별 함수 목록 출력
  console.log('=' .repeat(80));
  console.log('📊 카테고리별 함수 목록\n');
  
  // Core Module
  console.log('🔷 CORE MODULE - Operations on Arrays\n');
  const coreCategories = [
    'core_array_arithmetic',
    'core_array_comparison', 
    'core_array_stats',
    'core_array_transform'
  ];
  
  coreCategories.forEach(catId => {
    if (functionsByCategory[catId] && functionsByCategory[catId].length > 0) {
      console.log(`\n  ${categoryNames[catId]} (${functionsByCategory[catId].length}개)`);
      console.log('  ' + '-'.repeat(60));
      functionsByCategory[catId].forEach((func, idx) => {
        console.log(`  ${(idx + 1).toString().padStart(2)}. ${func.name} (${func.id})`);
      });
    }
  });
  
  // Image Processing Module
  console.log('\n\n🔶 IMAGE PROCESSING MODULE\n');
  const imgprocCategories = [
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
  ];
  
  imgprocCategories.forEach(catId => {
    if (functionsByCategory[catId] && functionsByCategory[catId].length > 0) {
      console.log(`\n  ${categoryNames[catId]} (${functionsByCategory[catId].length}개)`);
      console.log('  ' + '-'.repeat(60));
      functionsByCategory[catId].forEach((func, idx) => {
        console.log(`  ${(idx + 1).toString().padStart(2)}. ${func.name} (${func.id})`);
      });
    }
  });
  
  console.log('\n' + '='.repeat(80));
  console.log('\n📈 통계 요약:\n');
  
  const totalFunctions = functionsAfterUpdate.length;
  console.log(`  전체 함수: ${totalFunctions}개`);
  console.log(`  Core 모듈: ${coreCategories.reduce((sum, cat) => sum + (functionsByCategory[cat]?.length || 0), 0)}개`);
  console.log(`  Image Processing 모듈: ${imgprocCategories.reduce((sum, cat) => sum + (functionsByCategory[cat]?.length || 0), 0)}개`);
  
  // High-level GUI Module 통계 추가
  const highguiCount = functionsByCategory['highgui']?.length || 0;
  if (highguiCount > 0) {
    console.log(`  High-level GUI 모듈: ${highguiCount}개`);
  }
  
  console.log('\n🔍 확인 방법:');
  console.log('   grep "category:" src/app/data/opencv-functions.ts | sort | uniq -c\n');
  console.log('🔄 되돌리기:');
  console.log(`   cp ${backupPath} ${FILE_PATH}\n`);
  
} catch (error) {
  console.error('❌ 오류 발생:', error.message);
  process.exit(1);
}