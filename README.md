# 🤖 Agente Bancario IA - Banco Guayaquil

Sistema inteligente de consultas bancarias que utiliza **GPT-4o-mini** con **Function Calling** para proporcionar información sobre cuentas, tarjetas y pólizas.

## ✨ Características

- 🧠 **IA Conversacional** - Usa GPT-4o-mini con Function Calling
- 🔧 **14 Herramientas Bancarias** - Acceso a datos de cuentas, tarjetas y pólizas
- 📊 **Análisis Inteligente** - Genera insights y patrones de datos
- 💬 **Contexto Conversacional** - Mantiene el historial de la conversación
- 🎯 **Cero Código Hardcodeado** - El LLM decide qué herramientas usar automáticamente

## 🚀 Inicio Rápido

### **Requisitos**
- Python 3.10+
- OpenAI API Key

### **Instalación**

#### **Opción 1: Usando pip (tradicional)**
```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd "AGENTE BANCARIO IA"

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API Key
# Crear archivo .env con:
OPENAI_API_KEY=tu_api_key_aquí

# 4. Ejecutar el agente
python main.py
```

#### **Opción 2: Usando uv (recomendado)**
```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd "AGENTE BANCARIO IA"

# 2. Instalar uv (si no lo tienes)
pip install uv

# 3. Instalar dependencias con uv
uv sync

# 4. Configurar API Key
# Crear archivo .env con:
OPENAI_API_KEY=tu_api_key_aquí

# 5. Ejecutar el agente
uv run python main.py
```

> **💡 Nota**: `uv` es más rápido y eficiente que `pip` para la gestión de dependencias. Si tienes `uv.lock` en el proyecto, se recomienda usar `uv sync`.

### **Credenciales de Prueba**
```
ID de usuario: 123456
Token: token123456
```

## 📋 Herramientas Disponibles

### **Cuentas (6)**
- `consultar_estado_cuenta` - Información general
- `consultar_saldo` - Saldo actual
- `consultar_movimientos_recientes` - Últimos 7 días
- `consultar_historial_completo` - Todos los movimientos
- `consultar_limite_disponible` - Límites diarios
- `consultar_resumen_mensual_cuenta` - Resumen por mes

### **Tarjetas (4)**
- `consultar_estado_tarjeta` - Información general
- `consultar_saldo_disponible_tarjeta` - Saldo/crédito disponible
- `consultar_transacciones_recientes_tarjeta` - Últimas transacciones
- `consultar_historial_completo_tarjeta` - Todas las transacciones

### **Pólizas (3)**
- `consultar_estado_poliza` - Información general
- `consultar_historial_pagos_poliza` - Historial de pagos
- `consultar_proximo_vencimiento_poliza` - Próximo vencimiento

## 💡 Ejemplos de Uso

### **Consultas Simples**
```
Usuario: "¿Cuál es mi saldo?"
Agente: "Tu saldo actual es de $2,500.00 USD."
```

### **Información Completa**
```
Usuario: "Dime más sobre mi cuenta"
Agente: [Combina automáticamente estado + límites + actividad reciente]
```

### **Análisis Inteligente**
```
Usuario: "Dame un insight de mis movimientos"
Agente: 
"📊 Resumen General:
   • Total movimientos: 10
   • Ingresos: +$2,900.00
   • Egresos: -$975.00
   
💡 Patrones:
   • Depósitos regulares día 24 (salarios)
   • Principales gastos: ATM y servicios
   
📈 Recomendación:
   Tu flujo de caja es positivo. Considera ahorrar parte de tus ingresos."
```

### **Contexto Conversacional**
```
Usuario: "¿Mi saldo?"
Agente: "$2,500.00 USD"

Usuario: "¿Y qué más?"
Agente: [Entiende el contexto y proporciona info adicional de la cuenta]
```

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────┐
│   Usuario hace consulta                 │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  AgenteBancario (gpt-4o-mini)           │
│  • Analiza consulta                     │
│  • Decide qué herramientas usar         │
│  • Ejecuta herramientas                 │
│  • Genera respuesta inteligente         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  BANKING_TOOLS (Catálogo)               │
│  • 14 herramientas bancarias            │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  ToolExecutor                           │
│  • CuentaBancaria                       │
│  • TarjetaBancaria                      │
│  • PolizaSeguro                         │
└─────────────────────────────────────────┘
```

## 📁 Estructura del Proyecto

```
.
├── main.py                      # Punto de entrada
├── src/
│   ├── agent.py                 # Agente principal con Function Calling
│   └── agent_tools.py           # Definición de herramientas y executor
├── _tools/
│   ├── cuentas.py               # Lógica de cuentas bancarias
│   ├── tarjetas.py              # Lógica de tarjetas
│   └── polizas.py               # Lógica de pólizas
├── _utils/
│   └── security.py              # Autenticación
└── prompts/
    └── system_prompt.txt           # Prompt unificado del sistema
```

## 🔧 Agregar Nueva Herramienta

Es muy fácil extender las capacidades:

```python
# 1. En src/agent_tools.py, agregar a BANKING_TOOLS:
{
    "type": "function",
    "function": {
        "name": "nueva_herramienta",
        "description": "Descripción clara de qué hace",
        "parameters": {...}
    }
}

# 2. En ToolExecutor.execute_tool():
elif tool_name == "nueva_herramienta":
    return self.objeto.nueva_herramienta(**tool_args)
```

¡El LLM automáticamente sabrá cuándo usarla!

## 🎯 Ventajas de la Arquitectura

| Aspecto | Implementación |
|---------|---------------|
| **Decisiones** | El LLM decide qué herramientas usar |
| **Respuestas** | Dinámicas y contextuales (no hardcodeadas) |
| **Herramientas** | Puede combinar múltiples automáticamente |
| **Análisis** | Genera insights de datos |
| **Mantenimiento** | Simple - solo agregar herramientas |
| **Escalabilidad** | Fácil - el LLM aprende nuevas herramientas |

## 📊 Modelo de IA

- **Modelo:** GPT-4o-mini (OpenAI)
- **Temperatura:** 0 (respuestas determinísticas)
- **Capacidades:** Function Calling / Tool Use
- **Contexto:** 128K tokens
- **Costo:** ~$0.15/1M tokens input, ~$0.60/1M tokens output

## 🔒 Seguridad

- Autenticación requerida para todas las consultas
- Datos de prueba simulados (no conexión a BD real)
- Validación de credenciales en `_utils/security.py`


## 🤝 Contribuir

Para agregar nuevas funcionalidades:
1. Agregar la herramienta en `src/agent_tools.py`
2. Implementar la lógica en `_tools/`
3. El LLM automáticamente aprenderá a usarla

## 📄 Licencia

Ver archivo `LICENSE`

## 🆘 Soporte

Para preguntas o problemas, contactar al equipo de desarrollo.