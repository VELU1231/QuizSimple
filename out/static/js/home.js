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
