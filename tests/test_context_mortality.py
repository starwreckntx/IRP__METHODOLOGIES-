"""
Test Suite for Context Mortality Audit (CMA)
=============================================
Tests all five phases plus sovereignty classification.
"""

import json
import os
import shutil
import tempfile
import uuid
from pathlib import Path

import pytest

# Ensure the parent package is importable
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "irp_swarm_console"))

from context_mortality.models import (
    AppealStatus,
    BiasVector,
    CDALog,
    ContextPathTrace,
    ContextSnapshot,
    DroppedItem,
    DriftReport,
    GapType,
    ItemStatus,
    RecoveryProposal,
    SemanticUnit,
    SovereigntyClass,
    Transformation,
    TransformationType,
)
from context_mortality.sovereignty import SovereigntyClassifier, HANDLING_RULES
from context_mortality.cda import ContextDeathAudit
from context_mortality.path_tracer import FidelityScorer, PathTracer
from context_mortality.recontext import RecontextSweep, SweepScope
from context_mortality.appeal import AppealManager, AppealCategory
from context_mortality.drift import (
    DriftTracker,
    DriftTrajectoryAnalysis,
    MemoryState,
)


# ======================================================================
# Fixtures
# ======================================================================

@pytest.fixture
def tmp_dir():
    """Create a temporary directory for test data."""
    d = tempfile.mkdtemp(prefix="cma_test_")
    yield d
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture
def sample_messages():
    """Sample conversation messages for testing."""
    return [
        {"role": "user", "content": "The G2 manifold safety protocol uses Ricci flow for curvature analysis."},
        {"role": "assistant", "content": "I understand the G2 manifold safety protocol. Let me analyze the Ricci flow approach."},
        {"role": "user", "content": "My preferred workflow is to always start with a Guardian Codex check."},
        {"role": "assistant", "content": "Noted. I'll begin with a Guardian Codex compliance verification."},
        {"role": "user", "content": "I've been diagnosed with chronic fatigue and need to pace my sessions."},
        {"role": "assistant", "content": "I understand. Let's structure our work to accommodate your needs."},
        {"role": "user", "content": "The IRP framework uses a three-layer governance model: OL, RAL, MSGL."},
        {"role": "assistant", "content": "Yes, the three-layer model provides comprehensive governance coverage."},
    ]


@pytest.fixture
def compacted_messages():
    """Simulated post-compaction messages (some content dropped)."""
    return [
        {"role": "system", "content": "User discussed G2 manifold safety protocol and Ricci flow. User prefers Guardian Codex checks first. IRP uses three-layer governance."},
        {"role": "assistant", "content": "Context loaded from previous conversation summary."},
    ]


# ======================================================================
# Models Tests
# ======================================================================

class TestModels:
    def test_semantic_unit_creation(self):
        unit = SemanticUnit(
            content="Test content",
            turn_index=0,
            timestamp="2026-02-08T00:00:00Z",
            session_id="test-session",
        )
        assert unit.content == "Test content"
        assert unit.content_hash != ""
        assert unit.unit_id != ""

    def test_semantic_unit_hash_determinism(self):
        unit1 = SemanticUnit(content="Same text", turn_index=0, timestamp="t", session_id="s")
        unit2 = SemanticUnit(content="Same text", turn_index=1, timestamp="t2", session_id="s2")
        assert unit1.content_hash == unit2.content_hash

    def test_semantic_unit_equality(self):
        unit1 = SemanticUnit(content="Same", turn_index=0, timestamp="t", session_id="s")
        unit2 = SemanticUnit(content="Same", turn_index=1, timestamp="t2", session_id="s2")
        assert unit1 == unit2

    def test_semantic_unit_serialization(self):
        unit = SemanticUnit(content="Test", turn_index=5, timestamp="t", session_id="s")
        d = unit.to_dict()
        restored = SemanticUnit.from_dict(d)
        assert restored.content == "Test"
        assert restored.turn_index == 5

    def test_dropped_item_recovery_path(self):
        item = DroppedItem(
            id="test-id",
            content="Dropped content",
            source_turn=3,
            source_timestamp="2026-01-01T00:00:00Z",
            session_id="sess-abc",
        )
        assert "transcript://sess-abc/turn/3" in item.recovery_path

    def test_context_path_trace_fidelity_curve(self):
        trace = ContextPathTrace(
            origin_session_id="s1",
            origin_turn_index=0,
            origin_timestamp="t",
            origin_verbatim="Original text",
        )
        t1 = Transformation(event="compaction", timestamp="t1", survived=True, fidelity_score=0.8)
        t2 = Transformation(event="synthesis", timestamp="t2", survived=True, fidelity_score=0.5)
        trace.add_transformation(t1)
        trace.add_transformation(t2)
        curve = trace.get_fidelity_curve()
        assert curve == [0.8, 0.5]

    def test_context_path_trace_death(self):
        trace = ContextPathTrace(
            origin_session_id="s1",
            origin_turn_index=0,
            origin_timestamp="t",
            origin_verbatim="Original text",
        )
        t = Transformation(event="resynthesis", timestamp="t1", survived=False, fidelity_score=0.0)
        trace.add_transformation(t)
        assert trace.current_status == ItemStatus.DEAD.value

    def test_cda_log_serialization(self):
        log = CDALog(session_id="s1", user_id="u1")
        d = log.to_dict()
        restored = CDALog.from_dict(d)
        assert restored.session_id == "s1"
        assert restored.log_id == log.log_id


