from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models import Usuario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")

        erro = None
        if not nome or not email or not senha:
            erro = "Preencha nome, e-mail e senha."
        elif len(senha) < 6:
            erro = "A senha precisa ter pelo menos 6 caracteres."
        elif senha != confirmar_senha:
            erro = "As senhas não conferem."
        elif Usuario.buscar_por_email(email):
            erro = "Já existe uma conta com esse e-mail."

        if erro:
            return render_template(
                "auth/registro.html", erro=erro, nome=nome, email=email
            )

        Usuario.criar(nome, email, senha)
        flash("Conta criada com sucesso! Faça login para continuar.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/registro.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        usuario = Usuario.buscar_por_email(email)
        if not usuario or not usuario.verificar_senha(senha):
            return render_template(
                "auth/login.html", erro="E-mail ou senha inválidos.", email=email
            )

        session["usuario_id"] = usuario.id
        session["usuario_nome"] = usuario.nome
        return redirect(url_for("tarefas.dashboard"))

    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
