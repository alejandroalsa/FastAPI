# Test unitario para comprobar la base de datos
from api import engine
import pytest
from sqlalchemy import text # Ejecutar consultas SQL en formato texto plano.
from sqlalchemy.exc import SQLAlchemyError


def test_connection_database():
  try:
    with engine.connect() as connetion:
      result = connetion.execute(text("SELECT name FROM categories"))
      rows = result.all()
      assert len(rows) > 0
  except SQLAlchemyError as excinfo:
    pytest.fail(f"Se ha producido un error en la conexión o en la consulta: {excinfo}")