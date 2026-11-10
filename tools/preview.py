"""Prints a dragon's stat block roughly as dnd5e shows it (for checking a build)."""
import json, re, sys
from fractions import Fraction
PROF = lambda cr: 2 + max(0, (int(cr) - 1) // 4) if cr >= 1 else 2
def mod(v): return (v - 10) // 2
def show(path):
    a = json.load(open(path)); s = a["system"]
    cr = s["details"]["cr"]; pb = PROF(cr); ab = {k: v["value"] for k, v in s["abilities"].items()}
    name = a["name"]
    def text(h):
        h = h.replace("[[lookup @name lowercase]]{monster}", name.lower())
        h = re.sub(r"\[\[lookup @labels\.description\.template[^\]]*\]\]", "<area>", h)
        h = re.sub(r"\[\[/save[^\]]*\]\]", "<save>", h); h = re.sub(r"\[\[/damage[^\]]*\]\]", "<damage>", h)
        h = re.sub(r"\[\[/item [^\]]*\]\]\{([^}]+)\}", r"\1", h); h = re.sub(r"&Reference\[([^\]]+)\]", r"\1", h)
        h = re.sub(r"\[\[lookup @labels\.description\.range[^\]]*\]\]", "<range>", h)
        h = re.sub(r"\[\[[^\]]*\]\]", "", h)
        return re.sub(r"<(?!area|save|damage|range)[^>]+>", " ", h).replace("  ", " ").strip()
    mv = s["attributes"]["movement"]; sn = s["attributes"]["senses"]; tr = s["traits"]
    print(f"== {name} ==  {tr['size']} dragon, {s['details']['alignment']}  CR {cr}  (prof +{pb})")
    print(f"AC {s['attributes']['ac']['flat']}  HP {s['attributes']['hp']['max']} ({s['attributes']['hp']['formula']})  "
          f"Speed " + ", ".join(f"{k} {v}" for k, v in mv.items() if k in ('walk','fly','swim','climb','burrow') and v))
    print("  " + "  ".join(f"{k.upper()} {v} ({mod(v):+d})" for k, v in ab.items()))
    print("  Saves: " + ", ".join(k for k, v in s["abilities"].items() if v["proficient"]), "| Senses:",
          {k: v for k, v in sn.items() if k in ('darkvision','blindsight','tremorsense','truesight') and v},
          "| Imm:", tr["di"]["value"], "Res:", tr["dr"]["value"], "CondImm:", tr["ci"]["value"], "| Lang:", tr["languages"]["value"])
    for it in a["items"]:
        acts = list((it["system"].get("activities") or {}).values())
        line = f"  * {it['name']}"
        for act in acts:
            if act["type"] == "attack":
                base = it["system"].get("damage", {}).get("base", {})
                extra = " + ".join(f"{p['number']}d{p['denomination']} {'/'.join(p['types'])}" for p in act["damage"]["parts"])
                line += f" [+{mod(ab['str']) + pb} to hit, {base.get('number')}d{base.get('denomination')}+{mod(ab['str'])} {'/'.join(base.get('types', []))}{' + ' + extra if extra else ''}, reach {it['system']['range'].get('reach')}]"
            elif act["type"] == "save":
                dc = 8 + pb + mod(ab[act['save']['dc']['calculation']]) if act['save']['dc']['calculation'] in ab else act['save']['dc']['formula']
                tpl = act['target']['template']
                parts = " + ".join(f"{p['number']}d{p['denomination']} {'/'.join(p['types'])}" for p in act["damage"]["parts"])
                line += f" [{act.get('name') or ''}: DC {dc} {'/'.join(act['save']['ability'])} {tpl.get('type') or ''} {tpl.get('size') or ''} {parts} {act['activation']['type']}{'' if not act['effects'] else ' +effect'}]"
        print(line)
        d = text(it["system"]["description"]["value"])
        if it["name"] not in ("Bite", "Claw", "Tail", "Claws") and d:
            print("      " + d[:400])
for p in sys.argv[1:]:
    show(p); print()
