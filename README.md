# 🎬 ViralFlow: OSINT-Driven Retention Video Engine & Script Generator

An autonomous AI engine that leverages **OSINT signals** (audience retention rates, hook timings, cut cadences, and sound profiles) to transform raw user concepts into viral video scripts, cinematography shot lists, and headless ComfyUI video generation workflows.

---

## ⚡ Features

- 🔍 **OSINT Retention Scraper:** Inspects open retention patterns (TikTok, Shorts, Reels) and filters out low-retention clickbait.
- 🎭 **AI Creative Director:** Breaks down raw concepts into multi-shot cinematic breakdowns (0-2s hook POV, tracking shots, pacing).
- 🎵 **Algorithmic Music Director:** Generates BPM targets, soundtrack genres, and Foley audio layers synced to key visual frames.
- 🚀 **1-Click Free GPU ComfyUI Pipeline:** Ready-to-use Google Colab / Kaggle `.ipynb` to generate videos for **100% free** using AnimateDiff / Wan2.1 / SVD.

---

## 📂 Repository Structure

```
├── osint_video_engine.py               # Core Python Engine & OSINT Director
├── ComfyUI_Free_GPU_Video_Engine.ipynb # 1-Click Free Google Colab / Kaggle Notebook
├── osint_director_payload.json         # Sample exported GPU render bundle
└── README.md                           # Documentation & Setup Guide
```

---

## 🚀 Quickstart

### 1. Generate Retention Scripts Locally
Run the Python script engine:
```bash
python osint_video_engine.py
```
This generates `osint_director_payload.json` containing:
- Multi-shot breakdown with timing cues
- Enhanced positive & negative diffusion prompts
- BPM & audio layering instructions

### 2. Free 1-Click Cloud GPU Rendering
1. Open [Google Colab](https://colab.research.google.com/) or [Kaggle](https://www.kaggle.com/).
2. Upload `ComfyUI_Free_GPU_Video_Engine.ipynb`.
3. Set Hardware Accelerator to **T4 GPU** (Free).
4. Run all cells to launch ComfyUI with public web access.

---

## 📄 License
MIT License
