import cv2
import asyncio
import json
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from core.processing.face_processor import FaceProcessor
from core.utils.logger import get_logger

logger = get_logger("WebBackend")
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="core/web/static"), name="static")

# Singleton components
class GlobalState:
    def __init__(self):
        self.processor = FaceProcessor()
        self.cap = None
        self.active_connections: list[WebSocket] = []
        self.loop = None
        # System Configuration
        self.global_detect = True
        self.auto_reg = False
        self.threshold = 0.85 # Higher threshold for better consistency

    def get_cap(self):
        if self.cap is None or not self.cap.isOpened():
            logger.info("📸 Initializing Camera Resource...")
            self.cap = cv2.VideoCapture(0)
            # Try to set resolution for better quality
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return self.cap

    async def broadcast(self, data):
        if not self.active_connections:
            return
        
        message = json.dumps(data)
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                disconnected.append(connection)
        
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)

    def update_config(self, config: dict):
        """Processes incoming commands from the UI."""
        if "global_detect" in config:
            self.global_detect = config["global_detect"]
            logger.info(f"⚙️ Config Updated: global_detect = {self.global_detect}")
            
        if "auto_reg" in config:
            self.auto_reg = config["auto_reg"]
            self.processor.auto_reg = self.auto_reg
            logger.info(f"⚙️ Config Updated: auto_reg = {self.auto_reg}")

        if "threshold" in config:
            self.threshold = float(config["threshold"])
            self.processor.match_threshold = self.threshold
            logger.info(f"⚙️ Config Updated: threshold = {self.threshold}")

state = GlobalState()

def gen_frames():
    """Video streaming generator function."""
    cap = state.get_cap()
    
    while True:
        success, frame = cap.read()
        if not success:
            logger.warning("⚠️ Camera frame drop. Retrying...")
            time.sleep(0.1)
            continue
        
        # Mirror for natural feedback
        frame = cv2.flip(frame, 1)
        
        try:
            # Face Analysis
            people = []
            if state.global_detect:
                people = state.processor.process_frame(frame)
            
            # Prepare Metadata
            metadata = []
            for p in people:
                x1, y1, x2, y2 = p.rect
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 210, 255), 2)
                cv2.putText(frame, p.id, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 210, 255), 2)
                
                metadata.append({
                    "id": p.id,
                    "rect": [int(x1), int(y1), int(x2), int(y2)],
                    "centroid": p.centroid.tolist() if hasattr(p.centroid, 'tolist') else p.centroid,
                    "age": getattr(p, 'age', 'N/A'),
                    "gender": getattr(p, 'gender', 'N/A')
                })
            
            # Always broadcast even if empty to clear UI
            if state.loop:
                asyncio.run_coroutine_threadsafe(
                    state.broadcast({"type": "update", "data": metadata}),
                    state.loop
                )
        except Exception as e:
            logger.error(f"❌ Core Error: {e}")

        # Encode Frame
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret: continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.get("/video_feed")
async def video_feed():
    if state.loop is None:
        state.loop = asyncio.get_running_loop()
    return StreamingResponse(gen_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    state.active_connections.append(websocket)
    if state.loop is None:
        state.loop = asyncio.get_running_loop()
        
    logger.info(f"🔌 WebSocket Connected. Total: {len(state.active_connections)}")
    
    # Send initial config to client
    await websocket.send_text(json.dumps({
        "type": "config",
        "data": {
            "global_detect": state.global_detect,
            "auto_reg": state.auto_reg,
            "threshold": state.threshold
        }
    }))

    try:
        while True:
            data = await websocket.receive_text()
            try:
                cmd = json.loads(data)
                if cmd.get("type") == "command":
                    state.update_config(cmd.get("data", {}))
            except Exception as e:
                logger.error(f"Malformed WS command: {e}")
    except WebSocketDisconnect:
        if websocket in state.active_connections:
            state.active_connections.remove(websocket)
        logger.info("🔌 WebSocket Disconnected.")

@app.get("/")
async def index():
    from fastapi.responses import FileResponse
    return FileResponse("core/web/static/index.html")

@app.on_event("shutdown")
def shutdown_event():
    if state.cap:
        state.cap.release()
        logger.info("📸 Camera Released.")

if __name__ == "__main__":
    import uvicorn
    # Use single worker to avoid camera conflicts
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
