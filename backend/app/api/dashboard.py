from flask import Blueprint, jsonify
from app import db
from app.models.client import Client
from app.models.note import Note
from app.models.task import Task
from flask_login import login_required

dashboard_api = Blueprint('dashboard_api', __name__)

@dashboard_api.route('/dashboard', methods=['GET'])
@login_required
def get_dashboard_data():
    total_clients = db.session.query(Client.id).count()
    total_notes = db.session.query(Note.id).count()
    recent_clients = Client.query.order_by(Client.id.desc()).limit(3).all()
    pending_tasks = Task.query.filter_by(status='Pendente').count()

    recent_activity = [
        {
            "id": client.id,
            "type": "new_client",
            "description": f"Novo cliente adicionado: {client.name}"
        } for client in recent_clients
    ]
    
    dashboard_data = {
        "totalClients": total_clients,
        "totalNotes": total_notes,
        "pendingTasks": pending_tasks,
        "activeProjects": 18, # Placeholder
        "recentActivity": recent_activity
    }

    return jsonify(dashboard_data)