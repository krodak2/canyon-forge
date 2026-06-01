#!/usr/bin/env python3
"""Generate Canyon Forge plan.json for the R2R2R 21-week build.
Source of truth: R2R2R_Plan_Spec.md  +  PLAN_IMPORT_SPEC.md.
Targets are DERIVED from the actual sessions so they always match (rule #5)."""

import json, collections

# ---------------------------------------------------------------- strength templates
def upper_a_blocks():  # CHEST focus
    return [
        {"name": "Chest Power", "emoji": "💪", "exercises": [
            {"name": "DB Bench / Floor Press", "equipment": "Dumbbells · Bench", "movementType": "reps",
             "sets": 4, "reps": [10, 10, 8, 8], "rest": 45, "swapGroup": "horiz_press",
             "note": "Chest focus this week — drive these, leave 1 in the tank."},
        ]},
        {"name": "Press + Row (superset)", "emoji": "🔁", "exercises": [
            {"name": "TRX Chest Press", "equipment": "TRX", "movementType": "reps",
             "sets": 3, "reps": 12, "rest": 30, "superset": "pp", "swapGroup": "horiz_press"},
            {"name": "TRX Row", "equipment": "TRX", "movementType": "reps",
             "sets": 3, "reps": 12, "rest": 30, "superset": "pp", "swapGroup": "horiz_pull",
             "note": "Back-to-back with the press, no rest between."},
        ]},
        {"name": "Shoulders + Biceps (superset)", "emoji": "🔁", "exercises": [
            {"name": "DB Overhead Press", "equipment": "Dumbbells", "movementType": "reps",
             "sets": 3, "reps": [10, 9, 8], "rest": 30, "superset": "sb", "swapGroup": "vert_press"},
            {"name": "DB Biceps Curl", "equipment": "Dumbbells", "movementType": "reps",
             "sets": 3, "reps": 12, "rest": 30, "superset": "sb", "swapGroup": "curl"},
        ]},
        {"name": "Triceps + Core (superset)", "emoji": "🔁", "exercises": [
            {"name": "DB Skullcrusher", "equipment": "Dumbbells · Bench", "movementType": "reps",
             "sets": 2, "reps": 12, "rest": 30, "superset": "tc", "swapGroup": "triceps"},
            {"name": "Dead Bug", "equipment": "Bodyweight", "movementType": "reps",
             "sets": 2, "reps": 8, "rest": 30, "perSide": True, "superset": "tc", "swapGroup": "deadbug", "logReps": False},
        ]},
    ]

def upper_b_blocks():  # BACK focus
    return [
        {"name": "Back Power", "emoji": "🏋️", "exercises": [
            {"name": "Bent-Over / Chest-Supported Row", "equipment": "Barbell / Dumbbells · Bench", "movementType": "reps",
             "sets": 4, "reps": [10, 8, 8, 6], "rest": 45, "swapGroup": "horiz_pull",
             "note": "Heavy horizontal pull — vertical pulling is owned by the dedicated pull-up program."},
        ]},
        {"name": "Row + Press (superset)", "emoji": "🔁", "exercises": [
            {"name": "1-Arm DB Row", "equipment": "Dumbbells · Bench", "movementType": "reps",
             "sets": 3, "reps": 10, "rest": 30, "perSide": True, "superset": "pp", "swapGroup": "horiz_pull"},
            {"name": "DB Floor Press / Push-Up", "equipment": "Dumbbells / Bodyweight", "movementType": "reps",
             "sets": 3, "reps": 12, "rest": 30, "superset": "pp", "swapGroup": "horiz_press",
             "note": "Back-to-back with the row, no rest between."},
        ]},
        {"name": "Shoulders + Biceps (superset)", "emoji": "🔁", "exercises": [
            {"name": "DB Lateral Raise", "equipment": "Dumbbells", "movementType": "reps",
             "sets": 3, "reps": 15, "rest": 30, "superset": "sb", "swapGroup": "delt"},
            {"name": "TRX Biceps Curl", "equipment": "TRX", "movementType": "reps",
             "sets": 3, "reps": 12, "rest": 30, "superset": "sb", "swapGroup": "curl"},
        ]},
        {"name": "Triceps + Core (superset)", "emoji": "🔁", "exercises": [
            {"name": "Close-Grip Push-Up", "equipment": "Bodyweight", "movementType": "reps",
             "sets": 2, "reps": 12, "rest": 30, "superset": "tc", "swapGroup": "triceps"},
            {"name": "Side Plank", "equipment": "Bodyweight", "movementType": "timed",
             "sets": 2, "seconds": 40, "rest": 30, "perSide": True, "superset": "tc", "swapGroup": "plank", "logReps": False},
        ]},
    ]

