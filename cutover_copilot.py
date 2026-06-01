"""
cutover-copilot: AI-assisted cutover playbook generator for ERP and infrastructure migrations.
https://github.com/TemitopeKadri/cutover-copilot

Usage:
    python cutover_copilot.py --input sample_migration.csv --output runbook.md
    python cutover_copilot.py --sample

MIT Licence — Copyright (c) 2026 Temitope Kadri
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("Error: anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)


# ── Risk assessment ───────────────────────────────────────────────────────────

def assess_step_risk(step: dict) -> str:
    """Return HIGH / MEDIUM / LOW risk for a migration step."""
    rollback = step.get("rollback_possible", "yes").strip().lower()
    duration = step.get("duration_mins", "0").strip()
    depends_on = step.get("depends_on", "").strip()
    notes = step.get("notes", "").strip().lower()

    high_risk_keywords = ["live", "production", "cutover", "switch", "failover",
                          "dns", "firewall", "database", "go-live", "cutoff"]

    try:
        duration_mins = int(duration)
    except ValueError:
        duration_mins = 0

    if rollback in ("no", "n", "false", "0"):
        return "HIGH"
    if any(kw in notes for kw in high_risk_keywords):
        return "HIGH"
    if duration_mins > 120:
        return "HIGH"
    if depends_on and len(depends_on.split(",")) > 2:
        return "MEDIUM"
    if duration_mins > 60:
        return "MEDIUM"
    return "LOW"


def build_phase_summary(steps: list[dict]) -> dict:
    """Group steps by phase and compute risk summary."""
    phases = {}
    for step in steps:
        phase = step.get("phase", "cutover").strip().lower()
        if phase not in phases:
            phases[phase] = {"steps": [], "risk_counts": {"HIGH": 0, "MEDIUM": 0, "LOW": 0}}
        risk = assess_step_risk(step)
        step["_risk"] = risk
        phases[phase]["steps"].append(step)
        phases[phase]["risk_counts"][risk] += 1
    return phases


# ── LLM call ──────────────────────────────────────────────────────────────────

def call_claude(prompt: str) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def generate_runbook(phases: dict, migration_name: str = "Migration") -> str:
    """Generate a structured cutover runbook using Claude."""

    phase_order = ["pre-cutover", "cutover", "post-cutover", "bau-handover"]
    steps_block = []

    for phase in phase_order:
        if phase not in phases:
            continue
        data = phases[phase]
        steps_text = "\n".join(
            f"  Step {s.get('step_id','')}: [{s['_risk']}] {s.get('step_name','')} | "
            f"Owner: {s.get('owner','')} | Duration: {s.get('duration_mins','')} mins | "
            f"Depends on: {s.get('depends_on','None')} | "
            f"Rollback possible: {s.get('rollback_possible','Yes')} | "
            f"Notes: {s.get('notes','')}"
            for s in data["steps"]
        )
        rc = data["risk_counts"]
        steps_block.append(
            f"Phase: {phase.upper()} | HIGH: {rc['HIGH']} MEDIUM: {rc['MEDIUM']} LOW: {rc['LOW']}\n"
            f"{steps_text}"
        )

    steps_text_full = "\n\n".join(steps_block)

    prompt = f"""You are a senior delivery manager producing a cutover runbook for a live production migration.

Migration: {migration_name}

Migration steps by phase:
{steps_text_full}

Produce a complete, structured cutover runbook in Markdown with these sections:

## Cutover Runbook: {migration_name}

### 1. Executive Summary
One paragraph: scope, go-live window, overall risk rating, and single most critical dependency.

### 2. Go / No-Go Gate Criteria
A table with columns: Gate | Timing | Criteria | Owner | Decision Authority
Include gates at T-48h, T-24h, T-4h, and T-0 (live).

### 3. Pre-Cutover Checklist (T-48h to T-0)
All pre-cutover steps as a numbered checklist with owner, duration, and completion checkbox [ ].

### 4. Live Cutover Sequence
Numbered steps in exact execution order. For each step:
- Step number, name, owner, duration
- Rollback trigger (specific condition that triggers rollback)
- Rollback action (exactly what to do if triggered)
- Completion sign-off box [ ]

### 5. Post-Cutover Validation
Validation steps and success criteria confirming the migration succeeded before BAU handover.

### 6. BAU Handover Criteria
Specific, measurable criteria that must be met before the project team stands down.

### 7. Top 3 Risks and Contingencies
The three highest-risk items with named contingency actions.

