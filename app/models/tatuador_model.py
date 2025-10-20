from app import db

class Tatuador(db.Model):
    __tablename__ = 'tatuador'

    id_tatuador = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=True)
    nome = db.Column(db.String(20), nullable=False)
    cidade = db.Column(db.String(20), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('tatuador', lazy=True))
