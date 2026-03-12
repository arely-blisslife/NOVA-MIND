"""
Motor de automatizaciones con IA para NOVA-MIND.
Identifica y genera recomendaciones de automatización para empresas.
"""

from dataclasses import dataclass
from typing import Optional
from .canvas import BusinessCanvas


@dataclass
class AutomationOpportunity:
    """Una oportunidad de automatización identificada por el motor de IA."""

    title: str
    description: str
    process: str          # Proceso o área de negocio
    technology: str       # Tecnología sugerida (RPA, IA, etc.)
    effort: str           # "bajo", "medio", "alto"
    roi_estimate: str     # Estimado de retorno
    steps: list[str]      # Pasos para implementar

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "process": self.process,
            "technology": self.technology,
            "effort": self.effort,
            "roi_estimate": self.roi_estimate,
            "steps": self.steps,
        }


# Base de conocimiento de automatizaciones por área
_AUTOMATION_KNOWLEDGE_BASE: list[dict] = [
    {
        "title": "Automatización de Atención al Cliente con Chatbot IA",
        "description": (
            "Implementa un asistente virtual inteligente que atienda el 70% de "
            "las consultas frecuentes 24/7, sin intervención humana, reduciendo "
            "tiempos de respuesta de horas a segundos."
        ),
        "process": "Atención al Cliente",
        "technology": "IA Conversacional (LLM + NLP)",
        "effort": "medio",
        "roi_estimate": "Reducción de 60-70% en costos de soporte en 6 meses",
        "steps": [
            "Mapear las 50 preguntas más frecuentes de clientes",
            "Seleccionar plataforma de chatbot (ej. Dialogflow, OpenAI API)",
            "Entrenar el modelo con historial de conversaciones",
            "Integrar con canales existentes (web, WhatsApp, email)",
            "Configurar escalamiento a humanos para casos complejos",
            "Medir y optimizar con métricas de satisfacción (CSAT)",
        ],
        "canvas_blocks": ["channels", "customer_relationships"],
    },
    {
        "title": "Pipeline de Ventas Automatizado con IA Predictiva",
        "description": (
            "Automatiza la calificación de leads, seguimiento y nurturing con "
            "IA predictiva que identifica las oportunidades con mayor probabilidad "
            "de cierre, aumentando la tasa de conversión hasta un 35%."
        ),
        "process": "Ventas y CRM",
        "technology": "Machine Learning + CRM Automation",
        "effort": "medio",
        "roi_estimate": "Aumento de 25-35% en tasa de cierre en 3 meses",
        "steps": [
            "Auditar el CRM actual e identificar datos disponibles",
            "Definir criterios de lead scoring con el equipo comercial",
            "Implementar modelo predictivo de probabilidad de cierre",
            "Configurar secuencias de email/WhatsApp automatizadas",
            "Crear alertas inteligentes para el equipo de ventas",
            "Monitorear KPIs: tasa de conversión, ciclo de venta, revenue",
        ],
        "canvas_blocks": ["customer_segments", "revenue_streams", "customer_relationships"],
    },
    {
        "title": "Generación de Contenido y Marketing con IA",
        "description": (
            "Automatiza la creación de contenido de marketing (emails, posts, "
            "anuncios) personalizado para cada segmento usando IA generativa, "
            "reduciendo el tiempo de producción en un 80%."
        ),
        "process": "Marketing y Comunicación",
        "technology": "IA Generativa (LLM)",
        "effort": "bajo",
        "roi_estimate": "Reducción de 80% en tiempo de producción de contenido",
        "steps": [
            "Definir guía de voz y tono de la marca",
            "Seleccionar plataforma de IA generativa (ej. OpenAI, Claude)",
            "Crear plantillas y prompts por tipo de contenido",
            "Integrar con herramientas de publicación (Hootsuite, Mailchimp)",
            "Establecer flujo de revisión humana mínima",
            "Analizar métricas de engagement para optimizar prompts",
        ],
        "canvas_blocks": ["channels", "customer_segments", "value_propositions"],
    },
    {
        "title": "Automatización de Facturación y Cobros",
        "description": (
            "Automatiza el ciclo completo de facturación, recordatorios de pago "
            "y conciliación contable, eliminando errores manuales y reduciendo "
            "días de cartera vencida."
        ),
        "process": "Finanzas y Administración",
        "technology": "RPA + OCR + Integración Contable",
        "effort": "medio",
        "roi_estimate": "Reducción de 90% en tiempo administrativo, -30% días cartera",
        "steps": [
            "Mapear proceso actual de facturación de inicio a fin",
            "Seleccionar herramienta RPA (ej. UiPath, Automation Anywhere)",
            "Automatizar generación y envío de facturas",
            "Configurar recordatorios automáticos de cobro por escalonamiento",
            "Integrar con sistema contable para conciliación automática",
            "Establecer reportes automáticos de flujo de caja",
        ],
        "canvas_blocks": ["revenue_streams", "cost_structure"],
    },
    {
        "title": "Monitoreo y Alertas Inteligentes de Negocio",
        "description": (
            "Implementa un sistema de Business Intelligence con IA que monitoree "
            "KPIs críticos 24/7 y envíe alertas proactivas cuando se detecten "
            "anomalías o tendencias relevantes."
        ),
        "process": "Inteligencia de Negocios",
        "technology": "BI + Detección de Anomalías con ML",
        "effort": "medio",
        "roi_estimate": "Detección 10x más rápida de problemas, decisiones en tiempo real",
        "steps": [
            "Definir los 10-15 KPIs más críticos del negocio",
            "Centralizar fuentes de datos en un Data Warehouse",
            "Implementar dashboards en tiempo real (ej. Power BI, Tableau)",
            "Configurar modelos de detección de anomalías",
            "Establecer canales de alerta (email, Slack, WhatsApp)",
            "Crear reportes ejecutivos automáticos semanales/mensuales",
        ],
        "canvas_blocks": ["key_activities", "key_resources"],
    },
    {
        "title": "Automatización de Recursos Humanos y Onboarding",
        "description": (
            "Digitaliza y automatiza el proceso de selección, onboarding y gestión "
            "de empleados, reduciendo el tiempo de contratación en un 50% y mejorando "
            "la experiencia del colaborador."
        ),
        "process": "Recursos Humanos",
        "technology": "ATS con IA + Workflows Automatizados",
        "effort": "medio",
        "roi_estimate": "50% menos tiempo en contratación, 40% mejor retención",
        "steps": [
            "Auditar el proceso actual de selección y onboarding",
            "Implementar ATS con screening de CVs por IA",
            "Automatizar agendamiento de entrevistas",
            "Crear portal de onboarding digital con tareas automáticas",
            "Configurar encuestas de clima y feedback automáticas",
            "Integrar con nómina y sistemas de RRHH existentes",
        ],
        "canvas_blocks": ["key_resources", "key_activities", "cost_structure"],
    },
    {
        "title": "Gestión Inteligente de Inventario y Cadena de Suministro",
        "description": (
            "Implementa predicción de demanda con IA para optimizar niveles de "
            "inventario, reducir stockouts y minimizar capital inmovilizado."
        ),
        "process": "Operaciones y Logística",
        "technology": "Forecasting con ML + ERP Integration",
        "effort": "alto",
        "roi_estimate": "Reducción 20-30% en inventario, -15% en stockouts",
        "steps": [
            "Recopilar histórico de ventas y datos de demanda (mínimo 2 años)",
            "Limpiar y preparar datos para modelado predictivo",
            "Entrenar modelo de forecasting de demanda por SKU",
            "Integrar predicciones con sistema ERP/WMS",
            "Automatizar órdenes de compra cuando se alcancen puntos de reorden",
            "Monitorear accuracy del modelo y reentrenar periódicamente",
        ],
        "canvas_blocks": ["key_activities", "key_resources", "cost_structure", "key_partnerships"],
    },
    {
        "title": "Personalización de Experiencia del Cliente con IA",
        "description": (
            "Implementa un motor de recomendaciones personalizado que adapte "
            "productos, ofertas y comunicaciones a cada cliente individual, "
            "aumentando el ticket promedio y la satisfacción."
        ),
        "process": "Experiencia del Cliente",
        "technology": "Recommendation Engine (Collaborative Filtering + IA)",
        "effort": "alto",
        "roi_estimate": "Aumento 15-25% en ticket promedio, +20% en retención",
        "steps": [
            "Unificar datos de comportamiento del cliente en una plataforma",
            "Desarrollar motor de recomendaciones (ej. con TensorFlow Recommenders)",
            "Segmentar clientes por comportamiento con clustering",
            "Integrar recomendaciones en todos los puntos de contacto",
            "Personalizar precios y ofertas por segmento",
            "Optimizar continuamente con A/B testing automatizado",
        ],
        "canvas_blocks": ["customer_segments", "value_propositions", "customer_relationships"],
    },
]


