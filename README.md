# 📘 AI StudyVision  
### Intelligent OCR-Powered Study Assistant (Free, Offline, Python + ML)

AI StudyVision is an end-to-end AI study assistant that converts handwritten or printed images into clean digital text, generates explanations, creates study notes, and prepares MCQs — all using **free offline AI (LLMs)**.  
This project uses OCR + Machine Learning + Local LLM models (via Ollama) + Streamlit UI.

---

## 🚀 Features

### 🔍 1. Image-to-Text OCR  
- Supports handwritten + printed text  
- Fast & accurate using **EasyOCR + Tesseract**  
- Completely offline  
- Auto text cleaning  

### 🤖 2. AI Explanation Engine  
Uses **local Llama 3.1 (8B)** model to generate:  
- Step-by-step explanation  
- Beginner-friendly summary  
- Advanced conceptual explanation  
- Topic definition & keywords  

### 📝 3. Auto Notes Generator  
- Creates structured notes  
- Bullet points  
- Short definitions  
- Important terms extraction  

### ❓ 4. AI-Generated MCQs  
- Creates 5–10 MCQs for any topic  
- 1 correct + 3 distractor options  
- Stores answers for learning analytics  

### 📊 5. Progress Dashboard  
- Tracks user performance  
- Weak topics detection  
- Accuracy graphs (using SQLite + Plotly)  
- Daily usage stats  

---

## 🏗️ Tech Stack

### 🧠 **AI/ML**
- Llama 3.1 (8B local model using Ollama)
- Scikit-Learn (TF-IDF + SVM Classifier)
- NumPy, Pandas

### 🖼️ **OCR**
- EasyOCR  
- Pytesseract  
- Pillow  

### 🌐 **Frontend / Backend**
- Streamlit (UI)
- FastAPI (optional backend)

### 💾 **Database**
- SQLite

### ⚙️ **Other Tools**
- Joblib  
- Matplotlib / Plotly  

---


