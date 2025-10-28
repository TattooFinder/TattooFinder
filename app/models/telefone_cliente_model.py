from app import db

class TelefoneCliente(db.Model):
    __tablename__ = 'telefone_cliente'

    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), primary_key=True)
    numero = db.Column(db.String(20), nullable=False)

    cliente = db.relationship('Cliente', backref=db.backref('telefones', lazy=True))