Be specific. Use the step names and owner names from the input. Do not use placeholder text."""

    return call_claude(prompt)


# ── File I/O ──────────────────────────────────────────────────────────────────

def load_steps(input_path: str) -> list[dict]:
    path = Path(input_path)
    if not path.exists():
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)
    if path.suffix.lower() == ".json":
        with open(path) as f:
            data = json.load(f)
        return data if isinstance(data, list) else data.get("steps", [])
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


SAMPLE_CSV = """step_id,phase,step_name,owner,duration_mins,depends_on,rollback_possible,notes
S01,pre-cutover,Final data backup — production database,DBA,60,,Yes,Must complete before any cutover activity
S02,pre-cutover,Freeze all transactions in legacy system,Finance Lead,15,S01,Yes,Communicate to all business users 30 mins before
S03,pre-cutover,Validate backup integrity,DBA,30,S01,Yes,Run checksum validation
S04,pre-cutover,Confirm infrastructure readiness,Infra Lead,20,S03,Yes,Network, firewall, DNS all checked
S05,cutover,Disable legacy system access,Infra Lead,10,S02,Yes,Revoke all user sessions
S06,cutover,Run data migration scripts — GL and AP,DBA,90,S05,No,Production database migration — no rollback once started
S07,cutover,Validate migrated data against reconciliation report,Finance Lead,45,S06,Yes,Row counts and spot-check on 50 transactions
S08,cutover,DNS cutover — point traffic to new system,Infra Lead,15,S07,Yes,30 min propagation window expected
S09,cutover,Smoke test — login and core transaction,Test Lead,30,S08,Yes,5 named test users confirm login and basic navigation
S10,post-cutover,Full regression test — Wave 1 modules,Test Lead,120,S09,Yes,
S11,post-cutover,Performance baseline check,Infra Lead,30,S10,Yes,Response times within agreed SLA thresholds
S12,bau-handover,Hypercare team briefing,PM,30,S11,Yes,
S13,bau-handover,Support ticket queue handover,PM,20,S12,Yes,
S14,bau-handover,Project team stand-down confirmation,PM,15,S13,Yes,Sign-off from programme sponsor required
"""


def create_sample(output_path: str = "sample_migration.csv") -> None:
    Path(output_path).write_text(SAMPLE_CSV, encoding="utf-8")
    print(f"Sample migration file created: {output_path}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="cutover-copilot: AI-assisted cutover runbook generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cutover_copilot.py --sample
  python cutover_copilot.py --input sample_migration.csv
  python cutover_copilot.py --input sample_migration.csv --output runbook.md --name "D365 Go-Live"
        """
    )
    parser.add_argument("--input", help="Path to migration steps CSV or JSON")
    parser.add_argument("--output", help="Path to write Markdown runbook (optional)")
    parser.add_argument("--name", default="Migration", help="Name of the migration (for the runbook title)")
    parser.add_argument("--sample", action="store_true", help="Generate a sample_migration.csv and exit")

    args = parser.parse_args()

    if args.sample:
        create_sample()
        return

    if not args.input:
        parser.print_help()
        return

    print(f"Loading migration steps from: {args.input}")
    steps = load_steps(args.input)
    print(f"Loaded {len(steps)} steps")

    phases = build_phase_summary(steps)

    print("\nPhase risk summary:")
    for phase, data in phases.items():
        rc = data["risk_counts"]
        print(f"  {phase.upper()}: {rc['HIGH']} HIGH | {rc['MEDIUM']} MEDIUM | {rc['LOW']} LOW")

    high_risk = [s for s in steps if s.get("_risk") == "HIGH"]
    if high_risk:
        print(f"\nHigh-risk steps ({len(high_risk)}):")
        for s in high_risk:
            rollback = s.get("rollback_possible", "yes").strip().lower()
            flag = "⚠️  NO ROLLBACK" if rollback in ("no", "n", "false", "0") else "⚠️"
            print(f"  {flag} {s.get('step_id','')} — {s.get('step_name','')} (Owner: {s.get('owner','')})")

    print(f"\nGenerating cutover runbook via Claude API...")
    runbook = generate_runbook(phases, migration_name=args.name)

    if args.output:
        Path(args.output).write_text(runbook, encoding="utf-8")
        print(f"Runbook written to: {args.output}")
    else:
        print("\n" + "═" * 60)
        print(runbook)
        print("═" * 60)


if __name__ == "__main__":
    main()
