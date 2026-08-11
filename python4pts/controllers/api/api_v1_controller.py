from flask import Blueprint, jsonify, request, session

from models import Tarefa, db
from models.tarefa import STATUS_VALIDOS

from ..utils import login_required

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

@api_v1_bp.route("/tarefas", methods=["GET"])
@login_required
def api_listar_tarefas():
    status = request.args.get("status", "")
    tarefas = Tarefa.listar_por_usuario(session["usuario_id"], status)
    return jsonify([t.to_dict() for t in tarefas])

@api_v1_bp.route("/tarefas", methods=["POST"])
@login_required
def api_criar_tarefa():
    dados = request.get_json(silent=True) or {}
    titulo = (dados.get("titulo") or "").strip()
    if not titulo:
        return jsonify({"erro": "O campo 'titulo' é obrigatório."}), 400

    status = dados.get("status", "pendente")
    if status not in STATUS_VALIDOS:
        status = "pendente"

    tarefa = Tarefa.criar(
        titulo=titulo,
        descricao=(dados.get("descricao") or "").strip(),
        status=status,
        usuario_id=session["usuario_id"],
    )
    return jsonify(tarefa.to_dict()), 201

@api_v1_bp.route("/tarefas/<int:tarefa_id>", methods=["PUT"])
@login_required
def api_atualizar_tarefa(tarefa_id):
    tarefa = db.session.get(Tarefa, tarefa_id)
    if not tarefa or tarefa.usuario_id != session["usuario_id"]:
        return jsonify({"erro": "Tarefa não encontrada."}), 404

    dados = request.get_json(silent=True) or {}
    status = dados.get("status")
    if status is not None and status not in STATUS_VALIDOS:
        return jsonify({"erro": "Status inválido."}), 400

    tarefa.atualizar(
        titulo=dados.get("titulo"),
        descricao=dados.get("descricao"),
        status=status,
    )
    return jsonify(tarefa.to_dict())

@api_v1_bp.route("/tarefas/<int:tarefa_id>", methods=["DELETE"])
@login_required
def api_excluir_tarefa(tarefa_id):
    tarefa = db.session.get(Tarefa, tarefa_id)
    if not tarefa or tarefa.usuario_id != session["usuario_id"]:
        return jsonify({"erro": "Tarefa não encontrada."}), 404

    tarefa.excluir()
    return jsonify({"mensagem": "Tarefa excluída com sucesso."})

@api_v1_bp.route("/progresso", methods=["GET"])
@login_required
def api_progresso():
    contagem = Tarefa.contar_por_status(session["usuario_id"])
    return jsonify(contagem)

@api_v1_bp.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "API está funcionando"}), 200
