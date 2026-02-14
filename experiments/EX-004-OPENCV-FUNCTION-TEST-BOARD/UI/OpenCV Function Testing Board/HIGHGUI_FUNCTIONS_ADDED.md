# ✅ High-level GUI 카테고리 및 함수 추가 완료

## 📊 추가된 내용

### 🆕 새로운 카테고리
- **카테고리 ID**: `highgui`
- **카테고리 이름**: High-level GUI
- **아이콘**: 🖥️
- **문서**: https://docs.opencv.org/4.x/d7/dfc/group__highgui.html

### 📝 추가된 함수 (총 21개)

#### 1️⃣ 윈도우 관리 (Window Management) - 8개

1. **namedWindow** - 윈도우 생성
   - 윈도우 이름, 플래그(AUTOSIZE, NORMAL, FULLSCREEN 등) 설정
   
2. **destroyWindow** - 윈도우 삭제
   - 지정된 이름의 윈도우 삭제
   
3. **destroyAllWindows** - 모든 윈도우 삭제
   - 생성된 모든 HighGUI 윈도우 삭제
   
4. **resizeWindow** - 윈도우 크기 조절
   - 너비, 높이 설정 (WINDOW_NORMAL에서만 작동)
   
5. **moveWindow** - 윈도우 이동
   - X, Y 좌표로 윈도우 위치 이동
   
6. **setWindowTitle** - 윈도우 제목 설정
   - 윈도우의 제목 텍스트 변경
   
7. **getWindowProperty** - 윈도우 속성 가져오기
   - FULLSCREEN, AUTOSIZE, ASPECT_RATIO, OPENGL, VISIBLE 속성 조회
   
8. **setWindowProperty** - 윈도우 속성 설정
   - 윈도우 속성 값 설정

#### 2️⃣ 키보드 입력 (Keyboard Input) - 2개

9. **waitKey** - 키보드 입력 대기
   - 지정된 시간(밀리초) 동안 키 입력 대기
   - delay=0이면 무한 대기
   
10. **pollKey** - 키보드 상태 확인
    - 대기하지 않고 즉시 현재 키 상태 반환

#### 3️⃣ 트랙바 (Trackbar/Slider) - 6개

11. **createTrackbar** - 트랙바 생성
    - 트랙바 이름, 윈도우, 초기값, 최대값 설정
    
12. **getTrackbarPos** - 트랙바 위치 가져오기
    - 현재 트랙바 위치 값 반환
    
13. **setTrackbarPos** - 트랙바 위치 설정
    - 트랙바를 지정된 위치로 이동
    
14. **setTrackbarMin** - 트랙바 최소값 설정
    - 트랙바의 최소값 설정
    
15. **setTrackbarMax** - 트랙바 최대값 설정
    - 트랙바의 최대값 설정

#### 4️⃣ ROI 선택 (Region of Interest) - 2개

16. **selectROI** - 관심 영역 선택
    - 마우스로 하나의 ROI 영역 선택
    - 십자선, 중심/모서리 시작 옵션
    
17. **selectROIs** - 여러 관심 영역 선택
    - 마우스로 여러 개의 ROI 영역 선택

#### 5️⃣ 마우스 이벤트 (Mouse Events) - 2개

18. **setMouseCallback** - 마우스 콜백 설정
    - 마우스 이벤트 핸들러 함수 등록
    - 이벤트 타입: LBUTTONDOWN, RBUTTONDOWN, MOUSEMOVE 등
    
19. **getMouseWheelDelta** - 마우스 휠 변화량
    - 마우스 휠의 스크롤 변화량 반환

#### 6️⃣ 기타 (Miscellaneous) - 2개

20. **startWindowThread** - 윈도우 스레드 시작
    - GUI 윈도우를 처리하는 스레드 시작
    
21. **imshow** - 이미지 표시
    - 윈도우에 이미지 표시
    - 웹 환경에서는 Canvas를 통해 표시

## 🎨 구현 특징

