from flask import Blueprint, render_template, abort
from app.services.quiz_service import get_all_quizzes, get_quiz

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
