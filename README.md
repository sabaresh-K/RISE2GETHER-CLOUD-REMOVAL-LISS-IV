# 🛰️ CloudClear-LISS — AI-Powered Satellite Imagery Cloud Removal & Reconstruction

A deep learning framework and interactive web platform for removing cloud-covered regions from high-resolution **LISS-IV** (5.8m spatial resolution) satellite imagery using a PyTorch GAN/UNet architecture and multi-sensor SAR fusion. The model reconstructs cloud-obscured ground terrain while preserving spatial structures, spectral integrity, and GIS metadata.

---

## 🌟 Key Features

- **5.8m Native LISS-IV Resolution Preservation:** Reconstructs obscured ground textures without spatial downscaling.
- **Multi-Sensor SAR Fusion Support:** Combines optical reflection with Sentinel-1 C-band active radar backscatter.
- **LISS-IV Multi-Band Stacking & Conversion Engine:** Dedicated preprocessing module to upload single-band GeoTIFFs (Band 2: Green, Band 3: Red, Band 4: NIR), perform 2%-98% radiometric haze normalization, and generate False Color Composite (FCC) PNGs & 3-band GeoTIFF rasters.
- **Interactive Streamlit Web Dashboard:** Modern dark titanium & emerald green space-themed pitch deck UI.
- **Quantitative Benchmark Evaluation:** Real-time calculation of PSNR, SSIM, RMSE, and SAM metrics.
- **GIS-Ready GeoTIFF Export:** Full spatial CRS projection metadata transfer for downstream land-use classification.

---

## 📂 Repository Structure

```text
RISE2GETHER-CLOUD-REMOVAL-LISS-IV/
│
├── checkpoints/          # Trained model weights & PyTorch generator checkpoints
├── configs/              # System configuration manifests
├── data/                 # Benchmark dataset assets & checkpoints
├── datasets/             # LISS-IV & Sentinel-1 paired patch datasets
├── evaluation/           # Quantitative evaluation scripts
├── models/               # PyTorch UNet & CycleGAN model architectures
├── outputs/              # Generated cloud-free rasters, comparisons & previews
├── preprocessing/        # Radiometric calibration & sub-pixel alignment modules
├── src/                  # Core application source code & Streamlit app (src/app.py)
├── server.py             # Python HTTP server & inference API endpoint
├── style.css             # Master dark space stylesheet
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 💻 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sabaresh-K/RISE2GETHER-CLOUD-REMOVAL-LISS-IV.git
cd RISE2GETHER-CLOUD-REMOVAL-LISS-IV
```

### 2. Create a Virtual Environment

```bash
python -m venv geo_ai_env
# On Windows:
geo_ai_env\Scripts\activate
# On Linux/macOS:
source geo_ai_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Application

### Launch Streamlit Interactive Web Application

```bash
python -m streamlit run src/app.py
```

Open your browser at `http://localhost:8501`.

### Launch Backend HTTP Inference Server

```bash
python server.py
```

Server active at `http://localhost:8000`.

---

## 📊 Performance Benchmarks

| Metric | Benchmark Value | Description |
|---|---|---|
| **PSNR** | **30.24 dB** | Peak Signal-to-Noise Ratio |
| **SSIM** | **0.8840** | Structural Similarity Index |
| **RMSE** | **0.0320** | Root Mean Square Error |
| **SAM** | **4.52°** | Spectral Angle Mapper |
| **Mask Accuracy** | **94.6%** | Cloud Mask Extraction Accuracy |
| **Inference Speed** | **2.84s** | Per 512x512 Patch |

---

## 👥 Team Rise2Gether

- **Sabaresh K**
- **Saadhana S**
- **Pranika R**

**Institution:** Sri Eshwar College of Engineering and Technology, Coimbatore, Tamil Nadu, India.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.