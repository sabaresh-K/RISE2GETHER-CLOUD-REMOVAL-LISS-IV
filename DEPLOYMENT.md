# 🚀 RISE2GETHER Deployment Guide: Satellite Cloud Removal Platform

Complete step-by-step instructions to deploy the **RISE2GETHER** Satellite Cloud Removal application online or on local servers.

---

## 🌟 Option 1: Deploy on Streamlit Community Cloud (Free & Fastest)

### Step 1: Create a GitHub Repository
1. Log in to [GitHub](https://github.com).
2. Click **New Repository** and name it `satellite-cloud-removal`.
3. In your local terminal, link your repository and push:
   ```bash
   git remote add origin https://github.com/YOUR_GITHUB_USERNAME/satellite-cloud-removal.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
2. Click **New app**.
3. Select your repository: `YOUR_GITHUB_USERNAME/satellite-cloud-removal`.
4. Set **Main file path** to: `src/app.py`.
5. Click **Deploy!** 🎉

---

## 🌟 Option 2: Deploy on Hugging Face Spaces (Free GPU/CPU Hosting)

### Step 1: Create a New Space
1. Log in to [Hugging Face](https://huggingface.co).
2. Click your profile picture -> **New Space**.
3. Name: `rise2gether-cloud-removal`.
4. Select **Streamlit** as the Space SDK.

### Step 2: Push Your Code to Hugging Face
Run the following commands in your project terminal:
```bash
git remote add hf https://huggingface.co/spaces/YOUR_HF_USERNAME/rise2gether-cloud-removal
git push hf main
```
Your app will build automatically and receive a free live link!

---

## 🌟 Option 3: Local Network / Laptop Server (Offline / College Presentations)

To run the server on your laptop and access it from mobile devices or other computers on the same Wi-Fi network:

### 1. Run Streamlit with Network Binding
```bash
python -m streamlit run src/app.py --server.address 0.0.0.0 --server.port 8501
```

### 2. Access the Application
- **On your laptop:** `http://localhost:8501`
- **On other devices (same Wi-Fi):** `http://<YOUR_LAPTOP_IP>:8501` (e.g. `http://192.168.1.5:8501`)

---

## 📋 Required Files Included in Repository
* `src/app.py` - Main Streamlit Web Application
* `requirements.txt` - Python Dependencies
* `data/generator_checkpoint.pth` - Trained Model Checkpoint

---

**Developed & Maintained by Team RISE2GETHER**
