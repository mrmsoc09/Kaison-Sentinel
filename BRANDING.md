# Kaison Sentinel Branding & Rename Guide

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

This project is designed to be renamed safely **without** violating third‑party licenses.

## What you may rename
- Product name in UI (`ui/index.html`, `ui/styles.css`)
- Marketing copy in docs (`README.md`, `docs/*`)
- Report branding (`config/report_formats/*`, `core/report_formatter.py`)
- Email templates (`config/prompts/email.*.json`)

## What you must not remove
- Third‑party notices and attribution requirements
- License texts for embedded or redistributed components
- Vendor or tool names where license requires attribution

## Recommended rename sequence
1) Update UI + docs references.
2) Update report + email templates.
3) Keep `NOTICE.md` intact with attribution list.
4) Validate that outputs still include required notices.

## Compliance note
If you embed or redistribute third‑party binaries, you must ship their licenses.
If you only *invoke* external tools present on the host, retain references and attribution in documentation.