# ---------------------------------------------------------------- session builders
# 16-week structured pull-up program. Day A=Volume, B=Tempo, C=Intensity.
# A/B = (sets, reps); Bt = tempo/loading cue; C = intensity-day description; acc = accessory.
PULL_PROGRAM = {
    1:  {"block": "Base", "A": (6, 3), "B": (4, 3), "Bt": "3s up / 1s hold / 3s down", "C": "1 all-out AMRAP, then 3 back-off sets at ~60% of that number.", "acc": "3×4 slow negatives (5s lower) + 2×20s dead hang"},
    2:  {"block": "Base", "A": (6, 3), "B": (4, 4), "Bt": "3-1-3 tempo", "C": "1 AMRAP, then 4 back-off sets at ~60%.", "acc": "3×4 negatives + 3×20s dead hang"},
    3:  {"block": "Base", "A": (7, 3), "B": (5, 3), "Bt": "3-1-3 tempo", "C": "1 AMRAP, then 4 back-off sets at ~60%.", "acc": "4×3 negatives + scapular pulls 3×8"},
    4:  {"block": "Base · DELOAD", "A": (4, 3), "B": (3, 3), "Bt": "3-1-3 tempo, easy", "C": "1 AMRAP only — note the number, no back-offs.", "acc": "light, optional"},
    5:  {"block": "Build", "A": (6, 4), "B": (4, 4), "Bt": "3-1-3 tempo", "C": "1 AMRAP, then 4 back-off sets at ~65%.", "acc": "4×3 negatives + weighted dead hang or 3×8 rows"},
    6:  {"block": "Build", "A": (7, 4), "B": (5, 4), "Bt": "3-1-3 tempo", "C": "1 AMRAP, then 4 back-off sets at ~65%.", "acc": "4×3 negatives + rows 4×8"},
    7:  {"block": "Build", "A": (6, 5), "B": (5, 4), "Bt": "3-1-3 tempo", "C": "1 AMRAP, then 4 back-off sets at ~65%.", "acc": "3×3 negatives + rows 4×10"},
    8:  {"block": "Build · DELOAD", "A": (4, 4), "B": (3, 4), "Bt": "3-1-3 tempo, easy", "C": "1 AMRAP only — retest, compare to wk4.", "acc": "light, optional"},
    9:  {"block": "Strength", "A": (7, 5), "B": (4, 3), "Bt": "+5–10 lb (or slower tempo if no weight)", "C": "1 AMRAP, then 4 back-off sets at ~70%.", "acc": "3×3 negatives (weighted if able) + rows 4×8"},
    10: {"block": "Strength", "A": (8, 5), "B": (4, 3), "Bt": "weighted / tempo", "C": "1 AMRAP, then 4 back-off sets at ~70%.", "acc": "3×3 weighted negatives + rows 4×8"},
    11: {"block": "Strength", "A": (6, 6), "B": (5, 3), "Bt": "weighted / tempo", "C": "1 AMRAP, then 5 back-off sets at ~70%.", "acc": "3×3 weighted negatives + rows 4×10"},
    12: {"block": "Strength · DELOAD", "A": (4, 5), "B": (3, 3), "Bt": "3-1-3 tempo", "C": "1 AMRAP only — retest, compare to wk8.", "acc": "light, optional"},
    13: {"block": "Peak", "A": (8, 5), "B": (5, 4), "Bt": "3-1-3 tempo", "C": "1 AMRAP, then 4 back-off sets at ~70%.", "acc": "3×3 negatives + rows 4×10"},
    14: {"block": "Peak", "A": (6, 6), "B": (5, 4), "Bt": "3-1-3 tempo", "C": "2 AMRAP sets (rest 3 min between), then 3 back-off sets at ~65%.", "acc": "3×3 negatives + rows 4×10"},
    15: {"block": "Peak", "A": (5, 7), "B": (4, 4), "Bt": "3-1-3 tempo", "C": "1 AMRAP, then 3 back-off sets at ~75%.", "acc": "2×3 negatives (taper begins)"},
    16: {"block": "Peak · TEST", "A": (4, 4), "B": (2, 3), "Bt": "light", "C": "Rest 3+ days before this. One all-out MAX TEST — record the number.", "acc": "none this week"},
}

