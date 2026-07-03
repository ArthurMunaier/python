from extensions import db


class Filme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    duracao = db.Column(db.Integer, nullable=False)

    sessoes = db.relationship(
        "Sessao",
        backref="filme",
        lazy=True
    )