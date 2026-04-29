"""One-shot script to write all static out/ files with green premium + dark/light theme + Quizller features."""
import os, pathlib

BASE = pathlib.Path(r"D:\velu velu\QuizSimple\QuizSimple-app\out")

def w(rel, content):
    p = BASE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"  wrote {rel}")

# ─────────────────────────────────────────────────────────────────────────────
# 1. CSS
# ─────────────────────────────────────────────────────────────────────────────
CSS = r"""/* ════════════════════════════════════════════════════════════
   QuizApp — Premium Green Theme  |  Light / Dark Mode
   Quizller features: staggered slide-ins, instant feedback,
   localStorage persistence, session timer.
   ════════════════════════════════════════════════════════════ */

/* ── Variables ── */
:root {
  --bg:          #070f12;
  --bg-alt:      #0c1a14;
  --card:        rgba(16,185,129,.07);
  --card-bdr:    rgba(16,185,129,.18);
  --nav-bg:      rgba(7,15,18,.9);
  --text:        #d1fae5;
  --text-muted:  #6ee7b7;
  --text-dim:    #4a7a68;
  --accent:      #10b981;
  --accent-lt:   #34d399;
  --accent-dk:   #059669;
  --accent-glow: rgba(16,185,129,.28);
  --danger:      #f87171;
  --warning:     #fbbf24;
  --opt-idle:    rgba(16,185,129,.07);
  --opt-hover:   rgba(16,185,129,.16);
  --opt-sel:     rgba(16,185,129,.22);
  --opt-sel-bdr: #10b981;
  --opt-correct: rgba(52,211,153,.32);
  --opt-wrong:   rgba(248,113,113,.28);
  --shadow:      0 8px 40px rgba(0,0,0,.5);
  --shadow-sm:   0 2px 10px rgba(0,0,0,.3);
  --r:           16px;
}
[data-theme="light"] {
  --bg:          #f0fdf4;
  --bg-alt:      #ffffff;
  --card:        #ffffff;
  --card-bdr:    rgba(5,150,105,.18);
  --nav-bg:      rgba(240,253,244,.93);
  --text:        #052e16;
  --text-muted:  #065f46;
  --text-dim:    #6b7280;
  --accent:      #059669;
  --accent-lt:   #10b981;
  --accent-dk:   #047857;
  --accent-glow: rgba(5,150,105,.18);
  --danger:      #ef4444;
  --warning:     #d97706;
  --opt-idle:    rgba(5,150,105,.05);
  --opt-hover:   rgba(5,150,105,.12);
  --opt-sel:     rgba(5,150,105,.17);
  --opt-sel-bdr: #059669;
  --opt-correct: rgba(5,150,105,.2);
  --opt-wrong:   rgba(239,68,68,.15);
  --shadow:      0 8px 40px rgba(0,0,0,.08);
  --shadow-sm:   0 2px 10px rgba(0,0,0,.05);
}

/* ── Reset ── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{
  font-family:'Inter',sans-serif;
  background:var(--bg);color:var(--text);
  min-height:100vh;overflow-x:hidden;
  transition:background .3s,color .3s;
}
a{color:inherit;text-decoration:none;}
ul{list-style:none;}
button{cursor:pointer;border:none;background:none;font:inherit;}

::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:var(--accent-dk);border-radius:99px;}

/* ── Navbar ── */
.navbar{
  position:fixed;top:0;left:0;right:0;z-index:100;
  display:flex;align-items:center;justify-content:space-between;
  padding:0 clamp(1rem,4vw,3rem);height:64px;
  background:var(--nav-bg);
  backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  border-bottom:1px solid var(--card-bdr);
  transition:background .3s,border-color .3s;
}
.nav-logo{
  display:flex;align-items:center;gap:.5rem;
  font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:1.2rem;
}
.logo-icon{
  display:grid;place-items:center;
  width:32px;height:32px;border-radius:8px;
  background:var(--accent);color:#070f12;font-weight:800;font-size:.9rem;
}
.nav-right{display:flex;align-items:center;gap:1rem;}
.nav-link{color:var(--text-muted);font-size:.875rem;font-weight:500;transition:color .2s;}
.nav-link:hover{color:var(--accent);}
.theme-toggle{
  display:grid;place-items:center;
  width:40px;height:40px;border-radius:50%;
  border:1px solid var(--card-bdr);background:var(--card);
  color:var(--text-muted);font-size:1.05rem;cursor:pointer;
  transition:border-color .2s,background .2s;
}
.theme-toggle:hover{border-color:var(--accent);color:var(--accent);}

/* ── Buttons ── */
.btn{
  display:inline-flex;align-items:center;justify-content:center;gap:.5rem;
  padding:.625rem 1.5rem;border-radius:99px;
  font-size:.875rem;font-weight:600;transition:all .2s;white-space:nowrap;
}
.btn-primary{
  background:var(--accent);color:#070f12;
  box-shadow:0 0 20px var(--accent-glow);
}
.btn-primary:hover{background:var(--accent-lt);transform:translateY(-2px);box-shadow:0 0 32px var(--accent-glow);}
.btn-primary:active{transform:translateY(0);}
.btn-outline{border:1px solid var(--accent);color:var(--accent);}
.btn-outline:hover{background:var(--opt-hover);}
.btn-lg{padding:.875rem 2.25rem;font-size:1rem;}
.btn-xl{padding:1rem 2.5rem;font-size:1.05rem;border-radius:var(--r);width:100%;}
.btn:disabled{opacity:.4;cursor:not-allowed;pointer-events:none;}

/* Badges */
.meta-badge{
  display:inline-flex;align-items:center;padding:.25rem .75rem;border-radius:99px;
  font-size:.72rem;font-weight:600;
  background:var(--opt-idle);border:1px solid var(--card-bdr);color:var(--text-muted);
}
.diff-easy  {color:var(--accent);border-color:var(--accent-glow);}
.diff-medium{color:var(--warning);border-color:rgba(251,191,36,.3);}
.diff-hard  {color:var(--danger);border-color:rgba(248,113,113,.3);}

/* ════════════════════════════════════════════════════════════
   HOMEPAGE
   ════════════════════════════════════════════════════════════ */
main{padding-top:64px;}

.hero{
  text-align:center;
  padding:clamp(4rem,10vw,8rem) clamp(1rem,4vw,2rem) clamp(3rem,6vw,5rem);
  background:
    radial-gradient(ellipse 70% 50% at 50% 0%,rgba(16,185,129,.12),transparent),
    var(--bg);
}
.hero-badge{
  display:inline-block;padding:.35rem 1rem;border-radius:99px;
  border:1px solid var(--accent-glow);background:rgba(16,185,129,.08);
  color:var(--accent);font-size:.76rem;font-weight:700;
  letter-spacing:.06em;text-transform:uppercase;margin-bottom:1.5rem;
}
.hero-title{
  font-family:'Space Grotesk',sans-serif;
  font-size:clamp(2.4rem,6vw,4.2rem);font-weight:700;line-height:1.1;
  margin-bottom:1.25rem;
}
.gradient-text{
  background:linear-gradient(135deg,var(--accent),var(--accent-lt) 60%,#a7f3d0);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.hero-subtitle{
  max-width:560px;margin:0 auto 2.5rem;
  color:var(--text-dim);font-size:1.05rem;line-height:1.7;
}

.quiz-section{max-width:1100px;margin:0 auto;padding:clamp(3rem,6vw,5rem) clamp(1rem,4vw,2rem);}
.section-header{text-align:center;margin-bottom:2.5rem;}
.section-title{
  font-family:'Space Grotesk',sans-serif;
  font-size:clamp(1.6rem,3.5vw,2.2rem);font-weight:700;margin-bottom:.5rem;
}
.section-sub{color:var(--text-dim);font-size:.95rem;}

.quiz-grid{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
  gap:1.5rem;
}
.quiz-card{
  display:flex;flex-direction:column;padding:1.75rem;
  border-radius:calc(var(--r) + 4px);
  border:1px solid var(--card-bdr);background:var(--card);
  box-shadow:var(--shadow-sm);
  transition:transform .25s,box-shadow .25s,border-color .25s;
  cursor:pointer;position:relative;overflow:hidden;
}
.quiz-card::before{
  content:'';position:absolute;inset:0;
  background:radial-gradient(circle at top right,var(--accent-glow),transparent 70%);
  opacity:0;transition:opacity .3s;
}
.quiz-card:hover{transform:translateY(-4px);box-shadow:var(--shadow);border-color:var(--accent);}
.quiz-card:hover::before{opacity:1;}
.card-icon{font-size:2.2rem;margin-bottom:1rem;}
.card-category{
  display:inline-block;font-size:.7rem;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;
  color:var(--accent);margin-bottom:.4rem;
}
.card-title{
  font-family:'Space Grotesk',sans-serif;
  font-size:1.2rem;font-weight:700;margin-bottom:.5rem;
}
.card-desc{color:var(--text-dim);font-size:.875rem;line-height:1.6;margin-bottom:1.25rem;flex:1;}
.card-meta{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:1rem;}
.card-arrow{
  align-self:flex-end;width:36px;height:36px;
  display:grid;place-items:center;border-radius:50%;
  border:1px solid var(--card-bdr);color:var(--text-dim);
  transition:all .2s;
}
.quiz-card:hover .card-arrow{background:var(--accent);border-color:var(--accent);color:#070f12;}

.how-section{
  background:var(--bg-alt);
  padding:clamp(3rem,6vw,5rem) clamp(1rem,4vw,2rem);
}
.how-section .section-header{margin-bottom:3rem;}
.steps-grid{
  max-width:900px;margin:0 auto;
  display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:2rem;
}
.step-card{
  text-align:center;padding:2rem 1.5rem;
  border-radius:var(--r);border:1px solid var(--card-bdr);background:var(--card);
}
.step-num{
  display:inline-grid;place-items:center;
  width:48px;height:48px;border-radius:50%;
  background:var(--accent-glow);border:1px solid var(--accent);
  color:var(--accent);
  font-family:'Space Grotesk',sans-serif;font-size:1.1rem;font-weight:700;
  margin-bottom:1rem;
}
.step-title{font-weight:700;font-size:1rem;margin-bottom:.5rem;}
.step-desc{color:var(--text-dim);font-size:.875rem;line-height:1.6;}

.footer{
  text-align:center;padding:2rem;
  border-top:1px solid var(--card-bdr);
  color:var(--text-dim);font-size:.82rem;
}
.footer a{color:var(--accent);}

/* ════════════════════════════════════════════════════════════
   QUIZ PAGE
   ════════════════════════════════════════════════════════════ */
.quiz-page{
  min-height:calc(100vh - 64px);padding-top:64px;
  display:flex;align-items:flex-start;justify-content:center;
}
.screen{display:none;width:100%;padding:2rem 1rem;}
.screen.active{display:block;}

/* Start */
.start-card{
  max-width:520px;margin:2rem auto;
  padding:2.5rem;border-radius:calc(var(--r) + 4px);
  border:1px solid var(--card-bdr);background:var(--card);
  box-shadow:var(--shadow);text-align:center;
}
.resume-banner{
  padding:1rem;border-radius:var(--r);
  background:rgba(16,185,129,.08);border:1px solid var(--accent-glow);
  margin-bottom:1.5rem;
  font-size:.9rem;color:var(--text-muted);
}
.resume-actions{display:flex;gap:.75rem;margin-top:.75rem;}
.resume-actions .btn{flex:1;}
.start-icon{font-size:3.5rem;margin-bottom:1rem;}
.start-category{
  display:inline-block;font-size:.75rem;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase;
  color:var(--accent);margin-bottom:.75rem;
}
.start-title{
  font-family:'Space Grotesk',sans-serif;
  font-size:1.8rem;font-weight:700;margin-bottom:.75rem;
}
.start-desc{color:var(--text-dim);font-size:.95rem;line-height:1.6;margin-bottom:1.5rem;}
.start-meta{display:flex;justify-content:center;flex-wrap:wrap;gap:.5rem;margin-bottom:1.5rem;}
.start-name-row{margin-bottom:1.5rem;text-align:left;}
.name-label{display:block;font-size:.8rem;font-weight:600;color:var(--text-muted);margin-bottom:.4rem;}
.name-input{
  width:100%;padding:.75rem 1rem;
  border-radius:var(--r);border:1px solid var(--card-bdr);
  background:var(--opt-idle);color:var(--text);font:inherit;font-size:.95rem;
  outline:none;transition:border-color .2s;
}
.name-input:focus{border-color:var(--accent);}
.name-input::placeholder{color:var(--text-dim);}
.start-tip{margin-top:1rem;font-size:.78rem;color:var(--text-dim);font-style:italic;}

/* Quiz screen */
.quiz-screen-inner{max-width:680px;margin:0 auto;}
.progress-wrap{margin-bottom:1.5rem;}
.progress-meta{
  display:flex;justify-content:space-between;align-items:center;
  font-size:.8rem;color:var(--text-dim);margin-bottom:.5rem;gap:.5rem;flex-wrap:wrap;
}
.progress-bar-bg{height:4px;border-radius:99px;background:var(--opt-idle);}
.progress-bar-fill{
  height:100%;border-radius:99px;
  background:linear-gradient(90deg,var(--accent-dk),var(--accent-lt));
  transition:width .4s cubic-bezier(.4,0,.2,1);width:0%;
}
.points-badge{
  padding:.2rem .7rem;border-radius:99px;
  font-size:.72rem;font-weight:700;
  background:rgba(16,185,129,.12);border:1px solid var(--accent-glow);
  color:var(--accent);margin-left:auto;
}
.question-text{
  font-family:'Space Grotesk',sans-serif;
  font-size:clamp(1rem,2.5vw,1.2rem);font-weight:600;line-height:1.5;
  color:var(--text);margin-bottom:1.5rem;
  transition:opacity .2s ease;
}

/* Options — Quizller staggered slide-in */
.options-list{display:flex;flex-direction:column;gap:.75rem;margin-bottom:1.75rem;}

@keyframes slideFromLeft{
  from{opacity:0;transform:translateX(-32px);}
  to  {opacity:1;transform:translateX(0);}
}
.option-item{
  display:flex;align-items:center;gap:1rem;
  padding:1rem 1.25rem;border-radius:var(--r);
  border:1px solid var(--card-bdr);background:var(--opt-idle);
  cursor:pointer;user-select:none;
  transition:background .18s,border-color .18s;
  animation:slideFromLeft .38s cubic-bezier(.4,0,.2,1) both;
}
.option-item:nth-child(1){animation-delay:.04s;}
.option-item:nth-child(2){animation-delay:.10s;}
.option-item:nth-child(3){animation-delay:.16s;}
.option-item:nth-child(4){animation-delay:.22s;}
.option-item:hover{background:var(--opt-hover);border-color:var(--accent);}
.option-item.selected{background:var(--opt-sel);border-color:var(--opt-sel-bdr);}

.option-letter{
  flex-shrink:0;width:30px;height:30px;border-radius:50%;
  display:grid;place-items:center;
  border:1px solid var(--card-bdr);
  font-size:.78rem;font-weight:700;color:var(--text-muted);
  background:var(--opt-idle);
  transition:background .18s,border-color .18s,color .18s;
}
.option-item.selected .option-letter{
  background:var(--accent);border-color:var(--accent);color:#070f12;
}
.option-text{flex:1;font-size:.95rem;line-height:1.4;}

/* Quizller instant feedback */
@keyframes correctPulse{0%,100%{transform:scale(1);}40%{transform:scale(1.025);}}
@keyframes wrongShake{0%,100%{transform:translateX(0);}25%{transform:translateX(-6px);}75%{transform:translateX(6px);}}

.option-item.feedback-correct{
  background:var(--opt-correct);border-color:var(--accent);
  animation:correctPulse .5s ease forwards;pointer-events:none;
}
.option-item.feedback-correct .option-letter{
  background:var(--accent);border-color:var(--accent);color:#070f12;
}
.option-item.feedback-wrong{
  background:var(--opt-wrong);border-color:var(--danger);
  animation:wrongShake .4s ease forwards;pointer-events:none;
}
.option-item.feedback-reveal{
  background:var(--opt-correct);border-color:var(--accent);pointer-events:none;
}
.option-item.feedback-reveal .option-letter{
  background:var(--accent);border-color:var(--accent);color:#070f12;
}
.option-item.feedback-dim{opacity:.45;pointer-events:none;}

/* Nav buttons */
.nav-buttons{display:flex;gap:.75rem;justify-content:flex-end;}
.btn-nav{
  padding:.75rem 1.75rem;border-radius:var(--r);
  font-size:.9rem;font-weight:600;
  border:1px solid var(--card-bdr);background:var(--card);
  color:var(--text-muted);cursor:pointer;
  transition:all .2s;
}
.btn-nav:hover:not(:disabled){border-color:var(--accent);color:var(--accent);background:var(--opt-hover);}
.btn-nav.primary{background:var(--accent);color:#070f12;border-color:var(--accent);}
.btn-nav.primary:hover:not(:disabled){background:var(--accent-lt);}
.btn-nav:disabled{opacity:.35;cursor:not-allowed;}

/* Loading */
.loading-screen{text-align:center;padding:5rem 2rem;}
.spinner{
  width:48px;height:48px;
  border:3px solid var(--card-bdr);border-top-color:var(--accent);
  border-radius:50%;animation:spin 1s linear infinite;
  margin:0 auto 1.5rem;
}
@keyframes spin{to{transform:rotate(360deg);}}
.loading-text{color:var(--text-dim);font-size:.95rem;}

/* Results */
.results-screen{max-width:680px;margin:0 auto;padding:2rem 0;}
.results-header{text-align:center;margin-bottom:2.5rem;}
.score-ring-wrap{position:relative;width:140px;height:140px;margin:0 auto 1.5rem;}
.score-ring-wrap svg{width:100%;height:100%;transform:rotate(-90deg);}
.score-ring-track{fill:none;stroke:var(--card-bdr);stroke-width:6;}
.score-ring-fill{
  fill:none;stroke:var(--accent);stroke-width:6;stroke-linecap:round;
  stroke-dasharray:339.29;stroke-dashoffset:339.29;
  transition:stroke-dashoffset 1.2s cubic-bezier(.4,0,.2,1) .3s,stroke .3s;
}
.ring-label{
  position:absolute;inset:0;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
}
.ring-score{font-family:'Space Grotesk',sans-serif;font-size:1.7rem;font-weight:700;}
.ring-max{font-size:.75rem;color:var(--text-dim);}
.result-pct{
  font-family:'Space Grotesk',sans-serif;font-size:2rem;font-weight:700;
  color:var(--accent);margin-bottom:.25rem;
}
.result-tier{font-size:1.2rem;font-weight:700;color:var(--accent);margin-bottom:.4rem;}
.result-name{color:var(--text-dim);font-size:.9rem;margin-bottom:.25rem;}
.result-time{color:var(--text-dim);font-size:.82rem;margin-bottom:.5rem;}
.result-msg{color:var(--text-muted);font-size:.95rem;}
.result-actions{
  display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;margin:2rem 0;
}
.review-section{margin-top:1rem;}
.review-section h3{
  font-family:'Space Grotesk',sans-serif;font-size:1rem;font-weight:700;
  margin-bottom:1rem;padding-bottom:.75rem;border-bottom:1px solid var(--card-bdr);
}
.review-list{display:flex;flex-direction:column;gap:.75rem;}
.review-item{
  border-radius:var(--r);border:1px solid var(--card-bdr);
  background:var(--card);padding:1rem 1.25rem;
}
.review-item.correct{border-color:rgba(16,185,129,.4);}
.review-item.wrong  {border-color:rgba(248,113,113,.3);}
.review-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:.5rem;}
.review-num{font-size:.75rem;font-weight:700;color:var(--text-dim);}
.review-item.correct .review-icon{color:var(--accent);}
.review-item.wrong   .review-icon{color:var(--danger);}
.review-question{font-weight:600;font-size:.9rem;margin-bottom:.6rem;line-height:1.4;}
.review-answers{font-size:.82rem;display:flex;flex-direction:column;gap:.25rem;}
.review-yours  {color:var(--text-dim);}
.review-correct{color:var(--accent);}
.review-pts{
  display:inline-block;margin-top:.5rem;
  font-size:.75rem;font-weight:700;padding:.15rem .6rem;border-radius:99px;
}
.review-item.correct .review-pts{background:rgba(16,185,129,.15);color:var(--accent);}
.review-item.wrong   .review-pts{background:rgba(248,113,113,.12);color:var(--danger);}

/* ── Responsive ── */
@media(max-width:600px){
  .start-card{margin:1rem;padding:1.75rem 1.25rem;}
  .nav-buttons{flex-wrap:wrap;}
  .btn-nav{flex:1;text-align:center;}
  .result-actions{flex-direction:column;}
  .result-actions .btn{width:100%;}
  .steps-grid{grid-template-columns:1fr;}
}
"""
w("static/css/style.css", CSS)

