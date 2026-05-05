from flask import Blueprint, request, jsonify
from models import db, User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()


# =========================
# 🔐 SIGNUP
# =========================
@auth_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()

        # ✅ Validate input
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"msg": "All fields are required"}), 400

        # ✅ Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"msg": "Email already exists"}), 400

        # ✅ Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # ✅ Create user
        user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "User created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# 🔑 LOGIN
# =========================
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        # ✅ Validate input
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"msg": "Email and password required"}), 400

        # ✅ Find user
        user = User.query.filter_by(email=email).first()

        # ❌ Invalid user
        if not user:
            return jsonify({"msg": "User not found"}), 404

        # ❌ Wrong password
        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({"msg": "Invalid credentials"}), 401

        # ✅ FIX: identity must be string
        token = create_access_token(identity=str(user.id))

        return jsonify({
            "msg": "Login successful",
            "token": token,
            "user_id": user.id
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500