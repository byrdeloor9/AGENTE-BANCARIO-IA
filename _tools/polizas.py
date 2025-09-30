"""
Módulo de gestión de pólizas de seguro
Implementa funcionalidades completas para consulta y gestión de pólizas de seguro
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta


class PolizaSeguro:
    """Clase para gestión completa de pólizas de seguro"""
    
    def __init__(self, usuario_id: str):
        """
        Inicializar póliza de seguro
        
        Args:
            usuario_id: Identificador único del usuario
        """
        self.usuario_id = usuario_id
        self._datos_polizas = self._cargar_datos_polizas()
        self._historial_pagos = self._cargar_historial_pagos()
        self._reclamos = self._cargar_reclamos()
    
    def _cargar_datos_polizas(self) -> Dict[str, Dict]:
        """Cargar datos base de las pólizas"""
        return {
            "123456": {
                "tipo": "hogar",
                "numero_poliza": "POL-HOG-2024-001",
                "valor_asegurado": 123456.0,
                "prima_mensual": 85.50,
                "fecha_vencimiento": "2026-01-01",
                "tasa_interes": 6.0,
                "estado": "activa",
                "cobertura": "Completa",
                "fecha_inicio": "2024-01-01",
                "deducible": 500.0
            },
            "456789": {
                "tipo": "auto",
                "numero_poliza": "POL-AUTO-2024-002",
                "valor_asegurado": 456789.0,
                "prima_mensual": 125.75,
                "fecha_vencimiento": "2027-01-01",
                "tasa_interes": 7.0,
                "estado": "activa",
                "cobertura": "Responsabilidad Civil + Daños Materiales",
                "fecha_inicio": "2024-01-01",
                "deducible": 250.0
            },
            "789101": {
                "tipo": "hogar",
                "numero_poliza": "POL-HOG-2024-003",
                "valor_asegurado": 789101.0,
                "prima_mensual": 110.25,
                "fecha_vencimiento": "2028-01-01",
                "tasa_interes": 8.0,
                "estado": "activa",
                "cobertura": "Completa + Robo",
                "fecha_inicio": "2024-01-01",
                "deducible": 750.0
            },
            "101112": {
                "tipo": "auto",
                "numero_poliza": "POL-AUTO-2024-004",
                "valor_asegurado": 101112.0,
                "prima_mensual": 95.00,
                "fecha_vencimiento": "2029-01-01",
                "tasa_interes": 10.0,
                "estado": "activa",
                "cobertura": "Responsabilidad Civil",
                "fecha_inicio": "2024-01-01",
                "deducible": 300.0
            }
        }
    
    def _cargar_historial_pagos(self) -> Dict[str, List[Dict]]:
        """Cargar historial de pagos por usuario (actualizados a 2025)"""
        return {
            "123456": [
                {"fecha": "2025-09-01", "monto": 85.50, "estado": "pagado", "metodo": "Débito automático", "periodo": "Septiembre 2025"},
                {"fecha": "2025-08-01", "monto": 85.50, "estado": "pagado", "metodo": "Débito automático", "periodo": "Agosto 2025"},
                {"fecha": "2025-07-01", "monto": 85.50, "estado": "pagado", "metodo": "Transferencia", "periodo": "Julio 2025"},
                {"fecha": "2025-06-01", "monto": 85.50, "estado": "pagado", "metodo": "Débito automático", "periodo": "Junio 2025"},
                {"fecha": "2025-05-01", "monto": 85.50, "estado": "pagado", "metodo": "Débito automático", "periodo": "Mayo 2025"},
                {"fecha": "2025-04-01", "monto": 85.50, "estado": "pagado", "metodo": "Débito automático", "periodo": "Abril 2025"}
            ],
            "456789": [
                {"fecha": "2025-09-01", "monto": 125.75, "estado": "pagado", "metodo": "Débito automático", "periodo": "Septiembre 2025"},
                {"fecha": "2025-08-01", "monto": 125.75, "estado": "pagado", "metodo": "Débito automático", "periodo": "Agosto 2025"},
                {"fecha": "2025-07-01", "monto": 125.75, "estado": "pagado", "metodo": "Transferencia", "periodo": "Julio 2025"},
                {"fecha": "2025-06-01", "monto": 125.75, "estado": "pagado", "metodo": "Débito automático", "periodo": "Junio 2025"},
                {"fecha": "2025-05-01", "monto": 125.75, "estado": "pagado", "metodo": "Débito automático", "periodo": "Mayo 2025"}
            ],
            "789101": [
                {"fecha": "2025-09-01", "monto": 110.25, "estado": "pagado", "metodo": "Débito automático", "periodo": "Septiembre 2025"},
                {"fecha": "2025-08-01", "monto": 110.25, "estado": "pagado", "metodo": "Débito automático", "periodo": "Agosto 2025"},
                {"fecha": "2025-07-01", "monto": 110.25, "estado": "pagado", "metodo": "Transferencia", "periodo": "Julio 2025"},
                {"fecha": "2025-06-01", "monto": 110.25, "estado": "pagado", "metodo": "Débito automático", "periodo": "Junio 2025"}
            ],
            "101112": [
                {"fecha": "2025-09-01", "monto": 95.00, "estado": "pagado", "metodo": "Débito automático", "periodo": "Septiembre 2025"},
                {"fecha": "2025-08-01", "monto": 95.00, "estado": "pagado", "metodo": "Débito automático", "periodo": "Agosto 2025"},
                {"fecha": "2025-07-01", "monto": 95.00, "estado": "pagado", "metodo": "Transferencia", "periodo": "Julio 2025"},
                {"fecha": "2025-06-01", "monto": 95.00, "estado": "pagado", "metodo": "Débito automático", "periodo": "Junio 2025"}
            ]
        }
    
    def _cargar_reclamos(self) -> Dict[str, List[Dict]]:
        """Cargar historial de reclamos por usuario"""
        return {
            "123456": [
                {"numero_reclamo": "REC-2024-001", "fecha": "2024-01-10", "tipo": "Robo", "monto": 1500.0, "estado": "Aprobado", "descripcion": "Robo de electrodomésticos"},
                {"numero_reclamo": "REC-2023-045", "fecha": "2023-11-15", "tipo": "Daño por agua", "monto": 800.0, "estado": "Pagado", "descripcion": "Daños por filtración"}
            ],
            "456789": [
                {"numero_reclamo": "REC-2024-002", "fecha": "2024-01-12", "tipo": "Choque", "monto": 2500.0, "estado": "En proceso", "descripcion": "Colisión trasera"},
                {"numero_reclamo": "REC-2023-078", "fecha": "2023-10-20", "tipo": "Granizo", "monto": 1200.0, "estado": "Aprobado", "descripcion": "Daños por granizo"}
            ],
            "789101": [
                {"numero_reclamo": "REC-2023-092", "fecha": "2023-12-05", "tipo": "Incendio", "monto": 5000.0, "estado": "Aprobado", "descripcion": "Daños menores por incendio"}
            ],
            "101112": []
        }
    
    def _validar_poliza(self) -> bool:
        """Validar si la póliza existe"""
        return self.usuario_id in self._datos_polizas
    
    def consultar_estado_poliza(self) -> Dict:
        """
        Consultar estado general de la póliza
        
        Returns:
            Dict con información completa de la póliza
        """
        if not self._validar_poliza():
            return {"error": "Poliza no encontrada"}
        
        datos = self._datos_polizas[self.usuario_id]
        fecha_vencimiento = datetime.strptime(datos["fecha_vencimiento"], "%Y-%m-%d")
        dias_restantes = (fecha_vencimiento - datetime.now()).days
        
        return {
            "usuario_id": self.usuario_id,
            "numero_poliza": datos["numero_poliza"],
            "tipo": datos["tipo"],
            "valor_asegurado": f"${datos['valor_asegurado']:,.2f}",
            "prima_mensual": f"${datos['prima_mensual']:,.2f}",
            "fecha_vencimiento": datos["fecha_vencimiento"],
            "tasa_interes": f"{datos['tasa_interes']}%",
            "estado": datos["estado"],
            "cobertura": datos["cobertura"],
            "fecha_inicio": datos["fecha_inicio"],
            "deducible": f"${datos['deducible']:,.2f}",
            "dias_restantes": dias_restantes
        }
    
    def consultar_valor_asegurado(self) -> Dict:
        """
        Consultar valor asegurado de la póliza
        
        Returns:
            Dict con información del valor asegurado
        """
        if not self._validar_poliza():
            return {"error": "Poliza no encontrada"}
        
        datos = self._datos_polizas[self.usuario_id]
        return {
            "usuario_id": self.usuario_id,
            "numero_poliza": datos["numero_poliza"],
            "tipo_poliza": datos["tipo"],
            "valor_asegurado": f"${datos['valor_asegurado']:,.2f}",
            "moneda": "USD",
            "fecha_consulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def consultar_historial_pagos(self, meses: int = 6) -> Dict:
        """
        Consultar historial de pagos de la póliza
        
        Args:
            meses: Número de meses hacia atrás para consultar
            
        Returns:
            Dict con historial de pagos
        """
        if not self._validar_poliza():
            return {"error": "Poliza no encontrada"}
        
        if self.usuario_id not in self._historial_pagos:
            return {"error": "No hay historial de pagos disponible"}
        
        fecha_limite = datetime.now() - timedelta(days=meses * 30)
        pagos_filtrados = []
        total_pagado = 0
        
        for pago in self._historial_pagos[self.usuario_id]:
            fecha_pago = datetime.strptime(pago["fecha"], "%Y-%m-%d")
            if fecha_pago >= fecha_limite:
                pagos_filtrados.append(pago)
                if pago["estado"] == "pagado":
                    total_pagado += pago["monto"]
        
        return {
            "usuario_id": self.usuario_id,
            "periodo_consultado": f"Últimos {meses} meses",
            "total_pagos": len(pagos_filtrados),
            "total_pagado": f"${total_pagado:,.2f}",
            "pagos": pagos_filtrados
        }
    
    def consultar_proximo_vencimiento(self) -> Dict:
        """
        Consultar información del próximo vencimiento
        
        Returns:
            Dict con información del próximo vencimiento
        """
        if not self._validar_poliza():
            return {"error": "Poliza no encontrada"}
        
        datos = self._datos_polizas[self.usuario_id]
        
        # Calcular próximo pago (primer día del mes siguiente)
        hoy = datetime.now()
        if hoy.month == 12:
            proximo_mes = hoy.replace(year=hoy.year + 1, month=1, day=1)
        else:
            proximo_mes = hoy.replace(month=hoy.month + 1, day=1)
        
        dias_restantes = (proximo_mes - hoy).days
        
        return {
            "usuario_id": self.usuario_id,
            "numero_poliza": datos["numero_poliza"],
            "proximo_pago": f"${datos['prima_mensual']:,.2f}",
            "fecha_vencimiento": proximo_mes.strftime("%Y-%m-%d"),
            "dias_restantes": dias_restantes,
            "estado_pago": "Pendiente" if dias_restantes > 0 else "Vencido"
        }
    
    def consultar_historial_reclamos(self) -> Dict:
        """
        Consultar historial de reclamos
        
        Returns:
            Dict con historial de reclamos
        """
        if not self._validar_poliza():
            return {"error": "Poliza no encontrada"}
        
        if self.usuario_id not in self._reclamos:
            return {"error": "No hay reclamos disponibles"}
        
        reclamos = self._reclamos[self.usuario_id]
        total_reclamos = len(reclamos)
        total_monto = sum(reclamo["monto"] for reclamo in reclamos)
        
        return {
            "usuario_id": self.usuario_id,
            "total_reclamos": total_reclamos,
            "total_monto_reclamos": f"${total_monto:,.2f}",
            "reclamos": reclamos
        }
    
    def consultar_cobertura_detallada(self) -> Dict:
        """
        Consultar cobertura detallada de la póliza
        
        Returns:
            Dict con información detallada de cobertura
        """
        if not self._validar_poliza():
            return {"error": "Poliza no encontrada"}
        
        datos = self._datos_polizas[self.usuario_id]
        
        # Coberturas específicas según el tipo de póliza
        coberturas_detalladas = {
            "hogar": {
                "incendio": "Cobertura completa",
                "robo": "Hasta $50,000",
                "daños_agua": "Cobertura completa",
                "responsabilidad_civil": "Hasta $100,000",
                "gastos_medicos": "Hasta $5,000"
            },
            "auto": {
                "responsabilidad_civil": "Hasta $300,000",
                "daños_materiales": "Valor comercial",
                "gastos_medicos": "Hasta $10,000",
                "robo": "Valor comercial",
                "granizo": "Valor comercial"
            }
        }
        
        return {
            "usuario_id": self.usuario_id,
            "numero_poliza": datos["numero_poliza"],
            "tipo_poliza": datos["tipo"],
            "cobertura_general": datos["cobertura"],
            "deducible": f"${datos['deducible']:,.2f}",
            "coberturas_detalladas": coberturas_detalladas.get(datos["tipo"], {}),
            "valor_asegurado": f"${datos['valor_asegurado']:,.2f}"
        }