# ─────────────────────────────────────────────────────────────────────────────
# 2. index.html
# ─────────────────────────────────────────────────────────────────────────────
INDEX = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>QuizApp \u2014 Premium Quiz Platform</title>
  <meta name="description" content="Challenge yourself with curated quizzes across knowledge, science, and pop culture." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="static/css/style.css" />
</head>
<body>

<nav class="navbar">
  <a href="index.html" class="nav-logo">
    <span class="logo-icon">Q</span>
    <span class="logo-text">QuizApp</span>
  </a>
  <div class="nav-right">
    <a href="#how-it-works" class="nav-link">How It Works</a>
    <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme" title="Toggle light / dark">\U0001f319</button>
  </div>
</nav>

<main>
  <section class="hero">
    <div class="hero-badge">\u2726 Premium Quiz Platform</div>
    <h1 class="hero-title">Challenge What<br /><span class="gradient-text">You Know</span></h1>
    <p class="hero-subtitle">
      Curated quizzes across knowledge, science &amp; pop culture.
      Go back, revise answers, see where you truly rank.
    </p>
    <a href="#quizzes" class="btn btn-primary btn-lg">Browse Quizzes \u2193</a>
  </section>

  <section class="quiz-section" id="quizzes">
    <div class="section-header">
      <h2 class="section-title">Pick a Quiz</h2>
      <p class="section-sub">3 categories \u00b7 Free \u00b7 No sign-up needed</p>
    </div>
    <div class="quiz-grid" id="quiz-grid">
      <p style="color:var(--text-dim);text-align:center;grid-column:1/-1">Loading quizzes\u2026</p>
    </div>
  </section>

  <section class="how-section" id="how-it-works">
    <div class="section-header">
      <h2 class="section-title">How It Works</h2>
      <p class="section-sub">Simple, fast, and fun</p>
    </div>
    <div class="steps-grid">
      <div class="step-card">
        <div class="step-num">1</div>
        <div class="step-title">Pick a Quiz</div>
        <p class="step-desc">Choose from General Knowledge, Science &amp; Tech, or Pop Culture.</p>
      </div>
      <div class="step-card">
        <div class="step-num">2</div>
        <div class="step-title">Answer Questions</div>
        <p class="step-desc">Navigate freely \u2014 go back and change any answer before finishing.</p>
      </div>
      <div class="step-card">
        <div class="step-num">3</div>
        <div class="step-title">See Your Score</div>
        <p class="step-desc">Get your tier (Genius \u2192 Novice), percentage, and a full question review.</p>
      </div>
    </div>
  </section>
