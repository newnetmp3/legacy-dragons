#!/usr/bin/env python3
"""Builds the Legacy Dragons compendium source from dragons.py.

Each dragon at each age starts from the dnd5e system's SRD 5.1 dragon of the
same age and tier (its "chassis": layout, attacks, legendary actions and the
numbers behind its challenge rating), then gets its own name, abilities,
damage types, breath weapons, traits, lore, lair actions and token.

  python3 tools/build.py <dnd5e checkout> <output folder for the JSON source>

<dnd5e checkout>: a clone of github.com/foundryvtt/dnd5e at the release the
module targets (packs/_source/monsters/dragon is read).
Then tools/pack.mjs compiles the JSON source into packs/legacy-dragons.
"""
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from dragons import AMPHIBIOUS, CHANGE_SHAPE, DRAGONS, FOLDERS, ICE_WALK  # noqa: E402

MODULE = "legacy-dragons"
AGES = ["wyrmling", "young", "adult", "ancient"]
AGE_NAME = {"wyrmling": "{n} Wyrmling", "young": "Young {n}", "adult": "Adult {n}", "ancient": "Ancient {n}"}
CHASSIS = {"chromatic": {1: "white", 2: "black", 3: "green", 4: "blue", 5: "red"},
           "metallic": {1: "brass", 2: "copper", 3: "bronze", 4: "silver", 5: "gold"}}
CONE = [15, 30, 60, 90]
LINE = [(30, 5), (60, 5), (90, 10), (120, 10)]
BURROW = [15, 20, 30, 40]
TOKEN_SIZE = {"tiny": 0.5, "sm": 1, "med": 1, "lg": 2, "huge": 3, "grg": 4}
LANG = {"deep speech": "deep", "auran": "auran", "aquan": "aquan"}
PHYSICAL = {"bludgeoning", "piercing", "slashing"}
DR = "[[lookup @name lowercase]]{monster}"
ID_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def new_id(*parts) -> str:
    """A stable 16-character Foundry id, so rebuilding doesn't change ids (and links)."""
    h = int(hashlib.sha256("/".join(map(str, parts)).encode()).hexdigest(), 16)
    out = ""
    for _ in range(16):
        h, r = divmod(h, 62)
        out += ID_CHARS[r]
    return out


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def fill(text: str) -> str:
    """{DR} -> "The"/"the" + the dragon's name, as dnd5e writes it."""
    text = re.sub(r"(^|[.!?]\s+)\{DR\}", lambda m: m.group(1) + "The " + DR, text)
    return text.replace("{DR}", "the " + DR)


def para(text: str) -> str:
    return "<p>" + fill(text) + "</p>"


def mod(score: int) -> int:
    return (score - 10) // 2


def prof(cr) -> int:
    return 2 if cr < 5 else 2 + (int(cr) - 1) // 4


def with_dc(text: str, system: dict) -> str:
    """{DC:con} -> 8 + proficiency bonus + Constitution modifier for this dragon."""
    return re.sub(r"\{DC:(\w+)\}", lambda m: str(8 + prof(system["details"]["cr"]) +
                                                  mod(system["abilities"][m.group(1)]["value"])), text)


class Chassis:
    def __init__(self, root: Path):
        self.dir = root / "packs" / "_source" / "monsters" / "dragon"
        self.cache = {}

    def get(self, color: str, age: str) -> dict:
        name = f"{color}-dragon-wyrmling.yml" if age == "wyrmling" else f"{age}-{color}-dragon.yml"
        if name not in self.cache:
            self.cache[name] = yaml.safe_load((self.dir / name).read_text())
        return copy.deepcopy(self.cache[name])

    def item(self, color: str, age: str, name: str) -> dict:
        return next(i for i in self.get(color, age)["items"] if i["name"] == name)


def is_breath(item) -> bool:
    return item["type"] == "feat" and (item["name"].endswith(" Breath") or item["name"] == "Breath Weapons")


def remap_ids(doc: dict, salt: str) -> dict:
    """New ids for the actor, its items, their activities and effects; references in text follow."""
    ids = {doc["_id"]}
    for it in doc["items"]:
        ids.add(it["_id"])
        ids.update((it["system"].get("activities") or {}).keys())
        ids.update(e["_id"] for e in it.get("effects", []))
    text = json.dumps(doc)
    for old in sorted(ids, key=len, reverse=True):
        text = text.replace(old, new_id(salt, old))
    return json.loads(text)


