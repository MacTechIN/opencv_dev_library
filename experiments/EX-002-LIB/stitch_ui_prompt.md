# Stitch UI Design Prompt: Face Analysis Dashboard

**Subject: Implementing a Premium Real-Time AI Face Analysis & Vector Management Dashboard**

## 1. Context & Objective
We are building a unified monitoring and control interface for a high-performance `FaceProcessor` library. The system uses OpenCV for detection and OpenFace for 128-dimensional vector embeddings, synced with Cloud Firestore. The goal is a professional, high-tech dashboard that visualizes mathematical face data and manages persistent identities.

## 2. Core UI Component Requirements (Dark Mode)

### A. Main Observation Deck (Hero Section)
*   **Live Stream**: Central high-res webcam feed.
*   **Visual Overlays**:
    *   Bounding Box (e.g., Slim Neon Blue rect).
    *   Floating Identity Label (e.g., "FaceID_001 | Trusted").
    *   Motion Centroid tracking lines (subtle trail).

### B. Functional Control Panel
*   **Toggles**:
    *   `Global Detection`: On/Off toggle.
    *   `Auto-Registration`: Toggle for new identity creation.
*   **Sliders**:
    *   `Match Threshold`: 0.0 to 1.0 (Default 0.6).
    *   `Tracking Sensitivity`: Distance multiplier.

### C. Mathematical Insight Panel (Vector Visualization)
*   **Vector Signature**: A heatmap or bar chart representing the 128-d floating-point values of the currently focused face.
*   **Similarity Score**: A percentage wheel or index (e.g., "Match Confidence: 94.2%").
    *   *Logic*: Distance < 0.2 (Very High), 0.2-0.5 (High), 0.5-0.6 (Match), > 0.6 (Unknown).

### D. Identity Management Gallery
*   **Persistent Cards**: A scrollable horizontal list of registered identities.
    *   **Image**: ROI crop of the registered face.
    *   **Status**: Online/Offline (based on last seen).
    *   **Actions**: "View Vector Data", "Sync to Cloud", "Rename/Delete".

### E. Live Audit Trail (Logs)
*   **Event Log**: A vertical scrolling terminal-style log.
    *   *Example*: `[16:42:01] System Ready: Models loaded successfully.`
    *   *Example*: `[16:42:15] FaceID_001 Detected. Euclidean Dist: 0.12`

## 3. Aesthetic & Technical Specs
*   **Technology Stack**: Next.js/React preferred with Tailwind CSS.
*   **Design System**:
    *   **Color Palette**: Deep Charcoal (#1A1A1A), Cyber Blue (#00D2FF), Success Green (#4ADE80).
    *   **Style**: Glassmorphism with subtle blurs and neon accents.
*   **Interactivity**: Smooth transitions when a person enters/leaves the frame.

## 4. Final Goal
"Make this interface feel like a mission-control center for a high-end security system, ensuring every vector and identity is transparent and verifiable in real-time."
