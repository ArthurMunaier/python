from flask import Blueprint, render_template, request, redirect, flash
from extensions import db

from models.filme import Filme
from models.sala import Sala
from models.sessao import Sessao

cinema = Blueprint("cinema", __name__)


@cinema.route("/")
def index():
    return render_template("index.html")


# ---------------- FILMES ----------------

@cinema.route("/filmes")
def filmes():
    lista = Filme.query.all()
    return render_template("filmes.html", filmes=lista)


@cinema.route("/filmes/novo", methods=["GET", "POST"])
def novo_filme():
    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        genero = request.form["genero"].strip()
        duracao = request.form["duracao"]

        if not titulo or not genero or not duracao.isdigit() or int(duracao) <= 0:
            flash("Preencha os dados do filme corretamente.")
            return redirect("/filmes/novo")

        filme = Filme(
            titulo=titulo,
            genero=genero,
            duracao=int(duracao)
        )

        db.session.add(filme)
        db.session.commit()

        flash("Filme cadastrado com sucesso.")
        return redirect("/filmes")

    return render_template("novo_filme.html")


@cinema.route("/filmes/editar/<int:id>", methods=["GET", "POST"])
def editar_filme(id):
    filme = Filme.query.get_or_404(id)

    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        genero = request.form["genero"].strip()
        duracao = request.form["duracao"]

        if not titulo or not genero or not duracao.isdigit() or int(duracao) <= 0:
            flash("Preencha os dados do filme corretamente.")
            return redirect(f"/filmes/editar/{id}")

        filme.titulo = titulo
        filme.genero = genero
        filme.duracao = int(duracao)

        db.session.commit()

        flash("Filme atualizado com sucesso.")
        return redirect("/filmes")

    return render_template("editar_filme.html", filme=filme)


@cinema.route("/filmes/excluir/<int:id>")
def excluir_filme(id):
    filme = Filme.query.get_or_404(id)

    if filme.sessoes:
        flash("Não é possível excluir um filme que possui sessões cadastradas.")
        return redirect("/filmes")

    db.session.delete(filme)
    db.session.commit()

    flash("Filme excluído com sucesso.")
    return redirect("/filmes")


# ---------------- SALAS ----------------

@cinema.route("/salas")
def salas():
    lista = Sala.query.all()
    return render_template("salas.html", salas=lista)


@cinema.route("/salas/nova", methods=["GET", "POST"])
def nova_sala():
    if request.method == "POST":
        numero = request.form["numero"]
        capacidade = request.form["capacidade"]

        if not numero.isdigit() or not capacidade.isdigit():
            flash("Número e capacidade devem ser valores numéricos.")
            return redirect("/salas/nova")

        if int(numero) <= 0 or int(capacidade) <= 0:
            flash("Número e capacidade devem ser maiores que zero.")
            return redirect("/salas/nova")

        sala_existente = Sala.query.filter_by(numero=int(numero)).first()

        if sala_existente:
            flash("Já existe uma sala com esse número.")
            return redirect("/salas/nova")

        sala = Sala(
            numero=int(numero),
            capacidade=int(capacidade)
        )

        db.session.add(sala)
        db.session.commit()

        flash("Sala cadastrada com sucesso.")
        return redirect("/salas")

    return render_template("nova_sala.html")


@cinema.route("/salas/editar/<int:id>", methods=["GET", "POST"])
def editar_sala(id):
    sala = Sala.query.get_or_404(id)

    if request.method == "POST":
        numero = request.form["numero"]
        capacidade = request.form["capacidade"]

        if not numero.isdigit() or not capacidade.isdigit():
            flash("Número e capacidade devem ser valores numéricos.")
            return redirect(f"/salas/editar/{id}")

        if int(numero) <= 0 or int(capacidade) <= 0:
            flash("Número e capacidade devem ser maiores que zero.")
            return redirect(f"/salas/editar/{id}")

        sala_existente = Sala.query.filter(
            Sala.numero == int(numero),
            Sala.id != id
        ).first()

        if sala_existente:
            flash("Já existe outra sala com esse número.")
            return redirect(f"/salas/editar/{id}")

        sala.numero = int(numero)
        sala.capacidade = int(capacidade)

        db.session.commit()

        flash("Sala atualizada com sucesso.")
        return redirect("/salas")

    return render_template("editar_sala.html", sala=sala)


@cinema.route("/salas/excluir/<int:id>")
def excluir_sala(id):
    sala = Sala.query.get_or_404(id)

    if sala.sessoes:
        flash("Não é possível excluir uma sala que possui sessões cadastradas.")
        return redirect("/salas")

    db.session.delete(sala)
    db.session.commit()

    flash("Sala excluída com sucesso.")
    return redirect("/salas")


# ---------------- SESSÕES ----------------

@cinema.route("/sessoes")
def sessoes():
    lista = Sessao.query.all()
    return render_template("sessoes.html", sessoes=lista)


@cinema.route("/sessoes/nova", methods=["GET", "POST"])
def nova_sessao():
    if request.method == "POST":
        horario = request.form["horario"]
        filme_id = request.form["filme"]
        sala_id = request.form["sala"]

        if not horario or not filme_id.isdigit() or not sala_id.isdigit():
            flash("Preencha os dados da sessão corretamente.")
            return redirect("/sessoes/nova")

        filme = Filme.query.get(int(filme_id))
        sala = Sala.query.get(int(sala_id))

        if not filme or not sala:
            flash("Filme ou sala inválidos.")
            return redirect("/sessoes/nova")

        sessao = Sessao(
            horario=horario,
            filme_id=int(filme_id),
            sala_id=int(sala_id)
        )

        db.session.add(sessao)
        db.session.commit()

        flash("Sessão cadastrada com sucesso.")
        return redirect("/sessoes")

    filmes = Filme.query.all()
    salas = Sala.query.all()

    return render_template("nova_sessao.html", filmes=filmes, salas=salas)


@cinema.route("/sessoes/editar/<int:id>", methods=["GET", "POST"])
def editar_sessao(id):
    sessao = Sessao.query.get_or_404(id)

    if request.method == "POST":
        horario = request.form["horario"]
        filme_id = request.form["filme"]
        sala_id = request.form["sala"]

        if not horario or not filme_id.isdigit() or not sala_id.isdigit():
            flash("Preencha os dados da sessão corretamente.")
            return redirect(f"/sessoes/editar/{id}")

        filme = Filme.query.get(int(filme_id))
        sala = Sala.query.get(int(sala_id))

        if not filme or not sala:
            flash("Filme ou sala inválidos.")
            return redirect(f"/sessoes/editar/{id}")

        sessao.horario = horario
        sessao.filme_id = int(filme_id)
        sessao.sala_id = int(sala_id)

        db.session.commit()

        flash("Sessão atualizada com sucesso.")
        return redirect("/sessoes")

    filmes = Filme.query.all()
    salas = Sala.query.all()

    return render_template(
        "editar_sessao.html",
        sessao=sessao,
        filmes=filmes,
        salas=salas
    )


@cinema.route("/sessoes/excluir/<int:id>")
def excluir_sessao(id):
    sessao = Sessao.query.get_or_404(id)

    db.session.delete(sessao)
    db.session.commit()

    flash("Sessão excluída com sucesso.")
    return redirect("/sessoes")