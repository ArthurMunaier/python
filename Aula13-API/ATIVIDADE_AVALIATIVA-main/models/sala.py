from extensions import db


class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False, unique=True)
    capacidade = db.Column(db.Integer, nullable=False)

    sessoes = db.relationship(
        "Sessao",
        backref="sala",
        lazy=True
    )