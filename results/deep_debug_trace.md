# Deep Debugging Time-series Trace

Generated at: Fri Feb 13 22:58:55 2026

| Step | Function | Input | Output | Status | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | cv2.imread | /Users/sl/Workspace/12.Antigravity/opencv_dev/experiments/EX-002-QWEN-VL/sample.jpg | (640, 640, 3) Array | ✅ OK | Image loaded correctly |
| 2 | QwenVLProcessor.__init__ | Default weights | Model on cpu | ✅ OK | Weights loaded |
| 3 | detect_and_analyze_persons | Frame Matrix | Parsed 1 objects | ✅ OK | Check console logs for 'Qwen-VL Raw Output Content' |
| 4 | draw_analysis_overlay | 1 items | Diff Sum: 1343129 | ✅ OK | Pixels actually modified |
