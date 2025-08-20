from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import os
from app import db
from app.models.file import File
from flask_login import login_required

files_api = Blueprint('files_api', __name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@files_api.route('/files', methods=['GET'])
@login_required
def get_files():
    files_list = File.query.all()
    files = [
        {
            "id": f.id,
            "name": f.name,
            "uploadDate": f.upload_date.isoformat(),
            "size": f.size
        } for f in files_list
    ]
    return jsonify(files)

@files_api.route('/files', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum ficheiro foi enviado."}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nenhum ficheiro foi selecionado."}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    file_size_kb = round(os.path.getsize(filepath) / 1024, 2)
    file_size_str = f"{file_size_kb} KB"
    
    new_file = File(name=filename, size=file_size_str, path=filepath)
    db.session.add(new_file)
    db.session.commit()
    
    response_data = {
        "id": new_file.id,
        "name": new_file.name,
        "uploadDate": new_file.upload_date.isoformat(),
        "size": new_file.size
    }
    
    return jsonify({
        "message": "Ficheiro carregado com sucesso!", 
        "file": response_data
    }), 201