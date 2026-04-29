/* ============================================================
   QuizSimple – Quiz Engine (quiz.js)
   ============================================================ */

(function () {
  'use strict';

  // ── DOM refs ──────────────────────────────────────────────
  const $ = id => document.getElementById(id);
  const screenStart   = $('screen-start');
  const screenQuiz    = $('screen-quiz');
  const screenLoading = $('screen-loading');
  const screenResults = $('screen-results');

  const btnStart    = $('btn-start');
  const btnNext     = $('btn-next');
  const nicknameInput = $('nickname-input');

  const progressFill = $('progress-fill');
  const progressText = $('progress-text');
  const navProgress  = $('nav-progress');

  const questionNum  = $('question-num');
  const questionText = $('question-text');
  const optionsGrid  = $('options-grid');

  const timerNum    = $('timer-num');
  const timerStroke = $('timer-stroke');
  const timerWrap   = $('timer-wrap');

  const resultsCard = $('results-card');

  // ── Quiz state ────────────────────────────────────────────
  const QUIZ       = window.QUIZ_DATA;
  const questions  = QUIZ.questions;
  const total      = questions.length;
  const isTimed    = QUIZ.timed;
  const timeLimit  = QUIZ.time_per_question || 15;
  const CIRCUMFERENCE = 2 * Math.PI * 26; // r=26, matches SVG

  let currentIdx  = 0;
  let answers     = [];          // user's chosen option indexes
  let selectedIdx = null;
  let timerInterval = null;
  let timeLeft    = timeLimit;
  let startTime   = null;
  let quizStartTime = null;

  // ── Helpers ───────────────────────────────────────────────
  const LETTERS = ['A', 'B', 'C', 'D', 'E'];

  function showScreen(id) {
    [screenStart, screenQuiz, screenLoading, screenResults].forEach(s => {
      if (s) s.classList.remove('active');
    });
    const target = $(id);
    if (target) target.classList.add('active');
  }

  function updateProgress(idx) {
    const pct = (idx / total) * 100;
    if (progressFill) progressFill.style.width = pct + '%';
    if (progressText) progressText.textContent = `Question ${idx + 1} of ${total}`;
    if (navProgress)  navProgress.textContent   = `${idx + 1} / ${total}`;
  }

  // ── Timer ─────────────────────────────────────────────────
  function startTimer() {
    if (!isTimed || !timerStroke) return;
    timeLeft = timeLimit;
    renderTimer();
    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
      timeLeft--;
      renderTimer();
      if (timeLeft <= 0) {
        clearInterval(timerInterval);
        onTimeUp();
      }
    }, 1000);
  }

  function stopTimer() {
    clearInterval(timerInterval);
  }

  function renderTimer() {
    if (!timerNum || !timerStroke) return;
    timerNum.textContent = timeLeft;
    const ratio  = timeLeft / timeLimit;
    const offset = CIRCUMFERENCE * (1 - ratio);
    timerStroke.style.strokeDashoffset = offset;
    if (timeLeft <= 5) {
      timerNum.classList.add('timer-urgent');
      timerStroke.style.stroke = '#ef4444';
    } else {
      timerNum.classList.remove('timer-urgent');
      timerStroke.style.stroke = QUIZ.color;
    }
  }

  function onTimeUp() {
    // Auto-select "no answer" (-1) and move on
    if (selectedIdx === null) {
      lockOptions(-1);
      answers.push(-1);
      if (btnNext) {
        btnNext.disabled = false;
        setTimeout(goNext, 800);
      }
    }
  }

  // ── Render question ───────────────────────────────────────
  function renderQuestion(idx) {
    selectedIdx = null;
    if (btnNext) btnNext.disabled = true;

    const q = questions[idx];
    if (questionNum)  questionNum.textContent  = `Question ${idx + 1}`;
    if (questionText) questionText.textContent = q.q;

    if (optionsGrid) {
      optionsGrid.innerHTML = '';
      q.options.forEach((opt, i) => {
        const btn = document.createElement('button');
        btn.className   = 'option-btn';
        btn.dataset.idx = i;
        btn.innerHTML   = `<span class="option-letter">${LETTERS[i]}</span><span>${opt}</span>`;
        btn.addEventListener('click', () => onOptionClick(i));
        optionsGrid.appendChild(btn);
      });
    }

    updateProgress(idx);
    startTime = Date.now();
    if (isTimed) startTimer();

    // Animate question card
    const card = $('question-card');
    if (card) {
      card.style.animation = 'none';
      card.offsetHeight; // reflow
      card.style.animation = 'slideIn 0.3s ease';
    }
  }

  function onOptionClick(idx) {
    if (selectedIdx !== null) return; // already answered
    selectedIdx = idx;
    stopTimer();

    const isScored = QUIZ.type === 'scored';

    // For scored quizzes show correct/wrong immediately
    if (isScored) {
      const correctIdx = questions[currentIdx].answer;
      Array.from(optionsGrid.children).forEach((btn, i) => {
        btn.disabled = true;
        if (i === correctIdx) btn.classList.add('correct');
        if (i === idx && idx !== correctIdx) btn.classList.add('wrong');
        if (i === idx) btn.classList.add('selected');
      });
    } else {
      // Personality quiz – just highlight selected
      Array.from(optionsGrid.children).forEach((btn, i) => {
        btn.disabled = true;
        if (i === idx) btn.classList.add('selected');
      });
    }

    answers.push(idx);
    if (btnNext) btnNext.disabled = false;

    // Auto-advance after short delay for better UX
    setTimeout(goNext, 600);
  }

  function lockOptions(correctIdx) {
    if (!optionsGrid) return;
    Array.from(optionsGrid.children).forEach((btn, i) => {
      btn.disabled = true;
      if (i === correctIdx && QUIZ.type === 'scored') btn.classList.add('correct');
    });
  }

  // ── Navigation ────────────────────────────────────────────
  function goNext() {
    stopTimer();
    currentIdx++;
    if (currentIdx < total) {
      renderQuestion(currentIdx);
    } else {
      submitResults();
    }
  }

  // ── Submit ────────────────────────────────────────────────
  function submitResults() {
    showScreen('screen-loading');
    const timeTaken = quizStartTime ? Math.round((Date.now() - quizStartTime) / 1000) : 0;
    const nickname  = nicknameInput ? (nicknameInput.value.trim() || 'Anonymous') : 'Anonymous';

    const payload = {
      quiz_id:    QUIZ.id,
      answers:    answers,
      time_taken: timeTaken,
      nickname:   nickname,
    };

    fetch('/api/submit', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    })
      .then(r => r.json())
      .then(result => {
        // Small delay for UX drama
        setTimeout(() => {
          renderResults(result);
          showScreen('screen-results');
          // Update nav
          if (navProgress) navProgress.textContent = '✓ Done';
        }, 800);
      })
      .catch(() => {
        // Offline fallback: calculate locally
        const localResult = calcLocal();
        renderResults(localResult);
        showScreen('screen-results');
      });
  }

  // ── Local fallback calculation (no network needed) ────────
  function calcLocal() {
    if (QUIZ.type === 'personality') {
      const totals = { A: 0, B: 0, C: 0, D: 0 };
      const keys   = ['A', 'B', 'C', 'D'];
      answers.forEach((ans, i) => {
        if (i < questions.length && ans >= 0) {
          const scoreMap = questions[i].scores[ans];
          Object.entries(scoreMap).forEach(([k, v]) => { totals[k] += v; });
        }
      });
      const dominant  = Object.keys(totals).reduce((a, b) => totals[a] > totals[b] ? a : b);
      const resultInfo = QUIZ.results[dominant];
      return { type: 'personality', label: resultInfo.label, desc: resultInfo.desc, emoji: resultInfo.emoji, totals };
    } else {
      let score = 0;
      const correctAnswers = [];
      answers.forEach((ans, i) => {
        const correct = questions[i].answer;
        correctAnswers.push(correct);
        if (ans === correct) score++;
      });
      const pct   = Math.round((score / total) * 100);
      let label = '', desc = '';
      for (const tier of QUIZ.scoring) {
        if (score >= tier.min) { label = tier.label; desc = tier.desc; break; }
      }
      return { type: 'scored', score, total, pct, label, desc, correct_answers: correctAnswers };
    }
  }

  // ── Render Results ────────────────────────────────────────
  function renderResults(result) {
    if (!resultsCard) return;
    let html = '';

    if (result.type === 'personality') {
      html += `<div class="result-emoji">${result.emoji || '🔮'}</div>`;
      html += `<h2 class="result-label">${result.label}</h2>`;
      html += `<p class="result-desc">${result.desc}</p>`;

      // Personality bars
      const barColors = { A: '#6c63ff', B: '#f59e0b', C: '#10b981', D: '#f64f59' };
      const barLabels = { A: '📊 Analytical Thinker', B: '⚡ Action Taker', C: '🤝 Social Connector', D: '🎨 Creative Visionary' };
      const maxVal = Math.max(...Object.values(result.totals), 1);
      html += '<div class="personality-bars">';
      Object.keys(result.totals).forEach(k => {
        const pct = Math.round((result.totals[k] / maxVal) * 100);
        html += `
          <div class="pbar-row">
            <div class="pbar-label">${barLabels[k]}</div>
            <div class="pbar-track">
              <div class="pbar-fill" style="width:0%;background:${barColors[k]}" data-pct="${pct}"></div>
            </div>
          </div>`;
      });
      html += '</div>';
    } else {
      // Scored quiz
      const pct = result.pct || 0;
      const circumference = 2 * Math.PI * 50;
      const offset = circumference * (1 - pct / 100);
      html += `
        <div class="score-ring-wrap">
          <div class="score-ring">
            <svg viewBox="0 0 120 120">
              <circle class="score-bg" cx="60" cy="60" r="50"/>
              <circle class="score-fill" cx="60" cy="60" r="50"
                      stroke="${QUIZ.color}"
                      stroke-dasharray="${circumference}"
                      stroke-dashoffset="${circumference}"
                      id="score-arc"/>
            </svg>
            <div class="score-text">
              <span class="score-num">${result.score}</span>
              <span class="score-denom">/ ${result.total}</span>
            </div>
          </div>
        </div>`;
      html += `<h2 class="result-label">${result.label}</h2>`;
      html += `<p class="result-desc">${result.desc} <strong>${pct}% correct.</strong></p>`;

      // Review answers
      if (result.correct_answers && result.correct_answers.length > 0) {
        html += `<div class="review-list">`;
        questions.forEach((q, i) => {
          const correct = result.correct_answers[i];
          const given   = answers[i];
          const isOk    = given === correct;
          html += `
            <div class="review-item ${isOk ? 'correct-item' : 'wrong-item'}">
              <strong>${isOk ? '✓' : '✗'} Q${i + 1}: ${q.q}</strong>
              ${isOk ? '' : `Your answer: ${given >= 0 ? q.options[given] : 'No answer'} · `}
              Correct: ${q.options[correct]}
            </div>`;
        });
        html += `</div>`;
      }
    }

    // Leaderboard placeholder (filled async)
    html += `<div id="lb-container"></div>`;

    // Share / Restart buttons
    html += buildActions(result);

    resultsCard.innerHTML = html;

    // Animate score arc
    requestAnimationFrame(() => {
      const arc = document.getElementById('score-arc');
      if (arc) {
        const circumference = 2 * Math.PI * 50;
        arc.style.transition = 'stroke-dashoffset 1s ease';
        arc.style.strokeDashoffset = circumference * (1 - (result.pct || 0) / 100);
      }
      // Animate personality bars
      document.querySelectorAll('.pbar-fill').forEach(el => {
        setTimeout(() => { el.style.width = el.dataset.pct + '%'; }, 100);
      });
    });

    // Load leaderboard
    if (result.type !== 'personality') {
      loadLeaderboard(result.leaderboard_id);
    }
  }

  function buildActions(result) {
    const shareText = buildShareText(result);
    const encoded   = encodeURIComponent(shareText);
    const twitterUrl = `https://twitter.com/intent/tweet?text=${encoded}`;

    return `
      <div class="result-actions">
        <button class="btn-share twitter" onclick="window.open('${twitterUrl}', '_blank')">
          🐦 Share on X
        </button>
        <button class="btn-share copy" id="btn-copy">📋 Copy Result</button>
      </div>
      <button class="btn-restart" id="btn-restart">🔄 Try Again</button>
      <a class="btn-home" href="/">← Back to All Quizzes</a>
    `;
  }

  function buildShareText(result) {
    if (result.type === 'personality') {
      return `I just took the "${QUIZ.title}" quiz and I'm: ${result.label} ${result.emoji || ''} Try it yourself! #QuizSimple`;
    }
    return `I scored ${result.score}/${result.total} (${result.pct}%) on the "${QUIZ.title}" quiz! ${result.label} — Can you beat me? #QuizSimple`;
  }

  function loadLeaderboard(highlightId) {
    fetch(`/api/leaderboard?quiz_id=${QUIZ.id}`)
      .then(r => r.json())
      .then(board => {
        if (!board.length) return;
        const container = document.getElementById('lb-container');
        if (!container) return;
        let rows = '';
        board.forEach((entry, i) => {
          const isMe = entry.id === highlightId;
          const medals = ['🥇', '🥈', '🥉'];
          const rank = medals[i] || (i + 1);
          rows += `
            <tr class="${isMe ? 'lb-highlight' : ''}">
              <td class="lb-rank">${rank}</td>
              <td>${escapeHtml(entry.nickname)}</td>
              <td>${entry.score}/${entry.total}</td>
              <td>${entry.pct}%</td>
            </tr>`;
        });
        container.innerHTML = `
          <div class="leaderboard">
            <h3>🏆 Top Scores</h3>
            <table class="lb-table">
              <thead><tr><th>#</th><th>Player</th><th>Score</th><th>Accuracy</th></tr></thead>
              <tbody>${rows}</tbody>
            </table>
          </div>`;
      })
      .catch(() => {}); // fail silently
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // ── Event delegation for dynamic buttons ─────────────────
  document.addEventListener('click', function (e) {
    if (e.target && e.target.id === 'btn-restart') {
      resetQuiz();
    }
    if (e.target && e.target.id === 'btn-copy') {
      const result = calcLocal();
      const text = buildShareText(result);
      navigator.clipboard && navigator.clipboard.writeText(text)
        .then(() => { e.target.textContent = '✓ Copied!'; setTimeout(() => { e.target.textContent = '📋 Copy Result'; }, 2000); })
        .catch(() => { e.target.textContent = '✗ Failed'; });
    }
    if (e.target && e.target.id === 'btn-next') {
      goNext();
    }
  });

  // ── Reset ─────────────────────────────────────────────────
  function resetQuiz() {
    currentIdx  = 0;
    answers     = [];
    selectedIdx = null;
    stopTimer();
    showScreen('screen-start');
    if (navProgress) navProgress.textContent = `1 / ${total}`;
  }

  // ── Init ──────────────────────────────────────────────────
  if (btnStart) {
    btnStart.addEventListener('click', () => {
      quizStartTime = Date.now();
      showScreen('screen-quiz');
      renderQuestion(0);
    });
  }

  // Pre-fill timer display
  if (timerNum && isTimed) {
    timerNum.textContent = timeLimit;
    if (timerStroke) {
      timerStroke.style.strokeDasharray  = CIRCUMFERENCE;
      timerStroke.style.strokeDashoffset = 0;
    }
  }
})();
