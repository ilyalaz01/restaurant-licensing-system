# 🏗️ TECHNICAL DOCUMENTATION

## Restaurant Licensing Assessment System

---

## TABLE OF CONTENTS

1. [System Architecture](#system-architecture)
2. [Component Details](#component-details)
3. [API Documentation](#api-documentation)
4. [Data Schema](#data-schema)
5. [Matching Algorithm](#matching-algorithm)
6. [Integration Points](#integration-points)

---

## SYSTEM ARCHITECTURE

### **High-Level Architecture Diagram**

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Home.jsx    │→ │Questionnaire │→ │  Report.jsx  │          │
│  │  (Landing)   │  │  (5 Steps)   │  │  (Display)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  React 18.3 + Vite 5.4 + Tailwind CSS 3.4                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ HTTP/HTTPS
                           │ JSON Payload
                           │
┌──────────────────────────┼──────────────────────────────────────┐
│                     SERVICE LAYER                                │
│                           │                                      │
│                    ┌──────▼──────┐                              │
│                    │   api.js    │                              │
│                    │ API Client  │                              │
│                    └──────┬──────┘                              │
│                           │                                      │
│  • submitQuestionnaire()  │                                      │
│  • getReport()            │                                      │
│  • getRegulations()       │                                      │
│  • healthCheck()          │                                      │
└───────────────────────────┴──────────────────────────────────────┘
                            │
                            │ REST API Calls
                            │ POST /api/questionnaire/submit
                            │ GET  /api/report/{report_id}
                            │
┌───────────────────────────┴──────────────────────────────────────┐
│                      BACKEND API LAYER                            │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                     index.py                              │   │
│  │  FastAPI Application + Route Handlers                     │   │
│  └────┬─────────────────┬──────────────────┬────────────────┘   │
│       │                 │                  │                     │
│       │ Validates       │ Matches          │ Saves               │
│       │                 │                  │                     │
│  ┌────▼──────┐    ┌─────▼──────┐    ┌─────▼──────┐             │
│  │business.py│    │matching_   │    │firebase_   │             │
│  │(Pydantic) │    │engine.py   │    │service.py  │             │
│  └───────────┘    └─────┬──────┘    └─────┬──────┘             │
│                          │                 │                     │
│                          │ Matched Regs    │ Stored Data         │
│                          │                 │                     │
│                    ┌─────▼──────┐          │                     │
│                    │gemini_     │          │                     │
│                    │service.py  │          │                     │
│                    └────────────┘          │                     │
│                                            │                     │
│  FastAPI 0.100 + Python 3.10 + Pydantic 2.0                     │
└───────────────────────────┬────────────────┴─────────────────────┘
                            │
                ┌───────────┼───────────┐
                │           │           │
        ┌───────▼─────┐ ┌──▼────────┐ ┌▼─────────────┐
        │regulations  │ │ Firebase  │ │ Google       │
        │.json        │ │ Firestore │ │ Gemini API   │
        │             │ │           │ │              │
        │ 30 Regs     │ │ NoSQL DB  │ │ 2.5 Flash    │
        │ Hebrew/Eng  │ │           │ │ AI Model     │
        └─────────────┘ └───────────┘ └──────────────┘
```

### **Data Flow Sequence**

```
┌────────┐                ┌─────────┐               ┌─────────┐
│ User   │                │Frontend │               │Backend  │
└───┬────┘                └────┬────┘               └────┬────┘
    │                          │                         │
    │ 1. Fills Questionnaire   │                         │
    ├─────────────────────────>│                         │
    │                          │                         │
    │                          │ 2. POST /submit         │
    │                          ├────────────────────────>│
    │                          │    business_details     │
    │                          │                         │
    │                          │                         │ 3. Validate
    │                          │                         │    (business.py)
    │                          │                         │
    │                          │                         │ 4. Match Regs
    │                          │                         │    (matching_engine.py)
    │                          │                         │
    │                          │                         │ 5. Generate Report
    │                          │                         │    (gemini_service.py)
    │                          │                         │
    │                          │                         │ 6. Save to DB
    │                          │                         │    (firebase_service.py)
    │                          │                         │
    │                          │ 7. Return report_id     │
    │                          │<────────────────────────┤
    │                          │    + summary + regs     │
    │                          │                         │
    │ 8. Display Report        │                         │
    │<─────────────────────────┤                         │
    │                          │                         │
```

### **Deployment Architecture**

```
┌──────────────────────────────────────────────────────────┐
│                    VERCEL CDN                            │
│  Global Edge Network • DDoS Protection • SSL             │
└────────────┬─────────────────────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼──────────┐  ┌──▼──────────┐
│ Frontend     │  │ Backend     │
│ Static Files │  │ Serverless  │
│              │  │ Functions   │
│ • HTML/CSS/JS│  │             │
│ • React Build│  │ • index.py  │
│ • Assets     │  │ • Auto-scale│
└──────────────┘  └──┬──────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    ┌────▼───┐  ┌───▼────┐  ┌───▼──────┐
    │Firebase│  │Gemini  │  │Vercel    │
    │Firestore│ │API     │  │Analytics │
    └────────┘  └────────┘  └──────────┘
```

---

## COMPONENT DETAILS

### **Frontend Components**

#### **1. Home.jsx**

**Purpose:** Landing page with project introduction

**Key Features:**
- Hero section with system description
- "Start Assessment" call-to-action button
- Responsive design with gradient background
- Navigation to questionnaire

**State Management:**
```javascript
// No complex state - stateless component
// Uses React Router for navigation
```

**Props:** None (standalone component)

**Routes:** 
- Path: `/`
- Navigates to: `/questionnaire`

---

#### **2. Questionnaire.jsx**

**Purpose:** 5-step form for collecting business information

**Architecture:**
```javascript
Component Structure:
├── State Management
│   ├── currentStep (1-5)
│   ├── formData (business details)
│   └── errors (validation)
│
├── Step Components
│   ├── Step 1: Basic Info (name, owner)
│   ├── Step 2: Size & Capacity
│   ├── Step 3: Business Features
│   ├── Step 4: Additional Details
│   └── Step 5: Review & Submit
│
└── Navigation
    ├── Previous/Next buttons
    ├── Progress indicator
    └── Validation per step
```

**State Structure:**
```javascript
const [formData, setFormData] = useState({
  // Step 1
  business_name: "",
  owner_name: "",
  email: "",
  phone: "",
  
  // Step 2
  size_sqm: 0,
  seating_capacity: 0,
  
  // Step 3
  features: {
    alcohol: false,
    delivery: false,
    outdoor_seating: false,
    kitchen_gas: false,
    live_music: false
  },
  
  // Step 4
  location: "",
  planned_opening_date: ""
});
```

**Validation Rules:**
```javascript
Step 2 Validation:
- size_sqm: 1-500 (required)
- seating_capacity: 0-500 (required)

Step 3 Validation:
- At least 1 feature must be selected

All Other Steps:
- Optional fields (except business_name)
```

**API Integration:**
```javascript
// On final submit
const response = await apiService.submitQuestionnaire(formData);
// Navigate to /report/{report_id}
navigate(`/report/${response.report_id}`);
```

---

#### **3. Report.jsx**

**Purpose:** Display AI-generated compliance report

**Architecture:**
```javascript
Component Structure:
├── Data Fetching
│   ├── Extract report_id from URL
│   ├── Fetch report from API
│   └── Loading/error states
│
├── Report Sections
│   ├── Business Summary
│   ├── AI Executive Summary
│   ├── Regulation List (filterable)
│   ├── Statistics (cost, timeline)
│   └── Next Steps
│
└── Interactive Features
    ├── Priority filter (All/Critical/High/Medium/Low)
    ├── Category filter
    ├── Expand/collapse regulations
    └── Print functionality
```

**Data Structure:**
```javascript
const [report, setReport] = useState({
  report_id: "",
  business_name: "",
  matched_regulations: [
    {
      id: "REG-001",
      title: "...",
      priority: "CRITICAL",
      description: "...",
      requirements: [...],
      estimated_cost: "...",
      estimated_timeframe: "..."
    }
  ],
  ai_summary: {
    executive_summary: "...",
    key_priorities: [...],
    timeline: "...",
    cost_estimate: "...",
    next_steps: [...]
  }
});
```

**Filter Logic:**
```javascript
// Priority filter
const filteredByPriority = regulations.filter(reg => 
  selectedPriority === 'all' || reg.priority === selectedPriority
);

// Category filter
const filteredByCategory = filteredByPriority.filter(reg =>
  selectedCategory === 'all' || reg.category === selectedCategory
);
```

---

### **Frontend Service Layer**

#### **api.js**

**Purpose:** HTTP client for backend communication

**Class Structure:**
```javascript
class ApiService {
  constructor() {
    this.baseURL = import.meta.env.VITE_API_URL;
  }
  
  async submitQuestionnaire(businessData) {...}
  async getReport(reportId) {...}
  async getRegulations() {...}
  async healthCheck() {...}
  getSessionId() {...}
}
```

**Error Handling:**
```javascript
try {
  const response = await fetch(url, config);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return await response.json();
} catch (error) {
  console.error('API Error:', error);
  throw error; // Propagate to component
}
```

---

### **Backend Components**

#### **1. index.py (Entry Point)**

**Purpose:** FastAPI application with route handlers

**Application Setup:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Restaurant Licensing API",
    version="1.0.0",
    description="AI-powered licensing assessment system"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Route Structure:**
```python
Endpoints:
├── GET  /                           # Root endpoint
├── GET  /api/health                 # Health check
├── POST /api/questionnaire/submit   # Main submission
├── GET  /api/report/{report_id}     # Retrieve report
└── GET  /api/regulations            # Get all regulations
```

---

#### **2. models/business.py**

**Purpose:** Pydantic models for data validation

**BusinessDetails Model:**
```python
from pydantic import BaseModel, Field
from typing import Optional, List

class BusinessDetails(BaseModel):
    # Required fields
    business_name: str = Field(..., min_length=1)
    owner_name: str = Field(..., min_length=1)
    size_sqm: int = Field(..., ge=1, le=500)
    seating_capacity: int = Field(..., ge=0, le=500)
    
    # Features (all optional)
    features: List[str] = Field(default_factory=list)
    
    # Optional fields
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    planned_opening_date: Optional[str] = None
```

**QuestionnaireSubmission Model:**
```python
class QuestionnaireSubmission(BaseModel):
    business_details: BusinessDetails
    submission_timestamp: Optional[str] = None
    session_id: Optional[str] = None
    user_agent: Optional[str] = None
```

**Validation Example:**
```python
# Automatic validation on request
@app.post("/api/questionnaire/submit")
async def submit(data: QuestionnaireSubmission):
    # If validation fails, FastAPI returns 422 automatically
    # If success, data is guaranteed valid
    business = data.business_details
    # ... process
```

---

#### **3. services/matching_engine.py**

**Purpose:** Core logic for regulation filtering

**Class Structure:**
```python
class MatchingEngine:
    def __init__(self, regulations_path: str):
        self.regulations = self._load_regulations(regulations_path)
    
    def match_regulations(
        self, 
        business_details: BusinessDetails,
        all_regulations: List[Dict]
    ) -> List[Dict]:
        """
        Returns list of applicable regulations
        """
```

**Matching Algorithm (detailed in section 5)**

---

#### **4. services/gemini_service.py**

**Purpose:** AI report generation via Google Gemini

**Class Structure:**
```python
import google.generativeai as genai

class GeminiService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_report(
        self,
        business_details: BusinessDetails,
        matched_regulations: List[Dict],
        language: str = "hebrew"
    ) -> Dict:
        """
        Generates AI-powered compliance report
        """
```

**Generation Process:**
1. Build system prompt with instructions
2. Build user prompt with business details + regulations
3. Call Gemini API with both prompts
4. Parse JSON response
5. Return structured report

---

#### **5. services/firebase_service.py**

**Purpose:** Database operations with Firestore

**Class Structure:**
```python
from firebase_admin import credentials, firestore
import firebase_admin

class FirebaseService:
    def __init__(self, credentials_json: dict):
        if not firebase_admin._apps:
            cred = credentials.Certificate(credentials_json)
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()
    
    async def save_business(self, data: dict) -> str:
        """Save business data, return report_id"""
    
    async def save_report(self, report_id: str, data: dict):
        """Save complete report"""
    
    async def get_report(self, report_id: str) -> dict:
        """Retrieve report by ID"""
```

**Collections:**
```
Firestore Structure:
├── businesses/
│   └── {report_id}/
│       ├── business_name
│       ├── size_sqm
│       ├── seating_capacity
│       ├── features
│       └── created_at
│
└── reports/
    └── {report_id}/
        ├── business_name
        ├── matched_regulations[]
        ├── ai_summary{}
        └── created_at
```

Note: Firestore reports storage is not in use right now, but can be useful for future updates.
---

## API DOCUMENTATION

### **Base URL**

**Production:** `https://restaurant-licensing-system-tz3z.vercel.app/`  
**Local:** `http://localhost:8000/api`

### **Authentication**

Currently: None (public API)  
Future: API key authentication for rate limiting

---

### **Endpoints**

#### **POST /api/questionnaire/submit**

Submit business questionnaire and receive compliance report.

**Request Body:**
```json
{
  "business_details": {
    "business_name": "My Restaurant",
    "owner_name": "John Doe",
    "size_sqm": 150,
    "seating_capacity": 80,
    "features": ["alcohol", "outdoor_seating"],
    "email": "john@example.com",
    "phone": "+972-50-1234567",
    "location": "Tel Aviv",
    "planned_opening_date": "2024-06-01"
  },
  "submission_timestamp": "2024-11-09T10:30:00Z",
  "session_id": "abc123",
  "user_agent": "Mozilla/5.0..."
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "report_id": "RPT-1699520400-abc123",
  "business_name": "My Restaurant",
  "matched_regulations_count": 24,
  "matched_regulations": [
    {
      "id": "REG-001",
      "title": "Business License",
      "title_english": "Business License",
      "category": "general_definitions",
      "priority": "CRITICAL",
      "description": "...",
      "requirements": ["..."],
      "estimated_cost": "₪500-2,000",
      "estimated_timeframe": "2-4 weeks",
      "authority": "Municipal Licensing Department"
    }
  ],
  "ai_summary": {
    "executive_summary": "Based on your business...",
    "key_priorities": [
      "Obtain business license immediately",
      "Schedule fire safety inspection"
    ],
    "timeline": "3-4 months for full compliance",
    "cost_estimate": "₪120,000-180,000",
    "next_steps": [
      "Week 1: Apply for business license",
      "Week 2: Contact fire department"
    ]
  },
  "generated_at": "2024-11-09T10:30:15Z",
  "ai_model": "gemini-1.5-flash",
  "language": "hebrew"
}
```

**Error Responses:**

```json
// 400 Bad Request
{
  "detail": "size_sqm must be between 1 and 500"
}

// 500 Internal Server Error
{
  "detail": "AI service temporarily unavailable",
  "error": "API rate limit exceeded"
}
```

---

#### **GET /api/report/{report_id}**

Retrieve previously generated report.

**Parameters:**
- `report_id` (path): Report identifier (e.g., RPT-1699520400-abc123)

**Response (200 OK):**
```json
{
  "report_id": "RPT-1699520400-abc123",
  "business_name": "My Restaurant",
  "matched_regulations": [...],
  "ai_summary": {...},
  "created_at": "2024-11-09T10:30:00Z"
}
```

**Error Responses:**
```json
// 404 Not Found
{
  "detail": "Report not found"
}
```

---

#### **GET /api/regulations**

Retrieve all available regulations (for reference).

**Response (200 OK):**
```json
{
  "total_count": 30,
  "categories": {
    "general_definitions": {...},
    "cross_sectional": {...},
    "health": {...},
    "fire": {...}
  },
  "regulations": [
    {
      "id": "REG-001",
      "title": "...",
      "category": "...",
      ...
    }
  ]
}
```

---

#### **GET /api/health**

Health check endpoint for monitoring.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2024-11-09T10:30:00Z",
  "services": {
    "database": "connected",
    "ai_service": "available",
    "regulations_loaded": true
  }
}
```

---

## DATA SCHEMA

### **Regulations JSON Structure**

**File:** `data/regulations.json`

```json
{
  "categories": {
    "general_definitions": {
      "name": "General Definitions",
      "name_hebrew": "הגדרות כלליות",
      "description": "Basic requirements for all businesses"
    },
    "cross_sectional": {
      "name": "Cross-Sectional Conditions",
      "name_hebrew": "תנאים חוצי מגזרים",
      "description": "Conditions applicable across all business types"
    },
    "health": {
      "name": "Health Requirements",
      "name_hebrew": "דרישות בריאות",
      "description": "Ministry of Health regulations"
    },
    "fire": {
      "name": "Fire Safety",
      "name_hebrew": "בטיחות אש",
      "description": "Fire department requirements"
    }
  },
  
  "regulations": [
    {
      "id": "REG-001",
      "title": "רישיון עסק",
      "title_english": "Business License",
      "category": "general_definitions",
      "priority": "CRITICAL",
      
      "description": "Every business must obtain a business license...",
      "description_english": "Every business must obtain a business license...",
      
      "requirements": [
        "Submit application to municipal licensing department",
        "Provide business plan and financial documents",
        "Pay application fee"
      ],
      "requirements_english": [...],
      
      "applicable_to": {
        "always_required": true,
        "size_threshold": null,
        "seating_threshold": null,
        "requires_both": false,
        "features": []
      },
      
      "estimated_cost": "₪500-2,000",
      "estimated_cost_english": "₪500-2,000",
      
      "estimated_timeframe": "2-4 weeks",
      "estimated_timeframe_english": "2-4 weeks",
      
      "authority": "Municipal Licensing Department",
      "authority_english": "Municipal Licensing Department",
      
      "notes": "...",
      "notes_english": "..."
    }
  ]
}
```

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (REG-XXX) |
| `title` | string | Regulation name in Hebrew |
| `title_english` | string | Regulation name in English |
| `category` | string | Category key from categories object |
| `priority` | enum | CRITICAL, HIGH, MEDIUM, LOW |
| `description` | string | Full explanation (Hebrew) |
| `requirements` | array | List of specific requirements |
| `applicable_to` | object | Matching conditions (see below) |
| `estimated_cost` | string | Cost range with currency |
| `estimated_timeframe` | string | Time estimate |
| `authority` | string | Responsible government body |

**Applicable_To Conditions:**

```json
{
  "always_required": false,
  "size_threshold": 50,           // Triggers if size >= 50
  "seating_threshold": null,      // No seating requirement
  "requires_both": false,         // OR logic (either size OR seating)
  "features": ["alcohol"]         // Requires alcohol feature
}
```

**Logic:**
- `always_required: true` → Applies to all businesses
- `size_threshold: X` → Applies if size_sqm >= X
- `seating_threshold: Y` → Applies if seating_capacity >= Y
- `requires_both: true` → Size AND Seating both must exceed thresholds
- `requires_both: false` → Size OR Seating (either one)
- `features: [...]` → Applies if business has ANY listed feature

---

### **Database Schema (Firestore) (not in use, but can be used in the future)**

#### **Collection: businesses**

```
businesses/{report_id}
├── business_name: string
├── owner_name: string
├── size_sqm: number
├── seating_capacity: number
├── features: array<string>
├── email: string | null
├── phone: string | null
├── location: string | null
├── planned_opening_date: string | null
└── created_at: timestamp
```

#### **Collection: reports**

```
reports/{report_id}
├── report_id: string
├── business_name: string
├── matched_regulations: array<object>
│   ├── [0]
│   │   ├── id: string
│   │   ├── title: string
│   │   ├── priority: string
│   │   └── ...
│   └── [1]...
│
├── ai_summary: object
│   ├── executive_summary: string
│   ├── key_priorities: array<string>
│   ├── timeline: string
│   ├── cost_estimate: string
│   └── next_steps: array<string>
│
├── metadata: object
│   ├── ai_model: string
│   ├── regulations_version: string
│   ├── language: string
│   └── processing_time: number
│
└── created_at: timestamp
```

---

## MATCHING ALGORITHM

### **Core Matching Logic**

**Algorithm Flow:**
```
1. Load all regulations from JSON
2. Initialize empty matched_regulations list
3. For each regulation:
   a. Check if always_required → Add to list
   b. Check threshold conditions → Add if met
   c. Check feature requirements → Add if met
4. Sort by priority (CRITICAL → HIGH → MEDIUM → LOW)
5. Return matched list
```

### **Detailed Pseudocode**

```python
def match_regulations(business, all_regulations):
    matched = []
    
    for regulation in all_regulations:
        conditions = regulation['applicable_to']
        
        # Rule 1: Always required regulations
        if conditions.get('always_required', False):
            matched.append(regulation)
            continue
        
        # Rule 2: Threshold-based matching
        size_ok = True
        seating_ok = True
        
        if conditions.get('size_threshold') is not None:
            size_ok = business.size_sqm >= conditions['size_threshold']
        
        if conditions.get('seating_threshold') is not None:
            seating_ok = business.seating_capacity >= conditions['seating_threshold']
        
        # Apply AND/OR logic
        if conditions.get('requires_both', False):
            # Both conditions must be true (AND)
            threshold_met = size_ok and seating_ok
        else:
            # At least one condition true (OR)
            threshold_met = size_ok or seating_ok
        
        # Check if any threshold exists and is met
        has_threshold = (
            conditions.get('size_threshold') is not None or 
            conditions.get('seating_threshold') is not None
        )
        
        if has_threshold and threshold_met:
            matched.append(regulation)
            continue
        
        # Rule 3: Feature-based matching
        required_features = conditions.get('features', [])
        if required_features:
            # Business must have ALL required features
            if all(feat in business.features for feat in required_features):
                matched.append(regulation)
                continue
    
    # Rule 4: Sort by priority
    priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    matched.sort(key=lambda r: priority_order.get(r['priority'], 4))
    
    return matched
```

### **Matching Examples**

**Example 1: Small Café**
```python
Business:
- size_sqm: 40
- seating_capacity: 25
- features: []

Matched Regulations:
✅ REG-001 (always_required: true)
✅ REG-002 (always_required: true)
❌ REG-015 (size_threshold: 50) - Business too small
❌ REG-028 (size: 301 AND seating: 300) - Thresholds not met
❌ REG-020 (features: ["alcohol"]) - No alcohol service

Total: 22 regulations
```

**Example 2: Medium Bar & Grill**
```python
Business:
- size_sqm: 85
- seating_capacity: 65
- features: ["alcohol", "outdoor_seating"]

Matched Regulations:
✅ REG-001 (always_required: true)
✅ REG-015 (size_threshold: 50) - 85 >= 50
✅ REG-020 (features: ["alcohol"]) - Has alcohol
✅ REG-021 (features: ["outdoor_seating"]) - Has outdoor
❌ REG-028 (size: 301 AND seating: 300) - Not large enough

Total: 24 regulations
```

**Example 3: Large Restaurant**
```python
Business:
- size_sqm: 400
- seating_capacity: 380
- features: ["alcohol", "kitchen_gas", "live_music"]

Matched Regulations:
✅ REG-001 (always_required: true)
✅ REG-015 (size_threshold: 50) - 400 >= 50
✅ REG-016 (seating_threshold: 50) - 380 >= 50
✅ REG-020 (features: ["alcohol"]) - Has alcohol
✅ REG-028 (size: 301 AND seating: 300) - 400 >= 301 AND 380 >= 300
✅ All feature-specific regulations

Total: 27 regulations
```

### **Edge Cases**

**Case 1: Exactly at Threshold**
```python
Business: size_sqm = 50
Regulation: size_threshold = 50
Result: ✅ MATCHED (>= comparison, not >)
```

**Case 2: AND Logic with One Condition Met**
```python
Business: size_sqm = 350, seating_capacity = 250
Regulation: size_threshold = 301 AND seating_threshold = 300
Result: ❌ NOT MATCHED (requires_both: true, but seating < 300)
```

**Case 3: OR Logic with One Condition Met**
```python
Business: size_sqm = 350, seating_capacity = 40
Regulation: size_threshold = 301 OR seating_threshold = 300
Result: ✅ MATCHED (requires_both: false, size condition met)
```

**Case 4: Multiple Features Required**
```python
Business: features = ["alcohol", "outdoor_seating"]
Regulation: features = ["alcohol", "outdoor_seating", "live_music"]
Result: ❌ NOT MATCHED (business missing "live_music")

Note: Current implementation requires ALL features
Future: Could add "any_of" vs "all_of" logic
```

### **Performance Considerations**

**Time Complexity:**
- Matching: O(n × m) where n = regulations, m = avg conditions per regulation
- Sorting: O(k log k) where k = matched regulations
- Overall: O(n × m + k log k)

**Typical Performance:**
- 30 regulations
- ~3-5 conditions per regulation
- Result: <10ms processing time

**Optimization Opportunities:**
1. Cache regulations in memory (already done)
2. Index regulations by threshold ranges
3. Parallel processing for large regulation sets
4. Precompute always_required list

---

## INTEGRATION POINTS

### **External Services**

#### **1. Google Gemini API**

**Integration:** `services/gemini_service.py`

**Configuration:**
```python
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')
```

**Request Format:**
```python
response = model.generate_content(
    [system_prompt, user_prompt],
    generation_config={
        "temperature": 0.7,
        "top_p": 0.95,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json"
    }
)
```

**Rate Limits:**
- Free Tier: 15 requests/minute
- Paid Tier: 1000 requests/minute
- Error Handling: Retry with exponential backoff

---

#### **2. Firebase Firestore**

**Integration:** `services/firebase_service.py`

**Configuration:**
```python
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(json.loads(os.getenv('FIREBASE_CREDENTIALS')))
firebase_admin.initialize_app(cred)
db = firestore.client()
```

**Operations:**
```python
# Write
doc_ref = db.collection('reports').document(report_id)
doc_ref.set(data)

# Read
doc = db.collection('reports').document(report_id).get()
if doc.exists:
    return doc.to_dict()
```

**Indexes:**
- Primary: report_id (document ID)
- Secondary: created_at (for queries)
- No compound indexes needed currently

---

#### **3. Vercel Serverless**

**Configuration:** `vercel.json`

```json
{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    }
  ],
  "env": {
    "GEMINI_API_KEY": "@gemini-api-key",
    "FIREBASE_CREDENTIALS": "@firebase-credentials"
  }
}
```

**Deployment:**
```bash
# Automatic on git push to main
vercel --prod

# Manual deployment
cd project-root
vercel deploy --prod
```

---

### **Environment Variables**

#### **Backend (.env)**
```env
# Required
GEMINI_API_KEY=AIza...
FIREBASE_CREDENTIALS={"type":"service_account",...}

# Optional
ALLOWED_ORIGINS=http://localhost:5173,https://yourdomain.com
LOG_LEVEL=INFO
```

#### **Frontend (.env)**
```env
# Required
VITE_API_URL=https://restaurant-licensing-system-tz3z.vercel.app/api

# Development
# VITE_API_URL=http://localhost:8000/api
```

---

### **Error Handling Strategy**

**Frontend:**
```javascript
try {
  const response = await apiService.submitQuestionnaire(data);
  // Success
} catch (error) {
  if (error.message.includes('429')) {
    // Rate limit - show retry message
  } else if (error.message.includes('500')) {
    // Server error - show support contact
  } else {
    // Generic error - show error message
  }
}
```

**Backend:**
```python
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if app.debug else "Contact support"
        }
    )
```

check link: https://restaurant-licensing-system-tz3z.vercel.app/api/health

---

## TESTING STRATEGY

### **Unit Tests**

**File:** `api/tests/test_matching_engine.py`

**Test Coverage:**
```python
def test_small_business_no_features():
    """Businesses below thresholds get only always_required"""
    
def test_medium_business_or_logic():
    """Either size OR seating triggers regulation"""
    
def test_large_business_and_logic():
    """Both size AND seating required"""
    
def test_feature_matching():
    """Feature-specific regulations apply correctly"""
    
def test_priority_sorting():
    """Results sorted CRITICAL > HIGH > MEDIUM > LOW"""
```

**Run Tests:**
```bash
cd api
python -m pytest tests/ -v

# Output:
# ✅ test_small_business_no_features PASSED
# ✅ test_medium_business_or_logic PASSED
# ✅ test_large_business_and_logic PASSED
# ✅ test_feature_matching PASSED
# ✅ test_priority_sorting PASSED
# ✅ test_edge_cases PASSED
# ✅ test_exactly_at_threshold PASSED
```

---

### **Response Times**

**Breakdown (POST /submit):**
- Validation: <10ms
- Matching: <10ms
- AI Generation: 10-15s (99%)
- Database Save: 0ms
- Response Build: <50ms

**Bottleneck:** Gemini API call (unavoidable)

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11 | Initial release |

---

**Document Status:** Complete  
**Last Updated:** November 2025  
**Maintained By:** Ilya Lazarev
