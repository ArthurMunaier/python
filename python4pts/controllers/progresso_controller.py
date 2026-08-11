from flask import Blueprint, render_template

from .utils import login_required

progresso_bp = Blueprint("progresso", __name__)

@progresso_bp.route("/progresso")
@login_required
def progresso():
    return render_template("progresso.html")