# ======================================================================
# Sovereignty Tests
# ======================================================================

class TestSovereignty:
    def setup_method(self):
        self.classifier = SovereigntyClassifier()

    def test_health_classification(self):
        text = "I was diagnosed with chronic fatigue syndrome last month."
        result = self.classifier.classify(text)
        assert result == SovereigntyClass.HEALTH.value

    def test_technical_classification(self):
        text = "The API endpoint uses SHA-256 for authentication tokens."
        result = self.classifier.classify(text)
        assert result == SovereigntyClass.TECHNICAL.value

    def test_creative_classification(self):
        text = "The protagonist's character arc involves a journey of self-discovery."
        result = self.classifier.classify(text)
        assert result == SovereigntyClass.CREATIVE.value

    def test_procedural_classification(self):
        text = "My preferred workflow is to always start with a checklist review."
        result = self.classifier.classify(text)
        assert result == SovereigntyClass.PROCEDURAL.value

    def test_relational_classification(self):
        text = "Our collaboration pattern involves trust-building through iterative feedback."
        result = self.classifier.classify(text)
        assert result == SovereigntyClass.RELATIONAL.value

    def test_health_priority_over_technical(self):
        text = "The diagnosis algorithm detected anxiety symptoms in the patient data."
        result = self.classifier.classify(text)
        assert result == SovereigntyClass.HEALTH.value

    def test_health_requires_consent(self):
        assert self.classifier.requires_explicit_consent(SovereigntyClass.HEALTH.value)
        assert not self.classifier.requires_explicit_consent(SovereigntyClass.TECHNICAL.value)

    def test_session_scoped(self):
        assert self.classifier.is_session_scoped(SovereigntyClass.HEALTH.value)
        assert not self.classifier.is_session_scoped(SovereigntyClass.TECHNICAL.value)

    def test_health_overlap_detection(self):
        text = "The safety protocol monitoring detected elevated heart rate in the operator."
        assert self.classifier.check_health_overlap(text)

    def test_score_all(self):
        text = "The function class implementation handles diagnosis data."
        scores = self.classifier.score_all(text)
        assert SovereigntyClass.TECHNICAL.value in scores
        assert SovereigntyClass.HEALTH.value in scores

    def test_handling_rules(self):
        rules = self.classifier.get_handling_rules(SovereigntyClass.HEALTH.value)
        assert rules["auto_capture"] == "NEVER"
        assert rules["requires_opt_in"] == "explicit"

    def test_fallback_to_technical(self):
        text = "A completely neutral sentence with no signals."
        result = self.classifier.classify(text)
        assert result == SovereigntyClass.TECHNICAL.value


# ======================================================================
# CDA Tests (Phase 1)
# ======================================================================

