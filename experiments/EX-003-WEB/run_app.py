import os
import sys
import subprocess
import webbrowser
import time

# Add project root to PYTHONPATH
project_root = os.getcwd()
os.environ["PYTHONPATH"] = f"{project_root}:{os.environ.get('PYTHONPATH', '')}"

def start_app():
    print("🚀 Starting FaceProcessor Mission Control Web App...")
    
    # Path to server script
    server_path = "core/web/server.py"
    
    # Check if dependencies are installed
    try:
        import fastapi
        import uvicorn
    except ImportError:
        print("❌ Missing dependencies. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"])

    # Launch server in a separate process or run it here
    # To keep it simple for the demo, we run it in this process
    print("🔗 Server starting at http://localhost:8000")
    
    # Wait a moment for server to warm up (optional)
    # webbrowser.open("http://localhost:8000") # Auto-open browser
    
    try:
        subprocess.run([sys.executable, server_path])
    except KeyboardInterrupt:
        print("\n👋 App closed.")

if __name__ == "__main__":
    start_app()
