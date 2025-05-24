from flask_sqlalchemy import SQLAlchemy
from cryptography.hazmat.primitives import serialization
import hashlib

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)  # SHA256 hex
    public_key = db.Column(db.Text, nullable=True)
    private_key = db.Column(db.Text, nullable=True)

    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def set_keys(self, private_pem, public_pem):
        self.private_key = private_pem
        self.public_key = public_pem

    def get_private_key(self):
        if self.private_key:
            return serialization.load_pem_private_key(self.private_key.encode(), password=None)
        return None

    def get_public_key(self):
        if self.public_key:
            return serialization.load_pem_public_key(self.public_key.encode())
        return None 