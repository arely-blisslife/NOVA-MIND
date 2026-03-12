"""Tests for NOVA-MIND: canvas, strategy engine, automation engine, and API."""

import sys
import os

# Add the project paths so imports resolve correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))

import pytest
from httpx import AsyncClient, ASGITransport

from nova_mind.canvas import BusinessCanvas
from nova_mind.strategy_engine import StrategyEngine
from nova_mind.automation_engine import AutomationEngine
from main import app


# ── BusinessCanvas ────────────────────────────────────────────────────────────

class TestBusinessCanvas:
    def test_empty_canvas_completeness_is_zero(self):
        canvas = BusinessCanvas()
        assert canvas.completeness_score() == 0.0

    def test_full_canvas_completeness_is_one(self):
        canvas = BusinessCanvas(
            customer_segments=["PyMEs"],
            value_propositions=["Reduce costs"],
            channels=["Website"],
            customer_relationships=["24/7 support"],
            revenue_streams=["Subscription"],
            key_resources=["Tech platform"],
            key_activities=["Software development"],
            key_partnerships=["Cloud provider"],
            cost_structure=["Staff"],
        )
        assert canvas.completeness_score() == 1.0

    def test_partial_canvas_completeness(self):
        canvas = BusinessCanvas(
            customer_segments=["Enterprises"],
            value_propositions=["Fast delivery"],
        )
        # 2 out of 9 blocks filled → ~0.222
        score = canvas.completeness_score()
        assert abs(score - 2 / 9) < 1e-9

    def test_incomplete_blocks_returns_unfilled(self):
        canvas = BusinessCanvas(customer_segments=["Startups"])
        incomplete = canvas.incomplete_blocks()
        assert "Segmentos de Clientes" not in incomplete
        assert "Propuesta de Valor" in incomplete
        assert len(incomplete) == 8

    def test_to_dict_contains_all_keys(self):
        canvas = BusinessCanvas(company_name="Acme", industry="Tech")
        d = canvas.to_dict()
        expected_keys = {
            "company_name", "industry", "customer_segments",
            "value_propositions", "channels", "customer_relationships",
            "revenue_streams", "key_resources", "key_activities",
            "key_partnerships", "cost_structure",
        }
        assert expected_keys == set(d.keys())


# ── StrategyEngine ────────────────────────────────────────────────────────────

class TestStrategyEngine:
    def setup_method(self):
        self.engine = StrategyEngine()

    def _full_canvas(self):
        return BusinessCanvas(
            customer_segments=["PyMEs"],
            value_propositions=["Reduce costs 30%"],
            channels=["Website", "App"],
            customer_relationships=["Self-service portal"],
            revenue_streams=["SaaS subscription"],
            key_resources=["Dev team", "Cloud infra"],
            key_activities=["Product development"],
            key_partnerships=["AWS", "Stripe"],
            cost_structure=["Payroll", "Infrastructure"],
        )

    def test_analyze_returns_recommendations(self):
        canvas = self._full_canvas()
        recs = self.engine.analyze(canvas)
        assert len(recs) > 0

    def test_analyze_respects_max_recommendations(self):
        canvas = self._full_canvas()
        recs = self.engine.analyze(canvas, max_recommendations=3)
        assert len(recs) == 3

    def test_recommendations_sorted_by_priority(self):
        canvas = self._full_canvas()
        recs = self.engine.analyze(canvas)
        priority_order = {"alta": 0, "media": 1, "baja": 2}
        for i in range(len(recs) - 1):
            assert priority_order[recs[i].priority] <= priority_order[recs[i + 1].priority]

    def test_recommendation_has_required_fields(self):
        canvas = BusinessCanvas(customer_segments=["Retail"])
        recs = self.engine.analyze(canvas)
        for rec in recs:
            assert rec.title
            assert rec.description
            assert rec.block
            assert rec.priority in {"alta", "media", "baja"}
            assert isinstance(rec.impact_areas, list)

    def test_quick_wins_returns_at_most_three(self):
        canvas = self._full_canvas()
        wins = self.engine.quick_wins(canvas)
        assert len(wins) <= 3

    def test_quick_wins_are_all_alta_priority(self):
        canvas = self._full_canvas()
        wins = self.engine.quick_wins(canvas)
        for w in wins:
            assert w.priority == "alta"

    def test_empty_block_elevates_media_to_alta(self):
        # With an empty canvas, media recommendations should be elevated to alta
        canvas = BusinessCanvas()  # all blocks empty
        recs = self.engine.analyze(canvas)
        priorities = {r.priority for r in recs}
        # With all blocks empty, all "media" should become "alta"
        assert "media" not in priorities


