import os
import urllib.request

def download_file(url: str, dest_path: str):
    """URL에서 파일을 다운로드합니다."""
    if os.path.exists(dest_path):
        print(f"이미 존재함: {dest_path}")
        return
    
    print(f"다운로드 중: {url} -> {dest_path}")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"완료: {dest_path}")
    except Exception as e:
        print(f"오류 발생: {e}")

def main():
    # 저장 경로 설정
    weights_dir = "assets/weights/face_models"
    os.makedirs(weights_dir, exist_ok=True)
    
    # 모델 URL 정의 (OpenCV DNN용 공개 모델)
    models = {
        "age_deploy.prototxt": "https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/age_deploy.prototxt",
        "age_net.caffemodel": "https://github.com/spmallick/learnopencv/raw/master/AgeGender/age_net.caffemodel",
        "gender_deploy.prototxt": "https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/gender_deploy.prototxt",
        "gender_net.caffemodel": "https://github.com/spmallick/learnopencv/raw/master/AgeGender/gender_net.caffemodel",
        "face_deploy.prototxt": "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt",
        "face_net.caffemodel": "https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel"
    }
    
    print("--- 얼굴 분석 모델 다운로드 시작 ---")
    for filename, url in models.items():
        dest = os.path.join(weights_dir, filename)
        download_file(url, dest)
    print("--- 모든 모델 다운로드 완료 ---")

if __name__ == "__main__":
    main()
