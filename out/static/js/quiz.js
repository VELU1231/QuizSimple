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
    nextArmedAt: 0,
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
    state.nextArmedAt = Date.now() + 220; // prevent accidental immediate next
    renderQuestion();
  }

  // ── Navigation ───────────────────────────────────────────────────────
  function goPrev() {
    if (state.currentIdx > 0) { state.currentIdx -= 1; renderQuestion(); }
  }

  function goNext() {
    if (Date.now() < state.nextArmedAt) return;
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
    Expert:  'Great work! You're well above average.',
    Learner: 'Good effort! Keep studying and you'll get there.',
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
