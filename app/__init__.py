from flask import Flask
from flask_socketio import SocketIO
from app.models.user import db
from app.routes.auth import auth
from app.routes.main import main

def create_app():
    app = Flask(__name__)
    app.secret_key = 'YourSecretKeyHere'  # Thay đổi secret key của bạn
    
    # Cấu hình
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    
    # Khởi tạo extensions
    db.init_app(app)
    socketio = SocketIO(app)
    
    # Đăng ký blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)
    
    # Tạo database
    with app.app_context():
        db.create_all()
    
    return app, socketio 