def plain_feat(template: dict, name: str, html: str, salt: str) -> dict:
    it = copy.deepcopy(template)
    it["_id"] = new_id(salt, "feat", name)
    it["name"] = name
    it["system"]["description"] = {"value": html, "chat": ""}
    it["system"]["identifier"] = slug(name)
    it["system"]["activities"] = {}
    it["system"]["uses"] = {"max": "", "recovery": [], "spent": 0}
    it["system"]["source"] = {"custom": "Legacy Dragons", "book": "", "page": "", "license": "", "rules": "2014", "revision": 1}
    it["system"]["properties"] = ["trait"]
    it["effects"] = []
    it["_stats"].pop("compendiumSource", None)
    it["_stats"]["duplicateSource"] = None
    return it


def breath_item(ch: Chassis, color: str, age: str, d: dict, chassis_breath: dict, salt: str) -> dict:
    """The dragon's breath weapon(s), built on the chassis's breath item (recharge 5-6)."""
    name, shape, types, save, what, *extra = d["breath"]
    age_i = AGES.index(age)
    acts = list(chassis_breath["system"]["activities"].values())
    dmg = next(a for a in acts if a.get("damage", {}).get("parts"))
    part = dmg["damage"]["parts"][0]
    number, die = part["number"], part["denomination"]

    a1 = copy.deepcopy(dmg)
    a1["_id"] = new_id(salt, "breath1")
    a1["name"] = name
    t = a1["target"]["template"]
    if shape == "cone":
        t.update(type="cone", size=str(CONE[age_i]), width="")
    else:
        length, width = LINE[age_i]
        t.update(type="line", size=str(length), width=str(width))
    a1["save"]["ability"] = [save]
    base = {k: v for k, v in part.items()}
    if len(types) == 2:  # half of each type
        half = max(1, number // 2)
        a1["damage"]["parts"] = [dict(copy.deepcopy(base), number=half, types=[types[0]]),
                                 dict(copy.deepcopy(base), number=number - half, types=[types[1]])]
    else:
        a1["damage"]["parts"] = [dict(copy.deepcopy(base), types=list(types))]
    a1["damage"]["onSave"] = "half"
    a1["effects"] = []
    a1["description"] = {"chatFlavor": "", "value": ""}  # the chassis's own text describes its breath
    acts_out = {a1["_id"]: a1}
    shape_text = f"[[lookup @labels.description.template activity={a1['_id']}]]"
    first = (f"{DR} exhales {what} in a {shape_text}. Each creature in that area must make a "
             f"[[/save activity={a1['_id']}]] saving throw, taking [[/damage average activity={a1['_id']}]] damage on a "
             f"failed save, or half as much damage on a successful one." + (" " + extra[0] if extra else ""))
    effects = []
    if d.get("breath2"):
        n2, save2, effect_text, status = d["breath2"]
        a2 = copy.deepcopy(a1)
        a2["_id"] = new_id(salt, "breath2")
        a2["name"] = n2
        a2["save"]["ability"] = [save2]
        a2["damage"] = {"onSave": "none", "parts": []}
        a2["sort"] = a1.get("sort", 0) + 1
        if status:
            eff = copy.deepcopy(ch.item("gold", "adult", "Breath Weapons")["effects"][0])
            eff["_id"] = new_id(salt, "effect", n2)
            eff["name"] = n2
            eff["statuses"] = [status]
            eff["changes"] = []
            eff["description"] = ""
            eff["img"] = "icons/svg/aura.svg"
            effects.append(eff)
            a2["effects"] = [{"_id": eff["_id"], "onSave": False, "level": {"min": None, "max": None}}]
        else:
            a2["effects"] = []
        acts_out[a2["_id"]] = a2
        second = (f"{DR} unleashes its {n2[0].lower() + n2[1:]} in a [[lookup @labels.description.template activity={a2['_id']}]]. Each creature in "
                  f"that area must succeed on a [[/save activity={a2['_id']}]] saving throw or {fill(effect_text)}")
        html = (f"<p>The {DR} uses one of the following breath weapons.</p>"
                f"<p><strong>{name}.</strong> The {first}</p><p><strong>{n2}.</strong> The {second}</p>")
        item_name = "Breath Weapons"
    else:
        html = f"<p>The {first}</p>"
        item_name = name
    it = copy.deepcopy(chassis_breath)
    it["_id"] = new_id(salt, "breath")
    it["name"] = item_name
    it["system"]["activities"] = acts_out
    it["system"]["description"] = {"value": fill(html).replace("The The ", "The "), "chat": ""}
    it["system"]["identifier"] = slug(item_name)
    it["system"]["source"] = {"custom": "Legacy Dragons", "book": "", "page": "", "license": "", "rules": "2014", "revision": 1}
    it["effects"] = effects
    it["_stats"].pop("compendiumSource", None)
    return it


def build_actor(ch: Chassis, d: dict, age: str, folder_id: str, sort: int) -> dict:
    age_i = AGES.index(age)
    color = CHASSIS[d["chassis"]][d["tier"]]
    a = ch.get(color, age)
    salt = f"{d['key']}/{age}"
    name = AGE_NAME[age].format(n=d["name"])
    s = a["system"]
    for ab, delta in d.get("abil", {}).items():
        s["abilities"][ab]["value"] = max(1, min(30, s["abilities"][ab]["value"] + delta))

    # Items: keep attacks and legendary machinery; replace breath and chassis-specific traits.
    chassis_breath = next(i for i in a["items"] if is_breath(i))
    keep = [i for i in a["items"] if not is_breath(i) and i["name"] not in ("Change Shape", "Amphibious", "Ice Walk")]
    items = []
    for it in keep:
        # A few SRD natural weapons have no damage type (the ancient gold dragon's claw).
        base = it["system"].get("damage", {}).get("base") if it["type"] == "weapon" else None
        if base is not None and not base.get("types"):
            base["types"] = [{"Bite": "piercing", "Claw": "slashing", "Claws": "slashing", "Tail": "bludgeoning"}
                             .get(it["name"], "bludgeoning")]
        if it["name"] == "Bite":
            for act in it["system"]["activities"].values():
                parts = act.get("damage", {}).get("parts") or []
                types = (d["breath"] or [None, None, []])[2]
                elem = [t for t in types if t not in PHYSICAL]
                if parts and elem and len(types) <= 2:
                    for p in parts:
                        p["types"] = [elem[0]]
                elif parts:
                    act["damage"]["parts"] = []
        if it["name"] == "Wing Attack" and d["folder"] == "lung":
            it["name"] = "Coil Sweep"
            it["system"]["identifier"] = "coil-sweep"
            it["system"]["description"]["value"] = it["system"]["description"]["value"].replace(
                "beats its wings", "sweeps its long, serpentine body")
            for act in it["system"]["activities"].values():
                act["name"] = "Sweep"
        items.append(it)
    if d["breath"]:
        items.append(breath_item(ch, color, age, d, chassis_breath, salt))
    feat_base = ch.item("gold", "adult", "Amphibious")
    for t in d.get("traits", []):
        if t == AMPHIBIOUS:
            items.append(copy.deepcopy(feat_base))
        elif t == ICE_WALK:
            items.append(copy.deepcopy(ch.item("white", "adult", "Ice Walk")))
        elif t == CHANGE_SHAPE:
            if age_i >= 2:
                items.append(copy.deepcopy(ch.item("gold", "adult", "Change Shape")))
        else:
            tname, text, from_age = t
            if age_i >= from_age:
                items.append(plain_feat(feat_base, tname, para(with_dc(text, s)), salt))
    if age_i >= 2:
        lair = "".join(f"<li>{fill(x)}</li>" for x in d["lair"])
        it = plain_feat(feat_base, "Lair Actions",
                        f"<p>On initiative count 20 (losing initiative ties), the {DR} takes a lair action to cause one "
                        f"of the following effects; it can't use the same effect two rounds in a row:</p><ul>{lair}</ul>",
                        salt)
        it["system"]["properties"] = []
        items.append(it)
        s.setdefault("resources", {})["lair"] = {"value": True, "initiative": 20}
    a["items"] = items

    # Abilities and hit points.
    m = re.match(r"\s*(\d+)d(\d+)", s["attributes"]["hp"]["formula"])
    n, die = int(m.group(1)), int(m.group(2))
    bonus = n * mod(s["abilities"]["con"]["value"])
    hp = n * (die + 1) // 2 + bonus
    s["attributes"]["hp"].update(value=hp, max=hp, formula=f"{n}d{die} + {bonus}" if bonus >= 0 else f"{n}d{die} - {-bonus}")

    # Movement and senses.
    mv = s["attributes"]["movement"]
    walk = mv.get("walk") or 30
    mv.update(burrow=0, swim=0, climb=0)
    move = d.get("move", {})
    if move.get("burrow"):
        mv["burrow"] = walk if move["burrow"] == 2 else BURROW[age_i]
    if move.get("swim"):
        mv["swim"] = walk if move["swim"] == 1 else mv.get("fly") or walk
    if move.get("climb"):
        mv["climb"] = walk
    if ICE_WALK in d.get("traits", []):
        mv["ignoredDifficultTerrain"] = ["ice", "snow"]
    elif "ignoredDifficultTerrain" in mv:
        mv["ignoredDifficultTerrain"] = []
    for k, v in d.get("senses", {}).items():
        s["attributes"]["senses"][k] = v

    # Traits and details.
    tr = s["traits"]
    types = [t for t in (d["breath"][2] if d["breath"] else []) if t not in PHYSICAL]
    di = list(d.get("di", []))
    tr["di"] = {"value": sorted(set(di)), "bypasses": [], "custom": ""}
    tr["dr"] = {"value": sorted(set(d.get("dr", [])) - set(di)), "bypasses": [], "custom": ""}
    tr["ci"] = {"value": sorted(set(d.get("ci", []))), "custom": ""}
    langs = list(tr["languages"]["value"])
    if age_i >= 1:
        langs += [LANG.get(x, x) for x in d.get("languages", [])]
    tr["languages"] = {"value": sorted(set(langs)), "custom": ""}
    det = s["details"]
    det["alignment"] = d["alignment"]
    det["environment"] = d["env"]
    det["biography"] = {"value": f"<p>{d['lore']}</p><p><em>Unofficial 5e conversion of a dragon from an earlier "
                                 f"edition of the game, for the Legacy Dragons module.</em></p>", "public": ""}
    if "source" in s:
        s["source"] = {"custom": "Legacy Dragons", "book": "", "page": "", "license": "", "rules": "2014", "revision": 1}

    # Identity, art, folder.
    img = f"modules/{MODULE}/tokens/{d['key']}.webp"
    a["name"] = name
    a["img"] = img
    tok = a["prototypeToken"]
    tok["name"] = name
    tok["texture"]["src"] = img
    size = TOKEN_SIZE.get(tr["size"], 1)
    tok["width"] = tok["height"] = size
    a["folder"] = folder_id
    a["sort"] = sort
    a["flags"] = {MODULE: {"dragon": d["key"], "age": age}}
    a["_stats"].pop("compendiumSource", None)
    a["_stats"]["duplicateSource"] = None

    a = remap_ids(a, salt)
    # Some SRD dragons link Multiattack to an item id that isn't there: point it at the item of that name.
    by_name = {it["name"].lower(): it["_id"] for it in a["items"]}
    local = set(by_name.values())
    for it in a["items"]:
        desc = it["system"]["description"]
        desc["value"] = re.sub(r"\[\[/item \.([A-Za-z0-9]{16})\]\]\{([^}]+)\}",
                               lambda m: m.group(0) if m.group(1) in local or m.group(2).lower() not in by_name
                               else f"[[/item .{by_name[m.group(2).lower()]}]]{{{m.group(2)}}}", desc["value"])
    a["_key"] = f"!actors!{a['_id']}"
    for it in a["items"]:
        it["_key"] = f"!actors.items!{a['_id']}.{it['_id']}"
        it["folder"] = None
        for e in it.get("effects", []):
            e["_key"] = f"!actors.items.effects!{a['_id']}.{it['_id']}.{e['_id']}"
            e["origin"] = None
    return a


def folder_doc(fid: str, name: str, parent: str | None, sort: int, color: str | None = None) -> dict:
    return {"name": name, "type": "Actor", "_id": fid, "folder": parent, "sorting": "a", "sort": sort,
            "color": color, "flags": {}, "description": "",
            "_stats": {"systemId": "dnd5e", "systemVersion": "6.0.6", "coreVersion": "14.370"},
            "_key": f"!folders!{fid}"}


def main():
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.json"):
        f.unlink()
    ch = Chassis(root)
    family_ids = {k: new_id("folder", k) for k in FOLDERS}
    for i, (k, label) in enumerate(FOLDERS.items()):
        (out / f"_folder_{k}.json").write_text(json.dumps(folder_doc(family_ids[k], label, None, i * 100000), indent=1))
    count = 0
    for di, d in enumerate(sorted(DRAGONS, key=lambda x: x["name"])):
        fid = new_id("folder", d["key"])
        (out / f"_folder_{d['key']}.json").write_text(
            json.dumps(folder_doc(fid, d["name"], family_ids[d["folder"]], di * 1000, d["color"]), indent=1))
        for ai, age in enumerate(AGES):
            actor = build_actor(ch, d, age, fid, ai * 100)
            (out / f"{d['key']}-{age}.json").write_text(json.dumps(actor, indent=1))
            count += 1
    print(f"{count} dragons, {len(DRAGONS)} types, written to {out}")


if __name__ == "__main__":
    main()
