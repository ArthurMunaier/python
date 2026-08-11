import os

from flask import Flask, redirect, url_for
from dotenv import load_dotenv

from controllers import auth_bp, tarefas_bp, progresso_bp
from controllers.api import api_v1_bp
from models import db

load_dotenv()

def criar_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )

    pasta = os.path.abspath(os.path.dirname(__file__))

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "chave-de-desenvolvimento-troque-isso")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        pasta, "tarefas.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(tarefas_bp)
    app.register_blueprint(progresso_bp)
    app.register_blueprint(api_v1_bp)

    @app.route("/")
    def raiz():
        return redirect(url_for("tarefas.dashboard"))

    with app.app_context():
        db.create_all()

    return app

app = criar_app()

if __name__ == "__main__":
    modo_debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(debug=modo_debug)