def pull_session(w, day, slot, prog_wk):
    """Build a pull-up session for the given program week (or maintenance if prog_wk is None)."""
    if prog_wk and prog_wk <= 16:
        sp = PULL_PROGRAM[prog_wk]
        acc, block = sp["acc"], sp["block"]
        if slot == "A":
            sets, reps = sp["A"]; title = "Pull-Ups — Volume"
            note = (f"[{block} · pull-up wk {prog_wk}] VOLUME — {sets}×{reps}. All sets submax, stop 0–1 reps "
                    f"before form breaks. Full dead hang, chin over bar. Rest ~2 min. Accessory: {acc}.")
            body = {"sets": sets, "reps": reps}
        elif slot == "B":
            sets, reps = sp["B"]; title = "Pull-Ups — Tempo"
            note = (f"[{block} · pull-up wk {prog_wk}] TEMPO — {sets}×{reps}, {sp['Bt']}. Crisp and submax. "
                    f"Rest ~2 min. Accessory: {acc}.")
            body = {"sets": sets, "reps": reps}
        else:
            title = "Pull-Ups — Intensity"
            note = (f"[{block} · pull-up wk {prog_wk}] INTENSITY — {sp['C']} Stop 0–1 before failure on AMRAP. "
                    f"Rest ~2 min (3 min around AMRAP sets). Accessory: {acc}.")
            body = {"sets": 1, "reps": "AMRAP"}
    else:  # maintenance — plan weeks 17–21, program already tested at wk16
        if slot == "B":
            title = "Pull-Ups — Maintenance (Tempo)"
            note = "Maintenance — 3×4 tempo (3-1-3), submax and crisp. Program's done; hold your gains, no PR chasing during the race taper."
            body = {"sets": 3, "reps": 4}
        else:
            title = "Pull-Ups — Maintenance"
            note = "Maintenance — 4×4 submax. Program's done; hold your gains, no testing during the race taper."
            body = {"sets": 4, "reps": 4}
    reps_n = _reps_num(body["reps"])
    dur = max(10, round((body["sets"] * (reps_n * 3 + 90) / 60 + 7) / 5) * 5)  # main sets + ~7m accessories/hangs
    return {"id": f"w{w}-{day}-pull", "type": "pullups", "title": title, "emoji": "🧗",
            "day": day, "rest": 90, **body, "duration": dur, "note": note}

# 14-week max-effort / muscular-endurance leg progression. One session/week, WO#1 on wk1.
# rj = rest/set for the jumps (+ goblet/KB), rb = rest/set for Box Step-Ups & Lunges,
# rx = rest between exercises (documented in note; engine auto-rests 60s between groups).
ME_PROGRAM = {
    1:  {"sets": 6, "wt": "Bodyweight",      "rj": 60, "rb": 30, "rx": 60},
    2:  {"sets": 6, "wt": "Bodyweight",      "rj": 60, "rb": 30, "rx": 60},
    3:  {"sets": 6, "wt": "Bodyweight",      "rj": 45, "rb": 30, "rx": 60},
    4:  {"sets": 5, "wt": "+≤10% BW (vest)", "rj": 60, "rb": 60, "rx": 60},
    5:  {"sets": 6, "wt": "+10% BW",         "rj": 45, "rb": 30, "rx": 90},
    6:  {"sets": 6, "wt": "+10% BW",         "rj": 40, "rb": 30, "rx": 60},
    7:  {"sets": 6, "wt": "+10% BW",         "rj": 30, "rb": 30, "rx": 60},
    8:  {"sets": 8, "wt": "+10% BW",         "rj": 45, "rb": 30, "rx": 60},
    9:  {"sets": 6, "wt": "+15% BW",         "rj": 40, "rb": 30, "rx": 45},
    10: {"sets": 8, "wt": "+15% BW",         "rj": 45, "rb": 30, "rx": 30},
    11: {"sets": 8, "wt": "+15% BW",         "rj": 30, "rb": 20, "rx": 30},
    12: {"sets": 8, "wt": "+15% BW",         "rj": 15, "rb": 15, "rx": 20},
    13: {"sets": 8, "wt": "+15% BW",         "rj": 10, "rb": 10, "rx": 10},
    14: {"sets": 8, "wt": "+15% BW",         "rj": 10, "rb": 10, "rx": 10},
}

def _reps_num(r):
    if r == "AMRAP":
        return 8
    if isinstance(r, list):
        return sum(r) / len(r)
    return r

def est_strength_min(blocks, group_rest=60):
    """Estimated minutes: sum sets × (work + between-set rest), + group rest between blocks."""
    total = 0
    for blk in blocks:
        for ex in blk["exercises"]:
            work = ex["seconds"] if ex["movementType"] == "timed" else _reps_num(ex["reps"]) * 2.5 * (2 if ex.get("perSide") else 1)
            rest = ex.get("rest", 30)
            sets = ex["sets"]
            total += sets * work + max(0, sets - 1) * rest
    total += group_rest * max(0, len(blocks) - 1)
    return max(15, round(total / 300) * 5)

