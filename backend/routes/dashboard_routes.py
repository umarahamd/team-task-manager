from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task
from datetime import datetime, date

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    try:
        user_id = get_jwt_identity()

        tasks = Task.query.filter_by(assigned_to=user_id).all()

        total = len(tasks)
        completed = len([t for t in tasks if t.status == "Completed"])
        pending = len([t for t in tasks if t.status == "Pending"])

        # ✅ FIXED overdue calculation
        overdue = 0
        for t in tasks:
            if t.due_date:
                try:
                    due = datetime.strptime(t.due_date, "%Y-%m-%d").date()
                    if due < date.today() and t.status != "Completed":
                        overdue += 1
                except:
                    pass  # ignore bad date format

        return jsonify({
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500