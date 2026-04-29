"""QuizSimple – Flask Quiz Web App MVP"""

import uuid
from datetime import datetime, timezone
import os
from flask import Flask, render_template, jsonify, request, session

app = Flask(__name__)
app.secret_key = "quizsimple-secret-2024"

# ---------------------------------------------------------------------------
# Quiz Data
# ---------------------------------------------------------------------------

QUIZZES = {
    "trivia": {
        "id": "trivia",
        "title": "Ultimate Tech IQ Test",
        "subtitle": "How much do you really know about tech?",
        "icon": "🧠",
        "type": "scored",
        "timed": False,
        "color": "#6c63ff",
        "questions": [
            {
                "q": "What does 'HTTP' stand for?",
                "options": [
                    "HyperText Transfer Protocol",
                    "High-Tech Transfer Process",
                    "HyperText Transmission Path",
                    "High Transfer Technology Protocol",
                ],
                "answer": 0,
            },
            {
                "q": "Which company created the Python programming language?",
                "options": ["Google", "Microsoft", "Guido van Rossum (independent)", "Apple"],
                "answer": 2,
            },
            {
                "q": "What does 'RAM' stand for?",
                "options": [
                    "Random Access Memory",
                    "Rapid Application Management",
                    "Read And Modify",
                    "Remote Access Mode",
                ],
                "answer": 0,
            },
            {
                "q": "Which social network was created by Mark Zuckerberg?",
                "options": ["Twitter", "LinkedIn", "Facebook", "Snapchat"],
                "answer": 2,
            },
            {
                "q": "What year was the first iPhone released?",
                "options": ["2005", "2006", "2007", "2008"],
                "answer": 2,
            },
            {
                "q": "What does 'AI' stand for in technology?",
                "options": [
                    "Advanced Interface",
                    "Artificial Intelligence",
                    "Automated Input",
                    "Analytical Integration",
                ],
                "answer": 1,
            },
            {
                "q": "Which programming language is known as the language of the web?",
                "options": ["Python", "Java", "C++", "JavaScript"],
                "answer": 3,
            },
            {
                "q": "What does 'URL' stand for?",
                "options": [
                    "Universal Resource Locator",
                    "Uniform Resource Locator",
                    "Universal Record Link",
                    "Unified Resource Language",
                ],
                "answer": 1,
            },
            {
                "q": "Which company makes the Android operating system?",
                "options": ["Apple", "Samsung", "Google", "Microsoft"],
                "answer": 2,
            },
            {
                "q": "What is the binary representation of the number 10?",
                "options": ["1010", "1100", "1001", "0110"],
                "answer": 0,
            },
            {
                "q": "What does 'CPU' stand for?",
                "options": [
                    "Central Processing Unit",
                    "Computer Performance Unit",
                    "Core Processing Utility",
                    "Central Program Utility",
                ],
                "answer": 0,
            },
            {
                "q": "Which of these is NOT a programming language?",
                "options": ["Swift", "Kotlin", "Photon", "Rust"],
                "answer": 2,
            },
            {
                "q": "What does 'SSD' stand for?",
                "options": [
                    "Super Speed Drive",
                    "Solid State Drive",
                    "System Storage Device",
                    "Secure Solid Disk",
                ],
                "answer": 1,
            },
            {
                "q": "Which company developed the Windows operating system?",
                "options": ["Apple", "IBM", "Microsoft", "Google"],
                "answer": 2,
            },
            {
                "q": "What is the most popular version control system used by developers?",
                "options": ["SVN", "Mercurial", "Git", "CVS"],
                "answer": 2,
            },
        ],
        "scoring": [
            {"min": 13, "label": "Tech Genius 🏆", "desc": "You're basically a walking encyclopedia of tech!"},
            {"min": 10, "label": "Tech Wizard 🧙", "desc": "Impressive! You clearly live and breathe technology."},
            {"min": 7, "label": "Tech Savvy 💡", "desc": "Solid knowledge — you know your stuff pretty well."},
            {"min": 4, "label": "Tech Curious 🔍", "desc": "You know the basics. Keep exploring!"},
            {"min": 0, "label": "Tech Newbie 🌱", "desc": "Everyone starts somewhere. The tech world awaits you!"},
        ],
    },
    "personality": {
        "id": "personality",
        "title": "What Kind of Thinker Are You?",
        "subtitle": "Discover your unique thinking style in 10 questions",
        "icon": "🔮",
        "type": "personality",
        "timed": False,
        "color": "#f64f59",
        "questions": [
            {
                "q": "When you face a new problem, what's your first instinct?",
                "options": [
                    "Analyze all the data before deciding",
                    "Trust your gut and act fast",
                    "Ask others for their opinions",
                    "Look for a creative workaround",
                ],
                "scores": [
                    {"A": 2, "B": 0, "C": 1, "D": 3},
                    {"A": 0, "B": 2, "C": 0, "D": 0},
                    {"A": 0, "B": 0, "C": 2, "D": 0},
                    {"A": 0, "B": 0, "C": 0, "D": 2},
                ],
            },
            {
                "q": "Your ideal work environment is:",
                "options": [
                    "A quiet office with clear processes",
                    "A fast-paced startup where things change daily",
                    "A collaborative open space full of people",
                    "A creative studio with freedom to experiment",
                ],
                "scores": [
                    {"A": 2, "B": 0, "C": 0, "D": 0},
                    {"A": 0, "B": 2, "C": 0, "D": 0},
                    {"A": 0, "B": 0, "C": 2, "D": 0},
                    {"A": 0, "B": 0, "C": 0, "D": 2},
                ],
            },
            {
                "q": "How do you make important decisions?",
                "options": [
                    "Spreadsheets, pros & cons lists, research",
                    "Quickly — hesitation is the enemy",
                    "After talking it through with trusted people",
                    "By imagining the wildest possibilities first",
                ],
                "scores": [
                    {"A": 2, "B": 0, "C": 0, "D": 0},
                    {"A": 0, "B": 2, "C": 0, "D": 0},
                    {"A": 0, "B": 0, "C": 2, "D": 0},
                    {"A": 0, "B": 0, "C": 0, "D": 2},
                ],
            },
            {
                "q": "When learning something new, you prefer:",
                "options": [
                    "Reading documentation and structured courses",
                    "Jumping in and learning by doing",
                    "Group workshops or study groups",
                    "Experimenting freely without a set plan",
                ],
                "scores": [
                    {"A": 2, "B": 0, "C": 0, "D": 0},
                    {"A": 0, "B": 2, "C": 0, "D": 0},
                    {"A": 0, "B": 0, "C": 2, "D": 0},
                    {"A": 0, "B": 0, "C": 0, "D": 2},
                ],
            },
            {
                "q": "Your friends would describe you as:",
                "options": [
                    "The logical, reliable one",
                    "The decisive, action-oriented one",
                    "The empathetic, social connector",
                    "The imaginative, ideas person",
                ],
                "scores": [
                    {"A": 2, "B": 0, "C": 0, "D": 0},
                    {"A": 0, "B": 2, "C": 0, "D": 0},
                    {"A": 0, "B": 0, "C": 2, "D": 0},
                    {"A": 0, "B": 0, "C": 0, "D": 2},
                ],
            },
            {
                "q": "On a weekend, you'd rather:",
                "options": [
                    "Solve a puzzle or read a non-fiction book",
                    "Try a new sport or activity you've never done",
                    "Host a dinner party or catch up with friends",
                    "Paint, write, make music, or build something",
                ],
                "scores": [
                    {"A": 2, "B": 0, "C": 0, "D": 0},
                    {"A": 0, "B": 2, "C": 0, "D": 0},
                    {"A": 0, "B": 0, "C": 2, "D": 0},
                    {"A": 0, "B": 0, "C": 0, "D": 2},
                ],
            },
            {
                "q": "Your biggest strength is:",
                "options": [
                    "Attention to detail and accuracy",
                    "Getting things done, fast",
                    "Making everyone feel included",
                    "Thinking outside the box",
                ],
                "scores": [
                    {"A": 2, "B": 0, "C": 0, "D": 0},
                    {"A": 0, "B": 2, "C": 0, "D": 0},
                    {"A": 0, "B": 0, "C": 2, "D": 0},
                    {"A": 0, "B": 0, "C": 0, "D": 2},
                ],
            },
            {
                "q": "When someone disagrees with you, you:",
                "options": [
                    "Present data and logical arguments",
                    "Stand firm — you know what you know",
                    "Try to understand their point of view first",
                    "Suggest a completely different approach",
                ],
                "scores": [
                    {"A": 2, "B": 0, "C": 0, "D": 0},
                    {"A": 0, "B": 2, "C": 0, "D": 0},
                    {"A": 0, "B": 0, "C": 2, "D": 0},
                    {"A": 0, "B": 0, "C": 0, "D": 2},
                ],
            },
            {
                "q": "The superpower you'd want most:",
                "options": [
                    "Perfect memory and instant knowledge",
                    "Super speed and reflexes",
                    "Mind reading and emotional connection",
                    "Reality manipulation and infinite creativity",
                ],
                "scores": [
                    {"A": 2, "B": 0, "C": 0, "D": 0},
                    {"A": 0, "B": 2, "C": 0, "D": 0},
                    {"A": 0, "B": 0, "C": 2, "D": 0},
                    {"A": 0, "B": 0, "C": 0, "D": 2},
                ],
            },
            {
                "q": "Your motto is closest to:",
                "options": [
                    '"Measure twice, cut once."',
                    '"Done is better than perfect."',
                    '"People first, always."',
                    '"Why not? Let\'s try it."',
                ],
                "scores": [
                    {"A": 2, "B": 0, "C": 0, "D": 0},
                    {"A": 0, "B": 2, "C": 0, "D": 0},
                    {"A": 0, "B": 0, "C": 2, "D": 0},
                    {"A": 0, "B": 0, "C": 0, "D": 2},
                ],
            },
        ],
        "results": {
            "A": {
                "label": "The Analytical Thinker 📊",
                "desc": "You're methodical, precise, and data-driven. You excel at breaking complex problems into logical steps and making decisions backed by evidence. Careers like engineering, science, finance, or software development suit you perfectly.",
                "emoji": "📊",
            },
            "B": {
                "label": "The Action Taker ⚡",
                "desc": "You're decisive, bold, and action-oriented. You thrive under pressure and prefer to learn by doing. Entrepreneurship, leadership, sports, and sales are your natural domains. You ship things fast.",
                "emoji": "⚡",
            },
            "C": {
                "label": "The Social Connector 🤝",
                "desc": "You're empathetic, collaborative, and people-focused. You make everyone feel heard and build strong relationships naturally. You'd thrive in HR, teaching, counseling, community management, or team leadership.",
                "emoji": "🤝",
            },
            "D": {
                "label": "The Creative Visionary 🎨",
                "desc": "You're imaginative, original, and always thinking outside the box. You see possibilities where others see walls. Design, art, writing, innovation, and entrepreneurship are your playgrounds.",
                "emoji": "🎨",
            },
        },
    },
    "speed": {
        "id": "speed",
        "title": "Speed Round: General Knowledge",
        "subtitle": "15 seconds per question — think fast!",
        "icon": "⚡",
        "type": "scored",
        "timed": True,
        "time_per_question": 15,
        "color": "#11998e",
        "questions": [
            {
                "q": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "answer": 2,
            },
            {
                "q": "How many continents are there on Earth?",
                "options": ["5", "6", "7", "8"],
                "answer": 2,
            },
            {
                "q": "What is 12 × 12?",
                "options": ["132", "144", "122", "148"],
                "answer": 1,
            },
            {
                "q": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Jupiter", "Saturn", "Mars"],
                "answer": 3,
            },
            {
                "q": "Who wrote 'Romeo and Juliet'?",
                "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                "answer": 1,
            },
            {
                "q": "What is the chemical symbol for gold?",
                "options": ["Go", "Gd", "Au", "Ag"],
                "answer": 2,
            },
            {
                "q": "How many sides does a hexagon have?",
                "options": ["5", "6", "7", "8"],
                "answer": 1,
            },
            {
                "q": "Which ocean is the largest?",
                "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
                "answer": 3,
            },
            {
                "q": "What year did World War II end?",
                "options": ["1943", "1944", "1945", "1946"],
                "answer": 2,
            },
            {
                "q": "What is the fastest land animal?",
                "options": ["Lion", "Horse", "Cheetah", "Leopard"],
                "answer": 2,
            },
        ],
        "scoring": [
            {"min": 9, "label": "Speed Champion 🥇", "desc": "Lightning fast AND accurate! Your brain works at superhuman speed."},
            {"min": 7, "label": "Quick Thinker ⚡", "desc": "Great performance under pressure. You rarely freeze up!"},
            {"min": 5, "label": "Steady Pacer 🏃", "desc": "Solid score! A bit more practice and you'll be unbeatable."},
            {"min": 3, "label": "Warming Up 🔥", "desc": "The clock is tough! Keep practicing your general knowledge."},
            {"min": 0, "label": "Just Starting 🌱", "desc": "Speed rounds are tricky. Try again — you'll improve fast!"},
        ],
    },
}


