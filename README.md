# 🚀 VentureLens

**VentureLens** is an AI-powered startup intelligence platform that analyzes startup ideas and generates structured insights including market potential, competitors, SWOT analysis, and startup viability scoring.

The platform helps founders validate startup ideas **before investing time and resources**.

---

# 🌐 Overview

VentureLens uses **AI reasoning + market signals** to evaluate startup concepts.
Users enter a startup idea and the system generates a detailed **intelligence report**.

The report includes:

* Idea Summary
* Target Users
* Market Insights (TAM / SAM / SOM)
* Competitor Landscape
* SWOT Analysis
* Evaluation Matrix
* Startup Viability Score

---

# 🧠 Key Features

### AI Startup Idea Analysis

Analyze startup ideas using a structured AI reasoning pipeline.

### Market Insights

Estimate market potential using TAM / SAM / SOM framework.

### Competitor Analysis

Identify competitors and evaluate their positioning.

### SWOT Analysis

Generate strengths, weaknesses, opportunities, and threats.

### Startup Score

Evaluate idea viability using multiple strategic factors.

### Interactive Intelligence Dashboard

Clean UI displaying analysis in structured modules.

---

# 🏗️ System Architecture

```text
User
 ↓
Frontend (React / Next.js)
 ↓
API Request
 ↓
Backend (FastAPI)
 ↓
AI Engine
 ↓
Gemini API
 ↓
SerpAPI (Market signals)
 ↓
Structured Intelligence Report
 ↓
Frontend Dashboard
```

---

# ⚙️ Tech Stack

## Frontend

* React / Next.js
* TailwindCSS
* TypeScript

## Backend

* Python
* FastAPI
* Uvicorn

## AI & Data

* Gemini API
* SerpAPI

---

# 📂 Project Structure

```text
venturelens/
│
├── frontend/
│   ├── components/
│   │   ├── IdeaInput
│   │   ├── AnalysisModule
│   │   ├── MarketInsights
│   │   ├── SWOTGrid
│   │
│   ├── pages/
│   │   └── index.tsx
│   │
│   ├── styles/
│   │   ├── globals.css
│   │   └── design-system.css
│
├── backend/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── services/
│   │   └── ai_analysis.py
│   │
│   ├── utils/
│   │   └── prompt_builder.py
│   │
│   └── main.py
│
├── public/
├── README.md
└── requirements.txt
```

---

# 🚀 Getting Started

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/venturelens.git
cd venturelens
```

---

## 2️⃣ Install Frontend Dependencies

```bash
cd frontend
npm install
```

---

## 3️⃣ Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## 4️⃣ Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=your_api_key
SERP_API_KEY=your_api_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 5️⃣ Run Backend

```bash
uvicorn main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

---

## 6️⃣ Run Frontend

```bash
npm run dev
```

Frontend runs at:

```
http://localhost:3000
```

---

# 🧪 Example Use Case

Input idea:

```
AI platform that helps students prepare for coding interviews
```

Generated report includes:

* Market opportunity
* Competitors like LeetCode or InterviewBit
* SWOT analysis
* Startup viability score

---

# 📊 Future Improvements

* AI pitch deck generator
* Startup idea similarity detection
* Founder dashboard with saved reports
* Investor readiness scoring
* Market trend prediction

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Submit a pull request

---

# 📄 License

MIT License

---

# ⭐ Support

If you find this project useful, consider giving it a **star ⭐ on GitHub**.
