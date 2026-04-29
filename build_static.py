"""
build_static.py — Writes all static files for the out/ folder.
Run: python build_static.py
"""
import os, json, textwrap

ROOT = os.path.join(os.path.dirname(__file__), "out")

def w(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote {rel}")

# ── Load quiz data ────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "app", "data", "quizzes.json")
with open(DATA_PATH, encoding="utf-8") as f:
    QUIZZES = json.load(f)

# ─────────────────────────────────────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────────────────────────────────────
CSS = """\
/* ===== QuizSimple — Green Premium + Light/Dark Mode =====
   Quizller-inspired: staggered animations, scale hover, instant feedback
   ============================================================ */

/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

/* ── Design Tokens ── */
:root {
  /* Green premium palette */
  --green-50:  #f0fdf4;
  --green-100: #dcfce7;
  --green-200: #bbf7d0;
  --green-400: #4ade80;
  --green-500: #22c55e;
  --green-600: #16a34a;
  --green-700: #15803d;
  --green-900: #14532d;
  --lime-400:  #a3e635;

  /* Light mode defaults */
  --bg:           #f8fafc;
  --surface:      #ffffff;
  --surface-2:    #f1f5f9;
  --border:       #e2e8f0;
  --text:         #0f172a;
  --text-muted:   #64748b;
  --accent:       #16a34a;
  --accent-light: #dcfce7;
  --accent-glow:  rgba(22,163,74,.18);
  --accent2:      #0ea5e9;
  --shadow:       0 4px 24px rgba(0,0,0,.08);
  --shadow-lg:    0 8px 40px rgba(0,0,0,.12);
  --radius:       14px;
  --radius-sm:    8px;
  --transition:   .25s cubic-bezier(.4,0,.2,1);
}

/* Dark mode */
[data-theme="dark"] {
  --bg:           #0d1117;
  --surface:      #161b22;
  --surface-2:    #1c2333;
  --border:       #30363d;
  --text:         #e6edf3;
  --text-muted:   #7d8590;
  --accent:       #22c55e;
  --accent-light: rgba(34,197,94,.12);
  --accent-glow:  rgba(34,197,94,.22);
  --accent2:      #38bdf8;
  --shadow:       0 4px 24px rgba(0,0,0,.4);
  --shadow-lg:    0 8px 40px rgba(0,0,0,.6);
}

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  font-family: 'Inter', sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  min-height: 100vh;
  transition: background var(--transition), color var(--transition);
}

a { color: inherit; text-decoration: none; }
button { cursor: pointer; font-family: inherit; border: none; background: none; }
ul { list-style: none; }
img { display: block; max-width: 100%; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 99px; }

/* ── Utility ── */
.container { width: min(1160px, 100% - 2rem); margin-inline: auto; }
.sr-only { position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0); }

/* ── Theme Toggle ── */
.theme-toggle {
  width: 42px; height: 42px;
  border-radius: 50%;
  border: 1.5px solid var(--border);
  background: var(--surface);
  color: var(--text);
  font-size: 1.1rem;
  display: grid; place-items: center;
  transition: var(--transition);
  box-shadow: var(--shadow);
}
.theme-toggle:hover { border-color: var(--accent); background: var(--accent-light); }

/* ── Navbar ── */
.navbar {
  position: sticky; top: 0; z-index: 100;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
.nav-inner {
  display: flex; align-items: center; justify-content: space-between;
  height: 64px;
}
.nav-logo { display: flex; align-items: center; gap: .5rem; }
.logo-icon {
  width: 36px; height: 36px; border-radius: 10px;
  background: linear-gradient(135deg, var(--green-600), var(--green-400));
  display: grid; place-items: center;
  font-size: 1.1rem; color: #fff; font-weight: 700;
  box-shadow: 0 2px 8px var(--accent-glow);
}
.logo-text {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700; font-size: 1.15rem; letter-spacing: -.02em;
  background: linear-gradient(135deg, var(--green-600), var(--green-500));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.nav-actions { display: flex; align-items: center; gap: .75rem; }

/* ── Hero ── */
.hero {
  padding: 5rem 0 3.5rem;
  text-align: center;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: .4rem;
  padding: .35rem .9rem;
  background: var(--accent-light);
  border: 1px solid var(--green-200);
  border-radius: 99px;
  font-size: .8rem; font-weight: 600;
  color: var(--accent);
  margin-bottom: 1.25rem;
  letter-spacing: .03em;
}
[data-theme="dark"] .hero-badge { border-color: rgba(34,197,94,.25); }
.hero-badge .badge-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--accent);
  animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
  0%,100% { opacity: 1; transform: scale(1); }
  50%      { opacity: .5; transform: scale(1.4); }
}
.hero h1 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 700; line-height: 1.1;
  letter-spacing: -.03em;
  margin-bottom: 1rem;
}
.gradient-text {
  background: linear-gradient(135deg, var(--green-600) 0%, var(--green-400) 50%, var(--lime-400) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero p {
  font-size: 1.1rem; color: var(--text-muted);
  max-width: 520px; margin: 0 auto 2rem;
}

/* ── Quiz Grid ── */
.quiz-section { padding: 1.5rem 0 4rem; }
.section-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.5rem; font-weight: 700;
  margin-bottom: 1.5rem;
  display: flex; align-items: center; gap: .6rem;
}
.section-title::before {
  content: '';
  display: block; width: 4px; height: 1.4em;
  background: linear-gradient(to bottom, var(--green-500), var(--green-400));
  border-radius: 99px;
}
.quiz-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
}
.quiz-card {
  display: flex; flex-direction: column;
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  padding: 1.4rem;
  transition: var(--transition);
  position: relative; overflow: hidden;
  box-shadow: var(--shadow);
}
.quiz-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--green-500), var(--lime-400));
  transform: scaleX(0); transform-origin: left;
  transition: transform var(--transition);
}
.quiz-card:hover { 
  border-color: var(--accent);
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg), 0 0 0 1px var(--accent-glow);
}
.quiz-card:hover::before { transform: scaleX(1); }
.card-icon { font-size: 2.2rem; margin-bottom: .75rem; display: block; }
.card-content { flex: 1; }
.card-category {
  font-size: .72rem; font-weight: 600; letter-spacing: .08em;
  text-transform: uppercase; color: var(--accent);
  display: block; margin-bottom: .3rem;
}
.card-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.1rem; font-weight: 700;
  margin-bottom: .4rem; line-height: 1.2;
}
.card-desc {
  font-size: .85rem; color: var(--text-muted);
  margin-bottom: 1rem; line-height: 1.5;
}
.card-meta { display: flex; gap: .5rem; flex-wrap: wrap; }
.meta-badge {
  font-size: .72rem; font-weight: 600; padding: .25rem .6rem;
  border-radius: 99px; background: var(--surface-2); color: var(--text-muted);
  border: 1px solid var(--border);
}
.diff-easy   { background: #dcfce7; color: #15803d; border-color: #bbf7d0; }
.diff-medium { background: #fef9c3; color: #854d0e; border-color: #fde68a; }
.diff-hard   { background: #fee2e2; color: #991b1b; border-color: #fecaca; }
[data-theme="dark"] .diff-easy   { background: rgba(34,197,94,.15); color: #4ade80; border-color: rgba(34,197,94,.3); }
[data-theme="dark"] .diff-medium { background: rgba(234,179,8,.15);  color: #facc15; border-color: rgba(234,179,8,.3); }
[data-theme="dark"] .diff-hard   { background: rgba(239,68,68,.15);  color: #f87171; border-color: rgba(239,68,68,.3); }
.card-arrow {
  margin-top: 1.25rem; font-size: 1.1rem; color: var(--text-muted);
  transition: var(--transition); align-self: flex-end;
}
.quiz-card:hover .card-arrow { color: var(--accent); transform: translateX(4px); }

/* ── How it works ── */
.how-section { padding: 3rem 0 4rem; border-top: 1px solid var(--border); }
.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.25rem; margin-top: 1.5rem;
}
.step-card {
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem; text-align: center;
  box-shadow: var(--shadow);
}
.step-num {
  width: 40px; height: 40px; border-radius: 50%;
  background: linear-gradient(135deg, var(--green-600), var(--green-400));
  color: #fff; font-weight: 700; font-size: 1.1rem;
  display: grid; place-items: center; margin: 0 auto .75rem;
  box-shadow: 0 2px 8px var(--accent-glow);
}
.step-card h3 { font-size: .95rem; font-weight: 700; margin-bottom: .35rem; }
.step-card p  { font-size: .82rem; color: var(--text-muted); }

/* ── Footer ── */
.footer {
  border-top: 1px solid var(--border);
  padding: 1.5rem 0; text-align: center;
  font-size: .8rem; color: var(--text-muted);
}

/* ═══════════════════════════════════════════════════════════════════
   QUIZ PAGE
   ═══════════════════════════════════════════════════════════════════ */

/* ── Screens ── */
.screen { display: none; }
.screen.active { display: block; }

/* ── Start Screen ── */
.start-wrap {
  min-height: calc(100vh - 64px);
  display: flex; align-items: center; justify-content: center;
  padding: 2rem 1rem;
}
.start-card {
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  padding: 2.5rem 2rem;
  max-width: 520px; width: 100%;
  text-align: center;
  box-shadow: var(--shadow-lg);
}
.start-card::before {
  content: '';
  display: block; height: 4px;
  background: linear-gradient(90deg, var(--green-500), var(--lime-400));
  border-radius: var(--radius) var(--radius) 0 0;
  margin: -2.5rem -2rem 2rem;
}
#start-icon { font-size: 3rem; margin-bottom: .5rem; }
#start-category {
  font-size: .72rem; font-weight: 600; letter-spacing: .08em;
  text-transform: uppercase; color: var(--accent);
}
#start-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.5rem; font-weight: 700; margin: .5rem 0;
}
#start-desc { font-size: .9rem; color: var(--text-muted); margin-bottom: 1rem; }
#start-meta { display: flex; gap: .5rem; justify-content: center; flex-wrap: wrap; margin-bottom: 1.5rem; }
.name-input {
  width: 100%; padding: .65rem 1rem;
  border: 1.5px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--surface-2);
  color: var(--text); font-size: .9rem; font-family: inherit;
  transition: var(--transition); margin-bottom: 1rem;
}
.name-input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-glow); }
.btn-primary {
  display: inline-flex; align-items: center; gap: .5rem;
  padding: .75rem 2rem; border-radius: var(--radius-sm);
  background: linear-gradient(135deg, var(--green-600), var(--green-500));
  color: #fff; font-weight: 600; font-size: .95rem;
  transition: var(--transition);
  box-shadow: 0 2px 12px var(--accent-glow);
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px var(--accent-glow);
}
.btn-primary:active { transform: none; }

/* ── Quiz Screen ── */
.quiz-layout { max-width: 700px; margin: 0 auto; padding: 2rem 1rem; }

/* Progress */
.progress-wrap { margin-bottom: 1.5rem; }
.progress-info {
  display: flex; justify-content: space-between; align-items: center;
  font-size: .8rem; font-weight: 600; color: var(--text-muted);
  margin-bottom: .5rem;
}
.progress-track {
  height: 6px; background: var(--surface-2);
  border-radius: 99px; overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--green-600), var(--green-400), var(--lime-400));
  border-radius: 99px;
  transition: width .4s ease;
}
.points-badge {
  display: inline-block;
  padding: .2rem .6rem; border-radius: 99px;
  background: var(--accent-light); color: var(--accent);
  border: 1px solid var(--green-200);
  font-size: .75rem; font-weight: 700;
}
[data-theme="dark"] .points-badge { border-color: rgba(34,197,94,.25); }

/* Question card */
.question-card {
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  padding: 1.75rem;
  margin-bottom: 1.25rem;
  box-shadow: var(--shadow);
}
.question-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  margin-bottom: .75rem; gap: 1rem;
}
#question-counter {
  font-size: .78rem; font-weight: 600; color: var(--text-muted);
  white-space: nowrap;
}
#question-text {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.15rem; font-weight: 600; line-height: 1.4;
}

/* Options — Quizller staggered slide-in */
.options-list { display: flex; flex-direction: column; gap: .65rem; }
.option-item {
  display: flex; align-items: center; gap: .85rem;
  padding: .85rem 1rem;
  background: var(--surface-2);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: border-color var(--transition), background var(--transition),
              transform .18s cubic-bezier(.4,0,.2,1),
              box-shadow var(--transition);
  /* staggered slide-in animation applied by JS */
  opacity: 0;
  transform: translateX(-16px);
}
/* Quizller-style: scale on hover */
.option-item:hover {
  border-color: var(--accent);
  background: var(--accent-light);
  transform: scale(1.012) translateX(0);
  box-shadow: 0 2px 12px var(--accent-glow);
}
.option-item.selected {
  border-color: var(--accent);
  background: var(--accent-light);
  opacity: 1 !important;
  transform: translateX(0) !important;
}
.option-item.correct {
  border-color: #16a34a; background: #dcfce7; color: #14532d;
}
.option-item.wrong {
  border-color: #dc2626; background: #fee2e2; color: #7f1d1d;
}
[data-theme="dark"] .option-item.correct {
  border-color: #22c55e; background: rgba(34,197,94,.15); color: #4ade80;
}
[data-theme="dark"] .option-item.wrong {
  border-color: #ef4444; background: rgba(239,68,68,.15); color: #f87171;
}
.option-letter {
  width: 28px; height: 28px; border-radius: 50%;
  background: var(--border); color: var(--text-muted);
  font-size: .75rem; font-weight: 700;
  display: grid; place-items: center; flex-shrink: 0;
  transition: var(--transition);
}
.option-item.selected .option-letter,
.option-item:hover .option-letter {
  background: var(--accent); color: #fff;
}
.option-item.wrong .option-letter { background: #dc2626; color: #fff; }
.option-item.correct .option-letter { background: #16a34a; color: #fff; }
.option-text { font-size: .9rem; font-weight: 500; }

/* Staggered animation keyframe */
@keyframes slideInOption {
  to { opacity: 1; transform: translateX(0); }
}
.option-item.anim-1 { animation: slideInOption .35s ease .05s forwards; }
.option-item.anim-2 { animation: slideInOption .35s ease .15s forwards; }
.option-item.anim-3 { animation: slideInOption .35s ease .25s forwards; }
.option-item.anim-4 { animation: slideInOption .35s ease .35s forwards; }

/* Nav buttons */
.quiz-nav {
  display: flex; justify-content: space-between; gap: .75rem;
  margin-top: 1rem;
}
.btn-nav {
  display: inline-flex; align-items: center; gap: .4rem;
  padding: .65rem 1.4rem; border-radius: var(--radius-sm);
  font-weight: 600; font-size: .9rem;
  transition: var(--transition);
  border: 1.5px solid var(--border);
  background: var(--surface); color: var(--text);
}
.btn-nav:hover:not(:disabled) {
  border-color: var(--accent); color: var(--accent);
  background: var(--accent-light);
}
.btn-nav:disabled {
  opacity: .4; cursor: not-allowed;
}
.btn-nav.btn-finish {
  background: linear-gradient(135deg, var(--green-600), var(--green-500));
  color: #fff; border-color: transparent;
  box-shadow: 0 2px 12px var(--accent-glow);
}
.btn-nav.btn-finish:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--green-700), var(--green-600));
  transform: translateY(-1px);
}

/* ── Loading Screen ── */
.loading-wrap {
  min-height: calc(100vh - 64px);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 1rem;
}
.spinner {
  width: 48px; height: 48px; border-radius: 50%;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  animation: spin .8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Results Screen ── */
.results-wrap { max-width: 680px; margin: 0 auto; padding: 2rem 1rem 4rem; }
.results-card {
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  padding: 2.5rem 2rem;
  text-align: center;
  margin-bottom: 1.5rem;
  box-shadow: var(--shadow-lg);
  position: relative; overflow: hidden;
}
.results-card::before {
  content: '';
  display: block; height: 4px;
  background: linear-gradient(90deg, var(--green-500), var(--lime-400));
  position: absolute; top: 0; left: 0; right: 0;
}
/* Score ring */
.score-ring-wrap { position: relative; width: 140px; height: 140px; margin: .5rem auto 1.25rem; }
.score-ring-svg { width: 140px; height: 140px; transform: rotate(-90deg); }
.score-ring-bg { fill: none; stroke: var(--border); stroke-width: 10; }
.score-ring-fg {
  fill: none; stroke-width: 10; stroke-linecap: round;
  stroke-dasharray: 339.3; stroke-dashoffset: 339.3;
  transition: stroke-dashoffset 1.2s cubic-bezier(.4,0,.2,1);
}
.score-center {
  position: absolute; inset: 0;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
#result-score { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; }
#result-max   { font-size: .75rem; color: var(--text-muted); font-weight: 600; }
#result-tier {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.4rem; font-weight: 700; margin-bottom: .35rem;
}
#result-pct { font-size: 2.2rem; font-weight: 700; color: var(--accent); margin-bottom: .5rem; }
#result-msg { font-size: .9rem; color: var(--text-muted); margin-bottom: 1.5rem; }
.result-actions { display: flex; gap: .75rem; justify-content: center; flex-wrap: wrap; }
.btn-secondary {
  padding: .65rem 1.4rem; border-radius: var(--radius-sm);
  border: 1.5px solid var(--border);
  background: var(--surface-2); color: var(--text);
  font-weight: 600; font-size: .9rem;
  transition: var(--transition);
}
.btn-secondary:hover { border-color: var(--accent); color: var(--accent); background: var(--accent-light); }

/* Review list */
.review-section h2 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.1rem; font-weight: 700;
  margin-bottom: 1rem; padding-bottom: .5rem;
  border-bottom: 1px solid var(--border);
}
.review-item {
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 1rem 1.1rem;
  margin-bottom: .65rem;
  border-left: 4px solid var(--border);
}
.review-item.correct { border-left-color: #16a34a; }
.review-item.wrong   { border-left-color: #dc2626; }
[data-theme="dark"] .review-item.correct { border-left-color: #22c55e; }
[data-theme="dark"] .review-item.wrong   { border-left-color: #ef4444; }
.review-header {
  display: flex; justify-content: space-between;
  font-size: .75rem; font-weight: 700; margin-bottom: .3rem;
  color: var(--text-muted);
}
.review-icon { font-size: .9rem; }
.review-item.correct .review-icon { color: #16a34a; }
.review-item.wrong   .review-icon { color: #dc2626; }
[data-theme="dark"] .review-item.correct .review-icon { color: #4ade80; }
[data-theme="dark"] .review-item.wrong   .review-icon { color: #f87171; }
.review-question { font-size: .88rem; font-weight: 600; margin-bottom: .4rem; }
.review-answers { font-size: .82rem; color: var(--text-muted); margin-bottom: .4rem; }
.review-answers span { display: block; }
.review-correct { color: #16a34a; font-weight: 600; }
[data-theme="dark"] .review-correct { color: #4ade80; }
.review-pts { font-size: .75rem; font-weight: 700; color: var(--accent); }

/* ── Responsive ── */
@media (max-width: 600px) {
  .hero { padding: 3rem 0 2rem; }
  .hero h1 { font-size: 1.75rem; }
  .quiz-grid { grid-template-columns: 1fr; }
  .steps-grid { grid-template-columns: 1fr; }
  .start-card { padding: 2rem 1.25rem; }
  .quiz-layout { padding: 1.25rem .75rem; }
  .results-wrap { padding: 1.25rem .75rem 3rem; }
  .result-actions { flex-direction: column; }
}

/* ── Animations ── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
.fade-up { animation: fadeUp .5s ease both; }
"""

# ─────────────────────────────────────────────────────────────────────────────
#  data.js
# ─────────────────────────────────────────────────────────────────────────────
DATA_JS = "window.ALL_QUIZZES = " + json.dumps(QUIZZES, ensure_ascii=False, indent=2) + ";\n"

# ─────────────────────────────────────────────────────────────────────────────
#  home.js
# ─────────────────────────────────────────────────────────────────────────────
HOME_JS = """\
/* home.js — Builds quiz cards from window.ALL_QUIZZES (static version) */
'use strict';

(function () {
  const DIFF_CLASS = { easy: 'diff-easy', medium: 'diff-medium', hard: 'diff-hard' };

  function esc(s) {
    return String(s)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function buildCard(quiz) {
    const questionCount = quiz.questions.length;
    const maxScore = quiz.questions.reduce((s, q) => s + (q.points || 1), 0);
    const diffKey  = (quiz.difficulty || '').toLowerCase();
    const diffCls  = DIFF_CLASS[diffKey] || '';

    const a = document.createElement('a');
    a.href      = `quiz.html?id=${encodeURIComponent(quiz.id)}`;
    a.className = 'quiz-card';
    a.setAttribute('aria-label', `Start ${quiz.title} quiz`);
    a.innerHTML = `
      <span class="card-icon">${esc(quiz.icon || '?')}</span>
      <div class="card-content">
        <span class="card-category">${esc(quiz.category)}</span>
        <h3 class="card-title">${esc(quiz.title)}</h3>
        <p class="card-desc">${esc(quiz.description)}</p>
        <div class="card-meta">
          <span class="meta-badge">${questionCount} Questions</span>
          <span class="meta-badge ${diffCls}">${esc(quiz.difficulty)}</span>
          <span class="meta-badge">${maxScore} pts max</span>
        </div>
      </div>
      <span class="card-arrow" aria-hidden="true">&rarr;</span>
    `;
    return a;
  }

  function init() {
    const grid = document.getElementById('quiz-grid');
    if (!grid) return;
    const quizzes = window.ALL_QUIZZES || [];
    if (!quizzes.length) {
      grid.innerHTML = '<p style="color:var(--text-muted);text-align:center;grid-column:1/-1;">No quizzes available.</p>';
      return;
    }
    grid.innerHTML = '';
    quizzes.forEach(q => grid.appendChild(buildCard(q)));
  }

  document.addEventListener('DOMContentLoaded', init);
})();
"""

# ─────────────────────────────────────────────────────────────────────────────
#  quiz.js  (Quizller features: staggered animations, localStorage, scale hover)
# ─────────────────────────────────────────────────────────────────────────────
QUIZ_JS = """\
/* quiz.js — Static quiz engine
   Quizller features: staggered option slide-in, scale-hover, localStorage progress
   Client-side scoring — no backend required
*/
'use strict';

(function () {
  // ── Load quiz from URL param ─────────────────────────────────────────────
  const params = new URLSearchParams(location.search);
  const quizId = params.get('id');
  const quiz   = (window.ALL_QUIZZES || []).find(q => q.id === quizId);

  if (!quiz) {
    document.body.innerHTML =
      '<div style="text-align:center;padding:4rem;font-family:sans-serif">' +
      '<h2>Quiz not found</h2><a href="index.html">← Back</a></div>';
    return;
  }

  // ── Storage key ─────────────────────────────────────────────────────────
  const STORAGE_KEY = `qs_progress_${quiz.id}`;

  // ── State ────────────────────────────────────────────────────────────────
  const state = {
    currentIdx: 0,
    answers:    {},     // { "0": optIdx, … }
    startTime:  null,
    submitted:  false,
  };

  // ── DOM refs ─────────────────────────────────────────────────────────────
  const screens = {
    start:   document.getElementById('start-screen'),
    quiz:    document.getElementById('quiz-screen'),
    loading: document.getElementById('loading-screen'),
    results: document.getElementById('results-screen'),
  };
  const questionEl    = document.getElementById('question-text');
  const optionsList   = document.getElementById('options-list');
  const pointsBadge   = document.getElementById('points-badge');
  const progressBar   = document.getElementById('progress-bar');
  const qCounter      = document.getElementById('question-counter');
  const answeredCount = document.getElementById('answered-count');
  const prevBtn       = document.getElementById('btn-prev');
  const nextBtn       = document.getElementById('btn-next');

  // ── Screens ──────────────────────────────────────────────────────────────
  function showScreen(name) {
    Object.values(screens).forEach(s => { if (s) s.classList.remove('active'); });
    if (screens[name]) screens[name].classList.add('active');
  }

  // ── Populate start screen ─────────────────────────────────────────────
  function populateStart() {
    const maxScore = quiz.questions.reduce((s, q) => s + (q.points || 1), 0);
    setText('start-icon',     quiz.icon     || '');
    setText('start-category', quiz.category || '');
    setText('start-title',    quiz.title    || '');
    setText('start-desc',     quiz.description || '');
    const meta = document.getElementById('start-meta');
    if (meta) meta.innerHTML =
      `<span class="meta-badge">${quiz.questions.length} questions</span>
       <span class="meta-badge diff-${(quiz.difficulty||'').toLowerCase()}">${quiz.difficulty || ''}</span>
       <span class="meta-badge">${maxScore} pts max</span>`;
  }

  function setText(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  }

  // ── Save / Restore localStorage progress (Quizller feature) ─────────────
  function saveProgress() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        currentIdx: state.currentIdx,
        answers:    state.answers,
        startTime:  state.startTime,
      }));
    } catch (_) {}
  }

  function restoreProgress() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return false;
      const saved = JSON.parse(raw);
      if (typeof saved.currentIdx !== 'number') return false;
      state.currentIdx = saved.currentIdx;
      state.answers    = saved.answers || {};
      state.startTime  = saved.startTime || Date.now();
      return true;
    } catch (_) { return false; }
  }

  function clearProgress() {
    try { localStorage.removeItem(STORAGE_KEY); } catch (_) {}
  }

  // ── Start ─────────────────────────────────────────────────────────────
  function startQuiz(resume) {
    if (!resume) {
      state.currentIdx = 0;
      state.answers    = {};
      state.startTime  = Date.now();
    }
    state.submitted = false;
    renderQuestion();
    showScreen('quiz');
  }

  // ── Render current question ───────────────────────────────────────────
  function renderQuestion() {
    const q     = quiz.questions[state.currentIdx];
    const total = quiz.questions.length;
    const done  = Object.keys(state.answers).length;

    qCounter.textContent      = `${state.currentIdx + 1} / ${total}`;
    answeredCount.textContent = `${done} answered`;
    const pct = ((state.currentIdx + 1) / total) * 100;
    progressBar.style.width   = `${pct}%`;
    pointsBadge.textContent   = `${q.points || 1} pt${(q.points || 1) !== 1 ? 's' : ''}`;

    // Animate question text
    questionEl.style.opacity  = '0';
    questionEl.textContent    = q.question;
    requestAnimationFrame(() => {
      questionEl.style.transition = 'opacity .25s ease';
      questionEl.style.opacity    = '1';
    });

    // Build options with Quizller staggered animation
    const userAns = state.answers[String(state.currentIdx)];
    optionsList.innerHTML = '';
    q.options.forEach((opt, idx) => {
      const li = document.createElement('li');
      li.className = `option-item anim-${idx + 1}`; // anim-1..4 → staggered CSS
      if (userAns === idx) li.classList.add('selected');

      const letter = document.createElement('span');
      letter.className   = 'option-letter';
      letter.textContent = String.fromCharCode(65 + idx);

      const text = document.createElement('span');
      text.className   = 'option-text';
      text.textContent = opt;

      li.appendChild(letter);
      li.appendChild(text);
      li.addEventListener('click', () => selectAnswer(idx));
      optionsList.appendChild(li);
    });

    // Nav state
    prevBtn.disabled = state.currentIdx === 0;
    const isLast     = state.currentIdx === total - 1;
    nextBtn.textContent = isLast ? 'Finish ✓' : 'Next →';
    nextBtn.classList.toggle('btn-finish', isLast);
    nextBtn.disabled    = userAns === undefined;

    saveProgress();
  }

  // ── Select answer (Quizller: instant highlight feedback) ───────────────
  function selectAnswer(optIdx) {
    state.answers[String(state.currentIdx)] = optIdx;
    renderQuestion();
  }

  // ── Navigation ───────────────────────────────────────────────────────
  function goPrev() {
    if (state.currentIdx > 0) { state.currentIdx -= 1; renderQuestion(); }
  }

  function goNext() {
    const total = quiz.questions.length;
    if (state.currentIdx < total - 1) {
      state.currentIdx += 1;
      renderQuestion();
    } else {
      finishQuiz();
    }
  }

  // ── Client-side scoring (no backend) ─────────────────────────────────
  function calculateScore(answers) {
    const TIER_MAP = [
      { pct: 90, tier: 'Genius',  color: '#eab308' },
      { pct: 70, tier: 'Expert',  color: '#22c55e' },
      { pct: 50, tier: 'Learner', color: '#8b5cf6' },
      { pct:  0, tier: 'Novice',  color: '#f87171' },
    ];
    let score = 0;
    const maxScore = quiz.questions.reduce((s, q) => s + (q.points || 1), 0);
    const results  = quiz.questions.map((q, i) => {
      const userAns   = answers[String(i)];
      const isCorrect = userAns === q.answer;
      if (isCorrect) score += (q.points || 1);
      return {
        question:       q.question,
        options:        q.options,
        answer:         q.answer,
        user_answer:    userAns !== undefined ? userAns : null,
        is_correct:     isCorrect,
        points:         q.points || 1,
        correct_answer: q.answer,
      };
    });
    const percentage = maxScore > 0 ? Math.round((score / maxScore) * 100) : 0;
    const { tier, color } = TIER_MAP.find(t => percentage >= t.pct);
    return { score, max_score: maxScore, percentage, tier, tier_color: color, results };
  }

  // ── Finish quiz ───────────────────────────────────────────────────────
  function finishQuiz() {
    if (state.submitted) return;
    state.submitted = true;
    showScreen('loading');
    clearProgress();
    // Small delay for UX (feel of processing)
    setTimeout(() => {
      const result = calculateScore(state.answers);
      renderResults(result);
      showScreen('results');
    }, 900);
  }

  // ── Render results ────────────────────────────────────────────────────
  const TIER_MSG = {
    Genius:  'Outstanding! You really know your stuff.',
    Expert:  'Great work! You\'re well above average.',
    Learner: 'Good effort! Keep studying and you\'ll get there.',
    Novice:  'Everyone starts somewhere — give it another shot!',
  };

  function renderResults(result) {
    setText('result-score', result.score);
    setText('result-max',   `/ ${result.max_score}`);
    setText('result-pct',   `${result.percentage}%`);
    setText('result-msg',    TIER_MSG[result.tier] || '');

    const tierEl = document.getElementById('result-tier');
    if (tierEl) { tierEl.textContent = result.tier; tierEl.style.color = result.tier_color; }

    // Score ring animation
    const ring = document.getElementById('score-ring-fg');
    if (ring) {
      const r  = 54;
      const c  = 2 * Math.PI * r;   // ≈ 339.3
      ring.style.stroke          = result.tier_color;
      ring.style.strokeDasharray = c;
      ring.style.strokeDashoffset = c;
      requestAnimationFrame(() => {
        ring.style.strokeDashoffset = c * (1 - result.percentage / 100);
      });
    }

    // Review list
    const reviewList = document.getElementById('review-list');
    if (!reviewList) return;
    reviewList.innerHTML = '';
    result.results.forEach((item, idx) => {
      const div = document.createElement('div');
      div.className = `review-item ${item.is_correct ? 'correct' : 'wrong'}`;
      const userTxt = item.user_answer !== null
        ? esc(item.options[item.user_answer])
        : '<em>No answer</em>';
      div.innerHTML = `
        <div class="review-header">
          <span class="review-num">Q${idx + 1}</span>
          <span class="review-icon">${item.is_correct ? '✓' : '✗'}</span>
        </div>
        <p class="review-question">${esc(item.question)}</p>
        <div class="review-answers">
          <span class="review-yours">Your answer: ${userTxt}</span>
          ${!item.is_correct
            ? `<span class="review-correct">Correct: ${esc(item.options[item.correct_answer])}</span>`
            : ''}
        </div>
        <span class="review-pts">${item.is_correct ? '+' + item.points : '0'}/${item.points} pts</span>
      `;
      reviewList.appendChild(div);
    });
  }

  // ── Utility ───────────────────────────────────────────────────────────
  function esc(s) {
    return String(s)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  // ── Init on DOM ready ─────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', () => {
    populateStart();

    // Check for saved progress
    const hasProgress = restoreProgress();
    const resumeBtn   = document.getElementById('resume-btn');
    if (hasProgress && Object.keys(state.answers).length > 0) {
      if (resumeBtn) resumeBtn.style.display = 'inline-flex';
      resumeBtn && resumeBtn.addEventListener('click', () => startQuiz(true));
    } else {
      if (resumeBtn) resumeBtn.style.display = 'none';
    }

    document.getElementById('start-btn').addEventListener('click', () => {
      clearProgress();
      state.currentIdx = 0; state.answers = {}; state.startTime = Date.now();
      startQuiz(false);
    });

    prevBtn.addEventListener('click', goPrev);
    nextBtn.addEventListener('click', goNext);

    document.getElementById('restart-btn')?.addEventListener('click', () => {
      clearProgress();
      state.currentIdx = 0; state.answers = {}; state.startTime = Date.now();
      state.submitted = false;
      populateStart();
      showScreen('start');
    });

    document.getElementById('home-btn')?.addEventListener('click', () => {
      window.location.href = 'index.html';
    });

    showScreen('start');
  });
})();
"""

# ─────────────────────────────────────────────────────────────────────────────
#  theme.js  (shared light/dark toggle)
# ─────────────────────────────────────────────────────────────────────────────
THEME_JS = """\
/* theme.js — Light/Dark mode toggle with localStorage persistence */
(function () {
  const STORAGE_KEY = 'qs_theme';
  const root = document.documentElement;

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    document.querySelectorAll('.theme-toggle').forEach(btn => {
      btn.textContent = theme === 'dark' ? '☀️' : '🌙';
      btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    });
  }

  function toggleTheme() {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    try { localStorage.setItem(STORAGE_KEY, next); } catch (_) {}
  }

  // Init: prefer localStorage, then system preference
  const saved  = (() => { try { return localStorage.getItem(STORAGE_KEY); } catch(_){return null;} })();
  const system = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  applyTheme(saved || system);

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.theme-toggle').forEach(btn => {
      btn.addEventListener('click', toggleTheme);
    });
  });
})();
"""

# ─────────────────────────────────────────────────────────────────────────────
#  index.html
# ─────────────────────────────────────────────────────────────────────────────
INDEX_HTML = """\
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="QuizSimple — Test your knowledge with beautifully crafted quizzes.">
  <title>QuizSimple — Test Your Knowledge</title>
  <link rel="stylesheet" href="static/css/style.css">
  <script src="static/js/theme.js"></script>
</head>
<body>

  <!-- ── Navbar ── -->
  <nav class="navbar" role="navigation" aria-label="Main navigation">
    <div class="container nav-inner">
      <a href="index.html" class="nav-logo" aria-label="QuizSimple home">
        <div class="logo-icon" aria-hidden="true">Q</div>
        <span class="logo-text">QuizSimple</span>
      </a>
      <div class="nav-actions">
        <button class="theme-toggle" aria-label="Toggle dark mode">🌙</button>
      </div>
    </div>
  </nav>

  <main>
    <!-- ── Hero ── -->
    <section class="hero" aria-labelledby="hero-heading">
      <div class="container">
        <div class="hero-badge">
          <span class="badge-dot" aria-hidden="true"></span>
          Free &amp; Open Source
        </div>
        <h1 id="hero-heading">
          Challenge Your Mind<br>
          <span class="gradient-text">Prove Your Knowledge</span>
        </h1>
        <p>Pick a quiz, answer at your own pace, and see how you rank — no account needed.</p>
      </div>
    </section>

    <!-- ── Quiz Grid ── -->
    <section class="quiz-section" aria-labelledby="quizzes-heading">
      <div class="container">
        <h2 class="section-title" id="quizzes-heading">Available Quizzes</h2>
        <div class="quiz-grid" id="quiz-grid" role="list">
          <noscript>
            <p style="color:var(--text-muted);text-align:center;grid-column:1/-1;">
              Please enable JavaScript to view the quizzes.
            </p>
          </noscript>
        </div>
      </div>
    </section>

    <!-- ── How it works ── -->
    <section class="how-section" aria-labelledby="how-heading">
      <div class="container">
        <h2 class="section-title" id="how-heading">How It Works</h2>
        <div class="steps-grid">
          <div class="step-card fade-up">
            <div class="step-num" aria-hidden="true">1</div>
            <h3>Pick a Quiz</h3>
            <p>Choose from Knowledge, Science, or Pop Culture — more coming soon.</p>
          </div>
          <div class="step-card fade-up" style="animation-delay:.1s">
            <div class="step-num" aria-hidden="true">2</div>
            <h3>Answer Questions</h3>
            <p>Navigate freely — go back to change your mind before finishing.</p>
          </div>
          <div class="step-card fade-up" style="animation-delay:.2s">
            <div class="step-num" aria-hidden="true">3</div>
            <h3>See Your Score</h3>
            <p>Get instant results with tier ranking and a full question review.</p>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container">
      <p>&copy; 2026 QuizSimple. Built with ♥ and JavaScript.</p>
    </div>
  </footer>

  <script src="static/js/data.js"></script>
  <script src="static/js/home.js"></script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────
#  quiz.html
# ─────────────────────────────────────────────────────────────────────────────
QUIZ_HTML = """\
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Quiz — QuizSimple</title>
  <link rel="stylesheet" href="static/css/style.css">
  <script src="static/js/theme.js"></script>
</head>
<body>

  <!-- ── Navbar ── -->
  <nav class="navbar" role="navigation" aria-label="Main navigation">
    <div class="container nav-inner">
      <a href="index.html" class="nav-logo" aria-label="QuizSimple home">
        <div class="logo-icon" aria-hidden="true">Q</div>
        <span class="logo-text">QuizSimple</span>
      </a>
      <div class="nav-actions">
        <button class="theme-toggle" aria-label="Toggle dark mode">🌙</button>
      </div>
    </div>
  </nav>

  <!-- ═══════════════════════════════
       START SCREEN
  ════════════════════════════════ -->
  <div id="start-screen" class="screen active" role="main">
    <div class="start-wrap">
      <div class="start-card fade-up">
        <div id="start-icon" aria-hidden="true"></div>
        <div id="start-category"></div>
        <h1 id="start-title"></h1>
        <p id="start-desc"></p>
        <div id="start-meta" role="list"></div>

        <label for="player-name" class="sr-only">Your name</label>
        <input
          type="text" id="player-name" class="name-input"
          placeholder="Your name (optional)" maxlength="40"
          autocomplete="off" spellcheck="false"
        >

        <div style="display:flex;gap:.75rem;justify-content:center;flex-wrap:wrap">
          <button id="start-btn" class="btn-primary">Start Quiz &rarr;</button>
          <button id="resume-btn" class="btn-secondary" style="display:none">Resume &rarr;</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ═══════════════════════════════
       QUIZ SCREEN
  ════════════════════════════════ -->
  <div id="quiz-screen" class="screen" role="main" aria-live="polite">
    <div class="quiz-layout">

      <!-- Progress -->
      <div class="progress-wrap">
        <div class="progress-info">
          <span id="question-counter">1 / 10</span>
          <span id="answered-count">0 answered</span>
          <span id="points-badge" class="points-badge">1 pt</span>
        </div>
        <div class="progress-track" role="progressbar" aria-valuemin="0" aria-valuemax="100">
          <div id="progress-bar" class="progress-fill" style="width:10%"></div>
        </div>
      </div>

      <!-- Question -->
      <div class="question-card">
        <p id="question-text" class=""></p>
      </div>

      <!-- Options -->
      <ul id="options-list" class="options-list" role="listbox" aria-label="Answer options"></ul>

      <!-- Navigation -->
      <div class="quiz-nav">
        <button id="btn-prev" class="btn-nav" disabled aria-label="Previous question">&larr; Prev</button>
        <button id="btn-next" class="btn-nav" disabled aria-label="Next question">Next &rarr;</button>
      </div>

    </div>
  </div>

  <!-- ═══════════════════════════════
       LOADING SCREEN
  ════════════════════════════════ -->
  <div id="loading-screen" class="screen" role="status" aria-label="Calculating results">
    <div class="loading-wrap">
      <div class="spinner" aria-hidden="true"></div>
      <p style="color:var(--text-muted);font-size:.9rem">Calculating your score&hellip;</p>
    </div>
  </div>

  <!-- ═══════════════════════════════
       RESULTS SCREEN
  ════════════════════════════════ -->
  <div id="results-screen" class="screen" role="main">
    <div class="results-wrap">

      <div class="results-card fade-up">
        <!-- Score ring -->
        <div class="score-ring-wrap" aria-label="Score ring">
          <svg class="score-ring-svg" viewBox="0 0 120 120" aria-hidden="true">
            <circle class="score-ring-bg" cx="60" cy="60" r="54"/>
            <circle id="score-ring-fg" class="score-ring-fg" cx="60" cy="60" r="54"/>
          </svg>
          <div class="score-center">
            <span id="result-score" style="font-family:'Space Grotesk',sans-serif;font-size:1.9rem;font-weight:700">0</span>
            <span id="result-max" style="font-size:.72rem;color:var(--text-muted);font-weight:600">/ 0</span>
          </div>
        </div>

        <div id="result-pct" style="font-size:2rem;font-weight:700;color:var(--accent);margin-bottom:.35rem">0%</div>
        <div id="result-tier" style="font-size:1.3rem;font-weight:700;margin-bottom:.4rem"></div>
        <p id="result-msg" style="font-size:.9rem;color:var(--text-muted);margin-bottom:1.5rem"></p>

        <div class="result-actions">
          <button id="restart-btn" class="btn-secondary">Try Again</button>
          <button id="home-btn" class="btn-primary">All Quizzes</button>
        </div>
      </div>

      <!-- Review -->
      <section class="review-section" aria-labelledby="review-heading">
        <h2 id="review-heading">Question Review</h2>
        <div id="review-list" role="list"></div>
      </section>

    </div>
  </div>

  <script src="static/js/data.js"></script>
  <script src="static/js/quiz.js"></script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────
#  Write everything
# ─────────────────────────────────────────────────────────────────────────────
print("Building static out/ folder...")

w("static/css/style.css",  CSS)
w("static/js/data.js",     DATA_JS)
w("static/js/home.js",     HOME_JS)
w("static/js/quiz.js",     QUIZ_JS)
w("static/js/theme.js",    THEME_JS)
w("index.html",            INDEX_HTML)
w("quiz.html",             QUIZ_HTML)

print("\n✓ All static files written successfully.")
print(f"  Root: {ROOT}")
