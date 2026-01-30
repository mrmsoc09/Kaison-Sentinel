# Persona Library

> Project: Kaison Sentinel — offline-first build. See START_HERE.md for current setup.
> Last updated: 2026-01-30

This build ships with 130 personas for both PraisonAI and LangStudio formats.

## Locations
- PraisonAI personas: `config/personas_praison/`
- LangStudio personas: `config/personas_langstudio/`

## Save new personas
Use `kai11/core/persona_library.py` to save any newly generated persona to both formats.

## Listing
```
python3 -m kai11.assets_cli --list personas_praison
python3 -m kai11.assets_cli --list personas_langstudio
```
