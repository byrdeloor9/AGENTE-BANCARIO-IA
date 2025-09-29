# Agente Bancario IA - Banco Guayaquil

Sistema de consultas bancarias inteligente que utiliza OpenAI GPT-3.5-turbo para responder consultas sobre cuentas, tarjetas y pólizas de seguro del Banco Guayaquil.

## Características

- **Consultas Generales**: Información sobre horarios, servicios, contacto y sucursales
- **Consultas Específicas**: Acceso a información de cuentas, tarjetas y pólizas (requiere autenticación)
- **Autenticación Condicional**: Solo solicita credenciales cuando es necesario
- **Interfaz Conversacional**: Diseño minimalista y amigable
- **Arquitectura POO**: Código modular y escalable

## Arquitectura del Proyecto

```
├── src/
│   ├── main.py              # Aplicación principal
│   └── __init__.py
├── _tools/                  # Módulos de datos bancarios
│   ├── __init__.py
│   ├── cuentas.py          # Gestión de cuentas bancarias
│   ├── tarjetas.py         # Gestión de tarjetas de crédito/débito
│   └── polizas.py          # Gestión de pólizas de seguro
├── _utils/                  # Utilidades del sistema
│   ├── __init__.py
│   └── security.py         # Autenticación de usuarios
├── prompts/                 # Templates de prompts
│   ├── prompt_agente_bancario.txt  # Para consultas específicas
│   └── prompt_general.txt          # Para consultas generales
├── tests/                   # Pruebas unitarias
│   ├── __init__.py
│   └── test_tools.py
├── pyproject.toml          # Configuración del proyecto
├── requirements.txt        # Dependencias
├── .env                    # Variables de entorno
└── README.md              # Este archivo
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.11+
- Cuenta de OpenAI con API key

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd agente-bancario-ia
   ```

2. **Instalar dependencias con uv**
   ```bash
   uv sync
   ```

3. **Ejecutar la aplicación**
   ```bash
   uv run python src/main.py
   ```

## Configuración

### Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
OPENAI_API_KEY=sk-tu_api_key_de_openai_aqui
```

### Dependencias Principales

- `langchain>=0.3.27`: Framework para aplicaciones LLM
- `langchain-openai>=0.2.8`: Integración con OpenAI
- `python-dotenv>=1.1.1`: Manejo de variables de entorno
- `pytest>=8.4.2`: Framework de testing

## Uso

### Inicio de la Aplicación

```bash
uv run python src/main.py
```

### Interfaz de Usuario

```
============================================================
BIENVENIDO AL AGENTE VIRTUAL DEL BANCO GUAYAQUIL
============================================================

Hola! Soy tu asistente virtual bancario.
Puedo ayudarte con información general o consultas específicas.

Opciones disponibles:
  - Consultas generales (sin autenticación)
  - Consultas de cuentas (requiere autenticación)
  - Consultas de tarjetas (requiere autenticación)
  - Consultas de pólizas (requiere autenticación)

Escribe 'salir' para terminar.
============================================================

- Agente: Hola! En qué puedo ayudarte hoy?

+ Consulta: Buenos dias
- Agente: ¡Buenos días! Muy bien, gracias por preguntar. Estoy aquí para ayudarte con cualquier consulta sobre nuestros servicios bancarios...

+ Consulta: Quiero consultar mi saldo
- Agente: Esta consulta requiere autenticación.

AUTENTICACIÓN REQUERIDA
------------------------------
Para acceder a esta información necesito verificar tu identidad.

Por favor, ingresa tus credenciales:
ID de usuario: 123456
Token de autenticación: token123456

- Agente: Autenticación exitosa! Ahora puedes acceder a toda tu información bancaria.
```

### Tipos de Consultas

#### Consultas Generales (Sin Autenticación)
- Horarios de atención
- Información de contacto
- Ubicación de sucursales
- Tipos de servicios disponibles
- Saludos y conversación casual

#### Consultas Específicas (Con Autenticación)
- **Cuentas**: Saldo, movimientos, límites
- **Tarjetas**: Estado, transacciones, límites, pago mínimo
- **Pólizas**: Estado, valor asegurado, pagos, reclamos, cobertura

### Credenciales de Prueba

Para testing, usa estas credenciales:
- **ID de usuario**: `123456`
- **Token**: `token123456`

## Testing

Ejecutar pruebas unitarias:

```bash
# Con pytest
pytest tests/ -v

# Con uv
uv run pytest tests/ -v
```

## Arquitectura de Clases

### AgenteBancario
- `_detectar_intencion()`: Identifica tipo de consulta
- `_obtener_datos_bancarios()`: Obtiene datos específicos
- `_formatear_contexto()`: Formatea información para el LLM
- `responder()`: Procesa consultas específicas
- `responder_general()`: Procesa consultas generales

### InterfazConsola
- `_mostrar_saludo_inicial()`: Muestra bienvenida
- `_solicitar_autenticacion()`: Maneja autenticación
- `_procesar_consulta()`: Procesa consultas individuales
- `_procesar_sesion()`: Bucle principal de interacción

### Clases de Datos Bancarios

#### CuentaBancaria
- `consultar_estado_cuenta()`
- `consultar_saldo()`
- `consultar_movimientos_recientes()`
- `consultar_limite_disponible()`

#### TarjetaBancaria
- `consultar_estado_tarjeta()`
- `consultar_saldo_disponible()`
- `consultar_transacciones_recientes()`
- `consultar_limite_disponible()`
- `consultar_informacion_pago_minimo()`

#### PolizaSeguro
- `consultar_estado_poliza()`
- `consultar_valor_asegurado()`
- `consultar_historial_pagos()`
- `consultar_historial_reclamos()`
- `consultar_cobertura_detallada()`

## Prompts

### Prompt Principal (`prompts/prompt_agente_bancario.txt`)
- Para consultas específicas sobre cuentas, tarjetas y pólizas
- Incluye contexto de datos bancarios del usuario

### Prompt General (`prompts/prompt_general.txt`)
- Para consultas generales sobre servicios del banco
- Información de horarios, contacto y servicios básicos
- Instrucciones específicas para no inventar información sobre préstamos

## Seguridad

- Autenticación requerida solo para consultas específicas
- Datos bancarios simulados para desarrollo
- Variables de entorno para API keys
- Validación de credenciales

## Desarrollo

### Estructura de Datos

Los datos bancarios están simulados en las clases correspondientes:
- **Cuentas**: IDs 123456, 456789, 789101, 101112
- **Tarjetas**: Diferentes tipos (crédito/débito) y marcas
- **Pólizas**: Seguros de hogar y auto

### Extensibilidad

El sistema está diseñado para fácil extensión:
- Agregar nuevos tipos de productos bancarios
- Implementar nuevas funcionalidades de consulta
- Integrar con sistemas bancarios reales
- Agregar nuevos canales de comunicación

## Roadmap

- [ ] Integración con base de datos real
- [ ] Interfaz web
- [ ] Soporte para múltiples idiomas
- [ ] Integración con WhatsApp/Telegram
- [ ] Dashboard de administración
- [ ] Métricas y analytics

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.
