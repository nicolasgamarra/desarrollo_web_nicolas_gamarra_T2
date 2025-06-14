# app.py (con soporte para comentarios por AJAX)
from flask import (Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify)
from config import Config
from models import (db, Actividad, Comuna, Region, Foto, ActividadTema, ContactarPor, Comentario)
from werkzeug.utils import secure_filename
import pathlib, datetime
from sqlalchemy import func, extract, case

BASE_DIR = pathlib.Path(__file__).parent.resolve()
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
app = Flask(__name__)
app.config.from_object(Config)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "clave_segura_para_flash"
db.init_app(app)

THEMES_LABEL = {"musica": "Música","deporte": "Deporte","ciencias": "Ciencias","religion": "Religión","politica": "Política","tecnologia": "Tecnología",
"juegos": "Juegos","baile": "Baile","comida": "Comida","otro": "Otro"}

@app.route("/")
def portada():
    ultimas = Actividad.query.order_by(Actividad.dia_hora_inicio.desc()).limit(5).all()
    return render_template("portada.html", actividades=ultimas, THEMES_LABEL=THEMES_LABEL)

@app.route("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html")


@app.route("/actividad/nueva", methods=["GET", "POST"])
def actividad_nueva():
    if request.method == "POST":
        errores=[]
        try:
            nombre = request.form.get("nombre", "").strip()
            email = request.form.get("email", "").strip()
            inicio = request.form.get("inicio")
            termino = request.form.get("termino")
            fotos_subidas = request.files.getlist("fotos")

            if not (3 <= len(nombre) <= 200):
                errores.append("El nombre debe tener entre 3 y 200 caracteres.")
            if "@" not in email or "." not in email:
                errores.append("Email inválido.")
            try:
                inicio_dt = datetime.datetime.fromisoformat(inicio)
            except:
                errores.append("Formato de fecha de inicio incorrecto.")
            fin_dt = None
            if termino:
                try:
                    fin_dt = datetime.datetime.fromisoformat(termino)
                    if fin_dt <= inicio_dt:
                        errores.append("La fecha de término debe ser posterior a la de inicio.")
                except:
                    errores.append("Formato de fecha de término incorrecto.")

            if not any(f.filename for f in fotos_subidas):
                errores.append("Debes subir al menos una foto.")
            if len(fotos_subidas) > 5:
                errores.append("No se pueden subir más de 5 fotos.")

            if "otro" in request.form.getlist("tema") and not request.form.get("tema_otro", "").strip():
                errores.append("Debes especificar el tema si seleccionas 'Otro'.")

            medios = request.form.getlist("contactar_medio")
            identificadores = request.form.getlist("contactar_id")
            for medio, identificador in zip(medios, identificadores):
                if not identificador.strip():
                    errores.append(f"Falta el identificador para {medio}.")

            if errores:
                for e in errores:
                    flash(e, "error")
                return redirect(url_for("actividad_nueva"))

            comuna_id = int(request.form["comuna"])
            act = Actividad(
                comuna_id=comuna_id,
                sector=request.form.get("sector") or None,
                nombre=nombre,
                email=email,
                celular=request.form.get("celular") or None,
                dia_hora_inicio=inicio_dt,
                dia_hora_termino=fin_dt,
                descripcion=request.form.get("descripcion") or None)
            for tema in request.form.getlist("tema"):
                glosa=request.form.get("tema_otro") if tema == "otro" else None
                act.temas.append(ActividadTema(tema=tema, glosa_otro=glosa))
            for medio,identificador in zip(medios,identificadores):
                if identificador.strip():
                    act.contactos.append(ContactarPor(nombre=medio, identificador=identificador.strip()))
            for f in fotos_subidas:
                if f and f.filename:
                    fname = secure_filename(f.filename)
                    ruta = UPLOAD_FOLDER/fname
                    f.save(ruta)
                    act.fotos.append(Foto(ruta_archivo=fname, nombre_archivo=fname))
            db.session.add(act)
            db.session.commit()
            flash("Actividad creada correctamente", "success")
            return redirect(url_for("portada"))
        except Exception as exc:
            db.session.rollback()
            flash(f" Error: {exc}", "danger")
    regiones = Region.query.all()
    return render_template("agregar_actividad.html", regiones=regiones)

