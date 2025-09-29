"""
Módulo de gestión de tarjetas bancarias
Implementa funcionalidades completas para consulta y gestión de tarjetas de crédito y débito
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta


class TarjetaBancaria:
    """Clase para gestión completa de tarjetas bancarias"""
    
    def __init__(self, usuario_id: str):
        """
        Inicializar tarjeta bancaria
        
        Args:
            usuario_id: Identificador único del usuario
        """
        self.usuario_id = usuario_id
        self._datos_tarjetas = self._cargar_datos_tarjetas()
        self._transacciones = self._cargar_transacciones()
    
    def _cargar_datos_tarjetas(self) -> Dict[str, Dict]:
        """Cargar datos base de las tarjetas"""
        return {
            "123456": {
                "tipo": "credito",
                "marca": "visa",
                "numero_tarjeta": "****1234",
                "limite_credito": 5000.0,
                "saldo_actual": 2500.0,
                "fecha_vencimiento": "2027-12-31",
                "estado": "activa",
                "tasa_interes": 18.5
            },
            "456789": {
                "tipo": "debito",
                "marca": "mastercard",
                "numero_tarjeta": "****5678",
                "limite_diario": 2000.0,
                "saldo_actual": 500.0,
                "fecha_vencimiento": "2026-08-31",
                "estado": "activa",
                "tasa_interes": 0.0
            },
            "789101": {
                "tipo": "debito",
                "marca": "visa",
                "numero_tarjeta": "****9012",
                "limite_diario": 1500.0,
                "saldo_actual": 1000.0,
                "fecha_vencimiento": "2026-05-31",
                "estado": "activa",
                "tasa_interes": 0.0
            },
            "101112": {
                "tipo": "credito",
                "marca": "mastercard",
                "numero_tarjeta": "****3456",
                "limite_credito": 8000.0,
                "saldo_actual": 2000.0,
                "fecha_vencimiento": "2028-03-31",
                "estado": "activa",
                "tasa_interes": 16.9
            }
        }
    
    def _cargar_transacciones(self) -> Dict[str, List[Dict]]:
        """Cargar historial de transacciones por usuario"""
        return {
            "123456": [
                {"fecha": "2024-01-15", "tipo": "compra", "monto": -150.0, "descripcion": "Supermercado ABC", "establecimiento": "ABC Store"},
                {"fecha": "2024-01-14", "tipo": "compra", "monto": -75.0, "descripcion": "Gasolinera XYZ", "establecimiento": "Shell"},
                {"fecha": "2024-01-13", "tipo": "pago", "monto": 500.0, "descripcion": "Pago mensual", "establecimiento": "Online"},
                {"fecha": "2024-01-12", "tipo": "compra", "monto": -300.0, "descripcion": "Tienda departamental", "establecimiento": "Sears"},
                {"fecha": "2024-01-11", "tipo": "interes", "monto": -45.0, "descripcion": "Intereses mensuales", "establecimiento": "Banco"}
            ],
            "456789": [
                {"fecha": "2024-01-15", "tipo": "retiro", "monto": -100.0, "descripcion": "Retiro ATM", "establecimiento": "ATM Plaza"},
                {"fecha": "2024-01-14", "tipo": "compra", "monto": -50.0, "descripcion": "Farmacia", "establecimiento": "Fybeca"},
                {"fecha": "2024-01-13", "tipo": "compra", "monto": -25.0, "descripcion": "Restaurante", "establecimiento": "McDonald's"},
                {"fecha": "2024-01-12", "tipo": "deposito", "monto": 300.0, "descripcion": "Deposito", "establecimiento": "Cajero"}
            ],
            "789101": [
                {"fecha": "2024-01-15", "tipo": "compra", "monto": -80.0, "descripcion": "Tienda de ropa", "establecimiento": "Zara"},
                {"fecha": "2024-01-14", "tipo": "compra", "monto": -120.0, "descripcion": "Electrónicos", "establecimiento": "Best Buy"},
                {"fecha": "2024-01-13", "tipo": "retiro", "monto": -60.0, "descripcion": "Retiro ATM", "establecimiento": "ATM Mall"}
            ],
            "101112": [
                {"fecha": "2024-01-15", "tipo": "compra", "monto": -200.0, "descripcion": "Vuelos", "establecimiento": "Avianca"},
                {"fecha": "2024-01-14", "tipo": "compra", "monto": -150.0, "descripcion": "Hotel", "establecimiento": "Marriott"},
                {"fecha": "2024-01-13", "tipo": "pago", "monto": 800.0, "descripcion": "Pago mensual", "establecimiento": "Online"}
            ]
        }
    
    def _validar_tarjeta(self) -> bool:
        """Validar si la tarjeta existe"""
        return self.usuario_id in self._datos_tarjetas
    
    def consultar_estado_tarjeta(self) -> Dict:
        """
        Consultar estado general de la tarjeta
        
        Returns:
            Dict con información completa de la tarjeta
        """
        if not self._validar_tarjeta():
            return {"error": "Tarjeta no encontrada"}
        
        datos = self._datos_tarjetas[self.usuario_id]
        
        if datos["tipo"] == "credito":
            disponible = datos["limite_credito"] - datos["saldo_actual"]
            return {
                "usuario_id": self.usuario_id,
                "tipo": datos["tipo"],
                "marca": datos["marca"],
                "numero_tarjeta": datos["numero_tarjeta"],
                "limite_credito": f"${datos['limite_credito']:,.2f}",
                "saldo_actual": f"${datos['saldo_actual']:,.2f}",
                "credito_disponible": f"${disponible:,.2f}",
                "fecha_vencimiento": datos["fecha_vencimiento"],
                "tasa_interes": f"{datos['tasa_interes']}%",
                "estado": datos["estado"]
            }
        else:  # débito
            return {
                "usuario_id": self.usuario_id,
                "tipo": datos["tipo"],
                "marca": datos["marca"],
                "numero_tarjeta": datos["numero_tarjeta"],
                "limite_diario": f"${datos['limite_diario']:,.2f}",
                "saldo_actual": f"${datos['saldo_actual']:,.2f}",
                "fecha_vencimiento": datos["fecha_vencimiento"],
                "estado": datos["estado"]
            }
    
    def consultar_saldo_disponible(self) -> Dict:
        """
        Consultar saldo disponible en la tarjeta
        
        Returns:
            Dict con información del saldo disponible
        """
        if not self._validar_tarjeta():
            return {"error": "Tarjeta no encontrada"}
        
        datos = self._datos_tarjetas[self.usuario_id]
        
        if datos["tipo"] == "credito":
            disponible = datos["limite_credito"] - datos["saldo_actual"]
            return {
                "usuario_id": self.usuario_id,
                "tipo_tarjeta": datos["tipo"],
                "limite_total": f"${datos['limite_credito']:,.2f}",
                "saldo_utilizado": f"${datos['saldo_actual']:,.2f}",
                "credito_disponible": f"${disponible:,.2f}",
                "porcentaje_utilizado": f"{(datos['saldo_actual'] / datos['limite_credito']) * 100:.1f}%"
            }
        else:  # débito
            return {
                "usuario_id": self.usuario_id,
                "tipo_tarjeta": datos["tipo"],
                "saldo_actual": f"${datos['saldo_actual']:,.2f}",
                "limite_diario": f"${datos['limite_diario']:,.2f}"
            }
    
    def consultar_transacciones_recientes(self, dias: int = 7) -> Dict:
        """
        Consultar transacciones recientes de la tarjeta
        
        Args:
            dias: Número de días hacia atrás para consultar
            
        Returns:
            Dict con lista de transacciones recientes
        """
        if not self._validar_tarjeta():
            return {"error": "Tarjeta no encontrada"}
        
        if self.usuario_id not in self._transacciones:
            return {"error": "No hay transacciones disponibles"}
        
        fecha_limite = datetime.now() - timedelta(days=dias)
        transacciones_filtradas = []
        
        for transaccion in self._transacciones[self.usuario_id]:
            fecha_trans = datetime.strptime(transaccion["fecha"], "%Y-%m-%d")
            if fecha_trans >= fecha_limite:
                transacciones_filtradas.append(transaccion)
        
        return {
            "usuario_id": self.usuario_id,
            "periodo_consultado": f"Últimos {dias} días",
            "total_transacciones": len(transacciones_filtradas),
            "transacciones": transacciones_filtradas
        }
    
    def consultar_resumen_mensual(self, mes: int = 1, año: int = 2024) -> Dict:
        """
        Consultar resumen de transacciones por mes
        
        Args:
            mes: Mes a consultar (1-12)
            año: Año a consultar
            
        Returns:
            Dict con resumen mensual
        """
        if not self._validar_tarjeta():
            return {"error": "Tarjeta no encontrada"}
        
        if self.usuario_id not in self._transacciones:
            return {"error": "No hay transacciones disponibles"}
        
        transacciones_mes = []
        total_compras = 0
        total_pagos = 0
        total_intereses = 0
        
        for transaccion in self._transacciones[self.usuario_id]:
            fecha_trans = datetime.strptime(transaccion["fecha"], "%Y-%m-%d")
            if fecha_trans.month == mes and fecha_trans.year == año:
                transacciones_mes.append(transaccion)
                
                if transaccion["tipo"] == "compra" or transaccion["tipo"] == "retiro":
                    total_compras += abs(transaccion["monto"])
                elif transaccion["tipo"] == "pago" or transaccion["tipo"] == "deposito":
                    total_pagos += transaccion["monto"]
                elif transaccion["tipo"] == "interes":
                    total_intereses += abs(transaccion["monto"])
        
        return {
            "usuario_id": self.usuario_id,
            "mes": mes,
            "año": año,
            "total_transacciones": len(transacciones_mes),
            "total_compras": f"${total_compras:,.2f}",
            "total_pagos": f"${total_pagos:,.2f}",
            "total_intereses": f"${total_intereses:,.2f}",
            "transacciones": transacciones_mes
        }
    
    def consultar_limite_disponible(self) -> Dict:
        """
        Consultar límite disponible en la tarjeta
        
        Returns:
            Dict con información de límites
        """
        if not self._validar_tarjeta():
            return {"error": "Tarjeta no encontrada"}
        
        datos = self._datos_tarjetas[self.usuario_id]
        
        if datos["tipo"] == "credito":
            disponible = datos["limite_credito"] - datos["saldo_actual"]
            return {
                "usuario_id": self.usuario_id,
                "tipo_tarjeta": datos["tipo"],
                "limite_total": f"${datos['limite_credito']:,.2f}",
                "saldo_utilizado": f"${datos['saldo_actual']:,.2f}",
                "credito_disponible": f"${disponible:,.2f}",
                "porcentaje_disponible": f"{(disponible / datos['limite_credito']) * 100:.1f}%"
            }
        else:  # débito
            # Simular uso del día
            uso_diario_simulado = 150.0
            return {
                "usuario_id": self.usuario_id,
                "tipo_tarjeta": datos["tipo"],
                "limite_diario": f"${datos['limite_diario']:,.2f}",
                "usado_hoy": f"${uso_diario_simulado:,.2f}",
                "disponible_hoy": f"${datos['limite_diario'] - uso_diario_simulado:,.2f}"
            }
    
    def consultar_informacion_pago_minimo(self) -> Dict:
        """
        Consultar información de pago mínimo (solo tarjetas de crédito)
        
        Returns:
            Dict con información de pago mínimo
        """
        if not self._validar_tarjeta():
            return {"error": "Tarjeta no encontrada"}
        
        datos = self._datos_tarjetas[self.usuario_id]
        
        if datos["tipo"] != "credito":
            return {"error": "Esta función solo aplica para tarjetas de crédito"}
        
        # Calcular pago mínimo (ejemplo: 3% del saldo o $25, lo que sea mayor)
        pago_minimo_porcentaje = datos["saldo_actual"] * 0.03
        pago_minimo = max(pago_minimo_porcentaje, 25.0)
        
        # Fecha de vencimiento del pago (ejemplo: 25 del mes siguiente)
        fecha_vencimiento = datetime.now().replace(day=25)
        if fecha_vencimiento.day > 25:
            fecha_vencimiento = fecha_vencimiento.replace(month=fecha_vencimiento.month + 1)
        
        return {
            "usuario_id": self.usuario_id,
            "saldo_actual": f"${datos['saldo_actual']:,.2f}",
            "pago_minimo": f"${pago_minimo:,.2f}",
            "fecha_vencimiento_pago": fecha_vencimiento.strftime("%Y-%m-%d"),
            "tasa_interes": f"{datos['tasa_interes']}%",
            "dias_restantes": (fecha_vencimiento - datetime.now()).days
        }


