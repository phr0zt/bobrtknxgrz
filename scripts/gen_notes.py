#!/usr/bin/env python3
"""Generates GEARS.md from the same catalog/edge data as technic-gear-atlas.html.
Run manually after editing the data below (kept in sync with the HTML by hand)."""

FAMILIES = {
    "a":    ("Spur — Group A", "The original Technic pitch (1977–). 8/16/24/40-tooth gears mesh freely with each other and with a matching pinion rack."),
    "b":    ("Spur — Group B (double-bevel)", "A finer, later pitch (1999–). 12/20/36-tooth double-bevel gears mesh with each other and a matching rack — but not with Group A."),
    "wc":   ("Worm & Crown", "Special-purpose Group A partners: a self-locking worm screw and a crown gear that bridges parallel and right-angle drives."),
    "diff": ("Differential", "Splits torque between two outputs through an internal bevel gear set housed in a ring."),
    "tt":   ("Turntables", "Large slewing rings for rotating platforms — driven at their perimeter, not charted against pinion gears here."),
    "rack": ("Racks", "Straight or curved linear tracks. Come in two pitches, one per spur family."),
    "iso":  ("Isolated / self-mesh only", "Bevels and wheels deliberately built to mesh only with an identical copy of themselves."),
    "chain":("Sprockets & chain", "A separate drive system entirely — chain-tread links ride on sprockets and never mesh tooth-to-tooth with a gear."),
}

ITEMS = [
    ("a8","a","8-Tooth Gear","8t","1977","The smallest common spur gear."),
    ("a16","a","16-Tooth Gear","16t","1979",""),
    ("a24","a","24-Tooth Gear","24t","1977","Also sold as a white clutch gear that slips above a torque threshold — meshes identically."),
    ("a40","a","40-Tooth Gear","40t","1977","The largest Group A spur gear; a heavy reduction stage."),
    ("b12","b","12-Tooth Double-Bevel","12t","1999","Runs parallel like a spur gear, or at 90° against another bevel."),
    ("b20","b","20-Tooth Double-Bevel","20t","1999",""),
    ("b36","b","36-Tooth Double-Bevel","36t","2002","The largest System-pitch gear; treated as parallel-only here."),
    ("worm","wc","Worm Gear (Screw)","1 thread","1985","Non-backdrivable — locks the output. Turns only 24t/40t Group A gears."),
    ("crown24","wc","24-Tooth Crown Gear","24t","1977","Doubles as a Group A spur gear and mates 90° with bevels."),
    ("diff","diff","Differential Housing","~28t ring","","Its input ring meshes at 90° with a bevel pinion."),
    ("tt28","tt","Small Turntable","28t","2012",""),
    ("tt56","tt","Large Turntable","56t","1990","Studless since 2004; a 60-tooth bevel-edge variant ran 2015–2022."),
    ("rackA","rack","Gear Rack — Group A pitch","linear","","Matches any 8/16/24/40-tooth pinion."),
    ("rackB","rack","Gear Rack — System pitch","linear","","Matches 12/20/36-tooth double-bevel pinions."),
    ("bevel14","iso","14-Tooth Bevel (original)","14t","1980","Superseded by the 12t bevel; meshes only with its own kind and the differential."),
    ("bevel2022","iso","22t / 14t Thick Bevel","22t / 14t","2022","A newer, stronger pair deliberately isolated from every other bevel."),
    ("knob","iso","Knob Wheel","6 lobes","","Chunky positive-drive wheel; meshes only with another knob wheel."),
    ("spr6","chain","Small Sprocket","6t","57520","Chain-drive only."),
    ("spr10","chain","Large Sprocket","10t","57519",""),
    ("spr14","chain","XL Sprocket","14t","42529",""),
    ("spr20","chain","Thin/Dual Sprocket","20t","32089","One chain loop can run mixed sprocket sizes together."),
]

EDGES = [
    ("a8","a16","spur"),("a8","a24","spur"),("a8","a40","spur"),
    ("a16","a24","spur"),("a16","a40","spur"),("a24","a40","spur"),
    ("a8","rackA","rack"),("a16","rackA","rack"),("a24","rackA","rack"),("a40","rackA","rack"),
    ("worm","a24","right"),("worm","a40","right"),
    ("crown24","a8","spur"),("crown24","a16","spur"),("crown24","a24","spur"),("crown24","a40","spur"),
    ("crown24","rackA","rack"),("crown24","worm","right"),("crown24","b12","right"),("crown24","bevel14","right"),
    ("b12","b20","right"),("b12","b36","spur"),("b20","b36","spur"),
    ("b12","rackB","rack"),("b20","rackB","rack"),("b36","rackB","rack"),
    ("diff","b12","right"),("diff","bevel14","right"),
]

