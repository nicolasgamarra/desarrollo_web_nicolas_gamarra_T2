from app import app
from models import Actividad

if __name__ == "__main__":
    with app.app_context():
        acts = (
            Actividad.query.order_by(Actividad.dia_hora_inicio.desc()).limit(5).all())
        if not acts:
            print("→ No hay actividades en la base de datos.")
        else:
            for a in acts:
                print(f"ID {a.id}: {a.nombre!r} @ {a.dia_hora_inicio}")
                print(f"   Fotos:   {len(a.fotos)}")
                print(f"   Temas:   {len(a.temas)}")
                print(f"   Contactos: {len(a.contactos)}\n")
