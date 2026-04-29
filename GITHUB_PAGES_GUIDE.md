# QuizSimple GitHub Pages Guide

This repository now contains a static build in the `out/` folder so it can be hosted for free on GitHub Pages.

## What was set up

- Static site folder: `out/`
- Homepage: `out/index.html`
- Quiz page: `out/quiz.html`
- Data bundle from Flask app: `out/static/js/data.js`
- Static quiz logic: `out/static/js/quiz.js`
- Auto deploy workflow: `.github/workflows/deploy-pages.yml`

## 1. Run locally (optional test)

From project root:

```powershell
cd "D:\velu velu\QuizSimple\QuizSimple-app"
python -m http.server 5500 -d out
```

Open:

`http://localhost:5500`

## 2. Push this project to GitHub

If this clone is on your machine and connected to your repo:

```powershell
cd "D:\velu velu\QuizSimple\QuizSimple-app"
git add .
git commit -m "Add static out build and GitHub Pages deployment"
git push origin main
```

## 3. Enable GitHub Pages in repository settings

1. Open your repository on GitHub.
2. Go to **Settings** -> **Pages**.
3. In **Build and deployment**, choose **Source: GitHub Actions**.
4. Save.

The workflow `.github/workflows/deploy-pages.yml` will deploy automatically on each push to `main`.

## 4. First deploy status

1. Open **Actions** tab in GitHub.
2. Wait for workflow **Deploy QuizSimple Static Site** to finish.
3. Your site URL appears in the workflow output and in **Settings** -> **Pages**.

Expected URL format:

`https://VELU1231.github.io/QuizSimple/`

## 5. Updating quiz content

If you edit quiz questions in `app.py`, regenerate `out/static/js/data.js`:

```powershell
cd "D:\velu velu\QuizSimple\QuizSimple-app"
.\.venv\Scripts\python.exe -c "import json; import app; print('window.ALL_QUIZZES = ' + json.dumps(app.QUIZZES, ensure_ascii=False, separators=(',', ':')) + ';')" | Out-File -FilePath out\static\js\data.js -Encoding utf8
```

Then commit and push:

```powershell
git add out/static/js/data.js
git commit -m "Update static quiz data"
git push origin main
```

## Notes

- This GitHub Pages version is fully static (no Flask backend).
- Leaderboard is browser-local using `localStorage`.
- Personality/scored logic runs entirely in the client.
