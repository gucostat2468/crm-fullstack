from flask import Blueprint, jsonify, request
from app import db
from app.models.user import User
from flask_login import login_user, logout_user, login_required

auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Usuário e senha são obrigatórios."}), 400

    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"error": "Este nome de usuário já existe."}), 409
    
    user = User(username=data.get('username'), email=data.get('email'))
    user.set_password(data.get('password'))
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "Usuário criado com sucesso!"}), 201

@auth_api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Usuário e senha são obrigatórios."}), 400

    user = User.query.filter_by(username=data.get('username')).first()
    
    if user is None or not user.check_password(data.get('password')):
        return jsonify({"error": "Credenciais inválidas."}), 401
    
    login_user(user, remember=True)
    return jsonify({"message": "Login realizado com sucesso!"})

@auth_api.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"})