def s_me_legs(w, wo):
    warm = [
        {"name": "High Knees", "equipment": "Bodyweight", "movementType": "timed",
         "sets": 1, "seconds": 40, "working": False, "logReps": False,
         "note": "Quick feet, drive the knees to hip height."},
        {"name": "Jumping Jacks", "equipment": "Bodyweight", "movementType": "timed",
         "sets": 1, "seconds": 40, "working": False, "logReps": False},
        {"name": "Butt Kicks", "equipment": "Bodyweight", "movementType": "timed",
         "sets": 1, "seconds": 30, "working": False, "logReps": False},
        {"name": "Bodyweight Squats", "equipment": "Bodyweight", "movementType": "reps",
         "sets": 1, "reps": 15, "rest": 0, "working": False, "logReps": False,
         "note": "Full depth, controlled — grease the pattern."},
        {"name": "Get-Ups", "equipment": "Bodyweight", "movementType": "reps",
         "sets": 1, "reps": 10, "rest": 20, "working": False, "logReps": False,
         "note": "Get up off the floor from lying down, any method."},
        {"name": "Burpees", "equipment": "Bodyweight", "movementType": "reps",
         "sets": 1, "reps": 10, "rest": 20, "working": False, "logReps": False},
    ]
    cool = [
        {"name": "Quad Stretch", "equipment": "Bodyweight", "movementType": "timed",
         "sets": 1, "seconds": 30, "perSide": True, "working": False, "logReps": False},
        {"name": "Standing Hamstring Stretch", "equipment": "Bodyweight", "movementType": "timed",
         "sets": 1, "seconds": 30, "perSide": True, "working": False, "logReps": False},
        {"name": "Calf Stretch", "equipment": "Bodyweight", "movementType": "timed",
         "sets": 1, "seconds": 30, "perSide": True, "working": False, "logReps": False},
    ]
    if wo:
        sp = ME_PROGRAM[wo]; sets = sp["sets"]; wt = sp["wt"]
        rj, rb, rx = sp["rj"], sp["rb"], sp["rx"]; added = wo >= 4
        title = f"Lower — ME Circuit (WO #{wo})"
        equip = "Box · Vest · Kettlebell · Dumbbell" if added else "Box · Bodyweight"
        notes = (f"ME LEG PROGRESSION · WO #{wo} — {wt}. {sets}×10 each; finish all sets of an exercise before "
                 f"the next. Hold the tempos, don't rush. Rests: jumps {rj}s/set · Box Step-Ups & Lunges "
                 f"{rb}s/set · {rx}s between exercises.")
    else:
        sets = 3; rj = rb = 45; rx = 60; added = False
        title = "Lower — Maintenance"
        equip = "Box · Bodyweight"
        notes = ("Lower maintenance — bodyweight, 3×10, easy. ME progression is complete; keep the patterns "
                 "sharp without fatiguing the legs during the race taper.")

    circuit = [
        {"name": "Split Jump Squat", "equipment": "Bodyweight / Vest", "movementType": "reps",
         "sets": sets, "reps": 10, "rest": rj, "perSide": True, "swapGroup": "split",
         "note": "~1 jump/sec each leg. Explosive up, soft controlled landing."},
        {"name": "Squat Jump", "equipment": "Bodyweight / Vest", "movementType": "reps",
         "sets": sets, "reps": 10, "rest": rj, "swapGroup": "squat",
         "note": "~1 jump per ½–1 sec. Full extension, soft landing."},
        {"name": "Box Step-Up", "equipment": "Box · Vest", "movementType": "reps",
         "sets": sets, "reps": 10, "rest": rb, "perSide": True, "swapGroup": "stepup",
         "note": "Box ≈75% of the height to the bottom of your kneecap. All R reps, then all L. ~1 rep/sec."},
        {"name": "Front Lunge", "equipment": "Bodyweight / Vest", "movementType": "reps",
         "sets": sets, "reps": 10, "rest": rb, "perSide": True, "swapGroup": "lunge",
         "note": "Gentle 40–60 cm (16–24 in) step. All R, then all L. ~1 rep/sec. Hits the glutes hardest."},
    ]
    if added:
        circuit += [
            {"name": "Goblet Squat to Overhead Press", "equipment": "Dumbbell / KB", "movementType": "reps",
             "sets": sets, "reps": 10, "rest": rj, "swapGroup": "squat"},
            {"name": "2-Hand Kettlebell Swing", "equipment": "Kettlebell", "movementType": "reps",
             "sets": sets, "reps": 10, "rest": rj, "swapGroup": "hinge"},
        ]

    work = 18  # avg seconds of work per set
    set_rests = [rj, rj, rb, rb] + ([rj, rj] if added else [])
    circuit_s = sum(sets * work + max(0, sets - 1) * r for r in set_rests) + max(0, len(set_rests) - 1) * rx
    dur = max(30, round((300 + circuit_s + 180) / 300) * 5)  # warm ~5m + circuit + cool ~3m, nearest 5m
    return {"id": f"w{w}-mon-lower", "type": "strength", "title": title, "emoji": "🦵", "day": "mon",
            "duration": dur, "groupRest": rx, "equipment": equip, "notes": notes,
            "blocks": [
                {"name": "Warm-Up", "emoji": "🔥", "exercises": warm},
                {"name": "Lower Power Circuit", "emoji": "🦵", "exercises": circuit},
                {"name": "Cool-Down", "emoji": "🧊", "exercises": cool},
            ]}

