import os
import urllib.request

def download_file(url: str, dest_path: str):
    """Downloads a file from a URL."""
    if os.path.exists(dest_path):
        print(f"Already exists: {dest_path}")
        return
    
    print(f"Downloading: {url} -> {dest_path}")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"Completed: {dest_path}")
    except Exception as e:
        print(f"Error occurred: {e}")

def main():
    # Set storage path
    weights_dir = "assets/weights/face_models"
    os.makedirs(weights_dir, exist_ok=True)
    
    # Define model URLs (Public models for OpenCV DNN)
    models = {
        "age_deploy.prototxt": "https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/age_deploy.prototxt",
        "age_net.caffemodel": "https://github.com/spmallick/learnopencv/raw/master/AgeGender/age_net.caffemodel",
        "gender_deploy.prototxt": "https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/gender_deploy.prototxt",
        "gender_net.caffemodel": "https://github.com/spmallick/learnopencv/raw/master/AgeGender/gender_net.caffemodel",
        "face_deploy.prototxt": "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt",
        "face_net.caffemodel": "https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel"
    }
    
    print("--- Face Analysis Model Download Started ---")
    for filename, url in models.items():
        dest = os.path.join(weights_dir, filename)
        download_file(url, dest)
    print("--- All Models Downloaded Successfully ---")

if __name__ == "__main__":
    main()
