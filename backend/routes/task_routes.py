from flask import Blueprint, request, jsonify
from models import db, Task
from flask_jwt_extended import jwt_required, get_jwt_identity

task_bp = Blueprint("task", __name__)


# =========================
# 📌 CREATE TASK
# =========================
@task_bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    try:
        data = request.get_json()
        user_id = int(get_jwt_identity())

        # ✅ Validate input
        if not data.get("title") or not data.get("due_date"):
            return jsonify({"msg": "Title and due_date required"}), 400

        task = Task(
            title=data["title"],
            description=data.get("description", ""),
            status="Pending",
            due_date=data["due_date"],
            project_id=data.get("project_id", 1),
            assigned_to=user_id   # 🔥 assign to logged-in user
        )

        db.session.add(task)
        db.session.commit()

        return jsonify({"msg": "Task created"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# 📋 GET TASKS
# =========================
@task_bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    try:
        user_id = int(get_jwt_identity())

        # ✅ Only user's tasks
        tasks = Task.query.filter_by(assigned_to=user_id).all()

        return jsonify([
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "status": t.status,
                "due_date": t.due_date
            }
            for t in tasks
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# 🔄 UPDATE TASK
# =========================
@task_bp.route("/tasks/<int:id>", methods=["PUT"])
@jwt_required()
def update_task(id):
    try:
        user_id = int(get_jwt_identity())
        task = Task.query.get(id)

        if not task:
            return jsonify({"msg": "Task not found"}), 404

        # ✅ Security check
        if task.assigned_to != user_id:
            return jsonify({"msg": "Unauthorized"}), 403

        data = request.get_json()

        # Update fields safely
        task.status = data.get("status", task.status)
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.due_date = data.get("due_date", task.due_date)

        db.session.commit()

        return jsonify({"msg": "Task updated"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# ❌ DELETE TASK
# =========================
@task_bp.route("/tasks/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    try:
        user_id = int(get_jwt_identity())
        task = Task.query.get(id)

        if not task:
            return jsonify({"msg": "Task not found"}), 404

        # ✅ Security check
        if task.assigned_to != user_id:
            return jsonify({"msg": "Unauthorized"}), 403

        db.session.delete(task)
        db.session.commit()

        return jsonify({"msg": "Task deleted"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500