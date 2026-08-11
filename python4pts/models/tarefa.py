from . import db
from .base import ModeloBase

STATUS_VALIDOS = ["pendente", "andamento", "concluida"]

STATUS_LABELS = {
    "pendente": "Pendente",
    "andamento": "Em andamento",
    "concluida": "Concluída",
}

STATUS_CORES = {
    "pendente": "warning",
    "andamento": "primary",
    "concluida": "success",
}

class Tarefa(ModeloBase):
    __tablename__ = "tarefas"

    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="pendente")
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    usuario = db.relationship("Usuario", back_populates="tarefas")

    @classmethod
    def listar_por_usuario(cls, usuario_id, status=None):
        query = cls.query.filter_by(usuario_id=usuario_id)
        if status and status in STATUS_VALIDOS:
            query = query.filter_by(status=status)
        return query.order_by(cls.data_criacao.desc()).all()

    @classmethod
    def contar_por_status(cls, usuario_id):
        contagem = {status: 0 for status in STATUS_VALIDOS}
        tarefas = cls.query.filter_by(usuario_id=usuario_id).all()
        for tarefa in tarefas:
            contagem[tarefa.status] = contagem.get(tarefa.status, 0) + 1
        return contagem

    @classmethod
    def criar(cls, titulo, descricao, status, usuario_id):
        if status not in STATUS_VALIDOS:
            status = "pendente"
        tarefa = cls(
            titulo=titulo,
            descricao=descricao,
            status=status,
            usuario_id=usuario_id,
        )
        db.session.add(tarefa)
        db.session.commit()
        return tarefa

    def atualizar(self, titulo=None, descricao=None, status=None):
        if titulo is not None:
            self.titulo = titulo
        if descricao is not None:
            self.descricao = descricao
        if status is not None and status in STATUS_VALIDOS:
            self.status = status
        db.session.commit()

    def excluir(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao or "",
            "status": self.status,
            "status_label": STATUS_LABELS.get(self.status, self.status),
            "status_cor": STATUS_CORES.get(self.status, "secondary"),
            "data_criacao": self.data_criacao.strftime("%d/%m/%Y %H:%M"),
        }

    def __repr__(self):
        return f"<Tarefa {self.id} {self.titulo} ({self.status})>"
