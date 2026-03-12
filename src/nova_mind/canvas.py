"""
Módulo de análisis del Modelo de Negocio (Business Model Canvas).
Define los 9 bloques del canvas y herramientas de análisis.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BusinessCanvas:
    """
    Representa los 9 bloques del Modelo de Negocio (Business Model Canvas).
    """

    # 1. Segmentos de Clientes
    customer_segments: list[str] = field(default_factory=list)

    # 2. Propuesta de Valor
    value_propositions: list[str] = field(default_factory=list)

    # 3. Canales
    channels: list[str] = field(default_factory=list)

    # 4. Relaciones con Clientes
    customer_relationships: list[str] = field(default_factory=list)

    # 5. Fuentes de Ingresos
    revenue_streams: list[str] = field(default_factory=list)

    # 6. Recursos Clave
    key_resources: list[str] = field(default_factory=list)

    # 7. Actividades Clave
    key_activities: list[str] = field(default_factory=list)

    # 8. Socios Clave
    key_partnerships: list[str] = field(default_factory=list)

    # 9. Estructura de Costos
    cost_structure: list[str] = field(default_factory=list)

    # Información adicional de la empresa
    company_name: Optional[str] = None
    industry: Optional[str] = None

    def completeness_score(self) -> float:
        """
        Calcula el porcentaje de completitud del canvas (0.0 a 1.0).
        """
        blocks = [
            self.customer_segments,
            self.value_propositions,
            self.channels,
            self.customer_relationships,
            self.revenue_streams,
            self.key_resources,
            self.key_activities,
            self.key_partnerships,
            self.cost_structure,
        ]
        filled = sum(1 for block in blocks if block)
        return filled / len(blocks)

    def incomplete_blocks(self) -> list[str]:
        """
        Devuelve la lista de bloques no completados.
        """
        mapping = {
            "Segmentos de Clientes": self.customer_segments,
            "Propuesta de Valor": self.value_propositions,
            "Canales": self.channels,
            "Relaciones con Clientes": self.customer_relationships,
            "Fuentes de Ingresos": self.revenue_streams,
            "Recursos Clave": self.key_resources,
            "Actividades Clave": self.key_activities,
            "Socios Clave": self.key_partnerships,
            "Estructura de Costos": self.cost_structure,
        }
        return [name for name, values in mapping.items() if not values]

    def to_dict(self) -> dict:
        return {
            "company_name": self.company_name,
            "industry": self.industry,
            "customer_segments": self.customer_segments,
            "value_propositions": self.value_propositions,
            "channels": self.channels,
            "customer_relationships": self.customer_relationships,
            "revenue_streams": self.revenue_streams,
            "key_resources": self.key_resources,
            "key_activities": self.key_activities,
            "key_partnerships": self.key_partnerships,
            "cost_structure": self.cost_structure,
        }
