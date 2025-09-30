"""
Agente Bancario IA - Banco Guayaquil
Sistema inteligente con Function Calling para consultas bancarias
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from dotenv import load_dotenv

# Agregar el directorio raíz al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent_tools import BANKING_TOOLS, ToolExecutor
from _utils.security import autenticar_usuario

load_dotenv()


class AgenteBancario:
    """Agente bancario que usa Function Calling de OpenAI para decidir qué herramientas usar"""
    
    def __init__(self):
        """Inicializar el agente con gpt-4o-mini y herramientas"""
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.conversation_history: List[Any] = []
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """Cargar el prompt del sistema desde archivo"""
        try:
            prompt_path = Path(__file__).parent.parent / "prompts" / "system_prompt.txt"
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            # Fallback si no se encuentra el archivo
            return """Eres un asistente bancario virtual del Banco Guayaquil.

**TU ROL:**
- Ayudar a los clientes con consultas sobre sus cuentas, tarjetas y pólizas
- Usar las herramientas disponibles para obtener información en tiempo real
- Generar respuestas claras, concisas y útiles
- Ser proactivo y ofrecer información relevante

**INSTRUCCIONES IMPORTANTES:**
1. SIEMPRE usa las herramientas disponibles para obtener datos actualizados
2. NO inventes información - solo usa datos de las herramientas
3. Si el usuario pide "más información" o "insights", usa MÚLTIPLES herramientas para dar una respuesta completa
4. Cuando pidan "más", "dime más", "qué más": combina información de varias herramientas para dar contexto completo
5. Para análisis o insights: obtén datos y proporciona análisis significativo
6. Sé conversacional pero preciso
7. Si no estás seguro qué herramienta usar, usa la más general primero

**EJEMPLOS DE USO DE HERRAMIENTAS:**
- "¿Cuál es mi saldo?" → consultar_saldo
- "Dame info de mi cuenta" → consultar_estado_cuenta
- "¿Qué más me puedes decir de mi cuenta?" → consultar_estado_cuenta + consultar_limite_disponible + consultar_movimientos_recientes
- "Dame un insight de mis movimientos" → consultar_historial_completo + análisis de patrones
- "Movimientos de mi cuenta" → consultar_historial_completo (o movimientos_recientes si especifica "recientes")

**FORMATO DE RESPUESTAS:**
- Responde en español natural y conversacional
- Usa emojis moderadamente para claridad (📊 💳 🛡️ ✅ ❌ etc.)
- Organiza información en secciones cuando sea relevante
- Proporciona contexto y análisis cuando sea apropiado
- Si usas múltiples herramientas, integra la información de forma coherente

