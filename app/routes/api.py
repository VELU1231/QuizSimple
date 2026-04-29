from flask import Blueprint, jsonify, request
from app.services.auth_service import require_auth
from app.services.quiz_service import (
    calculate_score,
    clear_leaderboard,
    get_all_quizzes,
    get_leaderboard,
    get_quiz,
    save_score,
)
from app.services.supabase_service import supabase_enabled

api_bp = Blueprint("api", __name__)


@api_bp.route("/quizzes")
def list_quizzes():
    return jsonify(get_all_quizzes())


@api_bp.route("/quiz/<quiz_id>")
def get_quiz_api(quiz_id: str):
    quiz = get_quiz(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404
    return jsonify(quiz)


@api_bp.route("/submit", methods=["POST"])
def submit():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    quiz_id = data.get("quiz_id", "").strip()
    answers = data.get("answers", {})
    name = (data.get("name", "") or "Anonymous").strip() or "Anonymous"

    if not quiz_id:
        return jsonify({"error": "quiz_id is required"}), 400

    quiz = get_quiz(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    result = calculate_score(quiz, answers)
    save_score(quiz_id, name, result["score"], result["max_score"])
    return jsonify(result)


@api_bp.route("/leaderboard")
def leaderboard():
    quiz_id = request.args.get("quiz_id")
    return jsonify(get_leaderboard(quiz_id))


@api_bp.route("/admin/leaderboard", methods=["GET"])
@require_auth
def admin_leaderboard():
    quiz_id = request.args.get("quiz_id")
    return jsonify(get_leaderboard(quiz_id))


@api_bp.route("/admin/leaderboard", methods=["DELETE"])
@require_auth
def admin_clear_leaderboard():
    payload = request.get_json(silent=True) or {}
    quiz_id = payload.get("quiz_id")
    deleted = clear_leaderboard(quiz_id)
    return jsonify({"deleted": deleted, "quiz_id": quiz_id})


@api_bp.route("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "storage": "supabase" if supabase_enabled() else "memory-fallback",
        }
    )