def s_upper(w, variant):
    blocks = upper_a_blocks() if variant == "A" else upper_b_blocks()
    title = "Upper — Chest Focus" if variant == "A" else "Upper — Back Focus"
    return {"id": f"w{w}-wed-upper", "type": "strength", "title": title, "emoji": "💪", "day": "wed",
            "duration": est_strength_min(blocks), "equipment": "Bar · Dumbbells · Bench · TRX",
            "notes": "Go hard — upper work doesn't cost the legs. Supersets (🔁) run back-to-back; rest only after the round.",
            "blocks": blocks}

def s_easy(w, day, t=45, notes="Conversational, nose-breathing. Z2 only — easy means easy."):
    return {"id": f"w{w}-{day}-easy", "type": "run", "title": "Easy Run", "emoji": "🏃", "day": day,
            "runType": "easy", "time": t, "targets": {"hrZone": "2", "rpe": 4}, "notes": notes}

def s_strides(w, day, t):
    return {"id": f"w{w}-{day}-flat", "type": "run", "title": "Flat Aerobic + Strides", "emoji": "🏃", "day": day,
            "runType": "easy", "time": t, "targets": {"hrZone": "2", "rpe": 4},
            "notes": "From home — flat canal paths / neighborhood. Easy Z2, finish with 6×20s relaxed strides."}

def s_tempo(w, day, t):
    warm, cool = 12, 8
    work = max(15, t - warm - cool)
    return {"id": f"w{w}-{day}-flat", "type": "run", "title": "Flat Tempo", "emoji": "🏃", "day": day,
            "runType": "tempo", "time": t, "targets": {"hrZone": "3-4", "rpe": 6},
            "segments": [
                {"label": "Warm-up", "time": warm, "intensity": "easy"},
                {"label": "Tempo", "time": work, "intensity": "comfortably hard / Z3–4"},
                {"label": "Cool-down", "time": cool, "intensity": "easy"},
            ],
            "notes": "From home — flat canal paths. Steady comfortably-hard, no hills. Aerobic-power work that replaces the old weekday vert (vert now lives on the weekend)."}

def s_weekday_quality(w, day, phase, wnum):
    t = {"Base": 40, "Build": 50, "Peak": 50, "Recovery": 35, "Taper": 35}.get(phase, 45)
    if phase in ("Build", "Peak") and wnum not in (16, 17):
        return s_tempo(w, day, t)
    return s_strides(w, day, t)

def est_run_min(dist, vert):
    # Calibrated to the April R2R (18.88 mi / 5,190 ft↑ / 8:02 moving): ~18 min/mi + 28 min per 1,000 ft↑.
    return round(dist * 18 + vert / 1000 * 28)

def s_long(w, day, title, dist, vert, notes, emoji="🥾", rpe=5, hr="2"):
    return {"id": f"w{w}-{day}-long", "type": "run", "title": title, "emoji": emoji, "day": day,
            "runType": "long", "distance": dist, "vertFt": vert, "time": est_run_min(dist, vert),
            "targets": {"hrZone": hr, "rpe": rpe}, "notes": notes}

def s_bike(w):
    return {"id": f"w{w}-sun-bike", "type": "bike", "title": "Z2 Spin", "emoji": "🚴", "day": "sun",
            "optional": True, "bikeType": "recovery", "time": 60, "targets": {"hrZone": "1-2", "rpe": 3},
            "notes": "Optional aerobic flush on the cycling base. Skip if legs need rest before Saturday."}

