"""
Agente Bancario IA - Sistema de consultas bancarias inteligente
Utiliza OpenAI GPT-3.5-turbo para responder consultas sobre cuentas, tarjetas y pólizas
"""

import os
import sys
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Configurar rutas de importación
sys.path.insert(0, str(Path(__file__).parent.parent))

from _utils.security import autenticar_usuario
from _tools import CuentaBancaria, TarjetaBancaria, PolizaSeguro

# Cargar variables de entorno
load_dotenv()

class AgenteBancario:
    """Agente bancario inteligente para consultas de clientes"""
    
    def __init__(self):
        """Inicializar el agente con configuración de LLM y prompt"""
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.prompt = self._cargar_prompt()
    
    def _cargar_prompt(self) -> PromptTemplate:
        """Cargar el template de prompt desde archivo"""
        prompt_path = Path(__file__).parent.parent / "prompts" / "prompt_agente_bancario.txt"
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_text = f.read()

        return PromptTemplate(
            input_variables=["consulta_usuario"],
            template=prompt_text + "\n\nNOTA: El usuario YA está autenticado y verificado. Puedes proporcionar la información solicitada.\nPregunta: {consulta_usuario}"
        )

    def _detectar_intencion(self, consulta: str) -> tuple[str, str]:
        """Detectar el tipo de consulta y subtipo basado en palabras clave"""
        consulta_lower = consulta.lower()

        if "cuenta" in consulta_lower:
            tipo_principal = "cuenta"
            if any(word in consulta_lower for word in ["saldo", "balance"]):
                subtipo = "saldo"
            elif any(word in consulta_lower for word in ["movimiento", "transaccion", "historial"]):
                subtipo = "movimientos"
            elif any(word in consulta_lower for word in ["limite", "límite"]):
                subtipo = "limite"
            else:
                subtipo = "estado"
        
        elif "tarjeta" in consulta_lower:
            tipo_principal = "tarjeta"
            if any(word in consulta_lower for word in ["saldo", "disponible", "balance"]):
                subtipo = "saldo"
            elif any(word in consulta_lower for word in ["movimiento", "transaccion", "historial", "compra"]):
                subtipo = "transacciones"
            elif any(word in consulta_lower for word in ["limite", "límite", "credito", "crédito"]):
                subtipo = "limite"
            elif any(word in consulta_lower for word in ["pago", "minimo", "mínimo", "vencimiento"]):
                subtipo = "pago_minimo"
            else:
                subtipo = "estado"
        
        elif any(word in consulta_lower for word in ["póliza", "poliza", "seguro"]):
            tipo_principal = "poliza"
            if any(word in consulta_lower for word in ["valor", "asegurado"]):
                subtipo = "valor"
            elif any(word in consulta_lower for word in ["pago", "prima", "vencimiento"]):
                subtipo = "pagos"
            elif any(word in consulta_lower for word in ["reclamo", "reclamos"]):
                subtipo = "reclamos"
            elif any(word in consulta_lower for word in ["cobertura", "coberturas"]):
                subtipo = "cobertura"
            else:
                subtipo = "estado"
        else:
            tipo_principal = "general"
            subtipo = "general"
        
        return tipo_principal, subtipo
    
    def _obtener_datos_bancarios(self, tipo_consulta: tuple[str, str], usuario_id: str) -> dict:
        """Obtener datos bancarios según el tipo y subtipo de consulta"""
        tipo_principal, subtipo = tipo_consulta
        
        if tipo_principal == "cuenta":
            cuenta = CuentaBancaria(usuario_id)
            if subtipo == "saldo":
                return cuenta.consultar_saldo()
            elif subtipo == "movimientos":
                return cuenta.consultar_movimientos_recientes()
            elif subtipo == "limite":
                return cuenta.consultar_limite_disponible()
            else:
                return cuenta.consultar_estado_cuenta()
        
        elif tipo_principal == "tarjeta":
            tarjeta = TarjetaBancaria(usuario_id)
            if subtipo == "saldo":
                return tarjeta.consultar_saldo_disponible()
            elif subtipo == "transacciones":
                return tarjeta.consultar_transacciones_recientes()
            elif subtipo == "limite":
                return tarjeta.consultar_limite_disponible()
            elif subtipo == "pago_minimo":
                return tarjeta.consultar_informacion_pago_minimo()
            else:
                return tarjeta.consultar_estado_tarjeta()
        
        elif tipo_principal == "poliza":
            poliza = PolizaSeguro(usuario_id)
            if subtipo == "valor":
                return poliza.consultar_valor_asegurado()
            elif subtipo == "pagos":
                return poliza.consultar_historial_pagos()
            elif subtipo == "reclamos":
                return poliza.consultar_historial_reclamos()
            elif subtipo == "cobertura":
                return poliza.consultar_cobertura_detallada()
            else:
                return poliza.consultar_estado_poliza()
        
        return {}
    
    def _formatear_contexto(self, tipo_consulta: tuple[str, str], datos: dict) -> str:
        """Formatear los datos bancarios como contexto para el LLM"""
        if "error" in datos:
            return ""
        
        tipo_principal, subtipo = tipo_consulta
        
        if tipo_principal == "cuenta":
            if subtipo == "saldo":
                return f"INFORMACIÓN DE SALDO: {datos['saldo_actual']} {datos['tipo_moneda']}, Consultado: {datos['fecha_consulta']}"
            elif subtipo == "movimientos":
                movimientos_str = self._formatear_lista_simple(datos.get('movimientos', []))
                return f"INFORMACIÓN DE MOVIMIENTOS: {datos['periodo_consultado']}, Total movimientos: {datos['total_movimientos']}, Lista: {movimientos_str}"
            elif subtipo == "limite":
                return f"INFORMACIÓN DE LÍMITES: Límite diario: {datos['limite_diario']}, Usado hoy: {datos['usado_hoy']}, Disponible: {datos['disponible_hoy']}"
            else:
                return f"INFORMACIÓN DE CUENTA: Tipo: {datos['tipo']}, Saldo: {datos['saldo_actual']}, Límite diario: {datos['limite_diario']}, Estado: {datos['estado']}"
        
        elif tipo_principal == "tarjeta":
            if subtipo == "saldo":
                if "limite_total" in datos:
                    return f"INFORMACIÓN DE SALDO TARJETA: Límite total: {datos['limite_total']}, Utilizado: {datos['saldo_utilizado']}, Disponible: {datos['credito_disponible']}, Uso: {datos['porcentaje_utilizado']}"
                else:
                    return f"INFORMACIÓN DE SALDO TARJETA: Saldo actual: {datos['saldo_actual']}, Límite diario: {datos['limite_diario']}"
            elif subtipo == "transacciones":
                transacciones_str = self._formatear_lista_simple(datos.get('transacciones', []))
                return f"INFORMACIÓN DE TRANSACCIONES: {datos['periodo_consultado']}, Total: {datos['total_transacciones']}, Lista: {transacciones_str}"
            elif subtipo == "limite":
                if "limite_total" in datos:
                    return f"INFORMACIÓN DE LÍMITES: Límite total: {datos['limite_total']}, Utilizado: {datos['saldo_utilizado']}, Disponible: {datos['credito_disponible']}, Porcentaje: {datos['porcentaje_disponible']}"
                else:
                    return f"INFORMACIÓN DE LÍMITES: Límite diario: {datos['limite_diario']}, Usado hoy: {datos['usado_hoy']}, Disponible: {datos['disponible_hoy']}"
            elif subtipo == "pago_minimo":
                return f"INFORMACIÓN DE PAGO MÍNIMO: Saldo actual: {datos['saldo_actual']}, Pago mínimo: {datos['pago_minimo']}, Vencimiento: {datos['fecha_vencimiento_pago']}, Días restantes: {datos['dias_restantes']}"
            else:
                if datos['tipo'] == "credito":
                    return f"INFORMACIÓN DE TARJETA CRÉDITO: Marca: {datos['marca']}, Número: {datos['numero_tarjeta']}, Límite: {datos['limite_credito']}, Saldo: {datos['saldo_actual']}, Disponible: {datos['credito_disponible']}"
                else:
                    return f"INFORMACIÓN DE TARJETA DÉBITO: Marca: {datos['marca']}, Número: {datos['numero_tarjeta']}, Límite diario: {datos['limite_diario']}, Saldo: {datos['saldo_actual']}"
        
        elif tipo_principal == "poliza":
            if subtipo == "valor":
                return f"INFORMACIÓN DE VALOR ASEGURADO: Número póliza: {datos['numero_poliza']}, Tipo: {datos['tipo_poliza']}, Valor: {datos['valor_asegurado']} {datos['moneda']}"
            elif subtipo == "pagos":
                pagos_str = self._formatear_lista_simple(datos.get('pagos', []))
                return f"INFORMACIÓN DE PAGOS: {datos['periodo_consultado']}, Total pagos: {datos['total_pagos']}, Total pagado: {datos['total_pagado']}, Lista: {pagos_str}"
            elif subtipo == "reclamos":
                reclamos_str = self._formatear_lista_simple(datos.get('reclamos', []))
                return f"INFORMACIÓN DE RECLAMOS: Total reclamos: {datos['total_reclamos']}, Monto total: {datos['total_monto_reclamos']}, Lista: {reclamos_str}"
            elif subtipo == "cobertura":
                return f"INFORMACIÓN DE COBERTURA: Póliza: {datos['numero_poliza']}, Tipo: {datos['tipo_poliza']}, Cobertura general: {datos['cobertura_general']}, Deducible: {datos['deducible']}, Detalles: {datos['coberturas_detalladas']}"
            else:
                return f"INFORMACIÓN DE PÓLIZA: Número: {datos['numero_poliza']}, Tipo: {datos['tipo']}, Valor: {datos['valor_asegurado']}, Prima: {datos['prima_mensual']}, Cobertura: {datos['cobertura']}, Estado: {datos['estado']}"
        
        return ""
    
    def _formatear_lista_simple(self, lista: list) -> str:
        """Formatear una lista de diccionarios de manera simple"""
        if not lista:
            return "Sin registros"
        
        elementos = []
        for item in lista[:5]:  # Limitar a 5 elementos
            if isinstance(item, dict):
                # Formatear solo los campos más importantes
                if 'fecha' in item and 'descripcion' in item:
                    elementos.append(f"{item['fecha']}: {item['descripcion']}")
                elif 'fecha' in item and 'tipo' in item:
                    elementos.append(f"{item['fecha']}: {item['tipo']}")
                else:
                    elementos.append(str(item)[:50] + "...")
            else:
                elementos.append(str(item)[:50])
        
        if len(lista) > 5:
            elementos.append(f"... y {len(lista) - 5} más")
        
        return "; ".join(elementos)
    
    def responder(self, consulta: str, usuario_id: str) -> str:
        """Procesar consulta del usuario y generar respuesta inteligente"""
        tipo_consulta = self._detectar_intencion(consulta)
        datos = self._obtener_datos_bancarios(tipo_consulta, usuario_id)
        
        if "error" in datos:
            return datos["error"]
        
        contexto = self._formatear_contexto(tipo_consulta, datos)
        consulta_completa = f"{consulta}\n{contexto}" if contexto else consulta
        
        return self.llm.invoke(self.prompt.format(consulta_usuario=consulta_completa)).content
    
    def responder_general(self, consulta: str) -> str:
        """Generar respuestas para consultas generales usando el LLM"""
        prompt_path = Path(__file__).parent.parent / "prompts" / "prompt_general.txt"
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()
        
        prompt_general = PromptTemplate(
            input_variables=["consulta"],
            template=prompt_template
        )
        
        try:
            respuesta = self.llm.invoke(prompt_general.format(consulta=consulta)).content
            return respuesta.strip()
        except Exception as e:
            # Respuesta de respaldo si hay error con el LLM
            return "Gracias por tu consulta. Estoy aquí para ayudarte con información sobre nuestros servicios bancarios. Puedo brindarte información sobre horarios, productos, sucursales y contacto. Si necesitas información específica sobre tus cuentas, tarjetas o pólizas, sería necesario que te autentiques. ¿Hay algo específico sobre nuestros servicios que te gustaría conocer?"


