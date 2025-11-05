# 🚀 Deployment Guide - Restaurant Licensing System

## Prerequisites
1. GitHub account
2. Vercel account (free)
3. Firebase account (free)
4. Google Cloud account for Gemini API (free tier)

## Step 1: Firebase Setup

### 1.1 Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create Project"
3. Name it: `restaurant-licensing`
4. Disable Google Analytics (optional)
5. Click "Create Project"

### 1.2 Set Up Realtime Database
1. In Firebase Console, go to "Realtime Database"
2. Click "Create Database"
3. Choose your region (closest to you)
4. Start in "Test mode" for now
5. Copy the database URL (you'll need it later)

### 1.3 Get Firebase Configuration
1. Go to Project Settings (gear icon)
2. Scroll to "Your apps" section
3. Click "Add app" → Choose Web (</>)
4. Register app name: `restaurant-licensing-web`
5. Copy the configuration object:

```javascript
const firebaseConfig = {
  apiKey: "...",
  authDomain: "...",
  databaseURL: "...",
  projectId: "...",
  storageBucket: "...",
  messagingSenderId: "...",
  appId: "..."
};
```

### 1.4 Set Database Rules (Important!)
Go to Realtime Database → Rules tab and set:

```json
{
  "rules": {
    "businesses": {
      ".read": true,
      ".write": true
    },
    "reports": {
      ".read": true,
      ".write": true
    },
    "regulations": {
      ".read": true,
      ".write": false
    },
    "analytics": {
      ".read": false,
      ".write": true
    }
  }
}
```

## Step 2: Google Gemini API Setup

### 2.1 Get API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the API key (keep it secure!)

## Step 3: GitHub Setup

### 3.1 Create Repository
1. Create a new repository on GitHub
2. Name: `restaurant-licensing-system`
3. Make it public or private (your choice)
4. Don't initialize with README

### 3.2 Push Code
```bash
cd restaurant-licensing
git init
git add .
git commit -m "Initial commit: Restaurant Licensing System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/restaurant-licensing-system.git
git push -u origin main
```

## Step 4: Vercel Deployment

### 4.1 Frontend Deployment
1. Go to [Vercel](https://vercel.com/)
2. Sign in with GitHub
3. Click "Add New Project"
4. Import your GitHub repository
5. Configure:
   - Framework Preset: `Vite`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

### 4.2 Environment Variables (Frontend)
In Vercel project settings → Environment Variables, add:

```
VITE_FIREBASE_API_KEY=your-firebase-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
VITE_API_URL=https://your-backend.vercel.app/api
```

### 4.3 Backend API Deployment
1. Create another Vercel project
2. Import the same repository
3. Configure:
   - Framework Preset: `Other`
   - Root Directory: `api`
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

### 4.4 Environment Variables (Backend)
In backend Vercel project settings, add:

```
GEMINI_API_KEY=your-gemini-api-key
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
```

### 4.5 Create Vercel Configuration
Create `api/vercel.json`:

```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

## Step 5: Firebase Admin SDK Setup (for Backend)

### 5.1 Generate Service Account Key
1. In Firebase Console → Project Settings → Service Accounts
2. Click "Generate new private key"
3. Save the JSON file securely
4. Add the content to Vercel environment variables as `FIREBASE_SERVICE_ACCOUNT`

## Step 6: Initial Data Setup

### 6.1 Upload Regulations to Firebase
1. Go to Firebase Console → Realtime Database
2. Click "Import JSON"
3. Upload the `api/data/regulations.json` file

OR use the Firebase Admin SDK to upload programmatically.

## Step 7: Testing

### 7.1 Test URLs
- Frontend: `https://your-app.vercel.app`
- Backend API: `https://your-api.vercel.app/api`
- API Health: `https://your-api.vercel.app/api/health`

### 7.2 Test Flow
1. Open frontend URL
2. Fill out the questionnaire
3. Submit and wait for report generation
4. Check Firebase Console for saved data

## Step 8: Custom Domain (Optional)

### 8.1 Add Custom Domain in Vercel
1. Go to Project Settings → Domains
2. Add your domain
3. Follow DNS configuration instructions

## Troubleshooting

### Common Issues:

**CORS Errors:**
- Make sure API URL in frontend env matches backend deployment
- Check CORS settings in `api/main.py`

**Firebase Connection Issues:**
- Verify Firebase configuration in environment variables
- Check database rules allow read/write
- Ensure database URL includes `https://`

**Gemini API Errors:**
- Verify API key is correct
- Check you're within free tier limits (60 requests/minute)
- Ensure API is enabled in Google Cloud Console

**Build Failures:**
- Check Node.js version compatibility
- Verify all dependencies are in `package.json`
- Check Python version (3.9+) for backend

## Production Checklist

- [ ] Firebase security rules configured properly
- [ ] Environment variables set in Vercel
- [ ] API endpoints tested
- [ ] Error handling working
- [ ] Mobile responsive design verified
- [ ] Performance optimized (lazy loading, caching)
- [ ] Analytics tracking working
- [ ] Backup/export functionality tested
- [ ] Rate limiting configured
- [ ] SSL certificates active (automatic with Vercel)

## Monitoring

### Firebase Console
- Monitor database usage
- Check analytics events
- Review error logs

### Vercel Dashboard
- Monitor function invocations
- Check build logs
- Review performance metrics

## Support

For deployment issues:
1. Check Vercel build logs
2. Review Firebase Console errors
3. Test API endpoints directly
4. Verify environment variables

## Next Steps

After successful deployment:
1. Test complete user flow
2. Set up monitoring alerts
3. Configure backup strategy
4. Plan for scaling if needed
5. Document API for future development

---

**Congratulations! Your Restaurant Licensing System is now live! 🎉**