def s_b2b(w, dist, vert):
    return {"id": f"w{w}-sun-b2b", "type": "run", "title": "Back-to-Back Long", "emoji": "🥾", "day": "sun",
            "runType": "long", "distance": dist, "vertFt": vert, "time": est_run_min(dist, vert),
            "targets": {"hrZone": "2", "rpe": 5},
            "notes": "On tired legs from yesterday — this is the durability adaptation. Easy Z2, time on feet, eat and drink on schedule."}

def s_rest(w, day, notes="Full rest. Light mobility / stretch optional."):
    return {"id": f"w{w}-{day}-rest", "type": "rest", "title": "Rest", "emoji": "😴", "day": day, "notes": notes}

# ---------------------------------------------------------------- per-week config
# kind: "std" standard week, "travel" Wk6, "race" Wk21
FUEL = "Full race nutrition: 60–90 g carb/hr (Tailwind + gels), 500–1000 mg sodium/hr."
HYDRO = "Drink aggressively on the descent — 15-min timer, sip every beep, even when not thirsty."

WEEKS = [
    # w, phase, focus, lower_variant, easy_t, (vert_laps,vert,vert_t), long(title,dist,vert,notes), sun
    (1, "Base", "Reactivate. Marquee: Humphreys Peak. Add strength.", "A", 40, (2,1600,55),
     ("Humphreys Peak", 12, 3300, "Season kickoff sustained climb. Steady hike-run, fuel every 30–45 min, never redline. " + HYDRO), "bike"),
    (2, "Base", "Cutback from Humphreys. Easy aerobic + lift intro.", "B", 40, (2,1200,45),
     ("Long Run", 7, 800, "Recovery long — Hawes rolling. Pure easy Z2, no vert hunting."), "bike"),
    (3, "Base", "Build aerobic base. Intro vert volume.", "A", 40, (2,1600,55),
     ("Pass Mountain Loop +", 9, 1500, "Pass Mtn CCW (sustained ~700 ft section) + add a Wind Cave lap. Time on feet."), "bike"),
    (4, "Build", "Vertical block opens. More vert, more volume.", "B", 45, (3,2400,80),
     ("Long Run", 10, 1800, "Hawes long loop + climb. Settle into all-day fueling rhythm."), "bike"),
    (5, "Build", "Peak pre-travel volume (NC departs ~Jul 2).", "A", 45, (3,2400,80),
     ("Long Run", 11, 2000, "Biggest pre-travel day. " + HYDRO), "bike"),
    # Wk6 = NC travel deload, handled as "travel"
    (6, "Recovery", "NC travel (Jul 2–11). Deload — bodyweight + easy miles, maintain only.", "B", 35, None,
     ("Easy Long", 6, 600, "Wherever you are in NC. Easy rolling, explore on foot. No structure — just move."), "travel"),
    (7, "Build", "Re-enter the vertical block. Rebuild after travel.", "A", 45, (2,1600,55),
     ("Long Run", 11, 2200, "Ease back into vert. Hawes + Pass Mtn."), "bike"),
    (8, "Build", "First true sustained climb of the block.", "B", 45, (3,2400,80),
     ("Peralta → Fremont Saddle +", 7, 2000, "First sustained climb. Pure trail to the saddle, extend past for more. Power-hike the steep, run the runnable. " + FUEL), "bike"),
    (9, "Build", "Consolidate vert. Lengthen time on feet.", "A", 45, (3,2400,80),
     ("Long Run", 12, 2500, "Superstition foothills mix. Practice eating solid food past hour 2."), "bike"),
    (10, "Build", "Back-to-back block begins. Sat + Sun stacked.", "B", 50, (3,2400,80),
     ("Long Run", 12, 3000, "Big vert day. " + HYDRO), ("b2b", 6, 800)),
    (11, "Build", "Repeat-climb durability. Peralta doubled.", "A", 50, (3,2400,80),
     ("Peralta ×2", 12, 4000, "Two full laps to the saddle. The repeat is the point — quads under sustained eccentric load. " + FUEL), ("b2b", 7, 1000)),
    (12, "Build", "Sustained vert + stacked Sunday.", "B", 50, (3,2400,80),
     ("Long Run", 13, 3500, "Superstition sustained climb. Dial fueling: 60–90 g/hr without GI trouble."), ("b2b", 8, 1000)),
    (13, "Peak", "Peak vertical. Two-trailhead big day.", "A", 50, (3,2400,80),
     ("Siphon Draw basin ×2 + Peralta", 13, 4800, "Two trailheads, biggest vert of the build. Stop before the Flatiron chute — no scrambling. Full kit, " + FUEL + " " + HYDRO), ("b2b", 8, 1200)),
    (14, "Peak", "Canyon simulation — descent-heavy, sustained.", "B", 50, (3,2400,80),
     ("Carney Springs → Carney Pass + Peralta", 13, 3800, "Canyon sim: long sustained climb then a long descent to hammer the quads (race crux is the climb-out on trashed legs). Stop before the summit ridge. " + FUEL), ("b2b", 9, 1200)),
    (15, "Peak", "Last big block week before rehearsal. Slight back-off.", "A", 50, (3,2400,80),
     ("Long Run", 12, 3000, "Controlled big day — bank durability without digging a hole before the rehearsal."), ("b2b", 8, 1000)),
    (16, "Peak", "FULL DRESS REHEARSAL (local). Then easy.", "B", 40, (2,1600,55),
     ("DRESS REHEARSAL — Siphon Draw + Peralta", 20, 6000, "3:30 AM headlamp start. ~8–10 hrs moving. Loaded vest 8–12 lb, race shoes, poles, lights. Run EVERYTHING exactly like race day: " + FUEL + " " + HYDRO + " Keep stopped time under 10%. This is the dry run that answers '16 vs 14.'"), "rest"),
    (17, "Recovery", "Recover from the rehearsal. Absorb the work.", "A", 35, (2,1200,45),
     ("Easy Long", 8, 1000, "Easy shakeout long. Legs lead — back off if the rehearsal left a mark."), "rest"),
    (18, "Peak", "Sharpen. Low volume, keep the engine lit.", "B", 45, (3,2400,75),
     ("Long Run", 12, 2500, "Quality sustained climb at goal effort. Sharp, not exhausting."), "bike"),
    (19, "Taper", "Taper begins. Trim volume, hold frequency.", "A", 40, (2,1600,55),
     ("Long Run", 9, 1500, "Shorter sustained climb. Stay crisp, don't chase fitness now — it's banked."), "rest"),
    (20, "Taper", "Deep taper. Stay loose, stay fresh.", "B", 35, (1,800,30),
     ("Long Run", 6, 800, "Short and easy. Legs should feel springy by the end."), "rest"),
    # Wk21 = race, handled as "race"
    (21, "Taper", "Race week. Travel, rest, execute.", "A", 30, None, None, "race"),
]

