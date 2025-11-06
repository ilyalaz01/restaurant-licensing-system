# Restaurant Licensing Assessment System - Frontend

AI-powered system to help restaurant owners understand licensing requirements in Israel.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Update .env with your backend URL (already set to production)
# VITE_API_URL=https://restaurant-licensing-system-tz3z.vercel.app

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Home.jsx           # Landing page
│   │   ├── Questionnaire.jsx  # Multi-step form
│   │   └── Report.jsx         # AI report display
│   ├── services/
│   │   ├── api.js            # Backend API integration
│   │   ├── config.js         # Firebase config
│   │   └── database.js       # Firebase database operations
│   ├── App.jsx               # Main app with routing
│   ├── main.jsx              # Entry point
│   └── index.css             # Global styles (Tailwind)
├── public/                    # Static assets
├── package.json              # Dependencies
└── vite.config.js           # Vite configuration
```

## 🎯 Features

### Multi-Step Questionnaire
- **Step 1:** Basic business information (name, owner, contact)
- **Step 2:** Size and capacity (sqm, seating)
- **Step 3:** Business features (alcohol, delivery, outdoor, gas, music)
- **Step 4:** Additional details (location, dates, existing business)
- **Step 5:** Review and submit

### AI-Generated Report
- Personalized summary
- Matched regulations by priority
- Required documents list
- Clear next steps
- Printable format

## 🔌 Backend Integration

The frontend connects to the FastAPI backend at:
```
https://restaurant-licensing-system-tz3z.vercel.app
```

### API Endpoints Used:
- `POST /api/questionnaire/submit` - Submit questionnaire
- `GET /api/report/{report_id}` - Get generated report
- `GET /api/health` - Health check

## 🎨 Styling

Built with **Tailwind CSS** for:
- Responsive design (mobile-first)
- Professional UI components
- Consistent color scheme
- Print-friendly report layout

## 🚀 Deployment

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Or connect via Vercel dashboard:
# 1. Import GitHub repository
# 2. Framework: Vite
# 3. Root Directory: frontend
# 4. Build Command: npm run build
# 5. Output Directory: dist
```

### Environment Variables on Vercel
Set these in your Vercel project settings:
```
VITE_API_URL=https://restaurant-licensing-system-tz3z.vercel.app
```

## 📱 User Flow

1. **Landing Page** - User sees overview and starts assessment
2. **Questionnaire** - User fills out 5-step form
3. **Loading** - AI analyzes business details
4. **Report** - User views personalized report with:
   - Business summary
   - Applicable regulations (by priority)
   - Required documents
   - Next steps
5. **Actions** - User can print report or start new assessment

## 🧪 Development

```bash
# Start dev server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 🔧 Configuration

### Vite Configuration
See `vite.config.js` for build settings.

### Tailwind Configuration
See `tailwind.config.js` for custom theme and styles.

## 📊 Data Flow

```
User Input (Questionnaire)
    ↓
Frontend Validation
    ↓
API Service (api.js)
    ↓
Backend API (FastAPI)
    ↓
AI Processing (Gemini)
    ↓
Report Generation
    ↓
Display to User
```

## 🎨 Design Decisions

### Why Multi-Step Form?
- Better UX for complex data collection
- Progressive disclosure of information
- Clear progress indication
- Easy validation per step

### Why Tailwind CSS?
- Rapid development
- Consistent design system
- Easy responsive design
- Small bundle size in production

### Why React Router?
- Clean URL structure
- Easy navigation
- Report sharing via URL
- Browser back/forward support

## 🔒 Security Notes

- No sensitive data stored in frontend
- All processing done on backend
- Environment variables for configuration
- CORS handled by backend

## 📈 Performance

- Lazy loading for routes
- Optimized build with Vite
- Minimal dependencies
- Responsive images and assets

## 🐛 Troubleshooting

### "Cannot connect to backend"
- Check `VITE_API_URL` in `.env`
- Verify backend is deployed and running
- Check network/CORS issues

### "Build fails"
- Ensure Node.js 18+
- Clear node_modules and reinstall
- Check for TypeScript errors in console

### "Styles not working"
- Ensure Tailwind is properly configured
- Check `postcss.config.cjs` exists
- Rebuild after config changes

## 📝 License

Part of the Restaurant Licensing Assessment System project.

## 👥 Contributors

Built as part of a technical assessment project demonstrating:
- Modern React development
- API integration
- Professional UI/UX
- AI-powered features
