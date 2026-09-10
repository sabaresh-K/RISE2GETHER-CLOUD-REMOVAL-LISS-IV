# 🌍 Generative AI-Based Cloud Removal and Reconstruction for LISS-IV Satellite Imagery


A deep learning framework for removing cloud-covered regions from high-resolution LISS-IV satellite imagery using a Generative Adversarial Network (GAN) based architecture. The model reconstructs cloud-obscured areas while preserving spatial structures and spectral consistency, enabling analysis-ready satellite imagery for downstream remote sensing applications.

---

# Project Overview

Cloud cover significantly limits the usability of optical satellite imagery in applications such as:

- Agriculture
- Disaster monitoring
- Environmental analysis
- Urban planning
- Land-use mapping

This project develops an end-to-end deep learning pipeline for cloud removal from LISS-IV imagery using a U-Net Generator trained with paired cloudy and cloud-free image patches.

---

# Features

- Patch-based LISS-IV preprocessing
- GAN-based cloud removal network
- PyTorch training pipeline
- Model checkpoint saving
- Batch inference on LISS-IV patches
- Visualization of predictions
- Quantitative evaluation using remote sensing metrics
- Modular project structure

---

# Repository Structure

```text
isro_hackathon/
│
├── checkpoints/
├── configs/
├── datasets/
├── evaluation/
├── models/
├── outputs/
│   ├── predictions/
│   ├── comparisons/
│   └── results.txt
│
├── preprocessing/
├── requirements/
├── src/
│
├── train_liss4.py
├── predict_liss4.py
├── evaluate_model.py
├── visualize_predictions.py
├── README.md
└── LICENSE
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/jeff8raaj/isro_hackathon.git
cd isro_hackathon
```

Create a virtual environment

```bash
python3 -m venv geo_ai_env
source geo_ai_env/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Training

Train the model

```bash
python train_liss4.py
```

Model checkpoints will be saved inside

```
checkpoints/
```

---

# Inference

Run prediction on the LISS-IV dataset

```bash
python predict_liss4.py
```

Predicted patches are saved to

```
outputs/predictions/
```

---

# Visualization

Generate comparison images

```bash
python visualize_predictions.py
```

Results are saved in

```
outputs/comparisons/
```

---

# Evaluation

Run quantitative evaluation

```bash
python evaluate_model.py
```

Results are saved in

```
outputs/results.txt
```

---

# Final Performance

| Metric | Value |
|---------|-------|
| PSNR | **37.2524 dB** |
| SSIM | **0.9461** |
| RMSE | **4.0317** |
| SAM | **1.3101°** |

---

# Sample Outputs

Prediction visualizations are available in

```
outputs/comparisons/
```

Each comparison contains

- Cloudy Input
- Ground Truth
- Predicted Cloud-Free Image

---

# Future Work

The following enhancements are planned and **not part of the current implementation**:

- Diffusion-based cloud removal
- Vision Transformer backbone
- Multi-modal Sentinel-1 integration
- DEM-assisted reconstruction
- Temporal image fusion
- Full-scene LISS-IV inference
- Web deployment using Streamlit

---

# Team

- Jeffrin S Raaj
- Sree Tharshan S
- L. Nibin Giovanni

---

# License


Licensed under the MIT License.