@app.route("/actividad/<int:actividad_id>")
def actividad_detalle(actividad_id):
    act = Actividad.query.get_or_404(actividad_id)
    return render_template("detalle.html", actividad=act, THEMES_LABEL=THEMES_LABEL)

@app.route("/api/comentarios/<int:actividad_id>", methods=["POST"])
def crear_comentario(actividad_id):
    actividad = Actividad.query.get_or_404(actividad_id)
    nombre = request.form.get("nombre", "").strip()
    texto = request.form.get("texto","").strip()
    if not nombre or not texto:
        return jsonify({"ok": False, "error":"Nombre y comentario requeridos."}), 400
    comentario = Comentario(nombre=nombre,texto=texto,actividad_id=actividad_id)
    try:
        db.session.add(comentario)
        db.session.commit()
        return jsonify({"ok": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/actividades")
def actividades_lista():
    page = request.args.get("page", 1, type=int)
    pagination = (Actividad.query
                  .order_by(Actividad.dia_hora_inicio.desc())
                  .paginate(page=page, per_page=5))
    return render_template("listar.html",
                           pagination=pagination,
                           actividades=pagination.items)


@app.route("/api/comentarios/<int:actividad_id>")
def obtener_comentarios(actividad_id):
    actividad = Actividad.query.get_or_404(actividad_id)
    comentarios = [{
        "nombre": c.nombre,
        "texto": c.texto,
        "fecha": c.fecha.strftime("%Y-%m-%d %H:%M")} for c in actividad.comentarios]
    return comentarios


@app.route("/api/estadisticas/actividades_por_dia")
def api_actividades_por_dia():
    from sqlalchemy import func
    resultados = (db.session.query(func.date(Actividad.dia_hora_inicio).label("fecha"),func.count().label("cantidad"))
        .group_by(func.date(Actividad.dia_hora_inicio))
        .order_by(func.date(Actividad.dia_hora_inicio))
        .all()
    )

    datos = [{"fecha": r.fecha.strftime("%Y-%m-%d"), "cantidad": r.cantidad} for r in resultados]
    return jsonify(datos)

@app.route("/api/estadisticas/actividades_por_tema")
def api_actividades_por_tema():
    from sqlalchemy import func
    resultados = (db.session.query(ActividadTema.tema,func.count().label("cantidad"))
        .group_by(ActividadTema.tema)
        .all())
    datos=[{"tema": r.tema, "cantidad": r.cantidad} for r in resultados]
    return jsonify(datos)


@app.route("/api/estadisticas/actividades_por_horario_mes")
def api_actividades_por_horario_mes():
    franjas = case((extract('hour',Actividad.dia_hora_inicio)<12,'mañana'),(extract('hour',Actividad.dia_hora_inicio)<18,'mediodia'),
    else_='tarde')
    resultados = (db.session.query(extract('month',Actividad.dia_hora_inicio).label("mes"),franjas.label("franja"),func.count().label("cantidad"))
        .group_by("mes","franja")
        .order_by("mes")
        .all())

    datos_por_franja = {"mañana":{}, "mediodia":{}, "tarde":{}}
    for r in resultados:
        mes =int(r.mes)
        franja =r.franja
        datos_por_franja[franja][mes] = r.cantidad

    meses = sorted(set(m for f in datos_por_franja.values() for m in f))
    datos_finales = {"meses": [mes for mes in meses],"series": [{"name": franja.capitalize(),"data": [datos_por_franja[franja].get(m, 0) for m in meses]}
            for franja in ["mañana", "mediodia", "tarde"]]}
    return jsonify(datos_finales)


if __name__ == "__main__":
    app.run(debug=True)


