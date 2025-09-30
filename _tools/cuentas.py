"""
Módulo de gestión de cuentas bancarias
Implementa funcionalidades completas para consulta y gestión de cuentas
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta


class CuentaBancaria:
    """Clase para gestión completa de cuentas bancarias"""
    
    def __init__(self, usuario_id: str):
        """
        Inicializar cuenta bancaria
        
        Args:
            usuario_id: Identificador único del usuario
        """
        self.usuario_id = usuario_id
        self._datos_cuentas = self._cargar_datos_cuentas()
        self._movimientos = self._cargar_movimientos()
    
    def _cargar_datos_cuentas(self) -> Dict[str, Dict]:
        """Cargar datos base de las cuentas"""
        return {
            "123456": {
                "tipo": "ahorros",
                "saldo": 2500.0,
                "limite_diario": 1000.0,
                "fecha_apertura": "2023-01-15",
                "estado": "activa"
            },
            "456789": {
                "tipo": "corriente",
                "saldo": 500.0,
                "limite_diario": 2000.0,
                "fecha_apertura": "2023-03-20",
                "estado": "activa"
            },
            "789101": {
                "tipo": "ahorros",
                "saldo": 1000.0,
                "limite_diario": 1500.0,
                "fecha_apertura": "2023-06-10",
                "estado": "activa"
            },
            "101112": {
                "tipo": "corriente",
                "saldo": 2000.0,
                "limite_diario": 3000.0,
                "fecha_apertura": "2023-09-05",
                "estado": "activa"
            }
        }
    
    def _cargar_movimientos(self) -> Dict[str, List[Dict]]:
        """Cargar historial de movimientos por usuario (incluye recientes e históricos)"""
        return {
            "123456": [
                # Movimientos recientes (últimos 7 días)
                {"fecha": "2025-09-28", "tipo": "deposito", "monto": 500.0, "descripcion": "Deposito en efectivo"},
                {"fecha": "2025-09-27", "tipo": "retiro", "monto": -200.0, "descripcion": "Retiro ATM"},
                {"fecha": "2025-09-26", "tipo": "transferencia", "monto": 150.0, "descripcion": "Transferencia recibida"},
                {"fecha": "2025-09-25", "tipo": "pago", "monto": -75.0, "descripcion": "Pago servicios"},
                {"fecha": "2025-09-24", "tipo": "deposito", "monto": 1000.0, "descripcion": "Salario"},
                # Movimientos históricos (más antiguos)
                {"fecha": "2025-08-15", "tipo": "deposito", "monto": 800.0, "descripcion": "Deposito agosto"},
                {"fecha": "2025-07-20", "tipo": "retiro", "monto": -300.0, "descripcion": "Retiro julio"},
                {"fecha": "2025-06-10", "tipo": "transferencia", "monto": 250.0, "descripcion": "Transferencia junio"},
                {"fecha": "2024-12-15", "tipo": "deposito", "monto": 1200.0, "descripcion": "Aguinaldo"},
                {"fecha": "2024-11-01", "tipo": "pago", "monto": -400.0, "descripcion": "Pago noviembre"}
            ],
            "456789": [
                {"fecha": "2025-09-28", "tipo": "retiro", "monto": -100.0, "descripcion": "Retiro ATM"},
                {"fecha": "2025-09-27", "tipo": "deposito", "monto": 300.0, "descripcion": "Deposito cheque"},
                {"fecha": "2025-09-26", "tipo": "pago", "monto": -150.0, "descripcion": "Pago tarjeta"},
                {"fecha": "2025-09-25", "tipo": "transferencia", "monto": 200.0, "descripcion": "Transferencia recibida"},
                {"fecha": "2025-08-10", "tipo": "deposito", "monto": 600.0, "descripcion": "Deposito agosto"},
                {"fecha": "2025-07-05", "tipo": "retiro", "monto": -200.0, "descripcion": "Retiro julio"}
            ],
            "789101": [
                {"fecha": "2025-09-28", "tipo": "deposito", "monto": 250.0, "descripcion": "Deposito ahorro"},
                {"fecha": "2025-09-27", "tipo": "interes", "monto": 15.0, "descripcion": "Intereses generados"},
                {"fecha": "2025-09-26", "tipo": "retiro", "monto": -50.0, "descripcion": "Retiro ATM"},
                {"fecha": "2025-08-20", "tipo": "deposito", "monto": 400.0, "descripcion": "Deposito agosto"}
            ],
            "101112": [
                {"fecha": "2025-09-28", "tipo": "deposito", "monto": 800.0, "descripcion": "Deposito salario"},
                {"fecha": "2025-09-27", "tipo": "pago", "monto": -300.0, "descripcion": "Pago hipoteca"},
                {"fecha": "2025-09-26", "tipo": "transferencia", "monto": -100.0, "descripcion": "Transferencia enviada"},
                {"fecha": "2025-08-15", "tipo": "deposito", "monto": 700.0, "descripcion": "Deposito agosto"}
            ]
        }
    
    def _validar_cuenta(self) -> bool:
        """Validar si la cuenta existe"""
        return self.usuario_id in self._datos_cuentas
    
    def consultar_estado_cuenta(self) -> Dict:
        """
        Consultar estado general de la cuenta
        
        Returns:
            Dict con información completa de la cuenta
        """
        if not self._validar_cuenta():
            return {"error": "Cuenta no encontrada"}
        
        datos = self._datos_cuentas[self.usuario_id]
        return {
            "usuario_id": self.usuario_id,
            "tipo": datos["tipo"],
            "saldo_actual": datos["saldo"],
            "limite_diario": datos["limite_diario"],
            "fecha_apertura": datos["fecha_apertura"],
            "estado": datos["estado"],
            "ultima_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def consultar_saldo(self) -> Dict:
        """
        Consultar saldo actual de la cuenta
        
        Returns:
            Dict con información del saldo
        """
        if not self._validar_cuenta():
            return {"error": "Cuenta no encontrada"}
        
        datos = self._datos_cuentas[self.usuario_id]
        return {
            "usuario_id": self.usuario_id,
            "saldo_actual": f"${datos['saldo']:,.2f}",
            "tipo_moneda": "USD",
            "fecha_consulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def consultar_movimientos_recientes(self, dias: int = 7) -> Dict:
        """
        Consultar movimientos recientes de la cuenta
        
        Args:
            dias: Número de días hacia atrás para consultar
            
        Returns:
            Dict con lista de movimientos recientes
        """
        if not self._validar_cuenta():
            return {"error": "Cuenta no encontrada"}
        
        if self.usuario_id not in self._movimientos:
            return {"error": "No hay movimientos disponibles"}
        
        fecha_limite = datetime.now() - timedelta(days=dias)
        movimientos_filtrados = []
        
        for movimiento in self._movimientos[self.usuario_id]:
            fecha_mov = datetime.strptime(movimiento["fecha"], "%Y-%m-%d")
            if fecha_mov >= fecha_limite:
                movimientos_filtrados.append(movimiento)
        
        return {
            "usuario_id": self.usuario_id,
            "periodo_consultado": f"Últimos {dias} días",
            "total_movimientos": len(movimientos_filtrados),
            "movimientos": movimientos_filtrados
        }
    
    def consultar_historial_completo(self) -> Dict:
        """
        Consultar historial completo de movimientos (sin filtro de fecha)
        
        Returns:
            Dict con todos los movimientos históricos
        """
        if not self._validar_cuenta():
            return {"error": "Cuenta no encontrada"}
        
        if self.usuario_id not in self._movimientos:
            return {"error": "No hay movimientos disponibles"}
        
        movimientos = self._movimientos[self.usuario_id]
        
        # Ordenar por fecha descendente (más reciente primero)
        movimientos_ordenados = sorted(
            movimientos, 
            key=lambda x: datetime.strptime(x["fecha"], "%Y-%m-%d"), 
            reverse=True
        )
        
        return {
            "usuario_id": self.usuario_id,
            "periodo_consultado": "Historial completo",
            "total_movimientos": len(movimientos_ordenados),
            "movimientos": movimientos_ordenados
        }
    
    def consultar_resumen_mensual(self, mes: int = 1, año: int = 2024) -> Dict:
        """
        Consultar resumen de movimientos por mes
        
        Args:
            mes: Mes a consultar (1-12)
            año: Año a consultar
            
        Returns:
            Dict con resumen mensual
        """
        if not self._validar_cuenta():
            return {"error": "Cuenta no encontrada"}
        
        if self.usuario_id not in self._movimientos:
            return {"error": "No hay movimientos disponibles"}
        
        movimientos_mes = []
        total_depositos = 0
        total_retiros = 0
        
        for movimiento in self._movimientos[self.usuario_id]:
            fecha_mov = datetime.strptime(movimiento["fecha"], "%Y-%m-%d")
            if fecha_mov.month == mes and fecha_mov.year == año:
                movimientos_mes.append(movimiento)
                if movimiento["monto"] > 0:
                    total_depositos += movimiento["monto"]
                else:
                    total_retiros += abs(movimiento["monto"])
        
        return {
            "usuario_id": self.usuario_id,
            "mes": mes,
            "año": año,
            "total_movimientos": len(movimientos_mes),
            "total_depositos": f"${total_depositos:,.2f}",
            "total_retiros": f"${total_retiros:,.2f}",
            "saldo_final": f"${total_depositos - total_retiros:,.2f}",
            "movimientos": movimientos_mes
        }
    
    def consultar_limite_disponible(self) -> Dict:
        """
        Consultar límite diario disponible
        
        Returns:
            Dict con información de límites
        """
        if not self._validar_cuenta():
            return {"error": "Cuenta no encontrada"}
        
        datos = self._datos_cuentas[self.usuario_id]
        
        # Simular uso del día (en un sistema real vendría de la base de datos)
        uso_diario_simulado = 250.0  # Simulado
        
        return {
            "usuario_id": self.usuario_id,
            "limite_diario": f"${datos['limite_diario']:,.2f}",
            "usado_hoy": f"${uso_diario_simulado:,.2f}",
            "disponible_hoy": f"${datos['limite_diario'] - uso_diario_simulado:,.2f}",
            "fecha_consulta": datetime.now().strftime("%Y-%m-%d")
        }