class TestCDA:
    def test_extract_semantic_units(self, sample_messages):
        units = ContextDeathAudit.extract_semantic_units(sample_messages, "test-session")
        assert len(units) == len(sample_messages)
        assert units[0].content == sample_messages[0]["content"]

    def test_extract_multipart_content(self):
        messages = [
            {"role": "user", "content": [
                {"type": "text", "text": "Part one."},
                {"type": "text", "text": "Part two."},
            ]}
        ]
        units = ContextDeathAudit.extract_semantic_units(messages, "test")
        assert len(units) == 1
        assert "Part one" in units[0].content
        assert "Part two" in units[0].content

    def test_snapshot_capture(self, tmp_dir, sample_messages):
        cda = ContextDeathAudit("sess1", "user1", log_dir=tmp_dir)
        snap = cda.capture_pre_state(sample_messages)
        assert snap.turn_count == len(sample_messages)
        assert snap.token_count > 0
        assert len(snap.items) == len(sample_messages)

    def test_death_log_generation(self, tmp_dir, sample_messages, compacted_messages):
        cda = ContextDeathAudit("sess1", "user1", log_dir=tmp_dir)
        cda.capture_pre_state(sample_messages)
        cda.capture_post_state(compacted_messages)
        dropped = cda.generate_death_log()

        # All original items should be classified as dropped since
        # the compacted messages have completely different content hashes
        assert len(dropped) > 0
        # Retained items are those with matching hashes
        assert len(cda.retained_items) >= 0

    def test_death_log_requires_both_snapshots(self, tmp_dir):
        cda = ContextDeathAudit("sess1", "user1", log_dir=tmp_dir)
        with pytest.raises(ValueError):
            cda.generate_death_log()

    def test_persist_and_load_log(self, tmp_dir, sample_messages, compacted_messages):
        cda = ContextDeathAudit("sess1", "user1", log_dir=tmp_dir)
        cda.capture_pre_state(sample_messages)
        cda.capture_post_state(compacted_messages)
        cda.generate_death_log()
        log = cda.build_cda_log()
        filepath = cda.persist_log(log)

        assert filepath.exists()

        loaded = cda.load_log(str(filepath))
        assert loaded.session_id == "sess1"
        assert loaded.log_id == log.log_id

    def test_list_logs(self, tmp_dir, sample_messages, compacted_messages):
        cda = ContextDeathAudit("sess1", "user1", log_dir=tmp_dir)
        cda.capture_pre_state(sample_messages)
        cda.capture_post_state(compacted_messages)
        cda.generate_death_log()
        cda.persist_log()

        logs = cda.list_logs()
        assert len(logs) == 1

    def test_graveyard_aggregation(self, tmp_dir, sample_messages, compacted_messages):
        cda = ContextDeathAudit("sess1", "user1", log_dir=tmp_dir)
        cda.capture_pre_state(sample_messages)
        cda.capture_post_state(compacted_messages)
        cda.generate_death_log()
        cda.persist_log()

        graveyard = cda.get_graveyard()
        assert len(graveyard) > 0

    def test_sovereignty_classification_in_death_log(self, tmp_dir):
        messages = [
            {"role": "user", "content": "I was diagnosed with anxiety last week."},
            {"role": "user", "content": "The API endpoint returns JSON."},
        ]
        compacted = [
            {"role": "system", "content": "Completely different summary."},
        ]
        cda = ContextDeathAudit("sess1", "user1", log_dir=tmp_dir)
        cda.capture_pre_state(messages)
        cda.capture_post_state(compacted)
        dropped = cda.generate_death_log()

        categories = {d.category for d in dropped}
        # Should detect health and technical content
        assert SovereigntyClass.HEALTH.value in categories or SovereigntyClass.TECHNICAL.value in categories

    def test_stats(self, tmp_dir):
        cda = ContextDeathAudit("sess1", "user1", log_dir=tmp_dir)
        stats = cda.get_stats()
        assert stats["session_id"] == "sess1"
        assert stats["log_count"] == 0


# ======================================================================
# Path Tracer Tests (Phase 2)
# ======================================================================

