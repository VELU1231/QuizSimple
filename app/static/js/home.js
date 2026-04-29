/* home.js — Renders quiz cards from window.ALL_QUIZZES */
'use strict';

(function () {
  const DIFF_CLASS = { easy: 'diff-easy', medium: 'diff-medium', hard: 'diff-hard' };

  function buildCard(quiz) {
    const a = document.createElement('a');
    a.href = `/quiz/${quiz.id}`;
    a.className = 'quiz-card';
    a.setAttribute('aria-label', `Start ${quiz.title} quiz`);

    const diffKey = (quiz.difficulty || '').toLowerCase();
    const diffClass = DIFF_CLASS[diffKey] || '';

    a.innerHTML = `
      <span class="card-icon">${escHtml(quiz.icon || '?')}</span>
      <div class="card-content">
        <span class="card-category">${escHtml(quiz.category)}</span>
        <h3 class="card-title">${escHtml(quiz.title)}</h3>
        <p class="card-desc">${escHtml(quiz.description)}</p>
        <div class="card-meta">
          <span class="meta-badge">${quiz.question_count} Questions</span>
          <span class="meta-badge ${diffClass}">${escHtml(quiz.difficulty)}</span>
          <span class="meta-badge">${quiz.max_score} pts</span>
        </div>
      </div>
      <span class="card-arrow" aria-hidden="true">&rarr;</span>
    `;
    return a;
  }

  function escHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function init() {
    const grid = document.getElementById('quiz-grid');
    if (!grid) return;

    const quizzes = window.ALL_QUIZZES || [];
    if (quizzes.length === 0) {
      grid.innerHTML = '<p style="color:var(--text-muted);text-align:center;">No quizzes available yet.</p>';
      return;
    }

    grid.innerHTML = ''; // clear noscript fallback
    quizzes.forEach((quiz) => grid.appendChild(buildCard(quiz)));
  }

  document.addEventListener('DOMContentLoaded', init);
})();
