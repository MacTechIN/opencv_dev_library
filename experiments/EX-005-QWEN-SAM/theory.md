# Theory: Grounding Qwen2-VL Detection with SAM 2

## 1. 개요 (Overview)
본 실험은 시각적 이해 능력이 뛰어난 **Qwen2-VL(VLM)**과 세계 최고 수준의 제로샷 세그멘테이션 성능을 가진 **SAM 2(Segment Anything Model 2)**를 결합하여, 단순히 객체를 박스로 찾는 것을 넘어 픽셀 단위로 정밀하게 분할하는 하이브리드 파이프라인을 구축하는 것을 목표로 합니다.

## 2. 하이브리드 아키텍처 (Hybrid Architecture)
이 시스템은 다음과 같은 'Grounding' 워크플로우를 따릅니다:

1. **VLM 기반 객체 탐지 (Visual Prompting)**: 
   - 사용자가 자연어로 "검은색 가방을 찾아줘"라고 요청하면, Qwen2-VL은 이미지 내 해당 객체의 위치를 정규화된 좌표(`[ymin, xmin, ymax, xmax]`)로 반환합니다.
2. **좌표 스케일링 (Coordinate Refinement)**:
   - Qwen-VL의 [0, 1000] 좌표를 실제 이미지 해상도에 맞게 변환합니다.
3. **SAM 2 프롬프트 입력 (Segmentation Grounding)**:
   - 변환된 바운딩 박스를 SAM 2의 `box` 프롬프트로 입력합니다. SAM 2는 이 박스를 '가이드' 삼아 객체의 정확한 윤곽을 계산합니다.
4. **결과 시각화 (Visualization)**:
   - 생성된 마스크를 원본 이미지에 투명 오버레이로 합성하여 최종 결과를 도출합니다.

## 3. 핵심 기술 요소 (Key Components)
### Qwen2-VL (The "Brain")
- **역할**: 이미지 내 객체의 의미론적 이해 및 대략적인 위치 지정.
- **특징**: 복잡한 문맥 파악 가능, JSON 형식의 구조화된 데이터 출력.

### SAM 2 (The "Scalpel")
- **역할**: 제공된 위치 정보를 바탕으로 객체의 경계를 픽셀 단위로 정밀하게 절삭.
- **특징**: 박스 프롬프트 하나만으로도 정교한 마스크 생성, 비디오 추적(Video Tracking) 확장 가능.

## 4. 기대 효과 (Expected Benefits)
- **정밀도 향상**: 기존 박스 기반 탐지의 한계를 넘어 정교한 형상 추출 가능.
- **다목적 활용**: 배경 제거, 객체별 필터링, 로봇 팔 제어를 위한 정밀 좌표 추출 등.

## 5. 참고 문헌
- [Grounding Qwen2-VL Detection with SAM 2 - DebuggerCafe](https://debuggercafe.com/grounding-qwen3-vl-detection-with-sam2/)
