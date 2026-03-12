"""
Motor de estrategias con IA para NOVA-MIND.
Genera recomendaciones estratégicas basadas en el Modelo de Negocio.
"""

from dataclasses import dataclass
from typing import Optional
from .canvas import BusinessCanvas


@dataclass
class StrategyRecommendation:
    """Una recomendación estratégica generada por el motor de IA."""

    title: str
    description: str
    block: str  # Bloque del canvas relacionado
    priority: str  # "alta", "media", "baja"
    impact_areas: list[str]

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "block": self.block,
            "priority": self.priority,
            "impact_areas": self.impact_areas,
        }


# Base de conocimiento de estrategias por bloque del canvas
_STRATEGY_KNOWLEDGE_BASE: dict[str, list[dict]] = {
    "customer_segments": [
        {
            "title": "Segmentación Avanzada con IA",
            "description": (
                "Utiliza algoritmos de clustering para identificar micro-segmentos "
                "de clientes con comportamientos similares, permitiendo mensajes "
                "ultra-personalizados que aumentan la conversión hasta un 40%."
            ),
            "priority": "alta",
            "impact_areas": ["ventas", "marketing", "retención"],
        },
        {
            "title": "Expansión a Nuevos Segmentos",
            "description": (
                "Analiza datos de mercado para detectar segmentos adyacentes "
                "donde tu propuesta de valor puede aplicarse con mínimas adaptaciones."
            ),
            "priority": "media",
            "impact_areas": ["crecimiento", "ingresos"],
        },
    ],
    "value_propositions": [
        {
            "title": "Diferenciación mediante Personalización IA",
            "description": (
                "Implementa un motor de personalización que adapte tu propuesta de "
                "valor en tiempo real según el perfil e historial de cada cliente."
            ),
            "priority": "alta",
            "impact_areas": ["retención", "satisfacción", "ingresos"],
        },
        {
            "title": "Validación Continua de Propuesta de Valor",
            "description": (
                "Establece ciclos de feedback automatizados con tus clientes para "
                "validar y refinar continuamente tu propuesta de valor."
            ),
            "priority": "media",
            "impact_areas": ["producto", "satisfacción"],
        },
    ],
    "channels": [
        {
            "title": "Omnicanalidad Integrada",
            "description": (
                "Centraliza la gestión de todos los canales (digital, físico, social) "
                "en una plataforma unificada con IA para ofrecer experiencias consistentes."
            ),
            "priority": "alta",
            "impact_areas": ["experiencia_cliente", "ventas", "eficiencia"],
        },
        {
            "title": "Canal de Autoservicio Digital",
            "description": (
                "Desarrolla un portal de autoservicio con chatbot IA que resuelva "
                "el 70% de las consultas sin intervención humana, reduciendo costos."
            ),
            "priority": "media",
            "impact_areas": ["costos", "satisfacción", "escalabilidad"],
        },
    ],
    "customer_relationships": [
        {
            "title": "CRM Potenciado con IA Predictiva",
            "description": (
                "Implementa un CRM con modelos predictivos que anticipen necesidades "
                "del cliente, reduzcan churn y generen oportunidades de upsell automáticas."
            ),
            "priority": "alta",
            "impact_areas": ["retención", "ingresos", "satisfacción"],
        },
        {
            "title": "Programa de Fidelización Inteligente",
            "description": (
                "Diseña un programa de lealtad dinámico donde la IA ajusta recompensas "
                "y beneficios en función del comportamiento individual de cada cliente."
            ),
            "priority": "media",
            "impact_areas": ["retención", "lifetime_value"],
        },
    ],
    "revenue_streams": [
        {
            "title": "Modelo de Precios Dinámicos",
            "description": (
                "Implementa pricing dinámico basado en IA que ajuste precios según "
                "demanda, competencia y disposición a pagar de cada segmento, "
                "maximizando el revenue hasta un 25%."
            ),
            "priority": "alta",
            "impact_areas": ["ingresos", "competitividad", "margen"],
        },
        {
            "title": "Nuevas Fuentes de Ingresos Digitales",
            "description": (
                "Identifica oportunidades de monetización de datos y activos digitales "
                "existentes como APIs, informes de inteligencia o servicios premium."
            ),
            "priority": "media",
            "impact_areas": ["ingresos", "diversificación"],
        },
    ],
    "key_resources": [
        {
            "title": "Estrategia de Datos como Activo Estratégico",
            "description": (
                "Implementa una arquitectura de datos centralizada (Data Lake/Warehouse) "
                "que convierta los datos de tu empresa en ventaja competitiva sostenible."
            ),
            "priority": "alta",
            "impact_areas": ["competitividad", "innovación", "eficiencia"],
        },
        {
            "title": "Plataforma Tecnológica Escalable",
            "description": (
                "Migra a una arquitectura cloud-native que permita escalar recursos "
                "bajo demanda y reducir costos de infraestructura hasta un 35%."
            ),
            "priority": "media",
            "impact_areas": ["costos", "escalabilidad", "velocidad"],
        },
    ],
    "key_activities": [
        {
            "title": "Automatización de Procesos con RPA e IA",
            "description": (
                "Identifica y automatiza tareas repetitivas de alto volumen mediante "
                "RPA (Robotic Process Automation) e IA, liberando hasta el 60% "
                "del tiempo de tu equipo para actividades de mayor valor."
            ),
            "priority": "alta",
            "impact_areas": ["eficiencia", "costos", "calidad"],
        },
        {
            "title": "Inteligencia de Negocios en Tiempo Real",
            "description": (
                "Despliega dashboards de BI con alertas inteligentes que permitan "
                "tomar decisiones basadas en datos en tiempo real."
            ),
            "priority": "alta",
            "impact_areas": ["decisiones", "velocidad", "resultados"],
        },
    ],
    "key_partnerships": [
        {
            "title": "Ecosistema de Partners Tecnológicos",
            "description": (
                "Construye alianzas estratégicas con proveedores de IA, plataformas "
                "cloud y startups tecnológicas para acceder a innovación sin desarrollarla internamente."
            ),
            "priority": "media",
            "impact_areas": ["innovación", "costos", "velocidad"],
        },
        {
            "title": "Co-creación con Clientes Clave",
            "description": (
                "Establece programas de co-innovación con tus 20 clientes más estratégicos "
                "para desarrollar soluciones a medida que luego puedas escalar."
            ),
            "priority": "media",
            "impact_areas": ["producto", "retención", "diferenciación"],
        },
    ],
    "cost_structure": [
        {
            "title": "Optimización de Costos con IA",
            "description": (
                "Aplica modelos de IA para analizar y optimizar tu estructura de costos, "
                "identificando ineficiencias ocultas y oportunidades de ahorro inmediatas."
            ),
            "priority": "alta",
            "impact_areas": ["costos", "margen", "eficiencia"],
        },
        {
            "title": "Modelo de Costos Variables Flexible",
            "description": (
                "Transforma costos fijos en variables mediante cloud computing y "
                "outsourcing inteligente, mejorando la resiliencia financiera."
            ),
            "priority": "media",
            "impact_areas": ["costos", "flexibilidad", "riesgo"],
        },
    ],
}


