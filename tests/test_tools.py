
import pytest
import sys
import os

# Agregar el directorio raíz al path de Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tools import consultar_cuenta, consultar_tarjeta, consultar_polizas

def test_consultar_cuenta_existente():
    resultado = consultar_cuenta("123456")
    assert resultado == {"tipo": "ahorros", "saldo": 2500.0}

def test_consultar_cuenta_no_existente():
    resultado = consultar_cuenta("999999")
    assert resultado == {"error": "Cuenta no encontrada"}

def test_consultar_tarjeta_existente():
    resultado = consultar_tarjeta("123456")
    assert resultado == {"tipo": "credito", "marca": "visa", "saldo": 2500.0}

def test_consultar_tarjeta_no_existente():
    resultado = consultar_tarjeta("999999") 
    assert resultado == {"error": "Tarjeta no encontrada"}

def test_consultar_poliza_existente():
    resultado = consultar_polizas("123456")
    assert resultado == {
        "tipo": "hogar",
        "valor": 123456,
        "Fecha de vencimiento": "2026-01-01",
        "Intereses": 6
    }

def test_consultar_poliza_no_existente():
    resultado = consultar_polizas("999999")
    assert resultado == {"error": "Poliza no encontrada"}
