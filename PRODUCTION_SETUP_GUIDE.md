# 🚀 QuizSimple Production Setup Guide

**Status:** ✅ Fully Implemented & Deployed  
**Last Updated:** April 29, 2026  
**Backend:** Deployed to Vercel  
**Frontend:** Deployed to GitHub Pages  
**Database:** Ready for Supabase setup  

---

## 📋 What's Been Completed

### ✅ Backend Features
- [x] Flask REST API (deployed to Vercel)
- [x] Session-based admin authentication (username/password)
- [x] Admin login page (`/auth/login`)
- [x] Admin dashboard (`/admin`) with:
  - Leaderboard table showing all scores
  - Filter by quiz_id
  - Clear leaderboard button (delete all scores)
  - Logout button
- [x] Protected API endpoints:
  - `GET /api/admin/leaderboard` (protected, returns JSON)
  - `DELETE /api/admin/leaderboard` (protected, clears scores)
- [x] Health check endpoint (`/api/health`) showing storage mode
- [x] Quiz submission endpoint (`/api/submit`) for storing scores
- [x] Supabase REST API integration (no native SDK to avoid build issues)
- [x] In-memory fallback when Supabase env vars missing

### ✅ Frontend Features
- [x] Quiz engine with prev/next navigation
- [x] Answer selection with visual feedback
- [x] **220ms armed guard to prevent accidental auto-advance** ⭐ (THE FIX)
- [x] localStorage progress recovery
- [x] Results screen with scoring
- [x] Deployed to GitHub Pages

### ✅ Database Setup
- [x] Supabase schema SQL prepared (enhanced with docs)
- [x] RLS policies for security
- [x] Performance indexes
- [x] Ready to run in Supabase SQL Editor

### ✅ Git & Deployment
- [x] Latest fixes committed to main
- [x] Backend deployed to Vercel (auto on commit)
- [x] Frontend deployed to GitHub Pages (auto on commit)

---

## 🔧 The Auto-Advance Bug Fix (SOLVED)

**Problem:** Quiz was advancing to next question immediately after clicking answer

**Root Cause:** No delay guard between answer selection and next button activation

**Solution:** Added `nextArmedAt` timestamp with 220ms guard

**How It Works:**
```javascript
// When user clicks answer:
function selectAnswer(optIdx) {
  state.answers[String(state.currentIdx)] = optIdx;
  state.nextArmedAt = Date.now() + 220;  // ← Set future timestamp
  renderQuestion();
}

// When user clicks Next button:
function goNext() {
  if (Date.now() < state.nextArmedAt) return;  // ← Guard: skip if not armed yet
  // ... proceed to next question
}
```

**Result:** 220ms delay (imperceptible to user) prevents accidental rapid double-taps from triggering auto-advance

**Files Modified:**
- `app/static/js/quiz.js` (backend)
- `out/static/js/quiz.js` (frontend/GitHub Pages)

---

## 🎯 Quick Start - 3 Steps to Production

### Step 1: Set Environment Variables on Vercel