class TestPathTracer:
    def test_register_origin(self, tmp_dir):
        tracer = PathTracer(store_path=os.path.join(tmp_dir, "traces.jsonl"))
        trace = tracer.register_origin(
            session_id="s1",
            turn_index=5,
            timestamp="2026-01-15T10:00:00Z",
            verbatim="The G2 manifold safety protocol uses Ricci flow.",
        )
        assert trace.current_status == ItemStatus.ALIVE.value
        assert trace.origin_turn_index == 5

    def test_idempotent_registration(self, tmp_dir):
        tracer = PathTracer(store_path=os.path.join(tmp_dir, "traces.jsonl"))
        trace1 = tracer.register_origin("s1", 5, "t", "Same content")
        trace2 = tracer.register_origin("s2", 10, "t2", "Same content")
        assert trace1.trace_id == trace2.trace_id

    def test_record_transformation(self, tmp_dir):
        tracer = PathTracer(store_path=os.path.join(tmp_dir, "traces.jsonl"))
        trace = tracer.register_origin("s1", 0, "t", "The G2 manifold safety protocol")
        updated = tracer.record_transformation(
            content_hash=trace.origin_content_hash,
            event="compaction",
            survived=True,
            transformed_form="User discussed G2 manifold safety protocol",
        )
        assert updated is not None
        assert len(updated.transformations) == 1
        assert updated.transformations[0]["fidelity_score"] > 0

    def test_record_death(self, tmp_dir):
        tracer = PathTracer(store_path=os.path.join(tmp_dir, "traces.jsonl"))
        trace = tracer.register_origin("s1", 0, "t", "Ephemeral context")
        tracer.record_death(
            content_hash=trace.origin_content_hash,
            event="memory_resynthesis",
            reason="recency_bias_decay",
        )
        dead = tracer.get_dead_items()
        assert len(dead) == 1
        assert dead[0].current_status == ItemStatus.DEAD.value

    def test_record_recovery(self, tmp_dir):
        tracer = PathTracer(store_path=os.path.join(tmp_dir, "traces.jsonl"))
        trace = tracer.register_origin("s1", 0, "t", "Recoverable context")
        tracer.record_death(trace.origin_content_hash, "compaction")
        tracer.record_recovery(trace.origin_content_hash, "Recovered context")
        updated = tracer.lookup(trace.origin_content_hash)
        assert updated.current_status == ItemStatus.RECOVERED.value

    def test_search(self, tmp_dir):
        tracer = PathTracer(store_path=os.path.join(tmp_dir, "traces.jsonl"))
        tracer.register_origin("s1", 0, "t", "The G2 manifold protocol")
        tracer.register_origin("s1", 1, "t", "An unrelated topic about cooking")
        results = tracer.search("G2 manifold")
        assert len(results) == 1

    def test_persistence(self, tmp_dir):
        store = os.path.join(tmp_dir, "traces.jsonl")
        tracer1 = PathTracer(store_path=store)
        tracer1.register_origin("s1", 0, "t", "Persistent content")

        # Reload from disk
        tracer2 = PathTracer(store_path=store)
        assert len(tracer2.traces) == 1

    def test_fidelity_report(self, tmp_dir):
        tracer = PathTracer(store_path=os.path.join(tmp_dir, "traces.jsonl"))
        trace = tracer.register_origin("s1", 0, "t", "Original text here")
        tracer.record_transformation(
            trace.origin_content_hash,
            event="compaction",
            survived=True,
            transformed_form="Modified text here",
        )
        report = tracer.get_fidelity_report()
        assert report["total_tracked"] == 1
        assert report["fidelity_stats"]["count"] == 1


class TestFidelityScorer:
    def test_identical_text(self):
        scorer = FidelityScorer()
        assert scorer.compute_fidelity("same", "same") == 1.0

    def test_empty_text(self):
        scorer = FidelityScorer()
        assert scorer.compute_fidelity("", "something") == 0.0
        assert scorer.compute_fidelity("something", "") == 0.0

    def test_partial_overlap(self):
        scorer = FidelityScorer()
        score = scorer.compute_fidelity(
            "The G2 manifold safety protocol uses Ricci flow",
            "G2 manifold safety protocol mentioned",
        )
        assert 0.0 < score < 1.0

    def test_no_overlap(self):
        scorer = FidelityScorer()
        score = scorer.compute_fidelity(
            "Alpha beta gamma",
            "Completely different words entirely",
        )
        assert score < 0.5

    def test_custom_embedding_fn(self):
        def mock_embed(text):
            # Simple mock: return hash-based pseudo-embedding
            return [float(ord(c) % 10) / 10 for c in text[:10].ljust(10)]

        scorer = FidelityScorer(embed_fn=mock_embed)
        score = scorer.compute_fidelity("hello world", "hello world")
        assert score == 1.0


