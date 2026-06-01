# Canyon Forge — training app + R2R2R plan

Start here. This repo holds the **app** and the **training plan** it imports, plus the
generator that produces the plan. If you're building/maintaining the app, read this file,
then `APP_BUILDER_NOTES.md`.

The plan is a periodized 21-week build (Jun 1 → Oct 22, 2026) toward a Grand Canyon
Rim-to-Rim-to-Rim, 16-hour target.

---

## File map

| File | What it is |
|------|------------|
| **`README.md`** | This orientation doc. |
| **`PLAN_IMPORT_SPEC.md`** | The v1 import schema — top-level shape, week/session objects, type-specific blocks, validation rules. The base contract. |
| **`APP_BUILDER_NOTES.md`** | **Read this second.** The deltas from the v1 spec the current plan relies on (literal rests, `groupRest`, `duration`). If the app and the spec ever disagree, these notes win. |
| **`plan.json`** | The generated plan the app imports. **Do not hand-edit** — it's overwritten on every regenerate. |
| **`build_plan.py`** | The generator. Source of truth for plan content. Edit here, then regenerate. |
| **`canyon-forge.html`** | The app (single-file PWA). Source of record. |
| **`index.html`** | Deployed copy of `canyon-forge.html` (kept in sync by `update.sh`). |
| **`sw.js`** | Service worker (offline/PWA). |
| **`update.sh`** | Regenerate `plan.json`, sync `index.html`, commit + push live. |

---

## The data contract, in one place

1. **Schema:** everything in `PLAN_IMPORT_SPEC.md` still holds (plan header → `weeks[]` →
   `sessions[]`; session types `strength` / `run` / `bike` / `pullups` / `mobility` / `rest`).
2. **Three extensions** the plan uses on top of v1 (full detail in `APP_BUILDER_NOTES.md`):
   - **`rest` is literal seconds** — do **not** snap to 15/30/45. Values seen: 10–90.
   - **`groupRest` (session-level, seconds)** — overrides the automatic 60 s between
     exercises/groups for that session. Used by the leg circuit.
   - **`duration` (minutes)** — a generated estimate on every strength/pull session;
     long runs also carry a `time` estimate. Display only, not a cap.
3. **Targets are derived from the sessions**, so the weekly progress bars always match
   what's scheduled — don't recompute them differently.

## How the plan is structured (what the app will render)

- **Mon** — ME leg circuit (14-week max-effort progression, WO#1–14) + Pull-Ups (Volume)
- **Tue** — Easy run (flat, from home) + Pull-Ups (Tempo)
- **Wed** — Upper lift (chest-focus / back-focus, alternating)
- **Thu** — Flat quality run (from home)
- **Fri** — Pull-Ups (Intensity / test)
- **Sat** — Long run / sustained vert climb (the key day)
- **Sun** — Optional Z2 bike → becomes a back-to-back long run in the build block

Pull-ups follow a separate 16-week structured program; the leg work is a 14-week ME
progression. Both taper into race week. See `build_plan.py` for the week-by-week config.

---

## Regenerating after a plan change

Edit `build_plan.py` (never `plan.json` directly), then:

```bash
./update.sh            # regenerates plan.json, syncs index.html, commits + pushes
# or just rebuild locally without deploying:
python3 build_plan.py  # prints a per-week summary and validates the output
```

`build_plan.py` validates on every run (unique IDs, legal days, well-formed blocks,
runs/bikes have a time or distance) and prints a week-by-week summary. If it fails, the
old `plan.json` is left untouched.
