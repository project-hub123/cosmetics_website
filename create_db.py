import os
import sys

# Добавляем путь проекта, чтобы импортировать app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import *

app = create_app()

with app.app_context():
    db.create_all()
    print("База данных успешно создана.")
