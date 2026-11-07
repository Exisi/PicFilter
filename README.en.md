
<p align="center">
  <img src="/doc/images/favicon.ico" width="50">
</p>

<p align="center">PicFilter is a simple image processing tool built with Pillow, designed for batch filtering large image collections.</p>

<p align="center">
  <a href="README.md">简体中文</a> | <strong>English</strong>
</p>

<p align="center">
  <img src="/doc/images/cover.png">
</p>

# Features

- Image deduplication based on pixel histograms
- Aspect ratio filtering by minimum/maximum ratio
- Dimension filtering by minimum/maximum width and height
- Image classification into landscape, portrait, and square
- Set operations: intersection, left/right difference, and symmetric difference between two image groups

# Tech Stack

- CustomTkinter
- Pillow
- Tkinter

# Project Structure

```text
PicFilter/
├─ App.py                  # Application entry point and main UI
├─ filter/
│  ├─ Filter.py            # Deduplication, filtering, classification, set operations
│  ├─ Load.py              # File traversal, copying, and directory creation
│  └─ MyImg.py             # Image detection, size classification, histograms
├─ utils/
│  ├─ I18n.py              # Translation loading and system language detection
│  ├─ Icon.py              # Embedded application icon
│  └─ Settings.py          # User preference persistence
├─ languages/
│  ├─ zh.json              # Chinese translations
│  └─ en.json              # English translations
├─ assets/
│  └─ icons/               # UI icons (light/dark variants)
├─ doc/
│  └─ images/              # README screenshots and application icon
├─ installer/              # Installer-related files
├─ scripts/                # Helper scripts
├─ .github/workflows/      # CI configuration
├─ package.json            # Version and project metadata
├─ requirements.txt        # Python dependencies
├─ README.md               # Chinese documentation
├─ README.en.md            # English documentation
└─ LICENSE                 # MIT License
```

# Getting Started

```bash
pip install -r requirements.txt
python App.py
```

# Notes

- Deduplication does not yet detect identical images with different dimensions.
- Deduplication deletes duplicate images directly; back up important files before running it.
- Ratio/dimension filtering and classification copy matching images to the output directory; source files are not deleted.
- The input and output directories must be different.

# License

This project is licensed under the [MIT License](LICENSE).