### 웹 환경 시뮬레이션
데스크톱 OpenCV의 GUI 기능을 웹 환경에서 시뮬레이션:
- 윈도우 관련 함수: 정보 텍스트 오버레이로 표시
- 트랙바: 시각적 프로그레스 바로 표시
- ROI 선택: 샘플 ROI를 사각형으로 표시
- 마우스 이벤트: 마우스 커서 위치를 원으로 표시
- 키보드 입력: 대기 메시지 표시

### 시각적 피드백
모든 함수에 색상별 시각적 표시:
- 🟡 윈도우 관리: 노란색 (255, 255, 0)
- 🔵 키보드 입력: 청록색 (0, 255, 255)
- 🟢 트랙바: 녹색 (100, 255, 100)
- 🟣 ROI 선택: 자홍색 (255, 100, 255)
- 🟠 마우스 이벤트: 주황색 (255, 200, 0)
- 🟢 이미지 표시: 녹색 (0, 255, 0)

## 📈 전체 통계 업데이트

### 이전
- 전체 함수: 186개
- 카테고리: 24개 (23개 + misc)
- Core 모듈: 31개
- Image Processing 모듈: 155개

### 현재
- **전체 함수: 207개** (+21개)
- **카테고리: 25개** (+1개)
- Core 모듈: 31개
- Image Processing 모듈: 155개
- **High-level GUI 모듈: 21개** (신규)

## 📚 함수별 상세 정보

### 파라미터 타입
- `select`: 드롭다운 선택 (윈도우 이름, 플래그, 이벤트 타입 등)
- `slider`: 숫자 입력 (크기, 위치, 값 등)

### 모든 함수에 포함된 정보
- ✅ 한글 이름 및 설명
- ✅ 상세 파라미터 설명
- ✅ 정확한 함수 문법 (syntax)
- ✅ OpenCV 공식 문서 링크
- ✅ 웹 환경 시뮬레이션 구현

## 🎯 교육적 가치

### 학생들이 배울 수 있는 내용

1. **윈도우 관리**
   - GUI 윈도우 생성과 관리
   - 윈도우 속성 제어
   
2. **사용자 입력 처리**
   - 키보드 입력 대기와 처리
   - 마우스 이벤트 핸들링
   
3. **대화형 컨트롤**
   - 트랙바를 통한 실시간 파라미터 조정
   - ROI 선택을 통한 영역 지정
   
4. **이미지 표시**
   - 처리된 이미지를 윈도우에 표시
   - 여러 윈도우 관리

## 💻 사용 예시

### 트랙바로 임계값 조정
```python
import cv2

cv2.namedWindow('Threshold Control')
cv2.createTrackbar('Threshold', 'Threshold Control', 127, 255, callback)
img = cv2.imread('image.jpg')
threshold = cv2.getTrackbarPos('Threshold', 'Threshold Control')
_, result = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
cv2.imshow('Threshold Control', result)
cv2.waitKey(0)
```

### ROI 선택 및 처리
```python
import cv2

img = cv2.imread('image.jpg')
roi = cv2.selectROI('Select Area', img)
x, y, w, h = roi
roi_img = img[y:y+h, x:x+w]
cv2.imshow('ROI', roi_img)
cv2.waitKey(0)
```

### 마우스 이벤트로 그리기
```python
import cv2

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)

cv2.namedWindow('Drawing')
cv2.setMouseCallback('Drawing', mouse_callback)
```

## 🔗 관련 문서

- [OpenCV High-level GUI 공식 문서](https://docs.opencv.org/4.x/d7/dfc/group__highgui.html)
- [OpenCV Python Tutorials - GUI Features](https://docs.opencv.org/4.x/dc/d4d/tutorial_py_table_of_contents_gui.html)

## ✨ 다음 단계

학생들은 이제 다음을 학습할 수 있습니다:

1. ✅ 기본 이미지 처리 (155개 함수)
2. ✅ 배열 연산 및 통계 (31개 함수)
3. ✅ **GUI 인터페이스 및 사용자 입력 (21개 함수)** ← NEW!
4. 향후: Video I/O, Object Detection, Machine Learning 등

---

**업데이트**: 2026-02-13  
**추가된 함수**: 21개  
**새로운 카테고리**: High-level GUI (highgui)  
**총 함수 개수**: 207개