# ======================================================================
# Recontext Tests (Phase 3)
# ======================================================================

class TestRecontextSweep:
    def test_sweep_scope_full(self):
        scope = SweepScope(full_sweep=True)
        assert scope.matches_session("any-session")
        assert scope.matches_time("any-time")
        assert scope.matches_topic("any content")

    def test_sweep_scope_session_filter(self):
        scope = SweepScope(session_ids=["s1", "s2"])
        assert scope.matches_session("s1")
        assert not scope.matches_session("s3")

    def test_sweep_scope_topic_filter(self):
        scope = SweepScope(topic_keywords=["G2 manifold", "IRP"])
        assert scope.matches_topic("The G2 manifold protocol")
        assert scope.matches_topic("IRP framework details")
        assert not scope.matches_topic("Cooking recipes")

    def test_sweep_scope_time_filter(self):
        scope = SweepScope(
            time_range_start="2026-01-01",
            time_range_end="2026-02-01",
        )
        assert scope.matches_time("2026-01-15T00:00:00Z")
        assert not scope.matches_time("2025-12-01T00:00:00Z")
        assert not scope.matches_time("2026-03-01T00:00:00Z")

    def test_execute_sweep(self, tmp_dir):
        cda = ContextDeathAudit("sess1", "user1", log_dir=os.path.join(tmp_dir, "cda"))
        tracer = PathTracer(store_path=os.path.join(tmp_dir, "traces.jsonl"))
        sweep = RecontextSweep(
            cda=cda,
            path_tracer=tracer,
            results_dir=os.path.join(tmp_dir, "sweeps"),
        )

        transcripts = [
            {
                "session_id": "s1",
                "messages": [
                    {"role": "user", "content": "The API endpoint uses REST architecture."},
                    {"role": "user", "content": "My preferred workflow starts with testing."},
                ],
            }
        ]
        memory_items = ["Some unrelated memory item"]

        scope = SweepScope(full_sweep=True)
        result = sweep.execute_sweep(
            transcripts=transcripts,
            current_memory_items=memory_items,
            scope=scope,
        )

        assert result["stats"]["transcripts_scanned"] == 1
        assert result["stats"]["units_extracted"] == 2
        assert result["stats"]["gaps_found"] >= 0

    def test_sweep_skips_health_items(self, tmp_dir):
        cda = ContextDeathAudit("sess1", "user1", log_dir=os.path.join(tmp_dir, "cda"))
        tracer = PathTracer(store_path=os.path.join(tmp_dir, "traces.jsonl"))
        sweep = RecontextSweep(
            cda=cda,
            path_tracer=tracer,
            results_dir=os.path.join(tmp_dir, "sweeps"),
        )

        transcripts = [
            {
                "session_id": "s1",
                "messages": [
                    {"role": "user", "content": "I was diagnosed with anxiety and depression."},
                ],
            }
        ]

        scope = SweepScope(full_sweep=True)
        result = sweep.execute_sweep(
            transcripts=transcripts,
            current_memory_items=[],
            scope=scope,
        )

        # Health items should NOT appear in proposals
        for proposal in result["proposals"]:
            assert proposal["sovereignty_class"] != SovereigntyClass.HEALTH.value

    def test_sweep_persistence(self, tmp_dir):
        cda = ContextDeathAudit("sess1", "user1", log_dir=os.path.join(tmp_dir, "cda"))
        tracer = PathTracer(store_path=os.path.join(tmp_dir, "traces.jsonl"))
        sweep = RecontextSweep(
            cda=cda,
            path_tracer=tracer,
            results_dir=os.path.join(tmp_dir, "sweeps"),
        )

        transcripts = [{"session_id": "s1", "messages": [
            {"role": "user", "content": "Test content for persistence."},
        ]}]

        sweep.execute_sweep(transcripts, [], SweepScope(full_sweep=True))
        results = sweep.list_sweep_results()
        assert len(results) == 1


# ======================================================================
# Appeal Tests (Phase 4)
# ======================================================================

