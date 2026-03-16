# VentureLens Production Deployment Guide

This guide ensures a smooth production deployment of the VentureLens AI SaaS application.

## 🚀 Quick Deployment Steps

### 1. Backend: Deploy to Render
1. Create a new **Web Service** on [Render.com](https://render.com).
2. Connect your GitHub repository.
3. Set the **Root Directory** to `backend`.
4. Render will automatically detect the `render.yaml` file.
5. Add the following **Environment Variables** in the Render dashboard:
   - `OPENAI_API_KEY`
   - `GEMINI_API_KEY`
   - `SECRET_KEY` (Generate a new one)
   - `VECTOR_DB_TYPE`: `faiss` (for Lite Mode without DB)

### 2. Frontend: Deploy to Vercel
1. Create a new project on [Vercel](https://vercel.com).
2. Connect your GitHub repository.
3. Set the **Root Directory** to `frontend`.
4. Add the **Environment Variable**:
   - `NEXT_PUBLIC_API_URL`: Your Render backend URL (e.g., `https://venturelens-api.onrender.com`)

---

## 🛠️ Configuration Files Reference
- **Backend Config**: `backend/render.yaml`
- **Frontend Config**: `frontend/vercel.json`
- **Variables Examplle**: `.env.example`

## ✅ Final Validation
- Backend endpoint `POST /api/evaluate-startup` is live.
- Frontend dashboard is connected to the Render URL.
- No sensitive keys are committed (verified via `.gitignore`).

---
*VentureLens Production Suite — Analytics Ready.*
