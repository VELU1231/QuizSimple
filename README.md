# 🎯 QuizSimple

A simple, addictive, monetizable quiz web app built with Python (Flask) and vanilla HTML/CSS/JavaScript.

---

## Features

- **3 Quiz Types:**
  - 🧠 **Tech Trivia** — 15-question scored multiple-choice quiz
  - 🔮 **Personality Quiz** — "What Kind of Thinker Are You?" (10 questions)
  - ⚡ **Speed Round** — 15-second timer per question, 10 questions
- 📱 Mobile-first responsive design
- ⏱ Per-question countdown timer (timed quiz)
- 🏆 In-session leaderboard
- 📤 Share results via X (Twitter) or clipboard
- 🔄 Restart quiz option
- Instant answer feedback (correct/wrong highlighting)

---

## Project Structure

```
QuizSimple/
├── app.py               # Flask backend + all quiz data
├── requirements.txt     # Python dependencies
├── static/
│   ├── css/style.css    # Mobile-first styles
│   └── js/quiz.js       # Quiz engine (vanilla JS)
└── templates/
    ├── index.html       # Homepage — quiz selection
    └── quiz.html        # Quiz + results page
```

---

## Setup & Run

### 1. Clone & enter the repo

```bash
git clone https://github.com/VELU1231/QuizSimple.git
cd QuizSimple
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | Python 3.8+, Flask 3              |
| Frontend | HTML5, CSS3, Vanilla JavaScript   |
| Storage  | In-memory (no database needed)    |
| Fonts    | Google Fonts – Poppins            |

---

## Monetization Ideas

1. **Google AdSense** — Place ads on the results page (high impressions per session).
2. **Premium Quizzes** — Lock advanced/niche quizzes behind a $2.99/month subscription.
3. **Branded Quizzes** — Sell custom quiz creation to businesses for lead generation.
4. **Affiliate Links** — Recommend books/courses based on quiz results.
5. **Sponsored Questions** — Brands pay to be featured in questions/options.

---

## License

MIT