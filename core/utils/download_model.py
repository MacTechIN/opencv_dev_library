from huggingface_hub import snapshot_download
import os

def download_model():
    """Utility to download the Qwen-2.5-VL model for offline use."""
    repo_id = "Qwen/Qwen2.5-VL-3B-Instruct"
    local_dir = "assets/weights/Qwen2.5-VL-3B-Instruct"
    token = os.getenv("HF_TOKEN")
    
    print(f"--- Starting download for '{repo_id}' ---")
    if token:
        print("💡 Auth token (HF_TOKEN) detected. Attempting high-speed download.")
    else:
        print("⚠️ Unauthenticated mode. Download speed may be limited (Setting HF_TOKEN recommended).")
    
    print(f"Storage path: {os.path.abspath(local_dir)}")
    
    try:
        snapshot_download(
            repo_id=repo_id,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            token=token
        )
        print("\n✅ Download complete! Ready for offline use.")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("Please check your internet connection and ensure 'huggingface_hub' is installed.")

if __name__ == "__main__":
    download_model()
