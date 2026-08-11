from functools import wraps

from flask import jsonify, redirect, request, session, url_for

def login_required(rota):

    @wraps(rota)
    def rota_protegida(*args, **kwargs):
        if not session.get("usuario_id"):
            if request.path.startswith("/api/"):
                return jsonify({"erro": "Não autenticado. Faça login novamente."}), 401
            return redirect(url_for("auth.login"))
        return rota(*args, **kwargs)

    return rota_protegida
