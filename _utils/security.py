# _utils/seguridad.py
def autenticar_usuario(usuario_id, token):
    """
    Autentica un usuario basado en su ID y token.
    Entradas: usuario_id, token
    Salida: True si autenticación exitosa, False en caso contrario
    """

    usuarios_validos = {
        "123456": "token123456",
        "456789": "token456789", 
        "789101": "token789101", 
        "101112": "token101112"
     }

    return usuarios_validos.get(usuario_id) == token