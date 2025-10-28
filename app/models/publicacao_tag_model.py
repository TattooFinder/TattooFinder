from app import db

class PublicacaoTag(db.Model):
    __tablename__ = 'publicacao_tag'

    id_publicacao = db.Column(db.Integer, db.ForeignKey('publicacao.id_publicacao'), primary_key=True)
    id_tag = db.Column(db.Integer, db.ForeignKey('tag.id_tag'), primary_key=True)
    q_publicacao = db.Column(db.Integer, nullable=False)

    publicacao = db.relationship('Publicacao', backref=db.backref('tags', lazy=True))
    tag = db.relationship('Tag', backref=db.backref('publicacoes', lazy=True))
