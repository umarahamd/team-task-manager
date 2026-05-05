from flask import Blueprint, request, jsonify
from models import db, Project, ProjectMember
from flask_jwt_extended import jwt_required, get_jwt_identity

project_bp = Blueprint("project", __name__)

@project_bp.route("/projects", methods=["POST"])
@jwt_required()
def create_project():
    user_id = get_jwt_identity()
    data = request.json

    project = Project(name=data["name"], created_by=user_id)
    db.session.add(project)
    db.session.commit()

    member = ProjectMember(user_id=user_id, project_id=project.id, role="Admin")
    db.session.add(member)
    db.session.commit()

    return {"msg": "Project created"}

@project_bp.route("/projects", methods=["GET"])
@jwt_required()
def get_projects():
    projects = Project.query.all()
    return jsonify([{"id": p.id, "name": p.name} for p in projects])