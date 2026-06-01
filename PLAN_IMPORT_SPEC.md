# Canyon Forge — Plan Import Spec (v1)

Hand this to whoever builds the plan (coach, AI, or you). Output **one file: `plan.json`**
following the structure below. If you'd rather write a table than JSON, see
**§7 Shorthand** — I'll convert it.

Goal context: 2 lift days/week, 3–4 runs/week, 0–1 bike/week, 3–4 pull-up sessions/week,
building toward **Grand Canyon Rim-to-Rim-to-Rim, fall 2026**. The plan is **periodized**:
one entry per training week, so it can ramp and taper.

---

## 1. Top-level shape

```json
{
  "plan": {
    "name": "Grand Canyon R2R2R Build",
    "goal": "R2R2R — fall 2026",
    "startDate": "2026-06-01",        // the Monday of week 1 (YYYY-MM-DD)
    "units": "imperial",              // miles, lbs, feet
    "scheduleMode": "byDay"           // "byDay" (assign weekdays) or "byCount" (just weekly counts)
  },
  "weeks": [ Week, Week, ... ]        // one object per training week, in order
}
```

The app computes **which week is current** from `startDate` (same way the pull-up plan
already works), and shows that week's sessions on the home screen.

---

## 2. Week object

```json
{
  "week": 1,
  "phase": "Base",                    // Base | Build | Peak | Taper | Recovery
  "focus": "Easy aerobic volume, intro vert",
  "targets": { "lift": 2, "run": 3, "bike": 1, "pullups": 3 },  // weekly counts → drives progress bars
  "sessions": [ Session, ... ]
}
```

`targets` feeds the "This week's targets" progress bars and the calendar. Use the
**counts you actually want that week** (they can change week to week).

---

## 3. Session object (common fields)

Every session has these, then a **type-specific block** from §4.

```json
{
  "id": "w1-mon-run",        // unique across the whole plan
  "type": "run",             // strength | run | bike | pullups | mobility | rest
  "title": "Easy Run",
  "emoji": "🏃",
  "day": "mon",              // mon..sun  (required if scheduleMode "byDay"; omit for "byCount")
  "optional": false,         // true for the "0–1x" bike / bonus sessions
  "notes": "Conversational pace, nose-breathing."
}
```

| `type` | Use for |
|--------|---------|
| `strength` | The Upper / Canyon-style lift days |
| `run` | Any run (easy, long, tempo, intervals, hills, vert) |
| `bike` | Any ride |
| `pullups` | Pull-up routine (can reuse the built-in progression) |
| `mobility` | Standalone stretch / mobility / core-only flow |
| `rest` | Explicit rest day marker (optional) |

---

## 4. Type-specific blocks

### 4a. `strength`  — reuses the app's existing engine

```json
"duration": 40,
"equipment": "Dumbbells · Bench · Box",
"blocks": [
  {
    "name": "Power Pillars", "emoji": "🧱",
    "exercises": [
      {
        "name": "DB Bench / Floor Press",
        "equipment": "Dumbbells",
        "movementType": "reps",        // "reps" or "timed"
        "sets": 4,
        "reps": [8,8,6,6],             // number | array per set | "AMRAP"   (reps only)
        "seconds": 30,                 // (timed only)
        "rest": 45,                    // between-set rest, seconds (15/30/45; 60 between groups is automatic)
        "perSide": true,               // optional
        "unit": "reps",                // "reps" (default) or "steps"
        "superset": "arms",            // optional: same key on adjacent exercises = back-to-back, counts as one set
        "working": true,               // false = warmup/cooldown (flows through, not logged)
        "logReps": true,               // false to skip rep-logging (carries, planks)
        "swapGroup": "horiz_press",    // optional: enables ⇄ swap to related moves (see §6)
        "video": "dQw4w9WgXcQ",        // optional: pinned YouTube id or full URL (else app auto-searches)
        "note": "Stop 1 short of failure."
      }
    ]
  }
]
```

