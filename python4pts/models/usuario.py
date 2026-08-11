from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .base import ModeloBase

class Usuario(ModeloBase):
    __tablename__ = "usuarios"

    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha_hash = db.Column(db.String(255), nullable=False)

    tarefas = db.relationship(
        "Tarefa", back_populates="usuario", lazy=True, cascade="all, delete-orphan"
    )

    @classmethod
    def criar(cls, nome, email, senha):
        usuario = cls(
            nome=nome,
            email=email,
            senha_hash=generate_password_hash(senha),
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @classmethod
    def buscar_por_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<Usuario {self.id} {self.nome}>"
