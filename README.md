# Live Body Size & Fit Recommendation System 🎥👕🤖

## 🚀 Project Overview
Live Body Size & Fit Recommendation System is an AI-powered web application that estimates a user’s **body size category (S, M, L, XL, etc.)** using **real-time video pose detection**.

The system analyzes **body part proportions** instead of exact measurements, making it more practical and accessible. The goal is to help users identify the **best-fitting clothing size** when shopping online, without using measuring tapes or physical trials.

This project is developed as a **Minimum Viable Product (MVP)** for the **Microsoft Imagine Cup Hackathon**.

---

## 🎯 Problem Statement
Online shopping often leads to:
- Confusion about correct clothing size
- Inconsistent size charts across brands
- High return rates due to poor fitting

Most users do not know their exact body measurements, and manual measurement is inconvenient.

There is a need for a **simple, contactless, and intelligent solution** that can estimate body size and recommend a best-fitting size using only a camera.

---

## 💡 Solution
Our solution uses a **video file + height** to:
1. Detect the human body in real time
2. Measure relative proportions of key body parts
3. Scale these measurements from pixel length to centimetres
4. Predict the most suitable clothing size (S / M / L / XL)

By using the **users height**, the system reduces dependency on camera distance.

---

## 🧠 Body Parts Estimated
The model estimates the size of the following body parts:

1. **Torso Length**
2. **Shoulder Length**
3. **Hip Lenght**
4. **Arm Length**
5. **Leg Length**
6. **Torso to Leg Ratio**

These features are combined to form a body profile used for size classification.

---

## 🧠 Tech Stack
### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- FastAPI

### Computer Vision & Machine Learning
- OpenCV
- MoveNet (Pose / Landmark Detection)
- TensorFlow / scikit-learn
- NumPy
- Pandas

---

## 🏗️ System Architecture
```mermaid
[Video Input + Height] 
↓
[Body / Pose Detection]
↓
[Body Part Measurement]
↓
[Ratio Normalization]
↓
[ML Size Classification]
↓
[Size Recommendation (S / M / L / XL)]
```

## ⚙️ Environment Setup

This project uses a Conda virtual environment.

### Prerequisites
- Conda (Anaconda / Miniconda)

### Setup Instructions
```bash
# Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name/backend/

# Create the environment
conda env create -f environment.yml

# Activate the environment
conda activate your_env_name
```

### Run the Project
```bash
# Run the API
cd your-repo-name/backend/
uvicorn app.main:app --reload

# Start your frontend
cd your-repo-name/frontend/
python -m http.server 5500
```