**LIMITACIONES:**
- NO puedes realizar transferencias, pagos ni modificaciones
- Para esas operaciones, indica al usuario que llame al 1800-BANCO-GUAYAQUIL"""
    
    def procesar_consulta(self, consulta: str, usuario_id: str) -> str:
        """
        Procesar consulta del usuario usando Function Calling
        
        Args:
            consulta: Consulta del usuario
            usuario_id: ID del usuario autenticado
            
        Returns:
            Respuesta del agente
        """
        try:
            # Agregar mensaje del usuario al historial
            self.conversation_history.append(HumanMessage(content=consulta))
            
            # Crear mensajes incluyendo system prompt
            messages = [SystemMessage(content=self.system_prompt)] + self.conversation_history
            
            # Primera llamada al LLM con tools disponibles
            response = self.llm.bind_tools(BANKING_TOOLS).invoke(messages)
            
            # Verificar si el LLM quiere usar herramientas
            if response.tool_calls:
                return self._handle_tool_calls(response, usuario_id)
            else:
                # El LLM respondió directamente
                respuesta = response.content
                self.conversation_history.append(AIMessage(content=respuesta))
                return respuesta
        
        except Exception as e:
            return f"Lo siento, ocurrió un error: {str(e)}"
    
    def _handle_tool_calls(self, response: Any, usuario_id: str) -> str:
        """Manejar las llamadas a herramientas que el LLM decidió usar"""
        executor = ToolExecutor(usuario_id)
        
        # Agregar respuesta del LLM al historial
        self.conversation_history.append(
            AIMessage(content=response.content, tool_calls=response.tool_calls)
        )
        
        # Ejecutar cada herramienta
        for tool_call in response.tool_calls:
            result = executor.execute_tool(tool_call["name"], tool_call["args"])
            
            self.conversation_history.append(
                ToolMessage(
                    content=json.dumps(result, ensure_ascii=False),
                    tool_call_id=tool_call["id"]
                )
            )
        
        # Segunda llamada al LLM para generar respuesta final
        messages = [SystemMessage(content=self.system_prompt)] + self.conversation_history
        final_response = self.llm.invoke(messages)
        
        respuesta_final = final_response.content
        self.conversation_history.append(AIMessage(content=respuesta_final))
        
        return respuesta_final
    
    def reset_conversation(self):
        """Reiniciar la conversación"""
        self.conversation_history = []


# ============================================================================
# INTERFAZ DE CONSOLA
# ============================================================================

class InterfazConsola:
    """Interfaz de consola para interactuar con el agente"""
    
    def __init__(self):
        self.agente = AgenteBancario()
        self.usuario_autenticado = False
        self.usuario_id = None
    
    def _mostrar_saludo_inicial(self):
        """Mostrar saludo inicial"""
        print("\n" + "="*70)
        print("           BANCO GUAYAQUIL - AGENTE VIRTUAL CON IA")
        print("="*70)
        print("\n🤖 ¡Hola! Soy tu asistente bancario inteligente.")
        print("\nPuedo ayudarte con:")
        print("  📊 Cuentas - saldo, movimientos, límites, análisis")
        print("  💳 Tarjetas - estado, transacciones, pagos")
        print("  🛡️  Pólizas - cobertura, pagos, vencimientos")
        print("\n💡 Tip: Puedes preguntarme 'qué más' o pedir 'insights' para análisis")
        print("\nEscribe 'salir' para terminar.")
        print("="*70)
    
    def _solicitar_autenticacion(self) -> bool:
        """Solicitar autenticación del usuario"""
        print("\n🔐 AUTENTICACIÓN REQUERIDA")
        print("-" * 70)
        
        while True:
            print("\nCredenciales:")
            usuario_id = input("  ID de usuario: ").strip()
            token = input("  Token: ").strip()
            
            if autenticar_usuario(usuario_id, token):
                print("\n✅ ¡Autenticación exitosa!")
                self.usuario_autenticado = True
                self.usuario_id = usuario_id
                return True
            else:
                print("\n❌ Credenciales incorrectas.")
                respuesta = input("\n¿Reintentar? (s/n): ").strip().lower()
                if respuesta not in ['s', 'si', 'sí', 'yes', 'y']:
                    return False
    
    def _procesar_sesion(self):
        """Bucle principal de consultas"""
        while True:
            try:
                consulta = input("\n💬 Tú: ").strip()
                
                if consulta.lower() in ["salir", "exit", "quit", "adiós", "bye"]:
                    print("\n👋 ¡Gracias por usar Banco Guayaquil! Que tengas un excelente día.")
                    break
                
                if not consulta:
                    continue
                
                # Procesar consulta
                respuesta = self.agente.procesar_consulta(consulta, self.usuario_id)
                print(f"\n🤖 Agente: {respuesta}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Sesión terminada. ¡Hasta pronto!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    def ejecutar(self):
        """Ejecutar la interfaz completa"""
        self._mostrar_saludo_inicial()
        
        if not self._solicitar_autenticacion():
            print("\n⚠️  No se pudo autenticar. Cerrando sesión.")
            return
        
        print("\n🤖 Agente: ¡Perfecto! ¿En qué puedo ayudarte hoy?")
        self._procesar_sesion()


def main():
    """Punto de entrada principal"""
    interfaz = InterfazConsola()
    interfaz.ejecutar()


if __name__ == "__main__":
    main()
