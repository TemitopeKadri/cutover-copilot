# Changelog

All notable changes to cutover-copilot are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.2.0] — 2026-06-09

### Added
- Sample D365 Business Central cutover plan (`sample_d365_cutover.csv`) — 22 steps across pre-cutover, cutover, post-cutover, and BAU handover phases
- Sample Azure cloud migration cutover plan (`sample_azure_migration.csv`) — 20 steps covering lift-and-shift workload migration
- CONTRIBUTING guide for practitioners who want to add sample plans or features

---

## [0.1.0] — 2026-06-01

### Added
- Initial release of `cutover_copilot.py` command-line tool
- CSV and JSON migration step input support
- Risk scoring per step — HIGH / MEDIUM / LOW based on rollback availability, duration, and notes keywords
- Phase grouping — pre-cutover, cutover, post-cutover, BAU handover
- Full structured cutover runbook generation via Claude API including:
  - Executive summary
  - Go/No-Go gate criteria table (T-48h, T-24h, T-4h, T-0)
  - Live cutover sequence with rollback triggers per step
  - Post-cutover validation checklist
  - BAU handover criteria
  - Top 3 risks and contingencies
- `--sample` flag to generate sample migration data
- `--name` flag to set the migration name in the runbook title
- MIT licence
- README with quickstart, input format, and roadmap

---
