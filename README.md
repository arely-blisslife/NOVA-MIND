# ⚡ NOVA-MIND

> **Ingeniero de IA que ayuda a empresas a explotar su máximo potencial con estrategias y automatizaciones.**

NOVA-MIND analiza el **Modelo de Negocio** de cualquier empresa usando los 9 bloques del _Business Model Canvas_ y genera recomendaciones estratégicas y oportunidades de automatización accionables, impulsadas por IA.

---

## 🖥️ Vista previa

| Formulario del Canvas | Resultados con IA |
|---|---|
| ![Landing](https://github.com/user-attachments/assets/ca4f276b-c8ed-4459-b567-807548aacbed) | ![Estrategias](https://github.com/user-attachments/assets/ad552a17-7f1c-42c8-a222-f475db02a38b) |

---

## 🚀 Funcionalidades

| Módulo | Descripción |
|---|---|
| 📋 **Canvas Analyzer** | Evalúa los 9 bloques del Business Model Canvas y calcula la completitud |
| 📊 **Strategy Engine** | Genera recomendaciones estratégicas priorizadas (alta / media / baja) |
| ⚙️ **Automation Engine** | Identifica oportunidades de automatización ordenadas por esfuerzo y ROI |
| 🎯 **Quick Wins** | Devuelve las 3 acciones de mayor impacto para resultados inmediatos |
| 🌐 **Web UI** | Interfaz visual para completar el canvas y explorar resultados |
| 📡 **REST API** | API documentada con FastAPI (OpenAPI / Swagger) |

---

## 🏗️ Estructura del proyecto

```
NOVA-MIND/
├── src/
│   └── nova_mind/
│       ├── __init__.py          # Versión y metadata
│       ├── canvas.py            # Modelo de datos: BusinessCanvas (9 bloques)
│       ├── strategy_engine.py   # Motor de estrategias con IA
│       └── automation_engine.py # Motor de automatizaciones con IA
├── api/
│   └── main.py                  # API REST con FastAPI
├── frontend/
│   └── index.html               # Interfaz web (vanilla HTML/CSS/JS)
├── tests/
│   └── test_nova_mind.py        # Suite de tests (28 pruebas)
├── requirements.txt
└── pytest.ini
```

---

## ⚙️ Instalación y uso

### Requisitos

- Python 3.12+

### Instalación

```bash
pip install -r requirements.txt
```

### Ejecutar el servidor

```bash
PYTHONPATH=src:api uvicorn api.main:app --reload
```

Luego abre **http://localhost:8000** en tu navegador.

### API Docs interactiva

```
http://localhost:8000/docs
```

---

## 📡 Endpoints de la API

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/health` | Estado del servicio |
| `POST` | `/api/canvas/analyze` | Análisis completo del canvas |
| `POST` | `/api/strategies` | Recomendaciones estratégicas |
| `POST` | `/api/strategies/quick-wins` | Top 3 estrategias de mayor impacto |
| `POST` | `/api/automations` | Oportunidades de automatización |
| `POST` | `/api/automations/quick-wins` | Automatizaciones de bajo esfuerzo |

### Ejemplo de petición

```bash
curl -X POST http://localhost:8000/api/canvas/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Mi Empresa",
    "industry": "E-commerce",
    "customer_segments": ["PyMEs del retail", "Consumidores online"],
    "value_propositions": ["Entrega en 24h", "Precios competitivos"],
    "channels": ["Tienda online", "App móvil"]
  }'
```

---

## 🧪 Tests

```bash
python -m pytest tests/ -v
```

28 pruebas que cubren: `BusinessCanvas`, `StrategyEngine`, `AutomationEngine` y todos los endpoints de la API.

---

## 🧩 Los 9 bloques del Business Model Canvas

1. **Segmentos de Clientes** — ¿A quién ayudas?
2. **Propuesta de Valor** — ¿Qué problema resuelves?
3. **Canales** — ¿Cómo llegas a tus clientes?
4. **Relaciones con Clientes** — ¿Cómo mantienes la relación?
5. **Fuentes de Ingresos** — ¿Cómo generas ingresos?
6. **Recursos Clave** — ¿Qué activos son indispensables?
7. **Actividades Clave** — ¿Qué procesos son críticos?
8. **Socios Clave** — ¿Con quién colaboras?
9. **Estructura de Costos** — ¿Cuáles son tus principales costos?
