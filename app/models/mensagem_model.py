from app import db

class Mensagem(db.Model):
    __tablename__ = 'mensagem'

    id_mensagem = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(20), nullable=False)
    data_publicacao = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=False)

    cliente = db.relationship('Cliente', backref=db.backref('mensagens', lazy=True))
