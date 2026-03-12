"""
API REST de NOVA-MIND con FastAPI.
Endpoints para análisis de canvas, estrategias y automatizaciones.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator
from typing import Optional
import os

from nova_mind.canvas import BusinessCanvas
from nova_mind.strategy_engine import StrategyEngine
from nova_mind.automation_engine import AutomationEngine

app = FastAPI(
    title="NOVA-MIND API",
    description=(
        "Ingeniero de IA que ayuda a empresas a explotar su máximo potencial "
        "con estrategias y automatizaciones basadas en el Modelo de Negocio."
    ),
    version="0.1.0",
)

# Mount static files for the frontend
_static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "static")
if os.path.isdir(_static_dir):
    app.mount("/static", StaticFiles(directory=_static_dir), name="static")

strategy_engine = StrategyEngine()
automation_engine = AutomationEngine()


# ---------- Pydantic schemas ----------

class CanvasInput(BaseModel):
    company_name: Optional[str] = None
    industry: Optional[str] = None
    customer_segments: list[str] = []
    value_propositions: list[str] = []
    channels: list[str] = []
    customer_relationships: list[str] = []
    revenue_streams: list[str] = []
    key_resources: list[str] = []
    key_activities: list[str] = []
    key_partnerships: list[str] = []
    cost_structure: list[str] = []
    max_results: Optional[int] = None

    @field_validator("max_results")
    @classmethod
    def max_results_must_be_positive(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 1:
            raise ValueError("max_results must be a positive integer")
        return v

    def to_canvas(self) -> BusinessCanvas:
        return BusinessCanvas(
            company_name=self.company_name,
            industry=self.industry,
            customer_segments=self.customer_segments,
            value_propositions=self.value_propositions,
            channels=self.channels,
            customer_relationships=self.customer_relationships,
            revenue_streams=self.revenue_streams,
            key_resources=self.key_resources,
            key_activities=self.key_activities,
            key_partnerships=self.key_partnerships,
            cost_structure=self.cost_structure,
        )


# ---------- Routes ----------

@app.get("/", include_in_schema=False)
async def root():
    """Sirve el frontend de NOVA-MIND."""
    frontend_path = os.path.join(
        os.path.dirname(__file__), "..", "frontend", "index.html"
    )
    if os.path.isfile(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "NOVA-MIND API v0.1.0 - visita /docs para la documentación"}


@app.get("/health")
async def health():
    """Verificación del estado del servicio."""
    return {"status": "ok", "service": "nova-mind"}


@app.post("/api/canvas/analyze")
async def analyze_canvas(data: CanvasInput):
    """
    Analiza el Modelo de Negocio (canvas) de la empresa y devuelve:
    - Puntuación de completitud del canvas
    - Bloques incompletos
    - Recomendaciones estratégicas
    - Oportunidades de automatización
    """
    canvas = data.to_canvas()

    strategies = strategy_engine.analyze(canvas, max_recommendations=data.max_results)
    automations = automation_engine.identify_opportunities(
        canvas, max_opportunities=data.max_results
    )

    return {
        "company_name": canvas.company_name,
        "canvas_completeness": round(canvas.completeness_score() * 100, 1),
        "incomplete_blocks": canvas.incomplete_blocks(),
        "strategies": [s.to_dict() for s in strategies],
        "automations": [a.to_dict() for a in automations],
    }


@app.post("/api/strategies")
async def get_strategies(data: CanvasInput):
    """
    Devuelve recomendaciones estratégicas basadas en el canvas de la empresa.
    """
    canvas = data.to_canvas()
    strategies = strategy_engine.analyze(canvas, max_recommendations=data.max_results)
    return {
        "company_name": canvas.company_name,
        "total": len(strategies),
        "strategies": [s.to_dict() for s in strategies],
    }


@app.post("/api/strategies/quick-wins")
async def get_strategy_quick_wins(data: CanvasInput):
    """
    Devuelve las 3 estrategias de mayor impacto y prioridad para resultados rápidos.
    """
    canvas = data.to_canvas()
    strategies = strategy_engine.quick_wins(canvas)
    return {
        "company_name": canvas.company_name,
        "quick_wins": [s.to_dict() for s in strategies],
    }


@app.post("/api/automations")
async def get_automations(data: CanvasInput):
    """
    Identifica oportunidades de automatización relevantes para la empresa.
    """
    canvas = data.to_canvas()
    automations = automation_engine.identify_opportunities(
        canvas, max_opportunities=data.max_results
    )
    return {
        "company_name": canvas.company_name,
        "total": len(automations),
        "automations": [a.to_dict() for a in automations],
    }


@app.post("/api/automations/quick-wins")
async def get_automation_quick_wins(data: CanvasInput):
    """
    Devuelve las automatizaciones de bajo esfuerzo y alto impacto para empezar ya.
    """
    canvas = data.to_canvas()
    automations = automation_engine.quick_wins(canvas)
    return {
        "company_name": canvas.company_name,
        "quick_wins": [a.to_dict() for a in automations],
    }