</main>

<footer class="footer">
  \u00a9 2025 QuizApp \u00b7 Static site on GitHub Pages \u00b7 <a href="https://github.com/VELU1231/QuizSimple">View Source</a>
</footer>

<script src="static/js/data.js"></script>
<script src="static/js/home.js"></script>
<script>
  (function () {
    var html = document.documentElement;
    var btn  = document.getElementById('theme-toggle');
    var saved = localStorage.getItem('qapp_theme') || 'dark';
    html.setAttribute('data-theme', saved);
    btn.textContent = saved === 'dark' ? '\U0001f319' : '\u2600\ufe0f';
    btn.addEventListener('click', function () {
      var cur  = html.getAttribute('data-theme');
      var next = cur === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('qapp_theme', next);
      btn.textContent = next === 'dark' ? '\U0001f319' : '\u2600\ufe0f';
    });
  })();
</script>
</body>
</html>
"""
w("index.html", INDEX)

# ─────────────────────────────────────────────────────────────────────────────
# 3. quiz.html
# ─────────────────────────────────────────────────────────────────────────────
QUIZ_HTML = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Quiz \u2014 QuizApp</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="static/css/style.css" />
</head>
<body>

<nav class="navbar">
  <a href="index.html" class="nav-logo">
    <span class="logo-icon">Q</span>
    <span class="logo-text">QuizApp</span>
  </a>
  <div class="nav-right">
    <a href="index.html" class="nav-link">\u2190 All Quizzes</a>
    <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme">\U0001f319</button>
  </div>
</nav>

<div class="quiz-page">

  <!-- ── START SCREEN ── -->
  <div class="screen" id="start-screen">
    <div class="start-card">

      <!-- Resume banner (hidden by default, shown by JS if saved progress exists) -->
      <div id="resume-banner" class="resume-banner" style="display:none">
        <strong>You have saved progress!</strong><br />
        Continue where you left off or start fresh.
        <div class="resume-actions">
          <button id="resume-btn" class="btn btn-primary">Resume</button>
          <button id="reset-btn" class="btn btn-outline">Start Fresh</button>
        </div>
      </div>

      <div class="start-icon" id="start-icon">\U0001f3af</div>
      <span class="start-category" id="start-category">Category</span>
      <h1 class="start-title" id="start-title">Loading\u2026</h1>
      <p class="start-desc" id="start-desc">Please wait\u2026</p>
      <div class="start-meta" id="start-meta"></div>

      <div class="start-name-row">
        <label for="player-name" class="name-label">Your Name (optional)</label>
        <input type="text" id="player-name" class="name-input" placeholder="Anonymous" maxlength="32" autocomplete="off" />
      </div>

      <button id="start-btn" class="btn btn-primary btn-xl">Start Quiz \u2192</button>
      <p class="start-tip">Tip: You can go back and revise any answer before finishing.</p>
    </div>
  </div>

  <!-- ── QUIZ SCREEN ── -->
  <div class="screen" id="quiz-screen">
    <div class="quiz-screen-inner">

      <div class="progress-wrap">
        <div class="progress-meta">
          <span id="question-counter">1 / 10</span>
          <span id="answered-count">0 answered</span>
          <span class="points-badge" id="points-badge">1 pt</span>
        </div>
        <div class="progress-bar-bg">
          <div class="progress-bar-fill" id="progress-bar"></div>
        </div>
      </div>

      <p class="question-text" id="question-text"></p>

      <ul class="options-list" id="options-list"></ul>

      <div class="nav-buttons">
        <button class="btn-nav" id="btn-prev" disabled>\u2190 Prev</button>
        <button class="btn-nav primary" id="btn-next" disabled>Next \u2192</button>
      </div>

    </div>
  </div>

  <!-- ── LOADING SCREEN ── -->
  <div class="screen" id="loading-screen">
    <div class="loading-screen">
      <div class="spinner"></div>
      <p class="loading-text">Calculating your score\u2026</p>
    </div>
  </div>

  <!-- ── RESULTS SCREEN ── -->
  <div class="screen" id="results-screen">
    <div class="results-screen">

      <div class="results-header">
        <div class="score-ring-wrap">
          <svg viewBox="0 0 120 120" aria-hidden="true">
            <circle class="score-ring-track" cx="60" cy="60" r="54" />
            <circle class="score-ring-fill"  id="score-ring-progress" cx="60" cy="60" r="54" />
          </svg>
          <div class="ring-label">
            <span class="ring-score"><span id="result-score">0</span></span>
            <span class="ring-max">/ <span id="result-max">0</span> pts</span>
          </div>
        </div>

        <div class="result-pct"  id="result-pct">0%</div>
        <div class="result-tier" id="result-tier">\u2014</div>
        <div class="result-name" id="result-name"></div>
        <div class="result-time" id="result-time"></div>
        <p  class="result-msg"  id="result-msg"></p>
      </div>

      <div class="result-actions">
        <button id="restart-btn" class="btn btn-primary btn-lg">Try Again</button>
        <a      id="home-btn"    href="index.html" class="btn btn-outline btn-lg">All Quizzes</a>
      </div>

      <div class="review-section">
        <h3>Question Review</h3>
        <ul class="review-list" id="review-list"></ul>
      </div>

    </div>
  </div>

</div><!-- .quiz-page -->

<script src="static/js/data.js"></script>
<script src="static/js/quiz.js"></script>
<script>
  /* Theme toggle */
  (function () {
    var html = document.documentElement;
    var btn  = document.getElementById('theme-toggle');
    var saved = localStorage.getItem('qapp_theme') || 'dark';
    html.setAttribute('data-theme', saved);
    btn.textContent = saved === 'dark' ? '\U0001f319' : '\u2600\ufe0f';
    btn.addEventListener('click', function () {
      var cur  = html.getAttribute('data-theme');
      var next = cur === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('qapp_theme', next);
      btn.textContent = next === 'dark' ? '\U0001f319' : '\u2600\ufe0f';
    });
  })();
</script>
</body>
</html>
"""
w("quiz.html", QUIZ_HTML)

