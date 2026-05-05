import os
from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes.auth_routes import auth_bp, bcrypt
from routes.project_routes import project_bp
from routes.task_routes import task_bp
from routes.dashboard_routes import dashboard_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# ✅ Load config
app.config.from_object(Config)

# ✅ Enable CORS (allow all origins)
CORS(app, resources={r"/*": {"origins": "*"}})

# ✅ Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# ✅ Register routes
app.register_blueprint(auth_bp)
app.register_blueprint(project_bp)
app.register_blueprint(task_bp)
app.register_blueprint(dashboard_bp)

# ✅ Create database
with app.app_context():
    db.create_all()

# ✅ Home route
@app.route("/")
def home():
    return "🚀 API Running Successfully"

# ✅ IMPORTANT: Railway requires dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)