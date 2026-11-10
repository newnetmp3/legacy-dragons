# Legacy Dragons

A Foundry VTT compendium of **144 dragons** for D&D 5e (2014 rules): 36 dragon
types from earlier editions of the game that never got an official 5e stat
block, each as a **wyrmling, young, adult and ancient** dragon, with tokens.

Dragons that already have a modern version (the chromatic, metallic and gem
dragons, deep dragons, dragon turtles, faerie dragons, shadow dragons and so on)
are left out.

Unofficial fan content: these are new 5e conversions of the old dragons'
concepts, written for this module, not copies of the original books.

## Install

In Foundry: **Add-on Modules → Install Module**, paste this into **Manifest URL**:

```
https://raw.githubusercontent.com/newnetmp3/legacy-dragons/main/module.json
```

Enable **Legacy Dragons** in your world. The compendium appears under
**Compendium Packs → Legacy Dragons**, in folders by family and dragon. Drag a
dragon onto a scene or into the Actors tab to use it.

Needs Foundry v14 and the dnd5e system 6.0 or newer.

## What each dragon has

- A full 2014-style stat block: Multiattack, Bite, Claw, Tail, Frightful Presence,
  Legendary Resistance and Legendary Actions (adult and ancient), breath weapon(s)
  with recharge, damage immunities and its own traits.
- Numbers built on the SRD dragon of the same age and power ("tier"), so challenge
  ratings line up with the Monster Manual's. Attack bonuses and save DCs are worked
  out by dnd5e from the dragon's own scores.
- Lair actions (adult and ancient), lore in the biography, and a token. The token
  is sized for the dragon (wyrmling 1×1 up to ancient 4×4).

## The dragons

**Planar Dragons**

| Dragon | Alignment | Breath | CR (wyrmling / young / adult / ancient) |
|---|---|---|---|
| Battle Dragon | Chaotic Good | Sonic Breath / Daunting Roar | 2 / 9 / 16 / 23 |
| Chaos Dragon | Chaotic Neutral | Chaos Breath / Confusion Breath | 2 / 8 / 15 / 22 |
| Ethereal Dragon | Neutral | Force Breath | 1 / 7 / 14 / 21 |
| Howling Dragon | Chaotic Evil | Howling Breath / Maddening Wail | 2 / 8 / 15 / 22 |
| Oceanus Dragon | Neutral Good | Lightning Breath / Euphoria Breath | 2 / 8 / 15 / 22 |
| Pyroclastic Dragon | Chaotic Neutral | Pyroclastic Breath / Ash Cloud | 4 / 10 / 17 / 24 |
| Radiant Dragon | Lawful Good | Radiant Breath / Flash Breath | 3 / 10 / 17 / 24 |
| Rust Dragon | Lawful Evil | Corrosion Breath | 2 / 7 / 14 / 21 |
| Styx Dragon | Chaotic Evil | Styx Breath / Oblivion Breath | 3 / 9 / 16 / 23 |
| Tarterian Dragon | Neutral Evil | Force Breath / Imprisoning Breath | 4 / 10 / 17 / 24 |

**Lung Dragons**

| Dragon | Alignment | Breath | CR (wyrmling / young / adult / ancient) |
|---|---|---|---|
| Chiang Lung | Lawful Neutral | Torrent Breath | 2 / 8 / 15 / 22 |
| Li Lung | Neutral | Quake Breath | 2 / 8 / 15 / 22 |
| Lung Wang | Lawful Neutral | Steam Breath | 3 / 10 / 17 / 24 |
| Pan Lung | Neutral | Choking Breath | 1 / 7 / 14 / 21 |
| Shen Lung | Lawful Good | Spirit Breath | 2 / 9 / 16 / 23 |
| T'ien Lung | Lawful Good | Celestial Fire | 3 / 10 / 17 / 24 |
| Tun Mi Lung | Chaotic Evil | Typhoon Breath | 3 / 9 / 16 / 23 |
| Yu Lung | Neutral | Water Jet | 1 / 6 / 13 / 20 |

