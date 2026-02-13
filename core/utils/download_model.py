from huggingface_hub import snapshot_download
import os

def download_model():
    repo_id = "Qwen/Qwen2.5-VL-3B-Instruct"
    local_dir = "assets/weights/Qwen2.5-VL-3B-Instruct"
    
    print(f"--- '{repo_id}' 모델 다운로드 시작 ---")
    print(f"저장 경로: {os.path.abspath(local_dir)}")
    
    try:
        snapshot_download(
            repo_id=repo_id,
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        print("\n✅ 다운로드 완료! 이제 오프라인에서 사용할 수 있습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("인터넷 연결을 확인하거나 'huggingface_hub'가 설치되어 있는지 확인해 주세요.")

if __name__ == "__main__":
    download_model()