# ─────────────────────────────────────────────────────────────────────────────
# 4. data.js
# ─────────────────────────────────────────────────────────────────────────────
DATA_JS = r"""/* data.js — Embedded quiz data for GitHub Pages static site */
/* Source: app/data/quizzes.json */
window.ALL_QUIZZES = [
  {
    "id": "trivia",
    "title": "General Knowledge",
    "description": "Test your knowledge across history, geography, science, and everyday facts.",
    "category": "Knowledge",
    "icon": "\uD83C\uDF0D",
    "difficulty": "Medium",
    "questions": [
      {"question":"What is the capital city of Australia?","options":["Sydney","Melbourne","Canberra","Brisbane"],"answer":2,"points":2},
      {"question":"How many sides does a hexagon have?","options":["5","6","7","8"],"answer":1,"points":1},
      {"question":"Who wrote the play Romeo and Juliet?","options":["Charles Dickens","William Shakespeare","Jane Austen","Leo Tolstoy"],"answer":1,"points":1},
      {"question":"What is the largest ocean on Earth?","options":["Atlantic Ocean","Indian Ocean","Arctic Ocean","Pacific Ocean"],"answer":3,"points":2},
      {"question":"In which year did World War II end?","options":["1943","1944","1945","1946"],"answer":2,"points":2},
      {"question":"What is the smallest planet in our solar system?","options":["Venus","Mercury","Mars","Pluto"],"answer":1,"points":2},
      {"question":"How many bones are in the adult human body?","options":["185","196","206","214"],"answer":2,"points":3},
      {"question":"What is the chemical symbol for gold?","options":["Go","Ag","Au","Fe"],"answer":2,"points":2},
      {"question":"Which country is credited with inventing the printing press?","options":["China","Italy","Germany","France"],"answer":2,"points":3},
      {"question":"Approximately how fast does light travel per second?","options":["199,792 km/s","299,792 km/s","399,792 km/s","499,792 km/s"],"answer":1,"points":3}
    ]
  },
  {
    "id": "science",
    "title": "Science & Technology",
    "description": "Dive into computing, biology, physics, and the wonders of the natural world.",
    "category": "Science",
    "icon": "\uD83D\uDD2C",
    "difficulty": "Hard",
    "questions": [
      {"question":"What does CPU stand for?","options":["Central Processing Unit","Computer Processing Unit","Central Program Utility","Core Processor Unit"],"answer":0,"points":1},
      {"question":"Which planet is known as the Red Planet?","options":["Venus","Jupiter","Mars","Saturn"],"answer":2,"points":1},
      {"question":"What is commonly called the powerhouse of the cell?","options":["Nucleus","Ribosome","Mitochondria","Golgi apparatus"],"answer":2,"points":2},
      {"question":"What is the most abundant gas in Earth's atmosphere?","options":["Oxygen","Carbon Dioxide","Argon","Nitrogen"],"answer":3,"points":2},
      {"question":"Who is credited with inventing the telephone?","options":["Thomas Edison","Nikola Tesla","Alexander Graham Bell","James Watt"],"answer":2,"points":2},
      {"question":"What is the atomic number of carbon?","options":["4","5","6","8"],"answer":2,"points":3},
      {"question":"What type of electromagnetic wave is used in Wi-Fi?","options":["X-rays","Radio waves","Infrared","Ultraviolet"],"answer":1,"points":2},
      {"question":"What does DNA stand for?","options":["Deoxyribonucleic Acid","Dinitrogen Oxalate Acid","Dual Nucleic Arrangement","Dynamic Nuclear Acid"],"answer":0,"points":2},
      {"question":"What is the hardest natural substance on Earth?","options":["Quartz","Diamond","Titanium","Graphite"],"answer":1,"points":1},
      {"question":"Which programming language was created by Guido van Rossum?","options":["Java","Perl","Ruby","Python"],"answer":3,"points":2}
    ]
  },
  {
    "id": "pop-culture",
    "title": "Pop Culture",
    "description": "Movies, music, TV, and iconic moments from pop culture history.",
    "category": "Entertainment",
    "icon": "\uD83C\uDFAC",
    "difficulty": "Easy",
    "questions": [
      {"question":"Which film won the very first Academy Award for Best Picture?","options":["Casablanca","Gone with the Wind","Wings","Ben-Hur"],"answer":2,"points":3},
      {"question":"Who performed the iconic song Thriller?","options":["Michael Jackson","Prince","Elvis Presley","Madonna"],"answer":0,"points":1},
      {"question":"Which TV show is set in the fictional kingdom of Westeros?","options":["The Witcher","Game of Thrones","House of the Dragon","The Crown"],"answer":1,"points":1},
      {"question":"What is the highest-grossing film of all time (unadjusted for inflation)?","options":["Avengers: Endgame","Titanic","The Lion King","Avatar"],"answer":3,"points":3},
      {"question":"Which actor plays Tony Stark / Iron Man in the MCU?","options":["Chris Evans","Robert Downey Jr.","Chris Hemsworth","Mark Ruffalo"],"answer":1,"points":1},
      {"question":"In what year did Apple release the first iPhone?","options":["2005","2006","2007","2008"],"answer":2,"points":2},
      {"question":"Which band recorded the song Bohemian Rhapsody?","options":["The Beatles","Led Zeppelin","Queen","Pink Floyd"],"answer":2,"points":1},
      {"question":"What color is the famous front door of 10 Downing Street?","options":["Red","Blue","Black","Green"],"answer":2,"points":2},
      {"question":"Which streaming service produced Stranger Things?","options":["Amazon Prime Video","HBO Max","Disney+","Netflix"],"answer":3,"points":1},
      {"question":"In what fictional city does Batman protect the citizens?","options":["Metropolis","Star City","Gotham City","Central City"],"answer":2,"points":2}
    ]
  }
];
"""
w("static/js/data.js", DATA_JS)

