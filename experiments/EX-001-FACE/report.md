# Experiment EX-001-FACE: Face Tracking & Dashboard Logging

## Objective
To implement a persistent face tracking system that assigns unique IDs to detected individuals and maintains a real-time log file (Dashboard) that overwrites itself to show the current state of all tracked objects.

## Setup
- **Core Engine**: OpenCV DNN with Caffe models (ResNet-10 SSD for detection).
- **Tracking Logic**: Centroid-based tracking (NumPy-based implementation).
- **Dashboard**: `results/tracking_log.txt` (Live status view).

## Methodology
1. **Model Download**: Verified and downloaded lightweight pre-trained Caffe models.
2. **Persistence**: Implemented `CentroidTracker` to handle ID assignment and "disappeared" state management.
3. **Logging System**: Developed a dashboard logger that provides a snapshot of current tracked entities including position, size, and confidence score.

## Results
- **ID Persistence**: Success. IDs are assigned sequentially and maintained across frames.
- **Dashboard Utility**: Success. The log file accurately reflects the current status of the tracking system.
- **Visual Output**: Success. Tracked detections are visualized with IDs and centroids.

### Final Dashboard Output (Sample)
```text
=== FACE TRACKNG DASHBOARD (2026-02-13 03:56:35) ===
Total Active IDs: 1
--------------------------------------------------------------------------------
[ID 00] 03:56:35.051 | Pos: ( 816, 638) Size: 452x633 | Conf: 0.95 | TRACKING
--------------------------------------------------------------------------------
```

## Conclusion
The experiment demonstrates a robust foundation for multi-object tracking in video streams. The dashboard logging system provides an efficient way to monitor system status without cluttering disk space with append-only logs.
