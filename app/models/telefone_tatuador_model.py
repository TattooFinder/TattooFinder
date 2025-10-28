from app import db

class TelefoneTatuador(db.Model):
    __tablename__ = 'telefone_tatuador'

    id_tatuador = db.Column(db.Integer, db.ForeignKey('tatuador.id_tatuador'), primary_key=True)
    numero = db.Column(db.String(20), nullable=False)

    tatuador = db.relationship('Tatuador', backref=db.backref('telefones', lazy=True))
