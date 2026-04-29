from flask import Blueprint, abort, render_template, request

from app.services.auth_service import get_current_user, require_auth
from app.services.quiz_service import get_all_quizzes, get_leaderboard, get_quiz

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    quizzes = get_all_quizzes()
    return render_template("index.html", quizzes=quizzes)


@main_bp.route("/quiz/<quiz_id>")
def quiz_page(quiz_id: str):
    quiz = get_quiz(quiz_id)
    if not quiz:
        abort(404)
    return render_template("quiz.html", quiz=quiz)


@main_bp.route("/admin")
@require_auth
def admin_panel():
    quiz_id = request.args.get("quiz_id")
    rows = get_leaderboard(quiz_id)
    quizzes = get_all_quizzes()
    return render_template(
        "admin_dashboard.html",
        rows=rows,
        quizzes=quizzes,
        selected_quiz=quiz_id or "",
        user=get_current_user(),
    )
