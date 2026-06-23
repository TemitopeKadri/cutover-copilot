# Contributing to cutover-copilot

Thank you for your interest in contributing. This tool is built by delivery managers who have lived through high-stakes cutovers — contributions from practitioners are especially welcome.

---

## What we are looking for

- **Bug fixes** — if something does not work as described, open an issue and submit a fix
- **New sample cutover plans** — real-world examples for different platforms (SAP, Oracle, NetSuite, infrastructure migrations)
- **New output formats** — ServiceNow change request export, PDF runbook, Excel checklist
- **Prompt improvements** — better system prompts that produce more accurate runbooks
- **New features** — see the roadmap in README.md for planned additions
- **Documentation** — clearer examples, better explanations

---

## How to contribute

1. **Fork the repo** — click Fork at the top of the page
2. **Create a branch** — `git checkout -b feat/your-feature-name`
3. **Make your changes** — keep commits small and focused
4. **Test your changes** — run the tool against the sample data to confirm it works
5. **Submit a pull request** — describe what you changed and why

---

## Pull request guidelines

- One feature or fix per PR
- Include a brief description of what changed and why
- If fixing a bug, reference the issue number
- If adding a feature, update the README if usage changes
- Do not include your API key or any credentials in any file

---

## Adding sample cutover plans

Sample CSV files are especially welcome. Format:

```
step_id,phase,step_name,owner,duration_mins,depends_on,rollback_possible,notes
```

Phase values: `pre-cutover` | `cutover` | `post-cutover` | `bau-handover`

Name your file clearly: `sample_[platform]_cutover.csv` e.g. `sample_sap_cutover.csv`

---

## Reporting bugs

Open an issue with:
- What you expected to happen
- What actually happened
- Your Python version (`python --version`)
- The command you ran
- Any error messages

---

## Licence

By contributing you agree that your contributions will be licensed under the MIT Licence.

---

*Built by [Temitope Kadri MAPM](https://github.com/TemitopeKadri)*