Go to: [Vercel Dashboard](https://vercel.com) → Your Project → Settings → Environment Variables

Add these keys:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc... (from Supabase → Settings → API)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-strong-password-here
SECRET_KEY=output-of: python -c "import secrets; print(secrets.token_hex(32))"
FLASK_ENV=production
```

**Save and redeploy** (Vercel will auto-trigger)

### Step 2: Run Supabase Schema SQL

1. Open [Supabase Dashboard](https://supabase.com) → Your Project
2. Go to **SQL Editor** (left menu)
3. Click **New Query**
4. Copy entire contents from: `app/data/supabase_schema.sql`
5. Click **Run** (green play button)
6. Verify no red errors

**What this does:**
- Creates `public.quiz_scores` table
- Sets up 3 performance indexes
- Enables Row-Level Security
- Creates public read policy (everyone sees leaderboard)
- Creates service role policy (server-only writes)

### Step 3: Update Frontend API URL

Edit `out/index.html` and find:
```javascript
const API_URL = 'http://localhost:5000';
```

Change to your Vercel URL:
```javascript
const API_URL = 'https://quizsimple.vercel.app';  // example
```

Then commit and push:
```bash
git add out/index.html
git commit -m "config: update API endpoint to production"
git push origin main
```

GitHub Pages will automatically redeploy.

---

## 🔐 Environment Variables Reference

Create `.env` file in project root (for local development):

```env
# Flask Config
FLASK_ENV=development  (or production)
SECRET_KEY=<random-32-char-hex-string>

# Supabase API
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc...  (⚠️ Keep secret! Never commit!)

# Admin Login
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password

# Optional
CORS_ORIGIN=https://velu1231.github.io  (for production)
```

**On Vercel:** Set these same variables in Environment Variables section (already sensitive)

---

## 🧪 Testing Checklist

### Frontend Test (https://velu1231.github.io/QuizSimple/)
- [ ] Page loads quiz list
- [ ] Click "Start Quiz"
- [ ] Answer question by clicking option
- [ ] **Verify: Next button is now clickable (not auto-advancing)**
- [ ] Click "Next" button manually
- [ ] Advance 2-3 questions
- [ ] Answer remaining and click "Finish"
- [ ] Enter name and submit
- [ ] See results page with score

### Backend API Tests (curl or Postman)

Check health:
```bash
curl https://quizsimple.vercel.app/api/health
# Expected: {"status": "ok", "storage": "supabase"}
```

Submit quiz score:
```bash
curl -X POST https://quizsimple.vercel.app/api/submit \
  -H "Content-Type: application/json" \
  -d '{
    "quiz_id": "test-quiz",
    "name": "Test Player",
    "score": 80,
    "max_score": 100,
    "answers": {"0": 0, "1": 1}
  }'
```

### Admin Panel Test (https://quizsimple.vercel.app/admin)
- [ ] Redirects to login page
- [ ] Login with Admin Username + Admin Password
- [ ] See leaderboard with scores from quiz submissions
- [ ] Filter by quiz_id dropdown
- [ ] Click "Clear Leaderboard" → prompts confirmation
- [ ] Click "Logout" → redirected to login
- [ ] Login again with wrong password → error message

### Supabase Database Test
1. Go to Supabase → Your Project → SQL Editor
2. Run:
```sql
SELECT * FROM public.quiz_scores ORDER BY created_at DESC LIMIT 5;
```
3. Should see quiz submissions from your testing

---

## 📂 File Structure & Purpose

```
QuizSimple/
├── app/
│   ├── routes/
│   │   ├── main.py       (GET / and GET /admin dashboard)
│   │   ├── auth.py       (GET/POST /auth/login, POST /auth/logout)
│   │   ├── api.py        (POST /api/submit, GET/DELETE /api/admin/leaderboard)
│   │   └── quiz.py       (GET /quiz/:id endpoint)
│   ├── services/
│   │   ├── auth_service.py      (Session login, @require_auth decorator)
│   │   ├── quiz_service.py      (Quiz scoring, leaderboard queries)
│   │   └── supabase_service.py  (REST API calls to Supabase)
│   ├── templates/
│   │   ├── admin_login.html     (Login form)
│   │   ├── admin_dashboard.html (Leaderboard + controls)
│   │   ├── quiz.html            (Quiz page)
│   │   └── base.html            (Layout template)
│   ├── static/
│   │   ├── js/
│   │   │   └── quiz.js          (220ms armed guard FIX HERE)
│   │   └── css/
│   │       └── style.css        (Admin + auth styles)
│   └── data/
│       └── supabase_schema.sql  (Database setup script) ⭐
├── out/
│   └── static/js/
│       └── quiz.js              (Same FIX mirrored for GitHub Pages)
├── run.py                       (Flask app entry point)
├── requirements.txt             (Python dependencies)
├── .env.example                 (Template for env vars)
└── PRODUCTION_SETUP_GUIDE.md   (This file)
```

---

## 🚨 Troubleshooting

### Quiz Still Auto-Advancing?
**Solution:**
1. Hard refresh browser: `Ctrl+Shift+Delete` → Clear cache
2. Force reload: `Ctrl+F5`
3. Check Network tab (F12) → `quiz.js` should have `nextArmedAt` in code
4. Verify Vercel deployment has new code (check commit hash in project)

### Admin Login Shows 401 Unauthorized
**Solution:**
1. Verify env vars are set on Vercel: Settings → Environment Variables
2. Check `ADMIN_USERNAME` and `ADMIN_PASSWORD` are correct
3. Redeploy Vercel after adding env vars
4. Try username: `admin` (default)

### Supabase Connection Failing
**Solution:**
1. Check `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are set
2. Verify they match your actual Supabase project
3. Test endpoint: `GET /api/health` should return:
   ```json
   {"status": "ok", "storage": "supabase"}
   ```
   If it shows `"storage": "memory-fallback"` → env vars not loaded
