# Restaurant Licensing System - Project Structure

## 🏗️ Complete Project Architecture

```
restaurant-licensing/
├── frontend/                      # React Frontend (Deploy to Vercel)
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Layout/
│   │   │   │   │   ├── Layout.jsx
│   │   │   │   │   ├── Header.jsx
│   │   │   │   │   ├── Footer.jsx
│   │   │   │   │   └── index.js
│   │   │   │   ├── Loading/
│   │   │   │   │   ├── LoadingSpinner.jsx
│   │   │   │   │   ├── LoadingSkeleton.jsx
│   │   │   │   │   └── index.js
│   │   │   │   └── Error/
│   │   │   │       ├── ErrorBoundary.jsx
│   │   │   │       ├── ErrorMessage.jsx
│   │   │   │       └── index.js
│   │   │   ├── questionnaire/
│   │   │   │   ├── QuestionnaireContainer.jsx
│   │   │   │   ├── StepManager/
│   │   │   │   │   ├── StepManager.jsx
│   │   │   │   │   ├── StepIndicator.jsx
│   │   │   │   │   └── StepNavigation.jsx
│   │   │   │   ├── steps/
│   │   │   │   │   ├── BusinessInfoStep.jsx
│   │   │   │   │   ├── SizeCapacityStep.jsx
│   │   │   │   │   ├── FeaturesStep.jsx
│   │   │   │   │   ├── ReviewStep.jsx
│   │   │   │   │   └── index.js
│   │   │   │   └── FormFields/
│   │   │   │       ├── TextField.jsx
│   │   │   │       ├── NumberField.jsx
│   │   │   │       ├── CheckboxGroup.jsx
│   │   │   │       └── index.js
│   │   │   ├── report/
│   │   │   │   ├── ReportContainer.jsx
│   │   │   │   ├── ReportHeader.jsx
│   │   │   │   ├── ReportSections/
│   │   │   │   │   ├── ExecutiveSummary.jsx
│   │   │   │   │   ├── RequirementsSection.jsx
│   │   │   │   │   ├── TimelineSection.jsx
│   │   │   │   │   ├── CostSection.jsx
│   │   │   │   │   └── ActionItems.jsx
│   │   │   │   ├── ExportOptions.jsx
│   │   │   │   └── RequirementCard.jsx
│   │   │   └── ui/              # Reusable UI components
│   │   │       ├── Button.jsx
│   │   │       ├── Card.jsx
│   │   │       ├── Badge.jsx
│   │   │       ├── Alert.jsx
│   │   │       ├── Progress.jsx
│   │   │       └── index.js
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── QuestionnairePage.jsx
│   │   │   ├── ReportPage.jsx
│   │   │   ├── AboutPage.jsx
│   │   │   └── NotFoundPage.jsx
│   │   ├── services/
│   │   │   ├── api/
│   │   │   │   ├── client.js       # Axios configuration
│   │   │   │   ├── endpoints.js    # API endpoint constants
│   │   │   │   └── interceptors.js # Request/response interceptors
│   │   │   ├── firebase/
│   │   │   │   ├── config.js       # Firebase configuration
│   │   │   │   ├── database.js     # Realtime Database operations
│   │   │   │   └── index.js
│   │   │   ├── questionnaire.service.js
│   │   │   ├── report.service.js
│   │   │   └── storage.service.js  # Local storage management
│   │   ├── hooks/
│   │   │   ├── useQuestionnaire.js
│   │   │   ├── useReport.js
│   │   │   ├── useFirebase.js
│   │   │   ├── useLoading.js
│   │   │   └── useError.js
│   │   ├── context/
│   │   │   ├── AppContext.jsx      # Global app state
│   │   │   ├── QuestionnaireContext.jsx
│   │   │   └── ThemeContext.jsx
│   │   ├── utils/
│   │   │   ├── constants.js        # App-wide constants
│   │   │   ├── validators.js       # Form validation functions
│   │   │   ├── formatters.js       # Data formatting utilities
│   │   │   ├── helpers.js          # General helper functions
│   │   │   └── regulations.js      # Regulation data and logic
│   │   ├── styles/
│   │   │   ├── index.css          # Global styles + Tailwind
│   │   │   └── animations.css     # Custom animations
│   │   ├── assets/
│   │   │   ├── images/
│   │   │   └── icons/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── router.jsx
│   ├── public/
│   │   └── favicon.ico
│   ├── .env.example
│   ├── .env.local
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── vercel.json              # Vercel configuration
│   └── README.md
│
├── api/                         # Python Backend (Vercel Serverless)
│   ├── main.py                 # Main FastAPI app
│   ├── requirements.txt
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py   # Gemini AI integration
│   │   ├── matching_engine.py  # Regulation matching logic
│   │   ├── firebase_service.py # Firebase operations
│   │   └── report_generator.py # Report generation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── business.py         # Business data models
│   │   ├── regulation.py       # Regulation models
│   │   └── report.py          # Report models
│   ├── data/
│   │   └── regulations.json    # Processed regulation data
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── vercel.json            # Vercel serverless config
│
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   ├── AI_USAGE.md
│   └── DEVELOPMENT_JOURNAL.md
│
├── .gitignore
├── README.md
└── package.json                # Root package.json for scripts
```

## 📦 Key Dependencies

### Frontend
- **Core**: React 18, Vite 5, React Router 6
- **UI**: Tailwind CSS 3, Framer Motion, React Icons
- **Forms**: React Hook Form, Yup validation
- **API**: Axios, React Query
- **Firebase**: firebase (Realtime Database)
- **Utils**: date-fns, uuid, jsPDF (for export)

### Backend (Python API)
- **Core**: FastAPI, Pydantic
- **AI**: google-generativeai
- **Firebase**: firebase-admin
- **Utils**: python-dotenv, python-multipart

## 🔥 Firebase Structure

```json
{
  "businesses": {
    "businessId": {
      "details": {...},
      "createdAt": "timestamp",
      "status": "active"
    }
  },
  "reports": {
    "reportId": {
      "businessId": "...",
      "generatedAt": "timestamp",
      "content": {...},
      "aiGenerated": true
    }
  },
  "regulations": {
    "categories": {...},
    "items": {...}
  },
  "analytics": {
    "daily": {...},
    "totals": {...}
  }
}
```

## 🚀 Deployment Configuration

### Vercel Frontend
- Auto-deploy from GitHub
- Environment variables in Vercel dashboard
- Build command: `npm run build`
- Output directory: `dist`

### Vercel API (Serverless)
- Python serverless functions
- API routes at `/api/*`
- Environment variables for secrets

## 📱 Component Responsibilities

### Smart Components (Containers)
- Handle business logic
- Connect to Firebase
- Manage state
- API calls

### Presentational Components
- Display data
- Handle UI interactions
- Reusable across pages
- No direct API calls

### Service Layer
- Centralized API communication
- Firebase operations
- Error handling
- Data transformation

### Context/State Management
- Global app state (AppContext)
- Form state (QuestionnaireContext)
- Theme preferences (ThemeContext)
