
def consultar_cuenta(usuario_id: str):
    
    """
    Simula consulta de información de cuentas.
    Entradas: usuario_id
    Salida: diccionario con saldo y tipo de cuenta
    """

    print("Consultando cuenta...")
    
    informacion_cuentas = {
        "123456": {"tipo": "ahorros", "saldo": 2500.0},
        "456789": {"tipo": "corriente", "saldo": 500.0},
        "789101": {"tipo": "ahorros", "saldo": 1000.0},
        "101112": {"tipo": "corriente", "saldo": 2000.0}
    }

    return informacion_cuentas.get(usuario_id, {"error": "Cuenta no encontrada"})
    

def consultar_tarjeta(usuario_id: str):
    """
    Simula consulta de información de tarjetas.
    Entradas: usuario_id
    Salida: diccionario con saldo y tipo de tarjeta
    """
    print("Consultando tarjeta...")

    informacion_tarjetas = {
        "123456": {"tipo": "credito", "marca": "visa", "saldo": 2500.0},
        "456789": {"tipo": "debito", "marca": "mastercard", "saldo": 500.0},
        "789101": {"tipo": "debito", "marca": "visa", "saldo": 1000.0},
        "101112": {"tipo": "credito", "marca": "mastercard", "saldo": 2000.0}
    }
    return informacion_tarjetas.get(usuario_id, {"error": "Tarjeta no encontrada"})

def consultar_polizas(usuario_id: str):
    """
    Simula consulta de información de polizas.
    Entradas: usuario_id
    Salida: diccionario con polizas
    """
    print("Consultando polizas...")

    informacion_polizas = {
        "123456": {"tipo": "hogar", "valor": 123456,"Fecha de vencimiento": "2026-01-01","Intereses": 6},
        "456789": {"tipo": "auto", "valor": 456789,"Fecha de vencimiento": "2027-01-01","Intereses": 7},
        "789101": {"tipo": "hogar", "valor": 789101,"Fecha de vencimiento": "2028-01-01","Intereses": 8},
        "101112": {"tipo": "auto", "valor": 101112,"Fecha de vencimiento": "2029-01-01","Intereses": 10}
    }

    return informacion_polizas.get(usuario_id, {"error": "Poliza no encontrada"})

if __name__ == "__main__":
    print("TOOLS")