# ---------------------------------------------------------------- assemble
def build_week(cfg):
    w, phase, focus, variant, easy_t, vert, long_cfg, sun = cfg
    sessions = []
    prog = w if w <= 16 else None  # pull-up program week (None = maintenance)
    wo_l = w if w <= 14 else None  # ME leg workout number (None = maintenance)

    if sun == "travel":  # Wk6 NC deload
        lo = s_me_legs(w, None)
        lo["title"] = "Lower — Travel (Bodyweight)"
        lo["notes"] = ("Travel week — bodyweight core four only (use a step/curb for step-ups; no vest/KB). "
                       "Keep it easy. Resume the ME progression (~WO #6) when home — treat a fully missed week as 'drop back two.'")
        up = s_upper(w, variant); up["equipment"] = "Bar / Bodyweight / TRX"; up["title"] = "Upper (Travel)"
        tp = pull_session(w, "tue", "A", prog)
        tp["note"] = "TRAVEL — do what you can. A bar is ideal; no bar = negatives off a sturdy edge + bands. " + tp["note"] + " Don't stress the desync — resume the progression when you're home."
        sessions += [
            lo,
            s_easy(w, "tue", easy_t, "Explore NC on foot. Easy Z2."), tp,
            up,
            s_rest(w, "thu"),
            s_rest(w, "fri"),
            s_long(w, "sat", *long_cfg[:3], notes=long_cfg[3]),
            s_rest(w, "sun"),
        ]
        # fix lower day -> it's tagged mon id; keep on mon
        return {"week": w, "phase": phase, "focus": focus, "sessions": sessions}

    if sun == "race":  # Wk21
        sessions = [
            s_easy(w, "mon", 30, "Shakeout — short and easy. Legs only, no vert. Final gear sort."),
            {"id": f"w{w}-mon-pull", "type": "pullups", "title": "Pull-Ups — Easy", "emoji": "🧗", "day": "mon",
             "rest": 90, "sets": 3, "reps": 3, "duration": 10, "note": "Race week — stay loose. 3×3 easy, optional. Everything's banked; save it for race day."},
            s_rest(w, "tue", "Travel to the canyon (lodging Tusayan / GC Village). Hydrate, carb-load, sleep."),
            {"id": f"w{w}-wed-shake", "type": "run", "title": "Leg-Opener Shakeout", "emoji": "🏃", "day": "wed",
             "runType": "recovery", "time": 20, "targets": {"hrZone": "1-2", "rpe": 2},
             "notes": "15–20 min very easy + a few strides. Stage all gear. Early to bed."},
            {"id": f"w{w}-thu-race", "type": "run", "title": "RACE DAY — R2R2R", "emoji": "🏔️", "day": "thu",
             "runType": "long", "distance": 44, "vertFt": 11000, "time": 960, "targets": {"rpe": 7},
             "notes": "16-hr target. SK down controlled (quad preservation) → respect the North Kaibab climb as the crux (hottest/longest) → return half is slower → win it on stopped-time discipline (<10%) and not blowing up the climb-out. " + FUEL + " " + HYDRO + " 100 mg caffeine pre-race; caffeinated gels saved for hour 8+."},
            s_rest(w, "fri", "Done. Eat, walk, celebrate."),
            s_rest(w, "sat"),
            s_rest(w, "sun"),
        ]
        return {"week": w, "phase": phase, "focus": focus, "sessions": sessions}

    # standard week
    sessions += [s_me_legs(w, wo_l), pull_session(w, "mon", "A", prog)]
    sessions += [s_easy(w, "tue", easy_t, "From home — flat canal paths / neighborhood. Conversational Z2."), pull_session(w, "tue", "B", prog)]
    sessions += [s_upper(w, variant)]
    sessions += [s_weekday_quality(w, "thu", phase, w)]
    sessions += [pull_session(w, "fri", "C", prog)]
    sessions += [s_long(w, "sat", *long_cfg[:3], notes=long_cfg[3])]
    if sun == "bike":
        sessions += [s_bike(w)]
    elif sun == "rest":
        sessions += [s_rest(w, "sun")]
    elif isinstance(sun, tuple) and sun[0] == "b2b":
        sessions += [s_b2b(w, sun[1], sun[2])]

    return {"week": w, "phase": phase, "focus": focus, "sessions": sessions}