# ─────────────────────────────────────────────────────────────────────────────
# 5. home.js
# ─────────────────────────────────────────────────────────────────────────────
HOME_JS = r"""/* home.js — Renders quiz cards from window.ALL_QUIZZES */
'use strict';

(function () {
  var DIFF_CLASS = { easy: 'diff-easy', medium: 'diff-medium', hard: 'diff-hard' };

  function esc(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function buildCard(quiz) {
    var qCount   = quiz.questions.length;
    var maxScore = quiz.questions.reduce(function (s, q) { return s + q.points; }, 0);
    var diffKey  = (quiz.difficulty || '').toLowerCase();
    var diffCls  = DIFF_CLASS[diffKey] || '';

    var a = document.createElement('a');
    a.href      = 'quiz.html?id=' + encodeURIComponent(quiz.id);
    a.className = 'quiz-card';
    a.setAttribute('aria-label', 'Start ' + quiz.title);

    a.innerHTML =
      '<span class="card-icon">'   + esc(quiz.icon || '?') + '</span>' +
      '<div class="card-content">' +
        '<span class="card-category">' + esc(quiz.category)    + '</span>' +
        '<h3  class="card-title">'     + esc(quiz.title)       + '</h3>'  +
        '<p   class="card-desc">'      + esc(quiz.description) + '</p>'   +
        '<div class="card-meta">' +
          '<span class="meta-badge">'              + qCount   + ' Questions</span>' +
          '<span class="meta-badge ' + diffCls + '">' + esc(quiz.difficulty) + '</span>' +
          '<span class="meta-badge">'              + maxScore + ' pts max</span>' +
        '</div>' +
      '</div>' +
      '<span class="card-arrow" aria-hidden="true">&rarr;</span>';

    return a;
  }

  function init() {
    var grid = document.getElementById('quiz-grid');
    if (!grid) return;
    var quizzes = window.ALL_QUIZZES || [];
    if (!quizzes.length) {
      grid.innerHTML = '<p style="color:var(--text-dim);text-align:center;grid-column:1/-1">No quizzes available.</p>';
      return;
    }
    grid.innerHTML = '';
    quizzes.forEach(function (q) { grid.appendChild(buildCard(q)); });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
"""
w("static/js/home.js", HOME_JS)

