from flask import Flask, request, render_template_string

app = Flask(__name__)

usuarios = [
    {"nome": "Arthur", "senha": "321"},
    {"nome": "dolga", "senha": "cotemig2026"},
    {"nome": "janaina", "senha": "cotemig2026"},
    {"nome": "antonio", "senha": "cotemig2026"}
]

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario_digitado = request.form.get("usuario")
        senha_digitada = request.form.get("senha")

        for usuario in usuarios:

            if (
                usuario_digitado == usuario["nome"]
                and senha_digitada == usuario["senha"]
            ):

                return f"<h1>Bem-vindo, {usuario_digitado}!</h1>"

        return "<h1>Login inválido</h1>"

    return render_template_string("""

        <h2>Login</h2>

        <form method="POST">

            <input type="text"
                   name="usuario"
                   placeholder="Usuário"><br><br>

            <input type="password"
                   name="senha"
                   placeholder="Senha"><br><br>

            <button type="submit">Entrar</button>

        </form>

    """)

if __name__ == "__main__":
    app.run(debug=True)