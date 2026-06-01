# Canyon Forge — import notes for the R2R2R plan

The plan in `plan.json` follows the v1 import spec with a few deliberate extensions.
Two small engine behaviors make it import and play correctly; the rest is informational.

## 1. Honor `rest` literally — do **not** snap to 15/30/45
Treat each exercise's `rest` (seconds) as the literal between-set rest and run the
timer for exactly that. The ME leg progression intentionally ramps density by shrinking
rest across the block (60 → 45 → 40 → 30 → 15 → 10 s). Snapping to 15/30/45 destroys
the whole progression. Values that appear in the file: **10, 15, 20, 30, 40, 45, 60, 90**.

(`rule #6` in the original spec said "keep rest to 15/30/45 for strength, pull-ups 90."
This plan supersedes that — the engine should accept any non-negative integer of seconds.)

## 2. New session-level field: `groupRest` (seconds)
Optional. When present on a session, it **overrides the automatic 60 s rest between
exercises/groups** for that session. Used by the ME leg circuit, where between-exercise
rest varies 10–90 s by workout. If `groupRest` is absent, keep the existing automatic 60 s.

## 3. `duration` is a generated estimate — display it, don't enforce it
Every `strength` and `pullups` session carries a `duration` (minutes) computed from
sets × work × rests. `run`/`bike` sessions use `time` (minutes) as before — and the long
trail runs now carry a `time` estimate too (≈18 min/mi + 28 min per 1,000 ft of climb,
calibrated to the athlete's real data). Safe to show as "~X min". It's an estimate, not a cap.

## 4. `working: false` warm-up / cool-down (already in spec)
The ME leg sessions include an aerobic warm-up, get-ups, burpees, and an aerobic cool-down
as `working: false` exercises (flow through, not logged) — standard convention, no change needed.

## Nothing else deviates
- Pull-ups stay `type: "pullups"` with `sets`/`reps`/`rest`/`note` (+ the new `duration`).
  Accessory work (negatives, dead hangs, rows) and AMRAP back-off sets live in `note`
  because the `pullups` type has no accessory/blocks field. If you ever want those logged
  as individual sets, the cleanest add would be an optional `accessory: [...]` array on
  the pullups type — flag it and we'll populate it.
- Runs/bikes, segments, and superset keys are all per the v1 spec.
