import os
import subprocess

def download_file(url: str, dest_path: str):
    """Downloads a file using curl for better reliability with large files."""
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        print(f"Already exists: {dest_path}")
        return
    
    print(f"Downloading: {url} -> {dest_path}")
    try:
        # Using curl with -L to follow redirects
        subprocess.run(["curl", "-L", url, "-o", dest_path], check=True)
        print(f"Completed: {dest_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    weights_dir = "assets/weights/face_models"
    os.makedirs(weights_dir, exist_ok=True)
    
    # Using stable URLs from verified sources
    models = {
        "age_deploy.prototxt": "https://raw.githubusercontent.com/GilLevi/AgeGenderDeepLearning/master/models/age_deploy.prototxt",
        "age_net.caffemodel": "https://raw.githubusercontent.com/GilLevi/AgeGenderDeepLearning/master/models/age_net.caffemodel",
        "gender_deploy.prototxt": "https://raw.githubusercontent.com/GilLevi/AgeGenderDeepLearning/master/models/gender_deploy.prototxt",
        "gender_net.caffemodel": "https://raw.githubusercontent.com/GilLevi/AgeGenderDeepLearning/master/models/gender_net.caffemodel",
        "face_deploy.prototxt": "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt",
        "face_net.caffemodel": "https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel",
        "openface.nn4.small2.v1.t7": "https://github.com/aakashjhawar/face-recognition-using-deep-learning/raw/master/openface_nn4.small2.v1.t7"
    }
    
    print("--- Face Analysis Model Download (Robust Mode) Started ---")
    for filename, url in models.items():
        dest = os.path.join(weights_dir, filename)
        download_file(url, dest)
    print("--- Model Check/Download Process Finished ---")

if __name__ == "__main__":
    main()