NOTES = [
    "**Group A vs. Group B don't natively mesh.** The 8/16/24/40-tooth family and the 12/20/36-tooth double-bevel family use different tooth pitches. Builders can sometimes force a mesh (e.g. 24t↔12t) by spacing axles off-grid — a known community technique, not a designed interface, so it isn't charted here.",
    "**The worm gear is one-way.** It can turn a 24t or 40t gear, but a 24t/40t gear can't turn it back — useful for locking mechanisms and unsuitable anywhere back-drive is needed.",
    "**Turntables are driven at the rim**, typically by a small gear or worm pressed against their outer teeth, but which pinion pitch is 'standard' isn't consistently documented — left off the matrix rather than guessed.",
    "**Sprockets never mesh with gears** at all. They connect only through Technic chain-tread links, and a single chain loop happily mixes sprocket sizes (e.g. a 6t driving a 14t) — that's the one compatibility axis in this subsystem, and it's a chain relationship, not a tooth mesh, so it isn't in the matrix.",
    "Sourced from fan references (Rebrickable, BrickNerd, Technicopedia and community write-ups), not LEGO's own documentation — solid for planning a build, not spec-grade for manufacturing.",
]

GLYPH = {"spur": "●", "right": "⟂", "rack": "▬"}

def build():
    by_id = {i[0]: i for i in ITEMS}
    links = {i[0]: [] for i in ITEMS}
    for a, b, mode in EDGES:
        links[a].append((b, mode))
        links[b].append((a, mode))

    out = []
    out.append("# Technic Gear Atlas — Reference Notes\n")
    out.append("Every LEGO Technic gear, bevel, worm, rack, turntable and sprocket, "
                "with teeth counts, families, and exactly what meshes with what. "
                "Companion notes to [`technic-gear-atlas.html`](technic-gear-atlas.html) "
                "and [`technic-gear-atlas.pdf`](technic-gear-atlas.pdf).\n")

    for fkey, (flabel, fdesc) in FAMILIES.items():
        members = [i for i in ITEMS if i[1] == fkey]
        out.append(f"## {flabel}\n")
        out.append(fdesc + "\n")
        out.append("| Part | Teeth | Since / part # | Meshes with | Notes |")
        out.append("|---|---|---|---|---|")
        for pid, fam, name, teeth, meta, note in members:
            mesh = ", ".join(f"{GLYPH[m]} {by_id[l][2]}" for l, m in links[pid]) or "—"
            out.append(f"| {name} | {teeth} | {meta or '—'} | {mesh} | {note or '—'} |")
        out.append("")

    out.append("## Compatibility matrix\n")
    out.append("Standard direct interfaces only — same-axle-spacing meshes a builder gets "
                "by just putting the parts together. `●` parallel/spur · `⟂` right-angle "
                "(bevel/crown/worm/differential) · `▬` rack & pinion · `·` no standard mesh.\n")

    ids = [i[0] for i in ITEMS]
    header = "| |" + "|".join(ids) + "|"
    sep = "|---|" + "|".join(["---"] * len(ids)) + "|"
    out.append(header)
    out.append(sep)
    for row_id in ids:
        row_links = dict(links[row_id])
        cells = []
        for col_id in ids:
            if row_id == col_id:
                cells.append("—")
            elif col_id in row_links:
                cells.append(GLYPH[row_links[col_id]])
            else:
                cells.append("·")
        out.append(f"| **{row_id}** |" + "|".join(cells) + "|")
    out.append("")
    out.append("Codes: " + ", ".join(f"`{i[0]}` {i[2]}" for i in ITEMS) + "\n")

    out.append("## Notes & caveats\n")
    for n in NOTES:
        out.append(f"- {n}")
    out.append("")
    out.append("---\n_Technic Gear Atlas — a fan reference, not an official LEGO document. Compiled Aug 2026._")

    return "\n".join(out)


if __name__ == "__main__":
    print(build())
