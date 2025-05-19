# ──────────────────────────────────────────────────────────────
#  app.py
# ──────────────────────────────────────────────────────────────
from flask import (Flask, render_template, request, redirect,url_for, flash, send_from_directory)
from config import Config
from models import (db, Actividad, Comuna, Region,Foto, ActividadTema, ContactarPor)
from werkzeug.utils import secure_filename
import pathlib, datetime
BASE_DIR      = pathlib.Path(__file__).parent.resolve()
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.config.from_object(Config)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
db.init_app(app)

@app.route("/")
def portada():
    ultimas = (
        Actividad.query
        .order_by(Actividad.dia_hora_inicio.desc())
        .limit(5).all()
    )
    return render_template("portada.html", actividades=ultimas)
@app.route("/actividad/nueva", methods=["GET", "POST"])
def actividad_nueva():
    if request.method == "POST":
        try:
            comuna_id_str = request.form["comuna"]
            comuna_id = int(comuna_id_str)

            act = Actividad(
                comuna_id  = comuna_id,
                sector= request.form.get("sector") or None,
                nombre= request.form["nombre"],
                email= request.form["email"],
                celular= request.form.get("celular") or None,
                dia_hora_inicio= datetime.datetime.fromisoformat(
                                     request.form["inicio"]),
                dia_hora_termino=(datetime.datetime.fromisoformat(request.form["termino"])
                    if request.form.get("termino") else None),
                descripcion= request.form.get("descripcion") or None
            )

            for tema in request.form.getlist("tema"):
                glosa = request.form.get("tema_otro") if tema == "otro" else None
                act.temas.append(ActividadTema(tema=tema, glosa_otro=glosa))

            medios= request.form.getlist("contactar_medio")
            identificadores= request.form.getlist("contactar_id")
            for medio, identificador in zip(medios, identificadores):
                if identificador.strip():
                    act.contactos.append(ContactarPor(nombre=medio, identificador=identificador))

            for f in request.files.getlist("fotos"):
                if f and f.filename:
                    fname = secure_filename(f.filename)
                    ruta  = UPLOAD_FOLDER / fname
                    f.save(ruta)
                    act.fotos.append(Foto(ruta_archivo=fname, nombre_archivo=fname))

            db.session.add(act)
            db.session.commit()
            flash("Actividad creada correctamente", "success")
            return redirect(url_for("portada"))

        except Exception as exc:
            db.session.rollback()
            flash(f" Error: {exc}", "danger")

    regiones=Region.query.all()
    return render_template("agregar_actividad.html", regiones=regiones)


@app.route("/actividades")
def actividades_lista():
    page= request.args.get("page", 1, type=int)
    pagination= (Actividad.query.order_by(Actividad.dia_hora_inicio.desc()).paginate(page=page, per_page=5))
    return render_template("listar.html",pagination=pagination,actividades=pagination.items)

@app.route("/actividad/<int:act_id>")
def actividad_detalle(act_id):
    act= Actividad.query.get_or_404(act_id)
    return render_template("detalle.html", act=act)
@app.route("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html")


@app.route("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