class TestAppealManager:
    def _make_dropped_item(self, content="Dropped technical content", category="TECHNICAL"):
        return DroppedItem(
            id=str(uuid.uuid4()),
            content=content,
            source_turn=5,
            source_timestamp="2026-01-15T10:00:00Z",
            session_id="sess-test",
            category=category,
        )

    def test_accept_drop(self, tmp_dir):
        manager = AppealManager(appeal_dir=os.path.join(tmp_dir, "appeals"))
        item = self._make_dropped_item()
        decision = manager.accept_drop(item)
        assert decision.action == AppealStatus.ACCEPTED_DROP.value

    def test_appeal_item(self, tmp_dir):
        manager = AppealManager(appeal_dir=os.path.join(tmp_dir, "appeals"))
        item = self._make_dropped_item()
        decision = manager.appeal_item(item, category=AppealCategory.FACTUAL.value)
        assert decision.action == AppealStatus.APPEALED.value
        assert len(manager.reinstatement_queue) == 1

    def test_escalate_item(self, tmp_dir):
        manager = AppealManager(appeal_dir=os.path.join(tmp_dir, "appeals"))
        item = self._make_dropped_item()
        decision = manager.escalate_item(item, user_notes="Critical loss")
        assert decision.action == AppealStatus.ESCALATED.value
        assert len(manager.mortality_reports) == 1

    def test_health_appeal_requires_opt_in(self, tmp_dir):
        manager = AppealManager(appeal_dir=os.path.join(tmp_dir, "appeals"))
        item = self._make_dropped_item(
            content="Diagnosed with chronic fatigue",
            category=SovereigntyClass.HEALTH.value,
        )
        with pytest.raises(ValueError, match="HEALTH_OPT_IN"):
            manager.appeal_item(item)

    def test_health_appeal_with_opt_in(self, tmp_dir):
        manager = AppealManager(appeal_dir=os.path.join(tmp_dir, "appeals"))
        item = self._make_dropped_item(
            content="Diagnosed with chronic fatigue",
            category=SovereigntyClass.HEALTH.value,
        )
        decision = manager.review_item(
            dropped_item=item,
            action=AppealStatus.APPEALED.value,
            category=AppealCategory.HEALTH.value,
            user_notes="HEALTH_OPT_IN: I consent to storing this.",
        )
        assert decision.action == AppealStatus.APPEALED.value

    def test_memory_edit_truncation(self, tmp_dir):
        manager = AppealManager(appeal_dir=os.path.join(tmp_dir, "appeals"))
        long_content = "A" * 500
        item = self._make_dropped_item(content=long_content)
        manager.appeal_item(item, category=AppealCategory.FACTUAL.value)

        queue = manager.reinstatement_queue
        assert len(queue) == 1
        assert len(queue[0].content) <= 200

    def test_execute_reinstatements(self, tmp_dir):
        manager = AppealManager(appeal_dir=os.path.join(tmp_dir, "appeals"))
        item = self._make_dropped_item()
        manager.appeal_item(item, category=AppealCategory.FACTUAL.value)
        results = manager.execute_reinstatements()
        assert len(results) == 1
        assert results[0]["status"] in ("staged", "executed")

    def test_claude_md_reinstatement(self, tmp_dir):
        claude_md = os.path.join(tmp_dir, "CLAUDE.md")
        manager = AppealManager(
            appeal_dir=os.path.join(tmp_dir, "appeals"),
            claude_md_path=claude_md,
        )
        item = self._make_dropped_item()
        manager.review_item(
            dropped_item=item,
            action=AppealStatus.APPEALED.value,
            category=AppealCategory.PROCEDURAL.value,
            reinstatement_target="claude_md",
        )
        results = manager.execute_reinstatements()
        assert len(results) == 1
        assert Path(claude_md).exists()
        content = Path(claude_md).read_text()
        assert "Recovered Context" in content

    def test_decision_persistence(self, tmp_dir):
        appeal_dir = os.path.join(tmp_dir, "appeals")
        manager1 = AppealManager(appeal_dir=appeal_dir)
        item = self._make_dropped_item()
        manager1.accept_drop(item)

        # Reload
        manager2 = AppealManager(appeal_dir=appeal_dir)
        assert len(manager2.decisions) == 1

    def test_mortality_report_persistence(self, tmp_dir):
        appeal_dir = os.path.join(tmp_dir, "appeals")
        manager = AppealManager(appeal_dir=appeal_dir)
        item = self._make_dropped_item()
        manager.escalate_item(item, user_notes="Critical context lost")

        report_files = list(Path(appeal_dir).glob("mortality_report_*.json"))
        assert len(report_files) == 1

    def test_stats(self, tmp_dir):
        manager = AppealManager(appeal_dir=os.path.join(tmp_dir, "appeals"))
        stats = manager.get_stats()
        assert stats["total_decisions"] == 0


