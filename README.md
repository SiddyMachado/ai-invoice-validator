# 🧾 AI Invoice Validator

An end-to-end AI application that extracts structured data from invoices using OCR and OpenAI-based LLM processing.

This project is designed as a foundation for building scalable AI-powered document processing systems.

---

## 🚀 Features

- Upload invoice documents (PDF, PNG, JPG)
- Extract key fields:
  - Invoice number  
  - Invoice date  
  - Total amount  
  - Currency  
  - Vendor name  
- Field-level confidence scoring
- Structured JSON output
- Persistent storage (PostgreSQL)
- File storage via S3-compatible bucket
- Live deployed frontend and backend

---

## 🧠 Architecture

---

## ⚙️ Tech Stack

- **Frontend**: Streamlit  
- **Backend**: FastAPI  
- **Database**: PostgreSQL (Railway)  
- **Storage**: S3-compatible bucket  
- **AI**:
  - OCR: Tesseract  
  - LLM: OpenAI API  
- **Infrastructure**:
  - Docker  
  - Railway (API + DB)  
  - Streamlit Cloud (UI)

---

## 📦 Processing Pipeline

Upload → OCR → LLM Extraction → Validation → Confidence Scoring → Store → Display

---

## 🔍 API Endpoints

- `POST /documents` → Upload and process document  
- `GET /documents/{document_id}/result` → Get single result  
- `GET /documents/results` → Get all processed documents  

> ⚠️ Note: Result retrieval endpoints are not yet integrated into the frontend UI.

---

## 🚧 Future Improvements

### 🗂️ Scalable Storage Enhancements
- Improve file access via presigned URLs
- Add file lifecycle management

---

### 🧠 Advanced LLM Confidence Scoring

Current limitation:
- Confidence scoring is partially heuristic / hardcoded

Planned improvements:
- LLM-generated confidence reasoning per field
- Validation based on proximity of extracted values to source text
- Explanation layer for extraction decisions
- Improved handling of ambiguous fields

---

### 📊 Accuracy Improvement & Learning Loop

- Introduce user feedback mechanism
- Store corrected outputs
- Build evaluation dataset
- Improve prompts and extraction reliability
- Enable iterative model improvements

---

### ⚡ Async Processing Pipeline

Current: Upload → Wait → Result

Planned: Upload → Queue → Background processing → Poll for result

- Introduce job queue (e.g. Celery / Redis)
- Improve scalability and responsiveness

---

### 🖥️ Frontend Enhancements

- Integrate result retrieval endpoints
- Add progress indicators
- Improve result visualization (beyond raw JSON)
- Better error handling and UX

---

### 🧪 Monitoring & Evaluation

- Track extraction accuracy
- Log model outputs
- Add confidence calibration metrics

---

## 🎯 Project Goal

This project demonstrates how to build: Scalable AI-powered document processing systems


It covers:
- End-to-end AI pipeline design  
- Backend + frontend integration  
- Cloud deployment and infrastructure  
- OCR + LLM integration  

---

## ⚠️ Disclaimer

This project is an MVP and is actively being extended toward a production-ready AI system.

---
