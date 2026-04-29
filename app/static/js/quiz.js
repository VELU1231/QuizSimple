/* quiz.js — Full quiz engine with prev/next navigation */
'use strict';

(function () {
  // ── State ────────────────────────────────────────────────
  const quiz = window.QUIZ_DATA;          // injected by quiz.html template
  const state = {
    currentIdx:  0,
    answers:     {},                      // { "0": optIdx, "1": optIdx, … }
    startTime:   null,
    submitted:   false,
    nextArmedAt: 0,
  };

  // ── DOM References ────────────────────────────────────────
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

  // ── Screen Management ─────────────────────────────────────
  function showScreen(name) {
    Object.keys(screens).forEach((k) => {
      screens[k].classList.toggle('active', k === name);
    });
  }

  // ── Start ─────────────────────────────────────────────────
  function startQuiz() {
    state.currentIdx = 0;
    state.answers    = {};
    state.submitted  = false;
    state.startTime  = Date.now();
    renderQuestion();
    showScreen('quiz');
  }

  // ── Render current question ───────────────────────────────
  function renderQuestion() {
    const q     = quiz.questions[state.currentIdx];
    const total = quiz.questions.length;
    const done  = Object.keys(state.answers).length;

    // Counter + answered
    qCounter.textContent    = `${state.currentIdx + 1} / ${total}`;
    answeredCount.textContent = `${done} answered`;

    // Progress bar
    const pct = ((state.currentIdx + 1) / total) * 100;
    progressBar.style.width = `${pct}%`;

    // Points badge
    pointsBadge.textContent = `${q.points} pt${q.points !== 1 ? 's' : ''}`;

    // Question text (animate)
    questionEl.style.opacity = '0';
    questionEl.textContent   = q.question;
    requestAnimationFrame(() => {
      questionEl.style.transition = 'opacity 0.25s ease';
      questionEl.style.opacity    = '1';
    });

    // Options
    const userAns = state.answers[String(state.currentIdx)];
    optionsList.innerHTML = '';
    q.options.forEach((opt, idx) => {
      const li = document.createElement('li');
      li.className = 'option-item';
      if (userAns === idx) li.classList.add('selected');

      const letter = document.createElement('span');
      letter.className   = 'option-letter';
      letter.textContent = String.fromCharCode(65 + idx);   // A B C D

      const text = document.createElement('span');
      text.className   = 'option-text';
      text.textContent = opt;

      li.appendChild(letter);
      li.appendChild(text);
      li.addEventListener('click', () => selectAnswer(idx));
      optionsList.appendChild(li);
    });

    // Nav buttons
    prevBtn.disabled = state.currentIdx === 0;
    const isLast     = state.currentIdx === total - 1;
    nextBtn.textContent = isLast ? 'Finish ✓' : 'Next →';
    nextBtn.disabled    = userAns === undefined;
  }

  // ── Select answer ─────────────────────────────────────────
  function selectAnswer(optIdx) {
    state.answers[String(state.currentIdx)] = optIdx;
    state.nextArmedAt = Date.now() + 220; // avoid accidental immediate next on double-tap
    renderQuestion();   // re-render highlights selection and enables Next
  }

  // ── Navigation ────────────────────────────────────────────
  function goPrev() {
    if (state.currentIdx > 0) {
      state.currentIdx -= 1;
      renderQuestion();
    }
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

  // ── Submit ────────────────────────────────────────────────
  async function finishQuiz() {
    if (state.submitted) return;
    state.submitted = true;

    showScreen('loading');

    const elapsed = Math.round((Date.now() - state.startTime) / 1000);
    const nameEl  = document.getElementById('player-name');
    const name    = (nameEl && nameEl.value.trim()) || 'Anonymous';

    try {
      const res = await fetch('/api/submit', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({
          quiz_id:         quiz.id,
          answers:         state.answers,
          name:            name,
          elapsed_seconds: elapsed,
        }),
      });

      if (!res.ok) throw new Error(`Server error ${res.status}`);
      const result = await res.json();
      renderResults(result);
      showScreen('results');
    } catch (err) {
      console.error('Quiz submit error:', err);
      state.submitted = false;
      showScreen('quiz');
      alert('Could not submit quiz. Please check your connection and try again.');
    }
  }

  // ── Render Results ────────────────────────────────────────
  const TIER_MESSAGES = {
    Genius:  'Outstanding! You really know your stuff.',
    Expert:  'Great work! You're well above average.',
    Learner: 'Good effort! Keep studying and you'll get there.',
    Novice:  'Everyone starts somewhere — give it another shot!',
  };

  function renderResults(result) {
    // Score numbers
    document.getElementById('result-score').textContent = result.score;
    document.getElementById('result-max').textContent   = result.max_score;
    document.getElementById('result-pct').textContent   = `${result.percentage}%`;

    // Tier
    const tierEl = document.getElementById('result-tier');
    tierEl.textContent  = result.tier;
    tierEl.style.color  = result.tier_color;

    // Message
    const msgEl = document.getElementById('result-msg');
    if (msgEl) msgEl.textContent = TIER_MESSAGES[result.tier] || '';

    // Animated score ring (SVG stroke-dashoffset)
    const ring = document.getElementById('score-ring-progress');
    if (ring) {
      const circumference = 2 * Math.PI * 54; // r = 54
      ring.style.stroke          = result.tier_color;
      ring.style.strokeDasharray = circumference;
      // start at 0 fill, then animate
      ring.style.strokeDashoffset = circumference;
      requestAnimationFrame(() => {
        ring.style.strokeDashoffset =
          circumference * (1 - result.percentage / 100);
      });
    }

    // Review list
    const reviewList = document.getElementById('review-list');
    reviewList.innerHTML = '';
    result.results.forEach((item, idx) => {
      const div = document.createElement('div');
      div.className = `review-item ${item.is_correct ? 'correct' : 'wrong'}`;

      const userText =
        item.user_answer !== null && item.user_answer !== undefined
          ? escHtml(item.options[item.user_answer])
          : '<em>No answer</em>';

      div.innerHTML = `
        <div class="review-header">
          <span class="review-num">Q${idx + 1}</span>
          <span class="review-icon">${item.is_correct ? '✓' : '✗'}</span>
        </div>
        <p class="review-question">${escHtml(item.question)}</p>
        <div class="review-answers">
          <span class="review-yours">Your answer: ${userText}</span>
          ${
            !item.is_correct
              ? `<span class="review-correct">Correct: ${escHtml(item.options[item.correct_answer])}</span>`
              : ''
          }
        </div>
        <span class="review-pts">${item.is_correct ? '+' + item.points : '0'}/${item.points} pts</span>
      `;
      reviewList.appendChild(div);
    });
  }

  // ── Utility ───────────────────────────────────────────────
  function escHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // ── Bind events on DOM ready ──────────────────────────────
  document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('start-btn').addEventListener('click', startQuiz);
    prevBtn.addEventListener('click', goPrev);
    nextBtn.addEventListener('click', goNext);

    document.getElementById('restart-btn')
      ?.addEventListener('click', startQuiz);

    document.getElementById('home-btn')
      ?.addEventListener('click', () => { window.location.href = '/'; });

    showScreen('start');
  });
})();
