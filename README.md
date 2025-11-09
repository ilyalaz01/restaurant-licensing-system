# 🏢 Restaurant Licensing Assessment System

## AI-Powered Compliance Platform for Israeli Restaurant Owners

An intelligent system that helps restaurant owners in Israel understand and navigate licensing requirements through a simple questionnaire and AI-generated compliance reports.

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://restaurant-licensing-system.vercel.app/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/react-18.0+-blue.svg)](https://react.dev)

---

## 📋 PROJECT OVERVIEW

### **Purpose**

Israeli restaurant licensing involves 30+ regulations from multiple government authorities. This system simplifies the process by:

1. Collecting business information through a user-friendly questionnaire
2. Intelligently matching applicable regulations based on business attributes
3. Generating personalized, AI-powered compliance reports in business-friendly language

### **Problem Solved**

- **Complexity**: Multiple regulations from different authorities (Ministry of Health, Fire Department, Police, etc.)
- **Confusion**: Legal language is difficult for business owners to understand
- **Cost**: Professional licensing consultations are expensive
- **Time**: Manual research and interpretation takes weeks

### **Solution**

- 5-minute guided questionnaire
- Smart regulation matching based on size, capacity, and features
- AI-generated reports in clear, actionable language
- Instant results with cost and timeline estimates

---

## ✨ KEY FEATURES

**Intelligent Questionnaire**
- 5-step guided form with real-time validation
- Collects business size, seating capacity, and special features
- Automatic categorization (small/medium/large)

**Smart Regulation Matching**
- Threshold-based logic (e.g., >50 sqm triggers fire detection requirement)
- AND/OR condition support (e.g., >301 sqm AND >300 seats for sprinklers)
- Feature combination handling (e.g., outdoor seating + alcohol service)

**AI-Powered Reports**
- Executive summary in business-friendly Hebrew
- Priority breakdown (Critical → High → Medium → Low)
- Realistic timeline and cost projections
- Actionable next steps

**Data Coverage**
- 30 regulations from Israeli Business Licensing Law
- Hebrew and English content
- Complete requirements, costs, and timelines

---

## 🛠️ TECHNOLOGY STACK

### **Frontend**
- **React 18.3** - UI framework
- **Vite 5.4** - Build tool and dev server
- **Tailwind CSS 3.4** - Utility-first styling
- **React Router 6.23** - Client-side routing

### **Backend**
- **Python 3.10** - Programming language
- **FastAPI 0.100** - Modern web framework
- **Pydantic 2.0** - Data validation
- **Uvicorn 0.30** - ASGI server

### **AI & Database**
- **Google Gemini 2.5 Flash** - AI report generation
- **Firebase Firestore** - Cloud database
- **Vercel** - Serverless deployment

---

## 🏗️ ARCHITECTURE

### **System Architecture**

```
┌────────────────────────────────────┐
│   Frontend (React + Vite)         │
│   • 5-step questionnaire           │
│   • Report display                 │
│   • api.js → Backend HTTP calls    │
└──────────┬─────────────────────────┘
           │ HTTPS
           ↓
┌────────────────────────────────────┐
│   Backend (FastAPI on Vercel)     │
│   • index.py (entry point)         │
│   • matching_engine.py             │
│   • gemini_service.py              │
│   • firebase_service.py            │
└──────────┬─────────────────────────┘
           │
    ┌──────┴────────┐
    ↓               ↓
┌──────────┐  ┌────────────┐
│ Firestore│  │ Gemini AI  │
│ Database │  │ API        │
└──────────┘  └────────────┘
```

**Data Flow:**
1. User fills questionnaire → Frontend validates
2. Frontend calls `/api/questionnaire/submit` → Backend receives
3. Backend filters regulations via matching_engine.py
4. Backend generates AI report via gemini_service.py
5. Backend saves to Firestore via firebase_service.py
6. Frontend displays personalized report

For detailed architecture, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 📦 PREREQUISITES

