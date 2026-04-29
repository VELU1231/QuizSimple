import json
from pathlib import Path

from app.services.supabase_service import fetch_top_scores, save_score_row, supabase_enabled

_DATA_FILE = Path(__file__).parent.parent / "data" / "quizzes.json"
_quizzes: list | None = None
_leaderboard: dict[str, list] = {}


def _load() -> list:
    global _quizzes
    if _quizzes is None:
        with open(_DATA_FILE, encoding="utf-8") as f:
            _quizzes = json.load(f)
    return _quizzes


def get_all_quizzes() -> list:
    """Return quiz summaries (no questions array) for the homepage grid."""
    return [
        {
            "id": q["id"],
            "title": q["title"],
            "description": q["description"],
            "category": q["category"],
            "icon": q["icon"],
            "difficulty": q["difficulty"],
            "question_count": len(q["questions"]),
            "max_score": sum(qu["points"] for qu in q["questions"]),
            "time_limit": q.get("time_limit", 0),
        }
        for q in _load()
    ]


def get_quiz(quiz_id: str) -> dict | None:
    for q in _load():
        if q["id"] == quiz_id:
            return q
    return None


def calculate_score(quiz: dict, answers: dict) -> dict:
    """
    answers: {str(qIdx): optionIdx}  — JSON object keys are always strings.
    Returns score breakdown + per-question review.
    """
    questions = quiz["questions"]
    max_score = sum(q["points"] for q in questions)
    score = 0
    results = []

    for i, q in enumerate(questions):
        user_answer = answers.get(str(i))
        correct = q["answer"]
        is_correct = user_answer == correct
        if is_correct:
            score += q["points"]
        results.append(
            {
                "question": q["question"],
                "options": q["options"],
                "correct_answer": correct,
                "user_answer": user_answer,
                "is_correct": is_correct,
                "points": q["points"],
            }
        )

    pct = (score / max_score * 100) if max_score else 0

    if pct >= 90:
        tier, tier_color = "Genius", "#fbbf24"
    elif pct >= 70:
        tier, tier_color = "Expert", "#06b6d4"
    elif pct >= 50:
        tier, tier_color = "Learner", "#8b5cf6"
    else:
        tier, tier_color = "Novice", "#f87171"

    return {
        "score": score,
        "max_score": max_score,
        "percentage": round(pct, 1),
        "tier": tier,
        "tier_color": tier_color,
        "results": results,
    }


def get_leaderboard(quiz_id: str | None = None) -> list:
    if supabase_enabled():
        rows = fetch_top_scores(quiz_id, limit=10)
        if rows:
            return [
                {
                    "name": r.get("name", "Anonymous"),
                    "score": r.get("score", 0),
                    "max_score": r.get("max_score", 0),
                    "quiz_id": r.get("quiz_id"),
                    "created_at": r.get("created_at"),
                }
                for r in rows
            ]

    if quiz_id:
        entries = _leaderboard.get(quiz_id, [])
        return sorted(entries, key=lambda x: x["score"], reverse=True)[:10]
    all_entries: list = []
    for entries in _leaderboard.values():
        all_entries.extend(entries)
    return sorted(all_entries, key=lambda x: x["score"], reverse=True)[:10]


def save_score(quiz_id: str, name: str, score: int, max_score: int) -> None:
    payload = {
        "quiz_id": quiz_id,
        "name": (name or "Anonymous")[:64],
        "score": int(score),
        "max_score": int(max_score),
    }

    if save_score_row(payload):
        return

    _leaderboard.setdefault(quiz_id, []).append(
        {"name": name, "score": score, "max_score": max_score}
    )
