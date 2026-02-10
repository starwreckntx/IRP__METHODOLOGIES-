"""
Context Mortality Audit — CLI Interface
========================================
Command-line interface for all CMA components.

Usage:
    python -m irp_swarm_console.context_mortality.cli <command> [options]

Commands:
    cda         Context Death Audit operations
    pathtrace   Path Tracer lookups and reports
    recontext   Execute recontext sweeps
    appeal      Manage appeals and reinstatements
    drift       Drift trajectory analysis
    stats       Show statistics across all components
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .cda import ContextDeathAudit
from .path_tracer import PathTracer
from .recontext import RecontextSweep, SweepScope
from .appeal import AppealManager, AppealCategory, AppealStatus
from .drift import DriftTracker, DriftTrajectoryAnalysis, MemoryState
from .models import DroppedItem, SovereigntyClass


def _default_base_dir() -> Path:
    """Return the default base directory for CMA data."""
    return Path(__file__).parent


def _print_json(data, indent=2):
    """Print a dict/list as formatted JSON."""
    print(json.dumps(data, indent=indent, ensure_ascii=False))


# ======================================================================
# CDA Commands
# ======================================================================

def cmd_cda(args):
    """Context Death Audit subcommands."""
    cda = ContextDeathAudit(
        session_id=args.session_id or "cli-session",
        user_id=args.user_id or "cli-user",
        log_dir=args.log_dir,
    )

    if args.cda_action == "stats":
        _print_json(cda.get_stats())

    elif args.cda_action == "list":
        logs = cda.list_logs()
        if not logs:
            print("No CDA logs found.")
            return
        for log_path in logs:
            print(f"  {log_path.name}")

    elif args.cda_action == "graveyard":
        graveyard = cda.get_graveyard()
        if not graveyard:
            print("Graveyard is empty.")
            return
        print(f"Total dropped items: {len(graveyard)}\n")
        for item in graveyard:
            print(f"  [{item.category}] {item.content[:80]}...")
            print(f"    Hash: {item.content_hash[:16]}...")
            print(f"    Turn: {item.source_turn} | Session: {item.session_id[:8]}...")
            print(f"    Appeal: {item.appeal_status}")
            print()

    elif args.cda_action == "show":
        if not args.log_file:
            print("Error: --log-file required for 'show' action.")
            return
        log = cda.load_log(args.log_file)
        _print_json(log.to_dict())

    elif args.cda_action == "snapshot":
        # Demo: capture pre/post from JSON files
        if not args.pre_file or not args.post_file:
            print("Error: --pre-file and --post-file required for 'snapshot'.")
            return
        with open(args.pre_file, "r") as f:
            pre_data = json.load(f)
        with open(args.post_file, "r") as f:
            post_data = json.load(f)

        cda.capture_pre_state(pre_data)
        cda.capture_post_state(post_data)
        dropped = cda.generate_death_log()
        log = cda.build_cda_log()
        filepath = cda.persist_log(log)
        print(f"CDA log written: {filepath}")
        print(f"Dropped items: {len(dropped)}")
        print(f"Retained items: {len(cda.retained_items)}")
        print(f"Compression ratio: {log.compression_ratio:.2f}x")

    else:
        print(f"Unknown CDA action: {args.cda_action}")


# ======================================================================
# Path Tracer Commands
# ======================================================================

def cmd_pathtrace(args):
    """Path Tracer subcommands."""
    tracer = PathTracer(store_path=args.store_path)

    if args.pt_action == "stats":
        _print_json(tracer.get_stats())

    elif args.pt_action == "search":
        if not args.keyword:
            print("Error: --keyword required for 'search' action.")
            return
        results = tracer.search(args.keyword)
        if not results:
            print(f"No traces found matching '{args.keyword}'.")
            return
        print(f"Found {len(results)} matching traces:\n")
        for trace in results:
            status_icon = {
                "ALIVE": "[+]",
                "DEAD": "[X]",
                "COMPRESSED": "[~]",
                "RECOVERED": "[R]",
            }.get(trace.current_status, "[?]")
            print(f"  {status_icon} {trace.origin_verbatim[:80]}...")
            print(f"      Hash: {trace.origin_content_hash[:16]}...")
            print(f"      Status: {trace.current_status}")
            print(f"      Transformations: {len(trace.transformations)}")
            fidelity = trace.get_fidelity_curve()
            if fidelity:
                print(f"      Latest fidelity: {fidelity[-1]:.4f}")
            print()

    elif args.pt_action == "lookup":
        if not args.content_hash:
            print("Error: --hash required for 'lookup' action.")
            return
        trace = tracer.lookup(args.content_hash)
        if trace is None:
            print(f"No trace found for hash: {args.content_hash}")
            return
        _print_json(trace.to_dict())

    elif args.pt_action == "dead":
        dead = tracer.get_dead_items()
        if not dead:
            print("No dead items found.")
            return
        print(f"Dead items: {len(dead)}\n")
        for trace in dead:
            print(f"  [X] {trace.origin_verbatim[:80]}...")
            print(f"      Died in: {trace.last_seen_in}")
            print(f"      Recoverable: {trace.recoverable}")
            print()

    elif args.pt_action == "fidelity":
        _print_json(tracer.get_fidelity_report())

    else:
        print(f"Unknown pathtrace action: {args.pt_action}")


# ======================================================================
# Recontext Commands
# ======================================================================

def cmd_recontext(args):
    """Recontext sweep subcommands."""
    cda = ContextDeathAudit(
        session_id=args.session_id or "cli-session",
        user_id=args.user_id or "cli-user",
    )
    tracer = PathTracer()
    sweep = RecontextSweep(cda=cda, path_tracer=tracer)

    if args.rc_action == "list":
        results = sweep.list_sweep_results()
        if not results:
            print("No sweep results found.")
            return
        for path in results:
            print(f"  {path.name}")

    elif args.rc_action == "show":
        if not args.result_file:
            print("Error: --result-file required for 'show' action.")
            return
        result = sweep.load_sweep_result(args.result_file)
        _print_json(result)

    elif args.rc_action == "run":
        if not args.transcripts_file:
            print("Error: --transcripts-file required for 'run' action.")
            return
        with open(args.transcripts_file, "r") as f:
            transcripts = json.load(f)

        memory_items = []
        if args.memory_file:
            with open(args.memory_file, "r") as f:
                memory_items = json.load(f)

        scope = SweepScope(
            session_ids=args.scope_sessions.split(",") if args.scope_sessions else None,
            topic_keywords=args.topic.split(",") if args.topic else None,
            full_sweep=args.full_sweep,
        )

        result = sweep.execute_sweep(
            transcripts=transcripts,
            current_memory_items=memory_items,
            scope=scope,
            fidelity_threshold=args.fidelity_threshold,
        )

        print(f"Sweep complete: {result['sweep_id']}")
        print(f"  Transcripts scanned: {result['stats']['transcripts_scanned']}")
        print(f"  Units extracted: {result['stats']['units_extracted']}")
        print(f"  Gaps found: {result['stats']['gaps_found']}")
        print(f"  Proposals generated: {result['stats']['proposals_generated']}")

    else:
        print(f"Unknown recontext action: {args.rc_action}")


# ======================================================================
# Appeal Commands
# ======================================================================

def cmd_appeal(args):
    """Appeal mechanism subcommands."""
    manager = AppealManager(
        appeal_dir=args.appeal_dir,
        claude_md_path=args.claude_md,
    )

    if args.ap_action == "stats":
        _print_json(manager.get_stats())

    elif args.ap_action == "history":
        history = manager.get_decision_history()
        if not history:
            print("No appeal decisions recorded.")
            return
        _print_json(history)

    elif args.ap_action == "queue":
        queue = manager.get_reinstatement_queue()
        if not queue:
            print("Reinstatement queue is empty.")
            return
        _print_json(queue)

    elif args.ap_action == "reports":
        reports = manager.get_mortality_reports()
        if not reports:
            print("No context mortality reports.")
            return
        _print_json(reports)

    elif args.ap_action == "execute":
        results = manager.execute_reinstatements()
        if not results:
            print("No pending reinstatements to execute.")
            return
        print(f"Executed {len(results)} reinstatements:")
        _print_json(results)

    else:
        print(f"Unknown appeal action: {args.ap_action}")


# ======================================================================
# Drift Commands
# ======================================================================

def cmd_drift(args):
    """Drift trajectory analysis subcommands."""
    tracker = DriftTracker(store_path=args.drift_store)

    if args.dr_action == "stats":
        _print_json(tracker.get_stats())

    elif args.dr_action == "trajectory":
        trajectory = tracker.get_trajectory()
        if not trajectory:
            print("No drift data recorded.")
            return
        _print_json(trajectory)

    elif args.dr_action == "trend":
        trend = tracker.get_trend()
        _print_json(trend)

    elif args.dr_action == "compare":
        if not args.state_a_file or not args.state_b_file:
            print("Error: --state-a and --state-b required for 'compare'.")
            return
        with open(args.state_a_file, "r") as f:
            a_data = json.load(f)
        with open(args.state_b_file, "r") as f:
            b_data = json.load(f)

        state_a = MemoryState.from_dict(a_data)
        state_b = MemoryState.from_dict(b_data)

        reference = None
        if args.reference_file:
            with open(args.reference_file, "r") as f:
                reference = json.load(f)

        dta = DriftTrajectoryAnalysis(state_a, state_b, reference)
        report = dta.generate_drift_report()

        # Record in tracker
        tracker.record_snapshot(report)

        print(f"Drift Report: {report.report_id}")
        print(f"  Drift coefficient: {report.drift_coefficient:.4f}")
        print(f"  Convergent: {report.convergent_count}")
        print(f"  Divergent: {report.divergent_count}")
        print(f"  Doubly dead: {report.doubly_dead_count}")
        print()
        print("Recommendations:")
        for rec in report.recommendations:
            print(f"  - {rec}")
        print()
        print("Full report:")
        _print_json(report.to_dict())

    else:
        print(f"Unknown drift action: {args.dr_action}")


# ======================================================================
# Stats Command
# ======================================================================

def cmd_stats(args):
    """Show statistics across all CMA components."""
    print("=== Context Mortality Audit — System Statistics ===\n")

    cda = ContextDeathAudit(
        session_id="stats",
        user_id="stats",
    )
    print("--- Context Death Audit ---")
    _print_json(cda.get_stats())
    print()

    tracer = PathTracer()
    print("--- Path Tracer ---")
    _print_json(tracer.get_stats())
    print()

    manager = AppealManager()
    print("--- Appeal Manager ---")
    _print_json(manager.get_stats())
    print()

    tracker = DriftTracker()
    print("--- Drift Tracker ---")
    _print_json(tracker.get_stats())


# ======================================================================
# Argument Parser
# ======================================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cma",
        description="Context Mortality Audit — CLI Interface",
    )
    parser.add_argument(
        "--session-id", default=None, help="Session ID for context"
    )
    parser.add_argument(
        "--user-id", default=None, help="User ID for context"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- CDA ---
    cda_parser = subparsers.add_parser("cda", help="Context Death Audit")
    cda_parser.add_argument(
        "cda_action",
        choices=["stats", "list", "graveyard", "show", "snapshot"],
        help="CDA action",
    )
    cda_parser.add_argument("--log-dir", default=None)
    cda_parser.add_argument("--log-file", default=None)
    cda_parser.add_argument("--pre-file", default=None)
    cda_parser.add_argument("--post-file", default=None)

    # --- Path Tracer ---
    pt_parser = subparsers.add_parser("pathtrace", help="Path Tracer")
    pt_parser.add_argument(
        "pt_action",
        choices=["stats", "search", "lookup", "dead", "fidelity"],
        help="Path Tracer action",
    )
    pt_parser.add_argument("--store-path", default=None)
    pt_parser.add_argument("--keyword", default=None)
    pt_parser.add_argument("--content-hash", "--hash", default=None)

    # --- Recontext ---
    rc_parser = subparsers.add_parser("recontext", help="Recontext Sweeps")
    rc_parser.add_argument(
        "rc_action", choices=["list", "show", "run"], help="Recontext action"
    )
    rc_parser.add_argument("--transcripts-file", default=None)
    rc_parser.add_argument("--memory-file", default=None)
    rc_parser.add_argument("--result-file", default=None)
    rc_parser.add_argument("--scope-sessions", default=None)
    rc_parser.add_argument("--topic", default=None)
    rc_parser.add_argument("--full-sweep", action="store_true")
    rc_parser.add_argument(
        "--fidelity-threshold", type=float, default=0.5
    )

    # --- Appeal ---
    ap_parser = subparsers.add_parser("appeal", help="Appeal Mechanism")
    ap_parser.add_argument(
        "ap_action",
        choices=["stats", "history", "queue", "reports", "execute"],
        help="Appeal action",
    )
    ap_parser.add_argument("--appeal-dir", default=None)
    ap_parser.add_argument("--claude-md", default=None)

    # --- Drift ---
    dr_parser = subparsers.add_parser("drift", help="Drift Trajectory Analysis")
    dr_parser.add_argument(
        "dr_action",
        choices=["stats", "trajectory", "trend", "compare"],
        help="Drift action",
    )
    dr_parser.add_argument("--drift-store", default=None)
    dr_parser.add_argument("--state-a", "--state-a-file", dest="state_a_file", default=None)
    dr_parser.add_argument("--state-b", "--state-b-file", dest="state_b_file", default=None)
    dr_parser.add_argument("--reference-file", default=None)

    # --- Stats ---
    subparsers.add_parser("stats", help="Show all component statistics")

    return parser


def main(argv: Optional[List[str]] = None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return

    dispatch = {
        "cda": cmd_cda,
        "pathtrace": cmd_pathtrace,
        "recontext": cmd_recontext,
        "appeal": cmd_appeal,
        "drift": cmd_drift,
        "stats": cmd_stats,
    }

    handler = dispatch.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
