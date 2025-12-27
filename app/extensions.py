# app/extensions.py
from flask_sqlalchemy import SQLAlchemy

# Inicializamos el objeto db sin la app todavía (Lazy Loading)
db = SQLAlchemy()