**Execution rules the engine already enforces** (so the builder doesn't restate them):
solo exercises = straight sets with their own `rest` between sets; exercises sharing a
`superset` key run back-to-back with rest only after the round; **60s between groups**;
10-second lead-in before every session. Pull-up ladder is the one exception at 90s.

### 4b. `run`

```json
"runType": "easy",          // easy | long | tempo | intervals | hills | vert | recovery
"time": 45,                 // target minutes (optional)
"distance": 5,              // miles (optional)
"vertFt": 800,              // elevation-gain target — IMPORTANT for R2R2R (optional)
"targets": { "pace": "9:30–10:30", "hrZone": "2", "rpe": 4 },   // any subset
"segments": [               // OPTIONAL — only for structured runs (intervals/tempo)
  { "label": "Warm-up", "time": 10, "intensity": "easy" },
  { "label": "Work", "reps": 5, "time": 3, "intensity": "5k effort",
    "recover": { "time": 2, "intensity": "jog" } },
  { "label": "Cool-down", "time": 10, "intensity": "easy" }
]
```

- A **simple run** = just `time`/`distance` + `targets`. No `segments` needed.
- A **structured run** = add `segments`; the app will auto-cycle them with timers like a lift.
- `vertFt` matters: R2R2R is ~11k ft up / 11k ft down — flag hill/vert sessions.

### 4c. `bike`  — same shape as run

```json
"bikeType": "endurance",    // endurance | recovery | intervals
"time": 60,
"distance": 18,
"targets": { "hrZone": "2", "rpe": 4, "cadence": "85–95" },
"segments": [ ... same format as run ... ]   // optional
```

### 4d. `pullups`

Either reuse the built-in progressive ladder (recommended — it already ramps weekly):

```json
"useBuiltInProgression": true
```

…or specify explicitly for a given week:

```json
"sets": 5, "reps": 3, "rest": 90, "note": "Submax, crisp reps."
```

### 4e. `mobility` / `rest`

```json
// mobility
"duration": 12,
"blocks": [ { "name":"Reset","emoji":"🧘","exercises":[ /* timed moves, working:false */ ] } ]

// rest
// no extra fields — just the common session fields with type:"rest"
```

---

## 5. One complete week (worked example)

```json
{
  "week": 1, "phase": "Base", "focus": "Aerobic base + lift intro",
  "targets": { "lift": 2, "run": 3, "bike": 1, "pullups": 3 },
  "sessions": [
    { "id":"w1-mon-pull","type":"pullups","title":"Pull-Ups","emoji":"🧗","day":"mon","useBuiltInProgression":true },
    { "id":"w1-mon-lift","type":"strength","title":"Upper","emoji":"💪","day":"mon","duration":38,
      "equipment":"Dumbbells · Bench","blocks":[ /* …Upper blocks… */ ] },
    { "id":"w1-tue-run","type":"run","title":"Easy Run","emoji":"🏃","day":"tue",
      "runType":"easy","time":40,"targets":{"hrZone":"2","rpe":4},"notes":"Conversational." },
    { "id":"w1-wed-pull","type":"pullups","title":"Pull-Ups","emoji":"🧗","day":"wed","useBuiltInProgression":true },
    { "id":"w1-thu-run","type":"run","title":"Hill Repeats","emoji":"⛰️","day":"thu","runType":"hills","time":45,"vertFt":900,
      "segments":[ {"label":"Warm-up","time":12,"intensity":"easy"},
        {"label":"Hill","reps":6,"time":2,"intensity":"hard uphill","recover":{"time":2,"intensity":"walk down"}},
        {"label":"Cool-down","time":10,"intensity":"easy"} ] },
    { "id":"w1-fri-lift","type":"strength","title":"Canyon","emoji":"🏔️","day":"fri","duration":46,
      "equipment":"DBs · Box · Pack","blocks":[ /* …Canyon blocks… */ ] },
    { "id":"w1-sat-long","type":"run","title":"Long Run","emoji":"🥾","day":"sat","runType":"long","distance":8,"vertFt":1200,
      "targets":{"hrZone":"2","rpe":5},"notes":"Time on feet. Hike the steep stuff." },
    { "id":"w1-sun-bike","type":"bike","title":"Z2 Spin","emoji":"🚴","day":"sun","optional":true,
      "bikeType":"recovery","time":50,"targets":{"hrZone":"1-2","rpe":3} }
  ]
}
```

---

## 6. Swap groups (optional, strength only)

To let me ⇄-swap a movement for related ones, tag it with a `swapGroup`. Existing groups
already wired in the app: `horiz_press, horiz_pull, vert_press, lat, curl, triceps, delt,
carry, hang_core, plank, squat, hinge, eccentric, split, lunge, stepup, walklunge,
calf_std, calf_sol, calf_sl, deadbug`. New groups are fine — just list 2–4 alternatives
and I'll add them.

---

## 7. Shorthand alternative (if you don't want to write JSON)

A coach can hand me a week as a simple table and I'll convert to the JSON above:

```
WEEK 1 — Base — targets: lift 2, run 3, bike 1, pullups 3
Mon  PullUps  built-in
Mon  Strength Upper (see lift sheet)
Tue  Run      easy 40min Z2
Wed  PullUps  built-in
Thu  Run      hills 45min, 6x2min uphill / 2min down, +900ft
Fri  Strength Canyon (see lift sheet)
Sat  Run      long 8mi Z2 +1200ft
Sun  Bike     optional, recovery 50min Z1-2
```

Strength sessions can point to a separate lift sheet in the same shorthand
(exercise, sets x reps, rest, superset-with).

---

## 8. Validation rules (so import doesn't choke)

1. Every `session.id` unique. `startDate` is a Monday. `day` ∈ mon..sun.
2. `strength` needs `blocks[].exercises[]`; each exercise has `movementType` + (`reps` or `seconds`).
3. `reps` is a number, an array (length = `sets`), or `"AMRAP"`. Timed uses `seconds`.
4. `run`/`bike`: include at least one of `time` / `distance`. `segments` optional; if present,
   each segment has a `time` (or `distance`) and `intensity`; intervals use `reps` + `recover`.
5. `targets` per week should match the sessions you list (e.g., if 3 runs, `run: 3`).
6. Keep `rest` to 15 / 30 / 45 for strength (60 between groups is automatic; pull-ups 90).
7. Distances in miles, weights in lbs, elevation in feet (per `units: imperial`).

---

## 9. Decisions for you to set (defaults I'll assume if unspecified)

- **Schedule mode:** `byDay` (assign weekdays) — *default*. Use `byCount` if you want a
  flexible menu and just hit weekly counts.
- **Plan length:** however many `weeks` you provide. For R2R2R I'd expect ~20–22 weeks
  ending with a 2–3 week taper. Builder decides.
- **Cardio detail:** simple (`time`/`distance`/`targets`) for easy & long days; `segments`
  only for intervals/tempo/hills.
- **Pull-ups:** `useBuiltInProgression: true` unless you want to override a week.

When the plan's ready, send me `plan.json` (or the shorthand) and I'll wire it into the app —
home screen, calendar, targets, and the in-session player for runs/bikes included.
```
