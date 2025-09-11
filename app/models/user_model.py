from app import db

class User(db.Model):
    __tablename__ = "usuário"

    id = db.Column(db.Integer, primary_key = true)
    nome = db.Column(db.String(100), nullable = false)
    email = db.Column(db.String(100), unique = true, nullable = false)
    senha = dbColumn(db.String(100), nullable = false)

    
