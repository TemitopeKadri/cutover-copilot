# cutover-copilot

**AI-assisted cutover playbook generator for ERP and infrastructure migrations.**

`cutover-copilot` takes your migration plan and produces a structured cutover runbook — go/no-go checkpoints, dependency map, rollback triggers, and BAU handover criteria — so your go-live is governed by a plan, not adrenaline.

Built from real zero-critical-incident cutover programmes in live data centre and ERP environments.

---

## What it does

- Reads a migration plan (CSV, JSON, or structured text)
- Identifies dependencies and critical path items
- Generates a structured cutover runbook with:
  - Pre-cutover checklist (T-48h, T-24h, T-4h, T-1h)
  - Go / No-Go decision gates with named criteria
  - Live cutover steps with owner, duration, and rollback trigger per step
  - BAU handover checklist
- Flags high-risk steps and suggests contingency actions

## Why it exists

Zero critical incidents at go-live does not happen by luck. It happens because every dependency is mapped, every rollback trigger is pre-agreed, and every owner knows exactly what they are doing and when. This tool generates that structure from your existing migration plan in minutes.

## Quickstart

```bash
pip install -r requirements.txt
python cutover_copilot.py --input sample_migration.csv --output runbook.md
```

## Input format

CSV with columns: `step_id`, `phase`, `step_name`, `owner`, `duration_mins`, `depends_on`, `rollback_possible`, `notes`

Phase values: `pre-cutover` | `cutover` | `post-cutover` | `bau-handover`

## Output

- `runbook.md` — full structured cutover runbook in Markdown
- Console summary — go/no-go gate criteria and top 3 risk items

## Requirements

- Python 3.9+
- Anthropic API key (set as `ANTHROPIC_API_KEY` environment variable)

## Roadmap

- [ ] ServiceNow change request template export
- [ ] D365 Business Central cutover checklist template
- [ ] Azure infrastructure migration variant
- [ ] Slack/Teams go-live war-room integration
- [ ] PDF runbook export

## Contributing

Pull requests welcome. Please open an issue first to discuss what you'd like to change.

## Licence

MIT — see [LICENSE](LICENSE)

---

*Part of an open-source toolkit for AI-assisted project delivery. See also: [agentic-pm](https://github.com/TemitopeKadri/agentic-pm), [erp-discovery-agent](https://github.com/TemitopeKadri/erp-discovery-agent), [prince2-agile-templates](https://github.com/TemitopeKadri/prince2-agile-templates)*
