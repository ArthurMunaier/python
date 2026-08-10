from flask import Flask
from extensions import db

from config import Config





def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)

    from controllers.cinema_controller import cinema
    app.register_blueprint(cinema)

    from controllers.api import api_v1_bp
    app.register_blueprint(api_v1_bp)

    with app.app_context():
        from models.filme import Filme
        from models.sala import Sala
        from models.sessao import Sessao

        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)