# ---------------------------------------------------------------------------
# In-memory score store (simple list, resets on restart — good enough for MVP)
# ---------------------------------------------------------------------------
leaderboard: list = []


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/")
def index():
    quizzes = [
        {
            "id": q["id"],
            "title": q["title"],
            "subtitle": q["subtitle"],
            "icon": q["icon"],
            "color": q["color"],
            "type": q["type"],
            "question_count": len(q["questions"]),
            "timed": q["timed"],
        }
        for q in QUIZZES.values()
    ]
    return render_template("index.html", quizzes=quizzes)


@app.route("/quiz/<quiz_id>")
def quiz(quiz_id):
    if quiz_id not in QUIZZES:
        return render_template("index.html", error="Quiz not found"), 404
    quiz_data = QUIZZES[quiz_id]
    return render_template("quiz.html", quiz=quiz_data)


@app.route("/api/quiz/<quiz_id>")
def api_quiz(quiz_id):
    if quiz_id not in QUIZZES:
        return jsonify({"error": "Quiz not found"}), 404
    return jsonify(QUIZZES[quiz_id])


@app.route("/api/submit", methods=["POST"])
def api_submit():
    data = request.get_json()
    quiz_id = data.get("quiz_id")
    answers = data.get("answers", [])
    time_taken = data.get("time_taken", 0)
    nickname = data.get("nickname", "Anonymous")[:30]

    if quiz_id not in QUIZZES:
        return jsonify({"error": "Invalid quiz"}), 400

    quiz_data = QUIZZES[quiz_id]
    questions = quiz_data["questions"]
    quiz_type = quiz_data["type"]

    if quiz_type == "personality":
        # Tally personality scores
        totals = {"A": 0, "B": 0, "C": 0, "D": 0}
        keys = ["A", "B", "C", "D"]
        for i, answer_idx in enumerate(answers):
            if i < len(questions) and 0 <= answer_idx < len(questions[i]["options"]):
                score_map = questions[i]["scores"][answer_idx]
                for k, v in score_map.items():
                    totals[k] += v
        dominant = max(totals, key=lambda k: totals[k])
        result_info = quiz_data["results"][dominant]
        result = {
            "type": "personality",
            "label": result_info["label"],
            "desc": result_info["desc"],
            "emoji": result_info["emoji"],
            "totals": totals,
        }
    else:
        # Scored quiz
        score = 0
        total = len(questions)
        correct_answers = []
        for i, answer_idx in enumerate(answers):
            if i < len(questions):
                correct = questions[i]["answer"]
                correct_answers.append(correct)
                if answer_idx == correct:
                    score += 1
            else:
                correct_answers.append(None)
        pct = round((score / total) * 100) if total else 0
        # Find scoring tier
        label = ""
        desc = ""
        for tier in quiz_data["scoring"]:
            if score >= tier["min"]:
                label = tier["label"]
                desc = tier["desc"]
                break
        result = {
            "type": "scored",
            "score": score,
            "total": total,
            "pct": pct,
            "label": label,
            "desc": desc,
            "correct_answers": correct_answers,
        }

    # Save to leaderboard (scored quizzes only)
    if quiz_type != "personality":
        entry = {
            "id": str(uuid.uuid4())[:8],
            "quiz_id": quiz_id,
            "quiz_title": quiz_data["title"],
            "nickname": nickname,
            "score": result.get("score", 0),
            "total": result.get("total", 1),
            "pct": result.get("pct", 0),
            "time_taken": time_taken,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        leaderboard.insert(0, entry)
        if len(leaderboard) > 100:
            leaderboard.pop()
        result["leaderboard_id"] = entry["id"]

    return jsonify(result)


@app.route("/api/leaderboard")
def api_leaderboard():
    quiz_id = request.args.get("quiz_id")
    board = leaderboard
    if quiz_id:
        board = [e for e in board if e["quiz_id"] == quiz_id]
    sorted_board = sorted(board, key=lambda x: (-x["pct"], x["time_taken"]))
    return jsonify(sorted_board[:10])


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n🚀 QuizSimple is running!")
    print("   Open http://localhost:5000 in your browser\n")
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, port=5000)