class StrategyEngine:
    """
    Motor de IA para generar estrategias de negocio basadas
    en el Modelo de Negocio de la empresa.
    """

    def analyze(
        self,
        canvas: BusinessCanvas,
        max_recommendations: Optional[int] = None,
    ) -> list[StrategyRecommendation]:
        """
        Analiza el canvas de la empresa y devuelve recomendaciones estratégicas.

        Args:
            canvas: Modelo de negocio de la empresa.
            max_recommendations: Número máximo de recomendaciones a devolver.

        Returns:
            Lista de recomendaciones ordenadas por prioridad.
        """
        recommendations: list[StrategyRecommendation] = []

        block_map = {
            "customer_segments": canvas.customer_segments,
            "value_propositions": canvas.value_propositions,
            "channels": canvas.channels,
            "customer_relationships": canvas.customer_relationships,
            "revenue_streams": canvas.revenue_streams,
            "key_resources": canvas.key_resources,
            "key_activities": canvas.key_activities,
            "key_partnerships": canvas.key_partnerships,
            "cost_structure": canvas.cost_structure,
        }

        block_labels = {
            "customer_segments": "Segmentos de Clientes",
            "value_propositions": "Propuesta de Valor",
            "channels": "Canales",
            "customer_relationships": "Relaciones con Clientes",
            "revenue_streams": "Fuentes de Ingresos",
            "key_resources": "Recursos Clave",
            "key_activities": "Actividades Clave",
            "key_partnerships": "Socios Clave",
            "cost_structure": "Estructura de Costos",
        }

        for block_key, block_values in block_map.items():
            strategies = _STRATEGY_KNOWLEDGE_BASE.get(block_key, [])
            for strategy in strategies:
                # Increase priority for empty blocks (need the most attention)
                priority = strategy["priority"]
                if not block_values and priority == "media":
                    priority = "alta"

                recommendations.append(
                    StrategyRecommendation(
                        title=strategy["title"],
                        description=strategy["description"],
                        block=block_labels[block_key],
                        priority=priority,
                        impact_areas=strategy["impact_areas"],
                    )
                )

        # Sort: alta priority first, then media, then baja
        priority_order = {"alta": 0, "media": 1, "baja": 2}
        recommendations.sort(key=lambda r: priority_order.get(r.priority, 99))

        if max_recommendations is not None:
            recommendations = recommendations[:max_recommendations]

        return recommendations

    def quick_wins(self, canvas: BusinessCanvas) -> list[StrategyRecommendation]:
        """
        Devuelve las 3 recomendaciones de mayor impacto y prioridad
        para resultados rápidos.
        """
        return self.analyze(canvas, max_recommendations=3)
