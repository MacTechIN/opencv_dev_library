# VisionAI-Platform Library Management & Coding Standards

This document defines the standard rules for systematically operating libraries and writing reusable functions within this platform.

## 1. Coding Standards

Functions must be **"readable, predictable, and independent."**

- **Naming**: 
  - Use `snake_case` and aim for `verb_noun` format. (e.g., `draw_bboxes`, `preprocess_image`)
  - Avoid ambiguous abbreviations. (`p_img` (X) -> `preprocess_image` (O))
- **Type Hinting**: 
  - Using Python type hints is mandatory.
  - Example: `def process(frame: np.ndarray) -> np.ndarray:`
- **Docstrings**: 
  - Comply with Google Style and specify **Function Description, Args, Returns, and Raises**.
- **Single Responsibility**: 
  - A single function should perform only one clearly defined task.

## 2. Library Promotion Process

Not all code is stored in `core/` from the beginning.

1.  **Experimenting Phase**: New features are written in `utils.py` or `main.py` inside `experiments/EX-XXX/`.
2.  **Verification Phase**: A feature becomes a candidate for promotion when it works successfully in experiments and shows potential for use in **at least two or more experiments**.
3.  **Promotion to Core**:
    - Modify the code to be generalized and independent of specific experiments.
    - Move it to the appropriate subdirectory in `core/`.
    - Record the promotion history in `{directory}+history.md`.

## 3. Directory Roles

- `core/base/`: Abstract classes and interface definitions that serve as parents for all processors.
- `core/processing/`: Primarily pure functions with clear **input -> output**, such as image filtering, ROI extraction, and color conversion.
- `core/models/`: Engine wrapper classes for loading and inferencing AI models.
- `core/utils/`: Support functions outside of business logic, such as logging, file I/O, and system checks.

## 4. Version & History Management

- Any changes must be recorded in the `history.md` of the corresponding directory.
- For **Breaking Changes** (changes that break existing code), increment the version by `vX.0.0` units and write a migration guide in `docs/`.

---

> [!TIP]
> **The best library is one where usage can be understood just by looking at the code, even without documentation.** Put the most effort into clear naming and type hinting.
