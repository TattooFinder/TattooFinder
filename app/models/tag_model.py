from app import db

class Tag(db.Model):
    __tablename__ = 'tag'

    id_tag = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    id_tatuador = db.Column(db.Integer, db.ForeignKey('tatuador.id_tatuador'), nullable=False)

    tatuador = db.relationship('Tatuador', backref=db.backref('tags', lazy=True))