# ---------------------------------------------------------------- derive targets + validate
TYPE2TARGET = {"strength": "lift", "run": "run", "bike": "bike", "pullups": "pullups"}

def derive_targets(week):
    c = collections.Counter()
    for s in week["sessions"]:
        k = TYPE2TARGET.get(s["type"])
        if k:
            c[k] += 1
    # always present keys for the progress bars
    return {k: c.get(k, 0) for k in ["lift", "run", "bike", "pullups"]}

weeks = []
for cfg in WEEKS:
    wk = build_week(cfg)
    wk_out = {"week": wk["week"], "phase": wk["phase"], "focus": wk["focus"],
              "targets": derive_targets(wk), "sessions": wk["sessions"]}
    weeks.append(wk_out)

plan = {
    "plan": {
        "name": "Grand Canyon R2R2R Build",
        "goal": "R2R2R — Oct 22, 2026 · 16-hour target",
        "startDate": "2026-06-01",
        "units": "imperial",
        "scheduleMode": "byDay",
    },
    "weeks": weeks,
}

# ---- validation ----
ids = [s["id"] for wk in weeks for s in wk["sessions"]]
assert len(ids) == len(set(ids)), "duplicate session id"
VALID_DAYS = {"mon","tue","wed","thu","fri","sat","sun"}
for wk in weeks:
    for s in wk["sessions"]:
        assert s["day"] in VALID_DAYS, s
        if s["type"] == "strength":
            assert s["blocks"], s
            for blk in s["blocks"]:
                for ex in blk["exercises"]:
                    assert ex["movementType"] in ("reps","timed")
                    if ex["movementType"] == "reps":
                        r = ex["reps"]
                        assert r == "AMRAP" or isinstance(r,int) or (isinstance(r,list) and len(r)==ex["sets"]), (s["id"],ex)
                        assert isinstance(ex["rest"], int) and ex["rest"] >= 0, (s["id"],ex)  # literal seconds; see APP_BUILDER_NOTES.md
                    else:
                        assert "seconds" in ex
        if s["type"] in ("run","bike"):
            assert ("time" in s) or ("distance" in s), s

with open("/Users/konradrodak/Documents/Training/plan.json", "w") as f:
    json.dump(plan, f, indent=2, ensure_ascii=False)

print(f"OK — {len(weeks)} weeks, {len(ids)} sessions, all ids unique, validation passed.")
for wk in weeks:
    t = wk["targets"]
    print(f"  Wk{wk['week']:>2} {wk['phase']:<9} lift{t['lift']} run{t['run']} bike{t['bike']} pull{t['pullups']}  — {wk['focus'][:48]}")
