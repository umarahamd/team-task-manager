from models import ProjectMember

def is_admin(user_id, project_id):
    member = ProjectMember.query.filter_by(
        user_id=user_id,
        project_id=project_id,
        role="Admin"
    ).first()
    return member is not None