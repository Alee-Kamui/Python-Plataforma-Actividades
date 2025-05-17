from app import create_app, db
from app.models import Usuario  # Importa tus modelos

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Base de datos creada correctamente.")