class AutomationEngine:
    """
    Motor de IA para identificar y priorizar oportunidades de automatización
    basadas en el Modelo de Negocio de la empresa.
    """

    def identify_opportunities(
        self,
        canvas: BusinessCanvas,
        max_opportunities: Optional[int] = None,
    ) -> list[AutomationOpportunity]:
        """
        Identifica oportunidades de automatización relevantes para la empresa
        basándose en los bloques del canvas completados.

        Args:
            canvas: Modelo de negocio de la empresa.
            max_opportunities: Número máximo de oportunidades a devolver.

        Returns:
            Lista de oportunidades ordenadas por esfuerzo (bajo primero).
        """
        filled_blocks = set()
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

        for block_key, values in block_map.items():
            if values:
                filled_blocks.add(block_key)

        opportunities: list[AutomationOpportunity] = []

        for item in _AUTOMATION_KNOWLEDGE_BASE:
            # Include automation if it relates to any filled block,
            # or if no blocks are filled (show all by default)
            related_blocks = set(item.get("canvas_blocks", []))
            if not filled_blocks or related_blocks & filled_blocks:
                opportunities.append(
                    AutomationOpportunity(
                        title=item["title"],
                        description=item["description"],
                        process=item["process"],
                        technology=item["technology"],
                        effort=item["effort"],
                        roi_estimate=item["roi_estimate"],
                        steps=item["steps"],
                    )
                )

        # Sort by effort: bajo first, then medio, then alto
        effort_order = {"bajo": 0, "medio": 1, "alto": 2}
        opportunities.sort(key=lambda o: effort_order.get(o.effort, 99))

        if max_opportunities is not None:
            opportunities = opportunities[:max_opportunities]

        return opportunities

    def quick_wins(self, canvas: BusinessCanvas) -> list[AutomationOpportunity]:
        """
        Devuelve las automatizaciones de bajo esfuerzo y alto impacto
        para resultados rápidos.
        """
        all_opps = self.identify_opportunities(canvas)
        return [o for o in all_opps if o.effort == "bajo"][:3]
