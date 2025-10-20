from app import db

class Publicacao(db.Model):
    __tablename__ = 'publicacao'

    id_publicacao = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(20), nullable=False)
    data_publicacao = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    id_tatuador = db.Column(db.Integer, db.ForeignKey('tatuador.id_tatuador'), nullable=False)

    tatuador = db.relationship('Tatuador', backref=db.backref('publicacoes', lazy=True))