# ── AutomationEngine ──────────────────────────────────────────────────────────

class TestAutomationEngine:
    def setup_method(self):
        self.engine = AutomationEngine()

    def _canvas_with_crm(self):
        return BusinessCanvas(
            customer_relationships=["Email support"],
            channels=["Website"],
        )

    def test_identify_opportunities_returns_results(self):
        canvas = BusinessCanvas()
        opps = self.engine.identify_opportunities(canvas)
        assert len(opps) > 0

    def test_identify_opportunities_respects_max(self):
        canvas = BusinessCanvas()
        opps = self.engine.identify_opportunities(canvas, max_opportunities=2)
        assert len(opps) == 2

    def test_opportunities_sorted_by_effort(self):
        canvas = BusinessCanvas()
        opps = self.engine.identify_opportunities(canvas)
        effort_order = {"bajo": 0, "medio": 1, "alto": 2}
        for i in range(len(opps) - 1):
            assert effort_order[opps[i].effort] <= effort_order[opps[i + 1].effort]

    def test_opportunity_has_required_fields(self):
        canvas = BusinessCanvas()
        opps = self.engine.identify_opportunities(canvas)
        for opp in opps:
            assert opp.title
            assert opp.description
            assert opp.process
            assert opp.technology
            assert opp.effort in {"bajo", "medio", "alto"}
            assert opp.roi_estimate
            assert isinstance(opp.steps, list)
            assert len(opp.steps) > 0

    def test_quick_wins_are_low_effort(self):
        canvas = BusinessCanvas()
        wins = self.engine.quick_wins(canvas)
        for w in wins:
            assert w.effort == "bajo"

    def test_filled_canvas_filters_relevant_automations(self):
        canvas = self._canvas_with_crm()
        opps = self.engine.identify_opportunities(canvas)
        # Should return automations related to channels/customer_relationships
        assert len(opps) > 0

    def test_to_dict_has_all_keys(self):
        canvas = BusinessCanvas()
        opps = self.engine.identify_opportunities(canvas, max_opportunities=1)
        d = opps[0].to_dict()
        expected = {"title", "description", "process", "technology", "effort", "roi_estimate", "steps"}
        assert expected == set(d.keys())


# ── API Endpoints ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
class TestAPI:
    async def _client(self):
        return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

    async def test_health_returns_ok(self):
        async with await self._client() as client:
            res = await client.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "ok"

    async def test_analyze_canvas_returns_full_response(self):
        payload = {
            "company_name": "Acme Corp",
            "customer_segments": ["SMBs in Mexico"],
            "value_propositions": ["Reduce admin costs"],
            "channels": ["SaaS platform"],
        }
        async with await self._client() as client:
            res = await client.post("/api/canvas/analyze", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["company_name"] == "Acme Corp"
        assert "canvas_completeness" in data
        assert "incomplete_blocks" in data
        assert "strategies" in data
        assert "automations" in data
        assert isinstance(data["strategies"], list)
        assert isinstance(data["automations"], list)

    async def test_analyze_canvas_empty_body(self):
        async with await self._client() as client:
            res = await client.post("/api/canvas/analyze", json={})
        assert res.status_code == 200
        data = res.json()
        assert data["canvas_completeness"] == 0.0

    async def test_strategies_endpoint(self):
        payload = {"customer_segments": ["Enterprises"]}
        async with await self._client() as client:
            res = await client.post("/api/strategies", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert "strategies" in data
        assert data["total"] == len(data["strategies"])

    async def test_strategies_quick_wins(self):
        async with await self._client() as client:
            res = await client.post("/api/strategies/quick-wins", json={})
        assert res.status_code == 200
        data = res.json()
        assert "quick_wins" in data
        assert len(data["quick_wins"]) <= 3

    async def test_automations_endpoint(self):
        async with await self._client() as client:
            res = await client.post("/api/automations", json={})
        assert res.status_code == 200
        data = res.json()
        assert "automations" in data
        assert data["total"] == len(data["automations"])

    async def test_automations_quick_wins(self):
        async with await self._client() as client:
            res = await client.post("/api/automations/quick-wins", json={})
        assert res.status_code == 200
        data = res.json()
        assert "quick_wins" in data

    async def test_max_results_respected(self):
        payload = {"max_results": 2}
        async with await self._client() as client:
            res = await client.post("/api/strategies", json=payload)
        assert res.status_code == 200
        assert len(res.json()["strategies"]) == 2

    async def test_invalid_max_results_returns_error(self):
        payload = {"max_results": 0}
        async with await self._client() as client:
            res = await client.post("/api/strategies", json=payload)
        assert res.status_code == 422