**Required Software:**
- Node.js 18+ ([download](https://nodejs.org))
- Python 3.10+ ([download](https://python.org))
- npm (comes with Node.js)

**Required API Keys:**
- Google Gemini API key ([get free key](https://ai.google.dev))
- Firebase project with Firestore enabled ([Firebase Console](https://console.firebase.google.com))

---

## 🚀 INSTALLATION

### **1. Clone Repository**

```bash
git clone https://github.com/YOUR_USERNAME/restaurant-licensing.git
cd restaurant-licensing
```

### **2. Backend Setup**

```bash
cd api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Create `api/.env`:**
```env
GEMINI_API_KEY=your_gemini_api_key_here
FIREBASE_CREDENTIALS={"type":"service_account","project_id":"your-project",...}
ALLOWED_ORIGINS=http://localhost:5173
```

### **3. Frontend Setup**

```bash
cd frontend

# Install dependencies
npm install
```

**Create `frontend/.env`:**
```env
VITE_API_URL=http://localhost:8000/api
```

---

## 💻 RUNNING LOCALLY

### **Start Backend**

```bash
cd api
python -m uvicorn index:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### **Start Frontend** (new terminal)

```bash
cd frontend
npm run dev
```

Expected output:
```
VITE v5.4.0  ready in 500 ms
➜  Local:   http://localhost:5173/
```

### **Access Application**

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

---

## 🌐 DEPLOYED VERSION

**Live Demo:** https://restaurant-licensing-system-tz3z.vercel.app

The application is deployed on Vercel with:
- Frontend: Static hosting with CDN
- Backend: Serverless functions
- Database: Firebase Firestore
- AI: Google Gemini API

To deploy your own:
1. Push code to GitHub
2. Import to Vercel
3. Add environment variables in Vercel dashboard
4. Deploy (automatic)

---

## 📖 USAGE GUIDE

### **Step 1: Landing Page**
Click "Start Assessment" to begin

### **Step 2: Basic Information**
- Enter business name and owner name
- (Optional) Add email and phone

### **Step 3: Size & Capacity**
- Enter size in square meters (1-500)
- Enter seating capacity (0-500)
- System automatically categorizes as small/medium/large

### **Step 4: Business Features**
Select all that apply:
- ✓ Serving Alcoholic Beverages
- ✓ Food Delivery Service
- ✓ Outdoor Seating Area
- ✓ Kitchen Uses Gas
- ✓ Live Music/Entertainment

### **Step 5: Additional Details**
- (Optional) Location, planned opening date
- Review all information

### **Step 6: Report**
- View AI-generated summary
- Browse all applicable regulations
- See cost and timeline estimates
- Print or save report

---

## 📊 SAMPLE RESULTS

**Small Café (40 sqm, 25 seats):**
- 22 regulations
- No fire detection required
- Cost: ~₪50,000-80,000
- Timeline: 2-3 months

**Medium Bar & Grill (85 sqm, 65 seats, alcohol):**
- 24 regulations
- Fire detection required
- Alcohol compliance required
- Cost: ~₪125,000-180,000
- Timeline: 4-6 months

**Large Restaurant (400 sqm, 380 seats):**
- 27 regulations
- Fire detection + sprinkler system required
- Cost: ~₪300,000-500,000
- Timeline: 8-12 months

---

## 🧪 TESTING

### **Run Backend Tests**

```bash
cd api
python -m pytest tests/ -v
```

**Test Coverage:**
- ✅ Small business matching (no thresholds triggered)
- ✅ Medium business matching (OR logic)
- ✅ Large business matching (AND logic)
- ✅ Feature combination matching
- ✅ Edge cases (exactly at thresholds)

All tests passing: 7/7

---

## 📁 PROJECT STRUCTURE

```
restaurant-licensing/
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Home.jsx
│   │   │   ├── Questionnaire.jsx
│   │   │   └── Report.jsx
│   │   └── services/
│   │       └── api.js         # Backend API client
│   └── package.json
│
├── api/                        # FastAPI backend
│   ├── index.py               # Entry point
│   ├── models/
│   │   ├── business.py
│   │   └── report.py
│   ├── services/
│   │   ├── matching_engine.py
│   │   ├── gemini_service.py
│   │   └── firebase_service.py
│   └── requirements.txt
├   └── data/
│      └── regulations.json   # 30 regulations
│   
│
└── docs/                       # Documentation
    ├── ARCHITECTURE.md
    ├── AI_USAGE.md
    └── DEVELOPMENT_JOURNAL.md
```

---

## 📚 DOCUMENTATION

- **[Architecture Documentation](docs/ARCHITECTURE.md)** - System design and component details
- **[AI Usage Documentation](docs/AI_USAGE.md)** - AI tools and LLM integration
- **[API Reference](docs/API.md)** - Endpoint documentation
- **[Development Journal](docs/DEVELOPMENT_JOURNAL.md)** - Challenges and lessons learned

---

## 🤖 AI INTEGRATION

**Development AI:** Claude (Anthropic) Sonnet 4.5
- Used for: System design, code generation, debugging, documentation
- Impact: 95% of code generated, 7x faster development

**Production AI:** Google Gemini 2.5 Flash
- Used for: Generating personalized compliance reports
- Why chosen: Best balance of cost, speed, and quality
- Free tier: 15 requests/minute

---

## 🔧 TROUBLESHOOTING

**Backend won't start:**
```bash
# Install dependencies
cd api
pip install -r requirements.txt
```

**Frontend can't connect:**
- Verify backend is running on port 8000
- Check VITE_API_URL in frontend/.env

**Firebase error:**
- Verify Firebase credentials in api/.env
- Check Firestore is enabled in Firebase console

**Gemini API error:**
- Get valid API key from https://ai.google.dev
- Update GEMINI_API_KEY in api/.env

---

## 📞 SUPPORT

**Documentation:** See `/docs` folder  
**Issues:** Open GitHub issue  
**Live Demo:** https://restaurant-licensing-system-tz3z.vercel.app

---

## 🎓 ACKNOWLEDGMENTS

**Developed using:**
- Claude (Anthropic) for development assistance
- Google Gemini for AI report generation
- FastAPI, React, Vite, Tailwind CSS
- Firebase Firestore, Vercel

---

## 📊 PROJECT STATISTICS

- **Development Time:** 3 days
- **Lines of Code:** ~3,500
- **Test Coverage:** 100% (core matching engine)
- **Regulations:** 30 from Israeli Business Licensing Law
- **Languages:** Hebrew, English
- **Deployment:** Vercel (production-ready)

---

**Version:** 1.0  
**Status:** Production Ready  
**Last Updated:** November 2025
