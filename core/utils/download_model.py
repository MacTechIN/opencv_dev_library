from huggingface_hub import snapshot_download
import os

def download_model():
    repo_id = "Qwen/Qwen2.5-VL-3B-Instruct"
    local_dir = "assets/weights/Qwen2.5-VL-3B-Instruct"
    token = os.getenv("HF_TOKEN")
    
    print(f"--- '{repo_id}' 모델 다운로드 시작 ---")
    if token:
        print("💡 인증 토큰(HF_TOKEN)이 감지되었습니다. 고속 다운로드를 시도합니다.")
    else:
        print("⚠️ 비인증 모드입니다. 속도가 느릴 수 있습니다 (HF_TOKEN 설정 권장).")
    
    print(f"저장 경로: {os.path.abspath(local_dir)}")
    
    try:
        snapshot_download(
            repo_id=repo_id,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            token=token
        )
        print("\n✅ 다운로드 완료! 이제 오프라인에서 사용할 수 있습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("인터넷 연결을 확인하거나 'huggingface_hub'가 설치되어 있는지 확인해 주세요.")

if __name__ == "__main__":
    download_model()
