from app import app, db
from sqlalchemy import text

with app.app_context():
    with open("region-comuna.sql", encoding="utf-8") as f:
        contenido = f.read()

    sentencias = [s.strip() for s in contenido.split(";") if s.strip()]
    for stmt in sentencias:
        db.session.execute(text(stmt))

    db.session.commit()
    print("→ Tablas region y comuna pobladas.")


