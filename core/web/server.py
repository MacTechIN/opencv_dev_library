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

# Initialize the Face Analysis Pipeline
processor = FaceProcessor()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.loop = asyncio.get_event_loop()

    async def library_connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

def gen_frames():
    """Video streaming generator function."""
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # Mirror image for natural feedback
        frame = cv2.flip(frame, 1)
        
        # Process the frame through the library
        people = processor.process_frame(frame)
        
        # Serialize metadata for WebSocket
        metadata = []
        for p in people:
            # Drawing on frame for the stream
            x1, y1, x2, y2 = p.rect
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 210, 255), 2)
            cv2.putText(frame, p.id, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 210, 255), 2)
            
            # Metadata for UI insights
            metadata.append({
                "id": p.id,
                "rect": [int(x1), int(y1), int(x2), int(y2)],
                "centroid": p.centroid.tolist(),
                "age": p.age,
                "gender": p.gender
            })
        
        # Broadcast metadata if people are detected
        if metadata:
            # We run this in the background to not block the stream
            asyncio.run_coroutine_threadsafe(
                manager.broadcast(json.dumps({"type": "update", "data": metadata})),
                manager.loop
            )

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(gen_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.library_connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def index():
    from fastapi.responses import FileResponse
    return FileResponse("core/web/static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
