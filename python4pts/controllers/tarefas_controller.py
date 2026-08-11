from flask import Blueprint, abort, redirect, render_template, request, session, url_for

from models import Tarefa, db
from models.tarefa import STATUS_CORES, STATUS_LABELS, STATUS_VALIDOS
from services import AdviceApi

from .utils import login_required

tarefas_bp = Blueprint("tarefas", __name__)
advice_api = AdviceApi()

@tarefas_bp.route("/dashboard")
@login_required
def dashboard():
    usuario_id = session["usuario_id"]
    status_filtro = request.args.get("status", "")

    tarefas = Tarefa.listar_por_usuario(usuario_id, status_filtro)
    frase, fonte_demo = advice_api.frase_do_dia()

    return render_template(
        "tarefas/dashboard.html",
        tarefas=tarefas,
        status_filtro=status_filtro,
        status_opcoes=STATUS_VALIDOS,
        status_labels=STATUS_LABELS,
        status_cores=STATUS_CORES,
        frase=frase,
        frase_demo=fonte_demo,
    )

@tarefas_bp.route("/nova_tarefa", methods=["GET", "POST"])
@login_required
def nova_tarefa():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", "pendente")

        if not titulo:
            return render_template(
                "tarefas/formulario.html",
                titulo_pagina="Nova tarefa",
                erro="O título da tarefa é obrigatório.",
                tarefa_titulo=titulo,
                tarefa_descricao=descricao,
                tarefa_status=status,
                status_opcoes=STATUS_VALIDOS,
                status_labels=STATUS_LABELS,
            )

        Tarefa.criar(titulo, descricao, status, session["usuario_id"])
        return redirect(url_for("tarefas.dashboard"))

    return render_template(
        "tarefas/formulario.html",
        titulo_pagina="Nova tarefa",
        status_opcoes=STATUS_VALIDOS,
        status_labels=STATUS_LABELS,
    )

def _buscar_tarefa_do_usuario(tarefa_id):
    tarefa = db.session.get(Tarefa, tarefa_id)
    if not tarefa or tarefa.usuario_id != session["usuario_id"]:
        abort(404)
    return tarefa

@tarefas_bp.route("/editar/<int:tarefa_id>", methods=["GET", "POST"])
@login_required
def editar(tarefa_id):
    tarefa = _buscar_tarefa_do_usuario(tarefa_id)

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        status = request.form.get("status", tarefa.status)

        if not titulo:
            return render_template(
                "tarefas/formulario.html",
                titulo_pagina="Editar tarefa",
                erro="O título da tarefa é obrigatório.",
                tarefa_id=tarefa.id,
                tarefa_titulo=titulo,
                tarefa_descricao=descricao,
                tarefa_status=status,
                status_opcoes=STATUS_VALIDOS,
                status_labels=STATUS_LABELS,
            )

        tarefa.atualizar(titulo=titulo, descricao=descricao, status=status)
        return redirect(url_for("tarefas.dashboard"))

    return render_template(
        "tarefas/formulario.html",
        titulo_pagina="Editar tarefa",
        tarefa_id=tarefa.id,
        tarefa_titulo=tarefa.titulo,
        tarefa_descricao=tarefa.descricao or "",
        tarefa_status=tarefa.status,
        status_opcoes=STATUS_VALIDOS,
        status_labels=STATUS_LABELS,
    )

@tarefas_bp.route("/excluir/<int:tarefa_id>", methods=["POST"])
@login_required
def excluir(tarefa_id):
    tarefa = _buscar_tarefa_do_usuario(tarefa_id)
    tarefa.excluir()
    return redirect(url_for("tarefas.dashboard"))