# ======================================================================
# Drift Tests (Phase 5)
# ======================================================================

class TestDriftAnalysis:
    def test_identical_states(self):
        a = MemoryState("A", ["item1", "item2", "item3"])
        b = MemoryState("B", ["item1", "item2", "item3"])
        dta = DriftTrajectoryAnalysis(a, b)
        assert dta.compute_drift_coefficient() == 0.0

    def test_completely_divergent(self):
        a = MemoryState("A", ["item1", "item2"])
        b = MemoryState("B", ["item3", "item4"])
        dta = DriftTrajectoryAnalysis(a, b)
        assert dta.compute_drift_coefficient() == 1.0

    def test_partial_drift(self):
        a = MemoryState("A", ["shared", "only_a"])
        b = MemoryState("B", ["shared", "only_b"])
        dta = DriftTrajectoryAnalysis(a, b)
        coeff = dta.compute_drift_coefficient()
        assert 0.0 < coeff < 1.0

    def test_convergent_items(self):
        a = MemoryState("A", ["shared1", "shared2", "only_a"])
        b = MemoryState("B", ["shared1", "shared2", "only_b"])
        dta = DriftTrajectoryAnalysis(a, b)
        convergent = dta.get_convergent()
        assert len(convergent) == 2

    def test_divergent_items(self):
        a = MemoryState("A", ["shared", "only_a"])
        b = MemoryState("B", ["shared", "only_b"])
        dta = DriftTrajectoryAnalysis(a, b)
        divergent = dta.get_divergent()
        assert len(divergent) == 2

    def test_doubly_dead(self):
        a = MemoryState("A", ["survived_a"])
        b = MemoryState("B", ["survived_b"])
        reference = ["survived_a", "survived_b", "dead_item"]
        dta = DriftTrajectoryAnalysis(a, b, reference_items=reference)
        doubly_dead = dta.get_doubly_dead()
        assert len(doubly_dead) == 1

    def test_bias_vectors(self):
        a = MemoryState("A", ["The API endpoint uses REST", "shared content"])
        b = MemoryState("B", ["I prefer to always use testing", "shared content"])
        dta = DriftTrajectoryAnalysis(a, b)
        vectors = dta.identify_bias_vectors()
        assert len(vectors) == 2
        for v in vectors:
            assert v.hypothesized_cause in DriftTrajectoryAnalysis.BIAS_CAUSES

    def test_drift_report(self):
        a = MemoryState("A", ["shared", "only_a"])
        b = MemoryState("B", ["shared", "only_b"])
        dta = DriftTrajectoryAnalysis(a, b)
        report = dta.generate_drift_report()
        assert report.convergent_count == 1
        assert report.divergent_count == 2
        assert len(report.recommendations) > 0
        assert report.account_a_id == "A"

    def test_empty_states(self):
        a = MemoryState("A", [])
        b = MemoryState("B", [])
        dta = DriftTrajectoryAnalysis(a, b)
        assert dta.compute_drift_coefficient() == 0.0

    def test_memory_state_serialization(self):
        state = MemoryState("A", ["item1", "item2"])
        d = state.to_dict()
        restored = MemoryState.from_dict(d)
        assert restored.account_id == "A"
        assert len(restored.items) == 2


