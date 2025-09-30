"""
Definición de Tools para el Agente Bancario
Cada función bancaria se expone como una herramienta que el LLM puede usar
"""

from typing import Dict, Any, List
from _tools.cuentas import CuentaBancaria
from _tools.tarjetas import TarjetaBancaria
from _tools.polizas import PolizaSeguro


# ============================================================================
# DEFINICIÓN DE TOOLS PARA OPENAI
# ============================================================================

BANKING_TOOLS = [
    # ==================== CUENTAS ====================
    {
        "type": "function",
        "function": {
            "name": "consultar_estado_cuenta",
            "description": "Obtiene información general de la cuenta bancaria del usuario: tipo, saldo, límite diario, fecha de apertura y estado",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_saldo",
            "description": "Consulta únicamente el saldo actual de la cuenta",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_movimientos_recientes",
            "description": "Consulta los movimientos recientes de la cuenta (últimos días). Útil para ver actividad reciente",
            "parameters": {
                "type": "object",
                "properties": {
                    "dias": {
                        "type": "integer",
                        "description": "Número de días hacia atrás para consultar movimientos (default: 7)",
                        "default": 7
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_historial_completo",
            "description": "Consulta TODOS los movimientos históricos de la cuenta sin filtro de fecha. Usar cuando el usuario pide 'todos', 'historial completo', 'históricos'",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_limite_disponible",
            "description": "Consulta los límites de transacciones: límite diario, usado hoy y disponible hoy",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_resumen_mensual_cuenta",
            "description": "Genera un resumen de movimientos por mes: total ingresado, retirado y cantidad de operaciones",
            "parameters": {
                "type": "object",
                "properties": {
                    "mes": {
                        "type": "integer",
                        "description": "Mes a consultar (1-12)",
                        "default": 1
                    },
                    "anio": {
                        "type": "integer",
                        "description": "Año a consultar",
                        "default": 2025
                    }
                },
                "required": []
            }
        }
    },
    
    # ==================== TARJETAS ====================
    {
        "type": "function",
        "function": {
            "name": "consultar_estado_tarjeta",
            "description": "Obtiene información general de la tarjeta: marca, número, límite, saldo, vencimiento y estado",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_saldo_disponible_tarjeta",
            "description": "Consulta el saldo y crédito disponible en la tarjeta",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_transacciones_recientes_tarjeta",
            "description": "Consulta las transacciones recientes de la tarjeta (últimos días)",
            "parameters": {
                "type": "object",
                "properties": {
                    "dias": {
                        "type": "integer",
                        "description": "Número de días hacia atrás para consultar transacciones (default: 7)",
                        "default": 7
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_historial_completo_tarjeta",
            "description": "Consulta TODAS las transacciones históricas de la tarjeta sin filtro de fecha",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    
    # ==================== PÓLIZAS ====================
    {
        "type": "function",
        "function": {
            "name": "consultar_estado_poliza",
            "description": "Obtiene información general de la póliza de seguro: tipo, número, valor asegurado, prima, cobertura y estado",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_historial_pagos_poliza",
            "description": "Consulta el historial de pagos de primas de la póliza",
            "parameters": {
                "type": "object",
                "properties": {
                    "meses": {
                        "type": "integer",
                        "description": "Número de meses hacia atrás para consultar pagos (default: 6)",
                        "default": 6
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_proximo_vencimiento_poliza",
            "description": "Consulta información del próximo vencimiento de pago de la póliza",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


# ============================================================================
# EJECUTOR DE TOOLS
# ============================================================================

class ToolExecutor:
    """Ejecuta las herramientas bancarias basándose en las llamadas del LLM"""
    
    def __init__(self, usuario_id: str):
        self.usuario_id = usuario_id
        self.cuenta = CuentaBancaria(usuario_id)
        self.tarjeta = TarjetaBancaria(usuario_id)
        self.poliza = PolizaSeguro(usuario_id)
    
    def execute_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta una herramienta específica
        
        Args:
            tool_name: Nombre de la herramienta a ejecutar
            tool_args: Argumentos para la herramienta
            
        Returns:
            Resultado de la ejecución de la herramienta
        """
        # ==================== CUENTAS ====================
        if tool_name == "consultar_estado_cuenta":
            return self.cuenta.consultar_estado_cuenta()
        
        elif tool_name == "consultar_saldo":
            return self.cuenta.consultar_saldo()
        
        elif tool_name == "consultar_movimientos_recientes":
            dias = tool_args.get("dias", 7)
            return self.cuenta.consultar_movimientos_recientes(dias=dias)
        
        elif tool_name == "consultar_historial_completo":
            return self.cuenta.consultar_historial_completo()
        
        elif tool_name == "consultar_limite_disponible":
            return self.cuenta.consultar_limite_disponible()
        
        elif tool_name == "consultar_resumen_mensual_cuenta":
            mes = tool_args.get("mes", 1)
            anio = tool_args.get("anio", 2025)
            return self.cuenta.consultar_resumen_mensual(mes=mes, año=anio)
        
        # ==================== TARJETAS ====================
        elif tool_name == "consultar_estado_tarjeta":
            return self.tarjeta.consultar_estado_tarjeta()
        
        elif tool_name == "consultar_saldo_disponible_tarjeta":
            return self.tarjeta.consultar_saldo_disponible()
        
        elif tool_name == "consultar_transacciones_recientes_tarjeta":
            dias = tool_args.get("dias", 7)
            return self.tarjeta.consultar_transacciones_recientes(dias=dias)
        
        elif tool_name == "consultar_historial_completo_tarjeta":
            return self.tarjeta.consultar_historial_completo()
        
        # ==================== PÓLIZAS ====================
        elif tool_name == "consultar_estado_poliza":
            return self.poliza.consultar_estado_poliza()
        
        elif tool_name == "consultar_historial_pagos_poliza":
            meses = tool_args.get("meses", 6)
            return self.poliza.consultar_historial_pagos(meses=meses)
        
        elif tool_name == "consultar_proximo_vencimiento_poliza":
            return self.poliza.consultar_proximo_vencimiento()
        
        else:
            return {"error": f"Herramienta '{tool_name}' no encontrada"}
