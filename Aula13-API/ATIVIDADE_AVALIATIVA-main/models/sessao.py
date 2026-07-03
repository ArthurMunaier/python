from extensions import db


class Sessao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.String(20), nullable=False)

    filme_id = db.Column(
        db.Integer,
        db.ForeignKey("filme.id"),
        nullable=False
    )

    sala_id = db.Column(
        db.Integer,
        db.ForeignKey("sala.id"),
        nullable=False
    )