# ─────────────────────────────────────────────────────────────────────────────
# 6. quiz.js  — Full engine + Quizller features (feedback, persistence, timer)
# ─────────────────────────────────────────────────────────────────────────────
QUIZ_JS = r"""/* quiz.js — Static quiz engine
   Quizller features adopted:
     - Staggered slide-in animations on options
     - Instant feedback flash on answer (correct=green, wrong=red+reveal)
     - localStorage progress persistence (resume on refresh)
     - Elapsed time shown in results
*/
'use strict';

(function () {

  // ── Load quiz from URL param ─────────────────────────────────────────────
  var params  = new URLSearchParams(location.search);
  var quizId  = params.get('id');
  var quiz    = null;

  if (window.ALL_QUIZZES) {
    quiz = window.ALL_QUIZZES.find(function (q) { return q.id === quizId; });
  }

  // ── State ────────────────────────────────────────────────────────────────
  var state = {
    currentIdx: 0,
    answers:    {},   // { "0": optIdx, "1": optIdx … }
    startTime:  null,
    submitted:  false,
    feedbackLocked: false,  // true during 800ms Quizller feedback animation
  };

  // ── DOM ──────────────────────────────────────────────────────────────────
  var screens = {
    start:   document.getElementById('start-screen'),
    quiz:    document.getElementById('quiz-screen'),
    loading: document.getElementById('loading-screen'),
    results: document.getElementById('results-screen'),
  };

  var progressBar   = document.getElementById('progress-bar');
  var qCounter      = document.getElementById('question-counter');
  var answeredCount = document.getElementById('answered-count');
  var pointsBadge   = document.getElementById('points-badge');
  var questionEl    = document.getElementById('question-text');
  var optionsList   = document.getElementById('options-list');
  var prevBtn       = document.getElementById('btn-prev');
  var nextBtn       = document.getElementById('btn-next');

  // ── Screen helper ────────────────────────────────────────────────────────
  function showScreen(name) {
    Object.keys(screens).forEach(function (k) {
      screens[k].classList.toggle('active', k === name);
    });
  }

  // ── localStorage persistence (Quizller: cookie-based; we use localStorage) ─
  var STORAGE_KEY = 'qapp_progress_' + quizId;

  function saveProgress() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        currentIdx: state.currentIdx,
        answers:    state.answers,
        startTime:  state.startTime,
      }));
    } catch (_) {}
  }

  function loadProgress() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return false;
      var data = JSON.parse(raw);
      if (!data || !data.answers || Object.keys(data.answers).length === 0) return false;
      state.currentIdx = data.currentIdx || 0;
      state.answers    = data.answers    || {};
      state.startTime  = data.startTime  || Date.now();
      return true;
    } catch (_) { return false; }
  }

  function clearProgress() {
    try { localStorage.removeItem(STORAGE_KEY); } catch (_) {}
  }

  // ── Populate start card ──────────────────────────────────────────────────
  function populateStart() {
    if (!quiz) {
      document.getElementById('start-title').textContent = 'Quiz not found';
      document.getElementById('start-desc').textContent  = 'Please go back and choose a valid quiz.';
      document.getElementById('start-btn').disabled      = true;
      return;
    }

    document.title = quiz.title + ' \u2014 QuizApp';
    document.getElementById('start-icon').textContent     = quiz.icon     || '\uD83C\uDFAF';
    document.getElementById('start-category').textContent = quiz.category || '';
    document.getElementById('start-title').textContent    = quiz.title;
    document.getElementById('start-desc').textContent     = quiz.description;

    var maxScore = quiz.questions.reduce(function (s, q) { return s + q.points; }, 0);
    var diffMap  = { easy: 'diff-easy', medium: 'diff-medium', hard: 'diff-hard' };
    var diffCls  = diffMap[(quiz.difficulty || '').toLowerCase()] || '';

    var meta = document.getElementById('start-meta');
    meta.innerHTML =
      '<span class="meta-badge">'              + quiz.questions.length + ' Questions</span>' +
      '<span class="meta-badge ' + diffCls + '">' + (quiz.difficulty || '') + '</span>' +
      '<span class="meta-badge">'              + maxScore + ' pts max</span>';
  }

  // ── Start quiz ───────────────────────────────────────────────────────────
  function startQuiz(resume) {
    if (!quiz) return;
    if (!resume) {
      state.currentIdx = 0;
      state.answers    = {};
      state.startTime  = Date.now();
      clearProgress();
    }
    state.submitted     = false;
    state.feedbackLocked = false;
    renderQuestion();
    showScreen('quiz');
  }

  // ── Render current question ──────────────────────────────────────────────
  function renderQuestion() {
    state.feedbackLocked = false;
    var q     = quiz.questions[state.currentIdx];
    var total = quiz.questions.length;
    var done  = Object.keys(state.answers).length;

    qCounter.textContent      = (state.currentIdx + 1) + ' / ' + total;
    answeredCount.textContent = done + ' answered';
    progressBar.style.width   = (((state.currentIdx + 1) / total) * 100) + '%';
    pointsBadge.textContent   = q.points + ' pt' + (q.points !== 1 ? 's' : '');

    // Animate question text
    questionEl.style.opacity = '0';
    questionEl.textContent   = q.question;
    requestAnimationFrame(function () {
      questionEl.style.transition = 'opacity .25s ease';
      questionEl.style.opacity    = '1';
    });

    // Build options (Quizller: staggered slide-in via CSS nth-child delays)
    var userAns = state.answers[String(state.currentIdx)];
    optionsList.innerHTML = '';

    q.options.forEach(function (opt, idx) {
      var li = document.createElement('li');
      li.className = 'option-item';
      if (userAns === idx) li.classList.add('selected');

      var letter       = document.createElement('span');
      letter.className = 'option-letter';
      letter.textContent = String.fromCharCode(65 + idx);   // A B C D

      var text         = document.createElement('span');
      text.className   = 'option-text';
      text.textContent = opt;

      li.appendChild(letter);
      li.appendChild(text);
      li.addEventListener('click', function () { selectAnswer(idx); });
      optionsList.appendChild(li);
    });

    // Nav buttons
    prevBtn.disabled = (state.currentIdx === 0);
    var isLast = (state.currentIdx === total - 1);
    nextBtn.textContent = isLast ? 'Finish \u2713' : 'Next \u2192';
    nextBtn.disabled    = (userAns === undefined);
    nextBtn.className   = 'btn-nav' + (isLast ? ' primary' : '');
  }

  // ── Select answer (Quizller: instant feedback animation) ─────────────────
  function selectAnswer(optIdx) {
    if (state.feedbackLocked) return;

    var key      = String(state.currentIdx);
    var q        = quiz.questions[state.currentIdx];
    var isFirst  = !(key in state.answers);

    state.answers[key] = optIdx;
    saveProgress();

    if (isFirst) {
      // Quizller-style: flash correct/wrong for 800 ms, then restore
      state.feedbackLocked = true;
      var items = optionsList.querySelectorAll('.option-item');
      var isCorrect = (optIdx === q.answer);

      items.forEach(function (li, idx) {
        li.style.pointerEvents = 'none';
        if (idx === optIdx) {
          li.classList.add(isCorrect ? 'feedback-correct' : 'feedback-wrong');
        } else if (!isCorrect && idx === q.answer) {
          li.classList.add('feedback-reveal');   // show correct answer
        } else {
          li.classList.add('feedback-dim');
        }
      });

      setTimeout(function () {
        renderQuestion();   // re-render without feedback classes
      }, 800);

    } else {
      // Already answered — just update highlight
      renderQuestion();
    }
  }

  // ── Navigation ───────────────────────────────────────────────────────────
  function goPrev() {
    if (state.feedbackLocked) return;
    if (state.currentIdx > 0) {
      state.currentIdx -= 1;
      saveProgress();
      renderQuestion();
    }
  }

  function goNext() {
    if (state.feedbackLocked) return;
    var total = quiz.questions.length;
    if (state.currentIdx < total - 1) {
      state.currentIdx += 1;
      saveProgress();
      renderQuestion();
    } else {
      finishQuiz();
    }
  }

  // ── Finish & score ────────────────────────────────────────────────────────
  function finishQuiz() {
    if (state.submitted) return;
    state.submitted = true;
    showScreen('loading');

    // Small delay to show loading spinner (feels premium like Quizller loader)
    setTimeout(function () {
      var result = calculateScore();
      clearProgress();
      renderResults(result);
      showScreen('results');
    }, 900);
  }

  // ── Client-side scoring (replaces Flask /api/submit) ─────────────────────
  function calculateScore() {
    var max_score = quiz.questions.reduce(function (s, q) { return s + q.points; }, 0);
    var score     = 0;
    var details   = quiz.questions.map(function (q, i) {
      var userAns    = state.answers[String(i)];
      var isCorrect  = (userAns === q.answer);
      if (isCorrect) score += q.points;
      return {
        question:       q.question,
        options:        q.options,
        user_answer:    userAns !== undefined ? userAns : null,
        correct_answer: q.answer,
        is_correct:     isCorrect,
        points:         q.points,
      };
    });

    var pct = max_score > 0 ? Math.round((score / max_score) * 100) : 0;
    var tier, tier_color, tier_msg;

    if (pct >= 90) {
      tier = 'Genius';  tier_color = '#fbbf24';
      tier_msg = 'Outstanding! You really know your stuff.';
    } else if (pct >= 70) {
      tier = 'Expert';  tier_color = '#10b981';
      tier_msg = "Great work! You're well above average.";
    } else if (pct >= 50) {
      tier = 'Learner'; tier_color = '#8b5cf6';
      tier_msg = "Good effort! Keep studying and you'll get there.";
    } else {
      tier = 'Novice';  tier_color = '#f87171';
      tier_msg = 'Everyone starts somewhere \u2014 give it another shot!';
    }

    var elapsed = state.startTime ? Math.round((Date.now() - state.startTime) / 1000) : 0;
    var mins = Math.floor(elapsed / 60);
    var secs = elapsed % 60;
    var timeStr = mins > 0
      ? mins + ' min ' + secs + ' sec'
      : secs + ' sec';

    return {
      score: score, max_score: max_score, percentage: pct,
      tier: tier, tier_color: tier_color, tier_msg: tier_msg,
      time_str: timeStr,
      results: details,
    };
  }

  // ── Render results ────────────────────────────────────────────────────────
  function escHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function renderResults(r) {
    document.getElementById('result-score').textContent = r.score;
    document.getElementById('result-max').textContent   = r.max_score;
    document.getElementById('result-pct').textContent   = r.percentage + '%';

    var tierEl = document.getElementById('result-tier');
    tierEl.textContent = r.tier;
    tierEl.style.color = r.tier_color;

    // Player name
    var nameEl = document.getElementById('player-name');
    var name   = (nameEl && nameEl.value.trim()) || '';
    var nameDisplay = document.getElementById('result-name');
    if (nameDisplay) nameDisplay.textContent = name ? 'Player: ' + name : '';

    // Elapsed time (Quizller feature)
    var timeDisplay = document.getElementById('result-time');
    if (timeDisplay) timeDisplay.textContent = 'Time: ' + r.time_str;

    var msgEl = document.getElementById('result-msg');
    if (msgEl) msgEl.textContent = r.tier_msg;

    // Score ring animation
    var ring = document.getElementById('score-ring-progress');
    if (ring) {
      var circumference = 2 * Math.PI * 54;   // r=54
      ring.style.stroke            = r.tier_color;
      ring.style.strokeDasharray   = circumference;
      ring.style.strokeDashoffset  = circumference;
      requestAnimationFrame(function () {
        ring.style.strokeDashoffset = circumference * (1 - r.percentage / 100);
      });
    }

    // Review list
    var reviewList = document.getElementById('review-list');
    reviewList.innerHTML = '';
    r.results.forEach(function (item, idx) {
      var div = document.createElement('div');
      div.className = 'review-item ' + (item.is_correct ? 'correct' : 'wrong');

      var userText = item.user_answer !== null && item.user_answer !== undefined
        ? escHtml(item.options[item.user_answer])
        : '<em>No answer</em>';

      div.innerHTML =
        '<div class="review-header">' +
          '<span class="review-num">Q' + (idx + 1) + '</span>' +
          '<span class="review-icon">' + (item.is_correct ? '\u2713' : '\u2717') + '</span>' +
        '</div>' +
        '<p class="review-question">' + escHtml(item.question) + '</p>' +
        '<div class="review-answers">' +
          '<span class="review-yours">Your answer: ' + userText + '</span>' +
          (!item.is_correct
            ? '<span class="review-correct">Correct: ' + escHtml(item.options[item.correct_answer]) + '</span>'
            : '') +
        '</div>' +
        '<span class="review-pts">' + (item.is_correct ? '+' + item.points : '0') + '/' + item.points + ' pts</span>';

      reviewList.appendChild(div);
    });
  }

  // ── Bind events ───────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    populateStart();

    // Check for saved progress (Quizller: used cookies; we use localStorage)
    var hasProgress = loadProgress();
    var resumeBanner = document.getElementById('resume-banner');
    var startBtn = document.getElementById('start-btn');

    if (hasProgress && quiz) {
      if (resumeBanner) {
        resumeBanner.style.display = 'block';
        startBtn.style.display     = 'none';
      }
      var resumeBtn = document.getElementById('resume-btn');
      var resetBtn  = document.getElementById('reset-btn');
      if (resumeBtn) resumeBtn.addEventListener('click', function () { startQuiz(true); });
      if (resetBtn)  resetBtn.addEventListener('click', function () {
        resumeBanner.style.display = 'none';
        startBtn.style.display     = '';
        clearProgress();
      });
    }

    if (startBtn) startBtn.addEventListener('click', function () { startQuiz(false); });
    if (prevBtn)  prevBtn.addEventListener('click', goPrev);
    if (nextBtn)  nextBtn.addEventListener('click', goNext);

    var restartBtn = document.getElementById('restart-btn');
    if (restartBtn) restartBtn.addEventListener('click', function () {
      showScreen('start');
      if (resumeBanner) resumeBanner.style.display = 'none';
      if (startBtn)     startBtn.style.display     = '';
    });

    showScreen('start');
  });

})();
"""
w("static/js/quiz.js", QUIZ_JS)

print("\nAll files written successfully.")
