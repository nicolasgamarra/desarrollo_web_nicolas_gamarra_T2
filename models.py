from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Region(db.Model):
    __tablename__ = "region"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)

class Comuna(db.Model):
    __tablename__ = "comuna"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey("region.id"), nullable=False)
    region = db.relationship("Region", backref="comunas")

class Actividad(db.Model):
    __tablename__ = "actividad"
    id = db.Column(db.Integer, primary_key=True)
    comuna_id = db.Column(db.Integer, db.ForeignKey("comuna.id"), nullable=False)
    comuna = db.relationship("Comuna", backref="actividades")

    sector = db.Column(db.String(100))
    nombre = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(15))
    dia_hora_inicio = db.Column(db.DateTime, nullable=False)
    dia_hora_termino = db.Column(db.DateTime)
    descripcion = db.Column(db.String(500))

    fotos = db.relationship("Foto", backref="actividad", cascade="all, delete-orphan")
    temas = db.relationship("ActividadTema", backref="actividad", cascade="all, delete-orphan")
    contactos = db.relationship("ContactarPor", backref="actividad", cascade="all, delete-orphan")
    comentarios = db.relationship("Comentario", backref="actividad", cascade="all, delete-orphan")

class Foto(db.Model):
    __tablename__ = "foto"
    id = db.Column(db.Integer, primary_key=True)
    ruta_archivo = db.Column(db.String(300),nullable=False)
    nombre_archivo = db.Column(db.String(300),nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey("actividad.id"),nullable=False)

class ActividadTema(db.Model):
    __tablename__ = "actividad_tema"
    id = db.Column(db.Integer, primary_key=True)
    tema = db.Column(db.Enum("musica", "deporte", "ciencias", "religion", "politica",
        "tecnologia", "juegos", "baile", "comida", "otro", name="tema_enum"),nullable=False)
    glosa_otro = db.Column(db.String(15))
    actividad_id = db.Column(db.Integer, db.ForeignKey("actividad.id"),nullable=False)

class ContactarPor(db.Model):
    __tablename__ = "contactar_por"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Enum("whatsapp", "telegram", "X", "instagram", "tiktok", "otra", name="contacto_enum"),nullable=False)
    identificador = db.Column(db.String(150),nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey("actividad.id"),nullable=False)

class Comentario(db.Model):
    __tablename__ = "comentario"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100),nullable=False)
    texto = db.Column(db.String(500),nullable=False)
    fecha = db.Column(db.DateTime,nullable=False, server_default=db.func.current_timestamp())
    actividad_id = db.Column(db.Integer, db.ForeignKey("actividad.id"),nullable=False)