class InterfazConsola:
    """Interfaz de consola para interactuar con el agente bancario"""
    
    def __init__(self):
        self.agente = AgenteBancario()
        self.usuario_autenticado = None
        self.usuario_id = None
    
    def _mostrar_saludo_inicial(self):
        """Mostrar saludo inicial y opciones disponibles"""
        print("\n" + "="*60)
        print("BIENVENIDO AL AGENTE VIRTUAL DEL BANCO GUAYAQUIL")
        print("="*60)
        print("\nHola! Soy tu asistente virtual bancario.")
        print("Puedo ayudarte con información general o consultas específicas.")
        print("\nOpciones disponibles:")
        print("  - Consultas generales (sin autenticación)")
        print("  - Consultas de cuentas (requiere autenticación)")
        print("  - Consultas de tarjetas (requiere autenticación)")
        print("  - Consultas de pólizas (requiere autenticación)")
        print("\nEscribe 'salir' para terminar.")
        print("="*60)
    
    def _solicitar_autenticacion(self) -> bool:
        """Proceso de autenticación del usuario"""
        print("\nAUTENTICACIÓN REQUERIDA")
        print("-" * 30)
        print("Para acceder a esta información necesito verificar tu identidad.")
        
        while True:
            print("\nPor favor, ingresa tus credenciales:")
            usuario_id = input("ID de usuario: ").strip()
            token = input("Token de autenticación: ").strip()
            
            if autenticar_usuario(usuario_id, token):
                print("\n- Agente: Autenticación exitosa! Ahora puedes acceder a toda tu información bancaria.")
                self.usuario_autenticado = True
                self.usuario_id = usuario_id
                return True
            else:
                print("\n- Agente: Autenticación fallida. Por favor, verifica tus credenciales.")
                
                respuesta = input("\n¿Deseas intentar nuevamente? (s/n): ").strip().lower()
                if respuesta not in ['s', 'si', 'sí', 'yes', 'y']:
                    print("\n- Agente: Regresando al modo consultas generales.")
                    return False
    
    def _requiere_autenticacion(self, consulta: str) -> bool:
        """Verificar si la consulta requiere autenticación"""
        consulta_lower = consulta.lower()
        palabras_autenticacion = ["cuenta", "tarjeta", "póliza", "poliza", "saldo", "movimiento", "límite", "limite"]
        return any(palabra in consulta_lower for palabra in palabras_autenticacion)
    
    def _procesar_consulta(self, consulta: str):
        """Procesar una consulta individual"""
        if self._requiere_autenticacion(consulta):
            if not self.usuario_autenticado:
                print("\n- Agente: Esta consulta requiere autenticación.")
                if not self._solicitar_autenticacion():
                    print("\n- Agente: Puedo ayudarte con consultas generales sin autenticación.")
                    print("- Agente: Por ejemplo: '¿Qué servicios ofrece el banco?' o '¿Cuáles son los horarios?'")
                    return

            respuesta = self.agente.responder(consulta, self.usuario_id)
            print(f"\n- Agente: {respuesta}")
        else:
            respuesta_general = self.agente.responder_general(consulta)
            print(f"\n- Agente: {respuesta_general}")
    
    def _procesar_sesion(self):
        """Bucle principal de consultas del usuario"""
        while True:
            try:
                consulta = input("\n+ Consulta: ").strip()
                
                if consulta.lower() in ["salir", "exit", "quit", "adios", "adiós", "bye"]:
                    print("\n- Agente: Gracias por usar el Agente Virtual del Banco Guayaquil!")
                    print("- Agente: Que tengas un excelente día!")
                    break
                
                if not consulta:
                    print("\n- Agente: Por favor, ingresa una consulta válida.")
                    continue
                
                self._procesar_consulta(consulta)
                
            except KeyboardInterrupt:
                print("\n\n- Agente: Sesión terminada por el usuario. Hasta la próxima!")
                break
            except Exception as e:
                print(f"\n- Agente: Ocurrió un error inesperado: {e}")
                print("- Agente: Por favor, intenta nuevamente.")
    
    def ejecutar(self):
        """Ejecutar la interfaz completa del agente"""
        try:
            self._mostrar_saludo_inicial()
            print("\n- Agente: Hola! En qué puedo ayudarte hoy?")
            self._procesar_sesion()
        
        except Exception as e:
            print(f"\n- Agente: Error crítico: {e}")
            print("- Agente: Por favor, reinicia la aplicación.")


def main():
    """Punto de entrada principal de la aplicación"""
    interfaz = InterfazConsola()
    interfaz.ejecutar()


if __name__ == "__main__":
    main()