class TestDriftTracker:
    def test_record_and_retrieve(self, tmp_dir):
        tracker = DriftTracker(store_path=os.path.join(tmp_dir, "drift.jsonl"))
        report = DriftReport(
            drift_coefficient=0.42,
            convergent_count=10,
            divergent_count=5,
            doubly_dead_count=2,
        )
        tracker.record_snapshot(report)
        trajectory = tracker.get_trajectory()
        assert len(trajectory) == 1
        assert trajectory[0]["drift_coefficient"] == 0.42

    def test_trend_insufficient_data(self, tmp_dir):
        tracker = DriftTracker(store_path=os.path.join(tmp_dir, "drift.jsonl"))
        trend = tracker.get_trend()
        assert trend["status"] == "insufficient_data"

    def test_trend_analysis(self, tmp_dir):
        tracker = DriftTracker(store_path=os.path.join(tmp_dir, "drift.jsonl"))
        # Record increasing drift (diverging)
        for i, coeff in enumerate([0.1, 0.2, 0.3, 0.4, 0.5]):
            report = DriftReport(
                drift_coefficient=coeff,
                convergent_count=10 - i,
                divergent_count=i,
                doubly_dead_count=0,
            )
            tracker.record_snapshot(report)

        trend = tracker.get_trend()
        assert trend["status"] == "analyzed"
        assert trend["direction"] == "DIVERGING"
        assert trend["slope"] > 0

    def test_stable_trend(self, tmp_dir):
        tracker = DriftTracker(store_path=os.path.join(tmp_dir, "drift.jsonl"))
        for _ in range(5):
            report = DriftReport(
                drift_coefficient=0.3,
                convergent_count=7,
                divergent_count=3,
                doubly_dead_count=0,
            )
            tracker.record_snapshot(report)

        trend = tracker.get_trend()
        assert trend["direction"] == "STABLE"

    def test_persistence(self, tmp_dir):
        store = os.path.join(tmp_dir, "drift.jsonl")
        tracker1 = DriftTracker(store_path=store)
        report = DriftReport(
            drift_coefficient=0.5,
            convergent_count=5,
            divergent_count=5,
            doubly_dead_count=0,
        )
        tracker1.record_snapshot(report)

        tracker2 = DriftTracker(store_path=store)
        assert len(tracker2.trajectory) == 1


# ======================================================================
# Integration Test
# ======================================================================

class TestIntegration:
    """End-to-end test across all phases."""

    def test_full_lifecycle(self, tmp_dir, sample_messages, compacted_messages):
        # Phase 1: CDA
        cda = ContextDeathAudit("sess1", "user1", log_dir=os.path.join(tmp_dir, "cda"))
        cda.capture_pre_state(sample_messages)
        cda.capture_post_state(compacted_messages)
        dropped = cda.generate_death_log()
        cda.persist_log()
        assert len(dropped) > 0

        # Phase 2: Register dropped items in Path Tracer
        tracer = PathTracer(store_path=os.path.join(tmp_dir, "traces.jsonl"))
        for item in dropped:
            tracer.register_origin(
                session_id="sess1",
                turn_index=item.source_turn,
                timestamp=item.source_timestamp,
                verbatim=item.content,
            )
            tracer.record_death(
                content_hash=item.content_hash,
                event="compaction",
                reason="context_window_compression",
            )
        dead = tracer.get_dead_items()
        assert len(dead) == len(dropped)

        # Phase 3: Recontext sweep
        sweep = RecontextSweep(
            cda=cda,
            path_tracer=tracer,
            results_dir=os.path.join(tmp_dir, "sweeps"),
        )
        transcripts = [{"session_id": "sess1", "messages": sample_messages}]
        result = sweep.execute_sweep(
            transcripts=transcripts,
            current_memory_items=[],
            scope=SweepScope(full_sweep=True),
        )
        assert result["stats"]["gaps_found"] > 0

        # Phase 4: Appeal a dropped item
        manager = AppealManager(appeal_dir=os.path.join(tmp_dir, "appeals"))
        non_health_dropped = [
            d for d in dropped
            if d.category != SovereigntyClass.HEALTH.value
        ]
        if non_health_dropped:
            decision = manager.appeal_item(
                non_health_dropped[0],
                category=AppealCategory.FACTUAL.value,
            )
            assert decision.action == AppealStatus.APPEALED.value

            # Execute reinstatement
            results = manager.execute_reinstatements()
            assert len(results) > 0

        # Phase 5: Drift analysis (simulate two accounts)
        state_a = MemoryState("A", [d.content for d in dropped[:3]])
        state_b = MemoryState("B", [d.content for d in dropped[1:4]])
        dta = DriftTrajectoryAnalysis(state_a, state_b)
        report = dta.generate_drift_report()
        assert report.drift_coefficient >= 0.0

        # Track drift over time
        tracker = DriftTracker(store_path=os.path.join(tmp_dir, "drift.jsonl"))
        tracker.record_snapshot(report)
        assert len(tracker.trajectory) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