4. Redeploy Vercel after adding/fixing env vars

### Leaderboard Empty in Admin Panel
**Solution:**
1. Verify Supabase table exists: Dashboard → Tables → `quiz_scores`
2. Submit a quiz first from frontend
3. Check Supabase → SQL Editor → run:
   ```sql
   SELECT COUNT(*) FROM public.quiz_scores;
   ```
4. If count is 0, scoring isn't reaching database
   - Check `/api/health` to verify storage mode
   - Check browser console (F12) for fetch errors

### CORS Errors
**Solution:**
1. Verify `API_URL` in `out/index.html` matches Vercel backend URL
2. Backend has CORS enabled for all origins (ok for public quiz)
3. Clear browser cache and reload

---

## 🔒 Security Checklist

- [x] Admin password NOT in code (stored in Vercel env vars)
- [x] Supabase service key NOT in code (stored in Vercel env vars)
- [x] RLS policies restrict writes to service role only
- [x] Session cookies used (not JWT tokens exposed)
- [x] Frontend deployed over HTTPS
- [x] Backend deployed over HTTPS (Vercel)
- [x] No hardcoded credentials in git history

---

## 📊 What Happens Behind the Scenes

### User Takes Quiz
1. Frontend loads quiz from JSON
2. User answers questions (220ms guard prevents accidental next)
3. User clicks "Finish"
4. Frontend POSTs to `/api/submit` with answers
5. Backend calculates score
6. Score saved to Supabase via REST API

### Admin Reviews Scores
1. Admin logs in at `/admin`
2. Flask sessions store username
3. `@require_auth` decorator protects route
4. Dashboard GETs `/api/admin/leaderboard` (protected)
5. Supabase returns scores (public read policy)
6. Table displayed with filtering options
7. Admin can DELETE to clear scores

### Leaderboard Queries
- **Get top scores:** `SELECT * FROM quiz_scores WHERE quiz_id = 'X' ORDER BY score DESC LIMIT 10`
- **Get all quizzes:** `SELECT DISTINCT(quiz_id) FROM quiz_scores`
- **Delete by quiz:** `DELETE FROM quiz_scores WHERE quiz_id = 'X'` (service role only)

---

## 📞 Support / Next Steps

**Already Done:**
✅ All code implemented and committed to main  
✅ Backend auto-deployed to Vercel  
✅ Frontend auto-deployed to GitHub Pages  
✅ Auto-advance bug fixed (220ms guard)  
✅ Admin panel fully functional  
✅ Supabase schema ready  

**Your Next Steps:**
1. Set Vercel environment variables (Step 1 above)
2. Run Supabase SQL schema (Step 2 above)
3. Update frontend API URL (Step 3 above)
4. Test with the checklist above
5. Monitor `/api/health` endpoint for storage mode

**Optional Future Enhancements:**
- Add quiz CRUD admin interface (create/edit/delete questions)
- Upgrade to Supabase Auth for multi-user admin support
- Add email notifications on quiz submission
- Export leaderboard to CSV
- Real-time leaderboard updates via Supabase Realtime

---

## 🎉 Done!

Your QuizSimple app is production-ready. Follow the 3 quick steps above to finish setup.

Questions? Check the troubleshooting section or review the code comments in:
- `app/services/auth_service.py` (authentication logic)
- `app/static/js/quiz.js` (frontend with 220ms guard)
- `app/data/supabase_schema.sql` (database structure)

**Current Deployment URLs:**
- 🎯 Frontend: https://velu1231.github.io/QuizSimple/
- ⚙️ Backend: https://quizsimple.vercel.app (or your Vercel URL)
- 🔐 Admin: https://quizsimple.vercel.app/admin