**Fourth Edition Chromatic Dragons**

| Dragon | Alignment | Breath | CR (wyrmling / young / adult / ancient) |
|---|---|---|---|
| Brown Dragon | Neutral Evil | Sand Breath / Blinding Sand | 2 / 7 / 14 / 21 |
| Gray Dragon | Chaotic Evil | Acid Breath / Petrifying Breath | 2 / 8 / 15 / 22 |

**Fourth Edition Metallic Dragons**

| Dragon | Alignment | Breath | CR (wyrmling / young / adult / ancient) |
|---|---|---|---|
| Adamantine Dragon | Lawful Neutral | Thunder Breath | 3 / 10 / 17 / 24 |
| Cobalt Dragon | Lawful Neutral | Cold Breath / Binding Breath | 2 / 8 / 15 / 22 |
| Iron Dragon | Lawful Evil | Lightning Breath | 3 / 9 / 16 / 23 |
| Mercury Dragon | Chaotic Neutral | Light Breath / Mirror Flash | 1 / 7 / 14 / 21 |
| Mithral Dragon | Lawful Good | Radiant Breath / Insight Breath | 3 / 10 / 17 / 24 |
| Orium Dragon | Neutral Evil | Poison Breath / Greed Breath | 2 / 8 / 15 / 22 |
| Steel Dragon | Lawful Good | Acid Breath / Debilitating Gas | 2 / 9 / 16 / 23 |

**Catastrophic Dragons**

| Dragon | Alignment | Breath | CR (wyrmling / young / adult / ancient) |
|---|---|---|---|
| Blizzard Dragon | Chaotic Evil | Blizzard Breath | 2 / 8 / 15 / 22 |
| Earthquake Dragon | Chaotic Evil | Earthquake Breath | 3 / 9 / 16 / 23 |
| Tempest Dragon | Chaotic Evil | Tempest Breath | 3 / 9 / 16 / 23 |
| Void Dragon | Neutral Evil | Void Breath / Unmaking Breath | 4 / 10 / 17 / 24 |
| Volcanic Dragon | Chaotic Evil | Lava Breath | 4 / 10 / 17 / 24 |

**Other Classic Dragons**

| Dragon | Alignment | Breath | CR (wyrmling / young / adult / ancient) |
|---|---|---|---|
| Cloud Dragon | Neutral | Frost Cloud | 2 / 9 / 16 / 23 |
| Fang Dragon | Neutral Evil | none (draining bite) | 2 / 8 / 15 / 22 |
| Mist Dragon | Neutral | Scalding Mist | 2 / 8 / 15 / 22 |
| Song Dragon | Chaotic Good | Lightning Breath / Paralyzing Gas | 1 / 7 / 14 / 21 |

## How it's built

`tools/dragons.py` holds every dragon (stats, breath weapons, traits, lore, lair
actions). `tools/build.py` turns each into Foundry actors, using the dnd5e system's
SRD 5.1 dragons as the base; `tools/tokens.mjs` draws the tokens and
`tools/pack.mjs` compiles the compendium:

```bash
git clone --depth 1 --branch release-6.0.6 https://github.com/foundryvtt/dnd5e.git /tmp/dnd5e
python3 tools/build.py /tmp/dnd5e src/legacy-dragons
(cd tools && npm install) && node tools/pack.mjs
```

Releases are published by `.github/workflows/release.yml` when the version in
`module.json` changes.

## Credits and licence

- Stat block structure and shared features (Multiattack, Frightful Presence,
  Legendary Resistance, Change Shape, Amphibious, Ice Walk and the legendary
  actions) come from the System Reference Document 5.1. See [LICENSE](LICENSE).
- Token icons: [game-icons.net](https://game-icons.net) by Lorc and Delapouite,
  CC BY 3.0.
- Legacy Dragons is unofficial Fan Content permitted under the Fan Content Policy.
  Not approved/endorsed by Wizards. Portions of the materials used are property
  of Wizards of the Coast. ©Wizards of the Coast LLC.
