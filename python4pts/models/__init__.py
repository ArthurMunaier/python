from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base import ModeloBase
from .usuario import Usuario
from .tarefa import Tarefa

__all__ = ["db", "ModeloBase", "Usuario", "Tarefa"]
