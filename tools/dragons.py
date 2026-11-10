"""The dragons: older-edition dragon families with no official 5e stat block.

Each entry is a 5e (2014 rules) conversion of the dragon's concept, written for
this module. Numbers come from the SRD dragon of the same age and "tier"
(see build.py), so the challenge ratings line up with the Monster Manual's.

In text, {DR} becomes "the <dragon name>" (lowercase, filled in by dnd5e), and {DC:con} the
save DC from that ability (8 + proficiency bonus + modifier) for each age.

Fields:
  key, name, folder        identifier, display name, compendium folder
  tier, chassis            1 (weakest, like white/brass) .. 5 (like red/gold); "chromatic" or "metallic"
  alignment, color, icon   2014-style alignment; token colour; game-icons.net icon (tools/icons)
  abil                     ability score changes from the chassis, e.g. {"dex": 2}
  breath                   primary breath: (name, shape cone|line, damage types, save, what it exhales[, extra sentence])
                           two damage types: half each; more: one roll, type chosen as the extra sentence says
  breath2                  optional second breath: (name, save, effect text, status or None)
  di, dr, ci               damage immunities, resistances, condition immunities
  move                     extra movement: burrow / swim / climb (scaled by age), or nofly
  senses                   extra senses at adult/ancient, e.g. {"truesight": 60}
  traits                   [(name, text, from_age)]  from_age: 0 wyrmling .. 3 ancient
  languages                extra languages besides Common and Draconic
  env, lore, lair          environment, biography, three lair actions
"""

FOLDERS = {
    "planar": "Planar Dragons",
    "lung": "Lung Dragons",
    "chromatic4": "Fourth Edition Chromatic Dragons",
    "metallic4": "Fourth Edition Metallic Dragons",
    "catastrophic": "Catastrophic Dragons",
    "other": "Other Classic Dragons",
}

LUNG_FLIGHT = ("Cloud Rider", "{DR} flies without wings, riding the air itself. It can't be knocked prone while "
               "flying, and its flight isn't affected by magic that would ground a winged creature.", 0)
CHANGE_SHAPE = "change_shape"  # copied from the SRD gold dragon (adult and ancient)
AMPHIBIOUS = "amphibious"      # copied from the SRD gold dragon
ICE_WALK = "ice_walk"          # copied from the SRD white dragon

DRAGONS = [
    # ---------------------------------------------------------------- planar
    dict(key="battle", name="Battle Dragon", folder="planar", tier=4, chassis="metallic",
         alignment="Chaotic Good", color="#a8732f", icon="spiked-dragon-head", abil={"str": 2, "cha": -2},
         breath=("Sonic Breath", "cone", ["thunder"], "con", "a thunderclap of sound"),
         breath2=("Daunting Roar", "wis", "be &Reference[frightened] of {DR} for 1 minute. A creature can repeat the "
                  "saving throw at the end of each of its turns, ending the effect on itself on a success.", "frightened"),
         di=["thunder"], ci=["deafened", "frightened"], move={"climb": 1},
         traits=[("Glory Seeker", "{DR} has advantage on attack rolls against a creature that attacked it since the "
                  "end of its last turn.", 1),
                 ("Honorable Duel", "When {DR} challenges a creature to single combat (no action required), it has "
                  "advantage on saving throws against that creature's effects until one of them drops to 0 hit points "
                  "or another creature harms either of them.", 2)],
         languages=["celestial"], env="Planar, Mountain",
         lore="Battle dragons roost on the war-torn slopes of the heroic plane of Ysgard, where fallen warriors rise each "
              "dawn to fight again. They prize courage above gold, keep careful tallies of worthy foes, and often "
              "spare an enemy who fought well. Their scales are the color of polished bronze, nicked by a thousand "
              "duels.",
         lair=["Distant war horns sound. Each creature of the dragon's choice within 120 feet must succeed on a DC 15 "
               "Wisdom saving throw or have disadvantage on attack rolls until initiative count 20 on the next round.",
               "Spectral weapons rise from the ground in a 20-foot-radius sphere the dragon can see within 120 feet. "
               "Each creature there must succeed on a DC 15 Dexterity saving throw or take 10 (3d6) slashing damage.",
               "The dragon chooses one creature it can see. Until initiative count 20 on the next round, that creature "
               "can't take reactions and other creatures can't help it with the Help action."]),
    dict(key="chaos", name="Chaos Dragon", folder="planar", tier=3, chassis="chromatic",
         alignment="Chaotic Neutral", color="#8a5cf5", icon="spiked-dragon-head", abil={"dex": 2, "int": 2},
         breath=("Chaos Breath", "cone", ["acid", "cold", "fire", "lightning", "thunder"], "dex",
                 "a burst of raw chaos",
                 "The damage type is random: roll a d6 (1 acid, 2 cold, 3 fire, 4 lightning, 5 thunder, 6 the dragon "
                 "chooses)."),
         breath2=("Confusion Breath", "wis", "be unable to tell friend from foe until the end of its next turn. On its turn it "
                  "rolls a d4: 1 it does nothing, 2 it moves in a random direction, 3-4 it attacks a random creature in "
                  "reach, or does nothing if there is none.", None),
         dr=["acid", "cold", "fire", "lightning", "thunder"], ci=["charmed"],
         traits=[("Shifting Scales", "At the start of each of its turns, {DR} gains immunity to one damage type of its "
                  "choice from acid, cold, fire, lightning, and thunder until the start of its next turn.", 1),
                 ("Unfixed Form", "{DR} can't be &Reference[petrified], and magic that would change its shape against its will has "
                  "no effect on it.", 2)],
         languages=["primordial"], env="Planar",
         lore="Chaos dragons swim through the churning soup of Limbo, where matter takes whatever shape a strong will "
              "gives it. Their scales ripple through every color in turn, and their moods change as quickly. They hoard "
              "nothing for long; a chaos dragon's lair is a heap of treasures it has forgotten it wanted.",
         lair=["The ground within 30 feet of a point the dragon can see turns to a random element until initiative "
               "count 20 on the next round: roll a d4 for mud (difficult terrain), ice (Dexterity save or fall prone), "
               "fire (5 (1d10) fire damage on entering), or empty air.",
               "Reality shudders. Each creature of the dragon's choice within 60 feet must succeed on a DC 15 Charisma "
               "saving throw or swap places with another random creature within that range.",
               "The dragon rolls on its Chaos Breath table; until the next lair action, its Bite deals that damage type."]),
    dict(key="ethereal", name="Ethereal Dragon", folder="planar", tier=2, chassis="metallic",
         alignment="Neutral", color="#8fc7d8", icon="spiked-dragon-head", abil={"dex": 2, "wis": 2},
         breath=("Force Breath", "line", ["force"], "dex", "a beam of shimmering force"),
         di=["force"], ci=["frightened"], senses={"truesight": 30},
         traits=[("Ethereal Sight", "{DR} can see 60 feet into the Ethereal Plane when it is on the Material Plane, and "
                  "vice versa.", 0),
                 ("Ethereal Step", "As a bonus action, {DR} magically shifts from the Material Plane to the Ethereal "
                  "Plane, or vice versa. It can't do so again until it finishes a short or long rest.", 1)],
         languages=[], env="Planar",
         lore="Ethereal dragons drift through the misty border between worlds, watching the Material Plane like "
              "spectators at a play. They are curious and patient, trading secrets with travelers who wander the Deep "
              "Ethereal, and they fiercely hunt the creatures that prey on lost souls there.",
         lair=["Curtains of ethereal mist fill a 20-foot cube; the area is heavily obscured until initiative count 20 "
               "on the next round.",
               "One creature the dragon can see within 120 feet must succeed on a DC 15 Charisma saving throw or "
               "be pulled into the Ethereal Plane until initiative count 20 on the next round.",
               "The dragon and up to three creatures it can see within 60 feet each teleport up to 30 feet to "
               "unoccupied spaces they can see."]),
    dict(key="howling", name="Howling Dragon", folder="planar", tier=3, chassis="chromatic",
         alignment="Chaotic Evil", color="#6d5f78", icon="spiked-dragon-head", abil={"cha": 2},
         breath=("Howling Breath", "cone", ["thunder"], "con", "a shrieking gale"),
         breath2=("Maddening Wail", "wis", "take 4d6 psychic damage and be &Reference[deafened] for 1 minute.", "deafened"),
         di=["thunder"], ci=["deafened"],
         traits=[("Endless Wind", "Ranged weapon attacks against {DR} have disadvantage while it is in a strong wind, "
                  "including the wind of its lair.", 0),
                 ("Unsettling Voice", "A creature that starts its turn within 30 feet of {DR} and can hear it can't "
                  "take reactions until the start of its next turn.", 2)],
         languages=["abyssal"], env="Planar, Underdark",
         lore="Howling dragons haunt the wind-scoured tunnels of Pandemonium, where the endless gale drives mortals "
              "mad. They delight in the sound of despair and keep it, it is said, in the hollow bones they hoard. Their "
              "dull gray-violet hides are pocked with holes that whistle as they fly.",
         lair=["A screaming wind fills the lair. Until initiative count 20 on the next round, each creature other than the "
               "dragon has disadvantage on Wisdom (Perception) checks and concentration saving throws.",
               "A gust pushes each creature of the dragon's choice within 60 feet up to 15 feet in a direction the "
               "dragon chooses (DC 15 Strength saving throw negates).",
               "One creature the dragon can see hears whispers of its fears: DC 15 Wisdom saving throw or it is "
               "&Reference[frightened] of the dragon until initiative count 20 on the next round."]),
    dict(key="oceanus", name="Oceanus Dragon", folder="planar", tier=3, chassis="metallic",
         alignment="Neutral Good", color="#3aa6a0", icon="spiked-dragon-head", abil={"wis": 2},
         breath=("Lightning Breath", "line", ["lightning"], "dex", "a crackling bolt of river lightning"),
         breath2=("Euphoria Breath", "wis", "be &Reference[charmed] by {DR} for 1 minute, filled with peaceful calm. The effect "
                  "ends early if the creature takes damage.", "charmed"),
         di=["lightning"], move={"swim": 1}, traits=[AMPHIBIOUS],
         languages=["celestial"], env="Planar, Coastal",
         lore="Oceanus dragons glide along the River Oceanus that winds through the peaceful plane of Elysium. They "
              "guide pilgrims and ferry the weary, and they collect beautiful river stones rather than coins. Their "
              "silver-teal scales shimmer like sunlight on running water.",
         lair=["The river rises. Water in a 20-foot square within 120 feet becomes a strong current; each creature "
               "there must succeed on a DC 15 Strength saving throw or be pushed 20 feet.",
               "A soothing song rises from the water. Each creature of the dragon's choice within 60 feet regains 10 "
               "(3d6) hit points.",
               "Lightning arcs between pools. One creature within 60 feet standing in water must make a DC 15 "
               "Dexterity saving throw, taking 10 (3d6) lightning damage on a failure."]),
    dict(key="pyroclastic", name="Pyroclastic Dragon", folder="planar", tier=5, chassis="chromatic",
         alignment="Chaotic Neutral", color="#c2410c", icon="spiked-dragon-head", abil={"con": 2, "int": -2},
         breath=("Pyroclastic Breath", "cone", ["fire", "thunder"], "dex",
                 "an exploding wave of ash and molten rock", "Half the damage is fire and half is thunder."),
         breath2=("Ash Cloud", "con", "be &Reference[blinded] until the end of its next turn, choking on ash.", "blinded"),
         di=["fire", "thunder"], move={"burrow": 1},
         traits=[("Molten Body", "A creature that touches {DR} or hits it with a melee attack while within 5 feet of "
                  "it takes 5 (1d10) fire damage.", 1)],
         languages=["primordial"], env="Planar, Volcano",
         lore="Pyroclastic dragons are born where elemental fire and earth grind together. Restless and destructive, "
              "they tunnel through the crusts of worlds and erupt from mountains with no warning. Their black scales "
              "glow orange along every seam.",
         lair=["Magma bursts from a point on the ground the dragon can see within 120 feet: each creature within 10 "
               "feet of it must make a DC 15 Dexterity saving throw, taking 14 (4d6) fire damage on a failure.",
               "The ground shakes. Each creature on the ground within 60 feet of the dragon must succeed on a DC 15 "
               "Dexterity saving throw or fall &Reference[prone].",
               "Ash fills a 20-foot-radius sphere; the area is heavily obscured until initiative count 20 on the "
               "next round."]),
    dict(key="radiant", name="Radiant Dragon", folder="planar", tier=5, chassis="metallic",
         alignment="Lawful Good", color="#f2cf5b", icon="spiked-dragon-head", abil={"wis": 2, "cha": 2},
         breath=("Radiant Breath", "line", ["radiant"], "dex", "a lance of pure light"),
         breath2=("Flash Breath", "con", "be &Reference[blinded] for 1 minute. A creature can repeat the saving throw at the "
                  "end of each of its turns, ending the effect on itself on a success.", "blinded"),
         di=["radiant"], ci=["blinded"], senses={"truesight": 60},
         traits=[("Radiant Aura", "Shadows flee {DR}: it sheds bright light in a 30-foot radius and dim light for an "
                  "additional 30 feet, and creatures in the bright light can't benefit from being &Reference[invisible].", 1)],
         languages=["celestial"], env="Planar, Mountain",
         lore="Radiant dragons dwell on the terraced slopes of Mount Celestia, guardians of law and goodness. They "
              "judge carefully and act decisively, and their counsel is sought by archons and mortals alike. Light "
              "pours from their mirrored scales.",
         lair=["Holy light fills a 20-foot-radius sphere; fiends and undead there must succeed on a DC 15 Wisdom "
               "saving throw or take 14 (4d6) radiant damage.",
               "The dragon names up to three creatures it can see; each gains 10 temporary hit points.",
               "Each creature of the dragon's choice within 60 feet must succeed on a DC 15 Charisma saving throw or "
               "be unable to speak a deliberate lie until initiative count 20 on the next round."]),
    dict(key="rust", name="Rust Dragon", folder="planar", tier=2, chassis="chromatic",
         alignment="Lawful Evil", color="#a0522d", icon="spiked-dragon-head", abil={"con": 2},
         breath=("Corrosion Breath", "line", ["acid"], "dex", "a spray of rust-laden acid"),
         di=["acid"],
         traits=[("Metal Eater", "When {DR} hits a creature wearing nonmagical metal armor with its Bite, the armor "
                  "takes a permanent and cumulative −1 penalty to the AC it offers. Armor reduced to an AC of 10 is "
                  "destroyed. A nonmagical metal weapon that hits {DR} takes the same penalty to damage rolls.", 0)],
         languages=["infernal"], env="Planar",
         lore="Rust dragons gnaw on the iron cubes of Acheron, endlessly drifting through that plane of eternal war. "
              "They eat metal, ruin weapons for sport, and serve as mercenaries to whichever army pays in iron. Their "
              "scales flake like corroded plate.",
         lair=["Rust bursts from metal within 60 feet: each creature wearing metal armor must succeed on a DC 15 "
               "Constitution saving throw or have its speed halved until initiative count 20 on the next round.",
               "An iron wall 30 feet long and 10 feet high rises between two points the dragon can see.",
               "The dragon chooses a metal object within 60 feet that isn't being worn or carried; it crumbles to rust."]),
    dict(key="styx", name="Styx Dragon", folder="planar", tier=4, chassis="chromatic",
         alignment="Chaotic Evil", color="#3d5229", icon="spiked-dragon-head", abil={"wis": -2, "cha": 2},
         breath=("Styx Breath", "cone", ["poison"], "con", "a torrent of foul water from the River Styx"),
         breath2=("Oblivion Breath", "int", "forget who its allies are until the end of its next turn. It treats every "
                  "creature as an enemy and can't take reactions.", None),
         di=["poison"], ci=["poisoned"], move={"swim": 1}, traits=[AMPHIBIOUS,
             ("Waters of Forgetting", "A creature that starts its turn &Reference[grappled] by {DR} or submerged in its lair's "
              "water must succeed on a DC {DC:con} Intelligence saving throw or forget the last hour.", 2)],
         languages=["abyssal", "infernal"], env="Planar, Swamp",
         lore="Styx dragons swim the black River Styx as it winds through the Lower Planes. A single drink of that water "
              "steals a mortal's memory, and the dragons hoard what they steal: names, oaths, and lost loves. Fiends of "
              "every kind pay them to guard crossings.",
         lair=["Black water surges in a 20-foot square; each creature there must succeed on a DC 15 Strength saving "
               "throw or be pulled under, &Reference[restrained] until initiative count 20 on the next round.",
               "A creature the dragon can see forgets one spell or action of the dragon's choice until initiative "
               "count 20 on the next round (DC 15 Intelligence saving throw negates).",
               "Fog rises from the water; the area within 60 feet of the dragon is lightly obscured."]),
    dict(key="tarterian", name="Tarterian Dragon", folder="planar", tier=5, chassis="chromatic",
         alignment="Neutral Evil", color="#5b2333", icon="spiked-dragon-head", abil={"int": 2},
         breath=("Force Breath", "cone", ["force"], "dex", "a crushing wave of force"),
         breath2=("Imprisoning Breath", "str", "be bound by chains of force, &Reference[restrained] for 1 minute. A creature "
                  "can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.",
                  "restrained"),
         di=["force"], ci=["charmed", "frightened"],
         traits=[("Jailer", "{DR} knows the location of any creature it has restrained in the last 24 hours, as long as "
                  "both are on the same plane.", 2)],
         languages=["abyssal", "infernal"], env="Planar",
         lore="Tarterian dragons prowl the prison plane of Carceri, where the betrayers of the multiverse are kept. "
              "They are wardens and torturers, cold and spiteful, and they collect prisoners as other dragons collect "
              "coins. Their dark red scales bear chain-like markings.",
         lair=["Chains erupt from a surface within 120 feet; one creature within 10 feet of them must succeed on a "
               "DC 15 Strength saving throw or be &Reference[restrained] until initiative count 20 on the next round.",
               "The exits of the lair seal with force until initiative count 20 on the next round.",
               "Each creature of the dragon's choice within 60 feet must succeed on a DC 15 Wisdom saving throw or have "
               "disadvantage on saving throws until initiative count 20 on the next round."]),
    # ---------------------------------------------------------------- lung
    dict(key="chiang-lung", name="Chiang Lung", folder="lung", tier=3, chassis="metallic",
         alignment="Lawful Neutral", color="#2f6f9f", icon="sea-dragon", abil={"wis": 2},
         breath=("Torrent Breath", "line", ["bludgeoning"], "str",
                 "a roaring torrent of river water", "A creature that fails the save is also knocked &Reference[prone]."),
         move={"swim": 1, "lung": 1}, traits=[LUNG_FLIGHT, AMPHIBIOUS, CHANGE_SHAPE],
         languages=["primordial"], env="Coastal, Forest",
         lore="Chiang lung are the river dragons, lords of rain and flood. They expect courtesy and offerings from the "
              "villages along their rivers, and reward them with gentle rains. Insult one and the river remembers.",
         lair=["The river floods: a 20-foot square becomes deep water until initiative count 20 on the next round.",
               "Rain falls within 120 feet; the area is lightly obscured and open flames go out.",
               "A wave strikes one creature within 60 feet: DC 15 Strength saving throw or be pushed 20 feet and fall "
               "&Reference[prone]."]),
    dict(key="li-lung", name="Li Lung", folder="lung", tier=3, chassis="metallic",
         alignment="Neutral", color="#8b6b3e", icon="sea-dragon", abil={"str": 2, "dex": -2},
         breath=("Quake Breath", "cone", ["thunder"], "con", "a deep, rumbling roar that shakes the earth"),
         di=["thunder"], move={"burrow": 1, "lung": 1}, senses={"tremorsense": 60},
         traits=[LUNG_FLIGHT, CHANGE_SHAPE,
                 ("Earth Glide", "{DR} can burrow through nonmagical, unworked earth and stone without disturbing the "
                  "material it moves through.", 0)],
         languages=["primordial"], env="Mountain, Underdark",
         lore="Li lung are earth dragons who sleep for years in caverns beneath mountains. They are fond of riddles and "
              "board games and keep careful records of the stones and veins of ore beneath their realm. Wake one "
              "rudely and the mountain shakes.",
         lair=["The ground within 60 feet heaves; each creature there must succeed on a DC 15 Dexterity saving throw "
               "or fall &Reference[prone].",
               "Stones fall from the ceiling in a 10-foot-radius area: DC 15 Dexterity saving throw or take 10 (3d6) "
               "bludgeoning damage.",
               "A pillar of stone rises to block a 10-foot square until initiative count 20 on the next round."]),
    dict(key="lung-wang", name="Lung Wang", folder="lung", tier=5, chassis="metallic",
         alignment="Lawful Neutral", color="#1c4e80", icon="sea-dragon", abil={"cha": 2},
         breath=("Steam Breath", "cone", ["fire"], "con", "a blast of scalding steam"),
         di=["fire"], move={"swim": 2, "lung": 1}, traits=[LUNG_FLIGHT, AMPHIBIOUS, CHANGE_SHAPE,
             ("Sea King", "Water creatures with an Intelligence of 3 or lower are &Reference[charmed] by {DR} while within 120 "
              "feet of it and obey its spoken commands.", 2)],
         languages=["primordial"], env="Coastal, Underwater",
         lore="The lung wang are the sea dragon kings, the greatest of their kind. Each rules an ocean from a coral "
              "palace, with a court of fish, turtles and lesser dragons, and demands tribute from every ship that "
              "crosses its waters.",
         lair=["A whirlpool forms in a 20-foot radius of water; each creature there must succeed on a DC 15 Strength "
               "saving throw or be pulled 15 feet toward its center.",
               "The dragon's court answers: up to three creatures of the dragon's choice regain 10 (3d6) hit points.",
               "Fog rolls in; everything more than 30 feet from the dragon is heavily obscured."]),
    dict(key="pan-lung", name="Pan Lung", folder="lung", tier=2, chassis="metallic",
         alignment="Neutral", color="#4a7c59", icon="sea-dragon", abil={"str": 2},
         breath=("Choking Breath", "cone", ["poison"], "con", "a cloud of choking green mist"),
         di=["poison"], ci=["poisoned"], move={"climb": 1, "lung": 1},
         traits=[LUNG_FLIGHT, CHANGE_SHAPE,
                 ("Coiling Grip", "When {DR} hits a Medium or smaller creature with its Bite, the creature is "
                  "&Reference[grappled] (escape DC {DC:str}) as the dragon coils around it. Until the grapple ends, the creature is "
                  "&Reference[restrained].", 0)],
         languages=[], env="Forest, Ruins",
         lore="Pan lung, the coiled dragons, are guardians. They wrap themselves around treasures, tombs and ancient "
              "temples and do not leave for anything short of the end of the world. They are calm, stubborn and very "
              "difficult to bribe.",
         lair=["Vines lash out in a 20-foot square: DC 15 Strength saving throw or be &Reference[restrained] until initiative "
               "count 20 on the next round.",
               "The doors and gates of the lair close and lock.",
               "Green mist fills a 20-foot sphere; the area is heavily obscured."]),
    dict(key="shen-lung", name="Shen Lung", folder="lung", tier=4, chassis="metallic",
         alignment="Lawful Good", color="#6aa5a1", icon="sea-dragon", abil={"wis": 2, "str": -2},
         breath=("Spirit Breath", "cone", ["radiant"], "wis", "a shimmering wave of spirit energy"),
         di=["radiant"], ci=["poisoned"], move={"swim": 1, "lung": 1},
         traits=[LUNG_FLIGHT, AMPHIBIOUS, CHANGE_SHAPE,
                 ("Spirit Guardian", "{DR} can see and speak with spirits and ghosts within 120 feet, and undead have "
                  "disadvantage on attack rolls against it.", 1)],
         languages=["celestial"], env="Coastal, Forest",
         lore="Shen lung are spirit dragons, keepers of rivers, lakes and the ghosts that linger near them. They are "
              "patient teachers and stern judges, and they are worshipped in many shrines along quiet waters.",
         lair=["Ancestral spirits appear; up to three creatures of the dragon's choice gain advantage on their next "
               "saving throw.",
               "An undead creature the dragon can see must succeed on a DC 15 Wisdom saving throw or be turned until "
               "initiative count 20 on the next round.",
               "Mist rises from the water; the area within 30 feet of the dragon is lightly obscured."]),
    dict(key="tien-lung", name="T'ien Lung", folder="lung", tier=5, chassis="metallic",
         alignment="Lawful Good", color="#e3b23c", icon="sea-dragon", abil={"cha": 2},
         breath=("Celestial Fire", "cone", ["fire", "radiant"], "dex", "golden fire", "Half the damage is fire and half is radiant."),
         di=["fire", "radiant"], move={"lung": 1}, traits=[LUNG_FLIGHT, CHANGE_SHAPE,
             ("Weather Lord", "{DR} can cast <em>control weather</em> once per day, requiring no components.", 3)],
         languages=["celestial"], env="Mountain, Planar",
         lore="The t'ien lung are the celestial dragons, who dwell among the clouds and serve the courts of heaven. "
              "They are proud, proper and generous to the deserving, and they keep the weather in good order.",
         lair=["Golden clouds gather; each creature of the dragon's choice within 120 feet gains 10 temporary hit points.",
               "A thunderbolt strikes a point within 120 feet: each creature within 10 feet must make a DC 15 Dexterity "
               "saving throw, taking 14 (4d6) lightning damage on a failure.",
               "Wind howls; each flying creature other than the dragon must succeed on a DC 15 Strength saving throw "
               "or descend 30 feet."]),
    dict(key="tun-mi-lung", name="Tun Mi Lung", folder="lung", tier=4, chassis="chromatic",
         alignment="Chaotic Evil", color="#3b4b6b", icon="sea-dragon", abil={"str": 2},
         breath=("Typhoon Breath", "cone", ["bludgeoning"], "str",
                 "a howling typhoon wind", "A creature that fails the save is also pushed 30 feet away."),
         dr=["lightning", "thunder"], move={"swim": 1, "lung": 1}, traits=[LUNG_FLIGHT, AMPHIBIOUS, CHANGE_SHAPE],
         languages=["primordial"], env="Coastal, Underwater",
         lore="Tun mi lung are typhoon dragons, wild and cruel, who sink ships and flatten villages for the joy of it. "
              "The other lung dragons consider them outlaws and hunt them when they can.",
         lair=["Wind blasts a 60-foot line; each creature there must succeed on a DC 15 Strength saving throw or be "
               "knocked &Reference[prone].",
               "Lightning strikes a creature within 120 feet: DC 15 Dexterity saving throw or take 14 (4d6) lightning "
               "damage.",
               "Driving rain fills the lair; ranged attacks have disadvantage until initiative count 20 on the next "
               "round."]),
    dict(key="yu-lung", name="Yu Lung", folder="lung", tier=1, chassis="metallic",
         alignment="Neutral", color="#e07b39", icon="sea-dragon", abil={"dex": 2},
         breath=("Water Jet", "line", ["bludgeoning"], "dex", "a jet of water"),
         move={"swim": 2, "lung": 1}, traits=[LUNG_FLIGHT, AMPHIBIOUS,
             ("Carp Leap", "{DR} can leap up to 30 feet out of water as part of its movement.", 0)],
         languages=[], env="Coastal, Forest",
         lore="Yu lung are carp dragons: great golden koi with dragon heads, who swim upstream for centuries in the "
              "hope of one day becoming true lung dragons. Playful and vain, they love praise and shiny things.",
         lair=["The water churns; each creature in water within 60 feet must succeed on a DC 13 Strength saving "
               "throw or be pushed 10 feet.",
               "A shimmer of scales dazzles one creature: DC 13 Wisdom saving throw or it is &Reference[charmed] until "
               "initiative count 20 on the next round.",
               "Mist rises; the area within 20 feet of the dragon is lightly obscured."]),
    # ---------------------------------------------------------------- 4e chromatic
    dict(key="brown", name="Brown Dragon", folder="chromatic4", tier=2, chassis="chromatic",
         alignment="Neutral Evil", color="#9c6b3c", icon="dragon-head", abil={"str": 2, "cha": -2},
         breath=("Sand Breath", "cone", ["slashing"], "dex", "a blast of scouring sand"),
         breath2=("Blinding Sand", "con", "be &Reference[blinded] until the end of its next turn.", "blinded"),
         dr=["fire"], move={"burrow": 2}, senses={"tremorsense": 60},
         traits=[("Sand Swimmer", "{DR} can burrow through sand as fast as it walks, and it can hold its breath for "
                  "1 hour.", 0),
                 ("Ambusher", "In the first round of combat, {DR} has advantage on attack rolls against any creature "
                  "that hasn't taken a turn yet.", 1)],
         languages=[], env="Desert",
         lore="Brown dragons swim beneath desert dunes and burst up to snatch prey from caravans. They rarely fly, "
              "and they are patient hunters who can wait a week beneath the sand for the right meal.",
         lair=["A sinkhole opens in a 20-foot square: DC 15 Dexterity saving throw or be &Reference[restrained] until initiative "
               "count 20 on the next round.",
               "Sand whirls in a 20-foot sphere; the area is heavily obscured.",
               "The dragon burrows up to its burrow speed without provoking opportunity attacks."]),
    dict(key="gray", name="Gray Dragon", folder="chromatic4", tier=3, chassis="chromatic",
         alignment="Chaotic Evil", color="#7d7f7d", icon="dragon-head", abil={"str": 2, "int": -2},
         breath=("Acid Breath", "cone", ["acid"], "dex", "a cloud of stinging acid"),
         breath2=("Petrifying Breath", "con", "begin to turn to stone and be &Reference[restrained]. It must repeat the saving "
                  "throw at the end of its next turn, becoming &Reference[petrified] on a failure or ending the effect on a "
                  "success.", "restrained"),
         di=["acid"], ci=["petrified"],
         traits=[("Ferocious Bite", "{DR} scores a critical hit with its Bite on a roll of 19 or 20.", 1)],
         languages=[], env="Mountain, Ruins",
         lore="Gray dragons are savage, quick to anger and slow to forgive. They decorate their lairs with the statues "
              "of those who failed to escape their petrifying breath, and they bite rather than talk.",
         lair=["Stone spikes erupt in a 20-foot square: DC 15 Dexterity saving throw or take 10 (3d6) piercing damage.",
               "A creature the dragon can see feels its limbs stiffen: DC 15 Constitution saving throw or its speed is "
               "0 until initiative count 20 on the next round.",
               "One statue in the lair animates and makes one attack (+7 to hit, 10 (2d6 + 3) bludgeoning damage)."]),
    # ---------------------------------------------------------------- 4e metallic
    dict(key="adamantine", name="Adamantine Dragon", folder="metallic4", tier=5, chassis="metallic",
         alignment="Lawful Neutral", color="#4b5563", icon="dragon-head", abil={"str": 2, "dex": -2},
         breath=("Thunder Breath", "cone", ["thunder"], "con", "a deafening blast of sound",
                 "A creature that fails the save is also &Reference[deafened] for 1 minute."),
         di=["thunder"], dr=["bludgeoning", "piercing", "slashing"], ci=["deafened"],
         traits=[("Adamantine Hide", "Any critical hit against {DR} becomes a normal hit.", 1)],
         languages=["dwarvish", "undercommon"], env="Underdark, Mountain",
         lore="Adamantine dragons rule vast realms deep beneath the earth. They are proud and territorial and "
              "consider themselves the rightful masters of every tunnel they can reach. Their scales are nearly "
              "impossible to pierce.",
         lair=["Stalactites fall: each creature of the dragon's choice within 60 feet must succeed on a DC 15 Dexterity "
               "saving throw or take 10 (3d6) piercing damage.",
               "The lair resounds; each creature within 60 feet must succeed on a DC 15 Constitution saving throw or "
               "be &Reference[deafened] until initiative count 20 on the next round.",
               "A tunnel collapses, sealing one exit until it is dug clear."]),
    dict(key="cobalt", name="Cobalt Dragon", folder="metallic4", tier=3, chassis="metallic",
         alignment="Lawful Neutral", color="#2b4fa0", icon="dragon-head", abil={"con": 2},
         breath=("Cold Breath", "cone", ["cold"], "con", "a blast of blue-white cold"),
         breath2=("Binding Breath", "str", "be encased in ice, &Reference[restrained] until the end of its next turn.",
                  "restrained"),
         di=["cold"], traits=[ICE_WALK],
         languages=[], env="Arctic, Mountain",
         lore="Cobalt dragons live in high, frozen lands and keep to themselves. They are wary of visitors and "
              "strict about their territory, but loyal to those few they come to trust.",
         lair=["Ice spreads across the ground within 60 feet; the area is difficult terrain until initiative count 20 "
               "on the next round.",
               "Icicles fall on a creature the dragon can see: DC 15 Dexterity saving throw or take 10 (3d6) piercing "
               "damage.",
               "Freezing fog fills a 20-foot sphere; the area is heavily obscured."]),
    dict(key="iron", name="Iron Dragon", folder="metallic4", tier=4, chassis="chromatic",
         alignment="Lawful Evil", color="#6b6b6b", icon="dragon-head", abil={"str": 2, "cha": -2},
         breath=("Lightning Breath", "cone", ["lightning"], "dex", "a storm of crackling sparks"),
         di=["lightning"],
         traits=[("Battle-Hardened", "{DR} has advantage on saving throws against being &Reference[frightened] or "
                  "&Reference[stunned].", 1)],
         languages=["giant"], env="Mountain, Hill",
         lore="Iron dragons are mercenaries and warlords, the fiercest of the metallic dragons. They hire out their "
              "strength, keep careful accounts of every debt, and take payment in blood when they must.",
         lair=["Lightning arcs between metal objects: each creature of the dragon's choice wearing metal armor within "
               "60 feet must succeed on a DC 15 Dexterity saving throw or take 10 (3d6) lightning damage.",
               "The dragon issues a command; one creature it can see must succeed on a DC 15 Wisdom saving throw or "
               "use its reaction to move up to its speed as the dragon directs.",
               "Iron spikes rise in a 10-foot square, making it difficult terrain."]),
    dict(key="mercury", name="Mercury Dragon", folder="metallic4", tier=2, chassis="metallic",
         alignment="Chaotic Neutral", color="#c0c6cc", icon="dragon-head", abil={"dex": 4, "str": -2},
         breath=("Light Breath", "line", ["radiant"], "dex", "a beam of blinding light"),
         breath2=("Mirror Flash", "con", "be &Reference[blinded] until the end of its next turn.", "blinded"),
         di=["radiant"], ci=["blinded"],
         traits=[("Quicksilver", "{DR} can take the Dash or Disengage action as a bonus action.", 0)],
         languages=[], env="Mountain, Hill",
         lore="Mercury dragons are flighty and unpredictable, as fast in their moods as in their movements. They "
              "love mirrors and polished things, and they make unreliable allies and forgiving enemies.",
         lair=["Mirrors of light flash; each creature of the dragon's choice within 60 feet must succeed on a DC 15 "
               "Constitution saving throw or be &Reference[blinded] until initiative count 20 on the next round.",
               "Illusory copies of the dragon appear; attack rolls against it have disadvantage until initiative count "
               "20 on the next round.",
               "The dragon teleports up to 60 feet to an unoccupied space it can see."]),
    dict(key="mithral", name="Mithral Dragon", folder="metallic4", tier=5, chassis="metallic",
         alignment="Lawful Good", color="#d9e6ef", icon="dragon-head", abil={"wis": 2, "int": 2, "str": -2},
         breath=("Radiant Breath", "cone", ["radiant"], "dex", "a cone of silvery light"),
         breath2=("Insight Breath", "wis", "be &Reference[stunned] until the end of its next turn, overwhelmed by visions.",
                  "stunned"),
         di=["radiant"], ci=["charmed"], senses={"truesight": 60},
         traits=[("Prophetic", "{DR} can't be surprised and has advantage on initiative rolls.", 1)],
         languages=["celestial"], env="Planar, Mountain",
         lore="Mithral dragons are prophets and servants of good gods, rarely seen on the Material Plane. When one "
              "appears, great events are near. They speak in riddles and act only when the time is right.",
         lair=["The dragon sees the future: until initiative count 20 on the next round, attack rolls against it have "
               "disadvantage.",
               "Radiance fills a 20-foot sphere; fiends and undead there take 14 (4d6) radiant damage (DC 15 "
               "Constitution saving throw for half).",
               "Up to three creatures of the dragon's choice gain advantage on their next attack roll or saving throw."]),
    dict(key="orium", name="Orium Dragon", folder="metallic4", tier=3, chassis="chromatic",
         alignment="Neutral Evil", color="#8a9a3a", icon="dragon-head", abil={"int": 2},
         breath=("Poison Breath", "cone", ["poison"], "con", "a cloud of green-gold poison"),
         breath2=("Greed Breath", "wis", "be &Reference[charmed] by {DR} until the end of its next turn, and drop whatever "
                  "valuables it holds.", "charmed"),
         di=["poison"], ci=["poisoned"],
         traits=[("Hoard Sense", "{DR} knows the direction and distance to any coin or gem from its hoard within 1 mile.", 1)],
         languages=["dwarvish"], env="Mountain, Underdark",
         lore="Orium dragons are greedy and calculating, and they believe every coin in the world belongs in their "
              "hoards. They bargain, scheme and steal, and they never forget a theft from their own treasure.",
         lair=["Poison gas fills a 20-foot sphere: DC 15 Constitution saving throw or take 10 (3d6) poison damage.",
               "Coins in the hoard rise and swarm one creature: DC 15 Dexterity saving throw or take 7 (2d6) "
               "bludgeoning damage and be &Reference[blinded] until initiative count 20 on the next round.",
               "The dragon knows the location of every creature within 120 feet carrying treasure."]),
    dict(key="steel", name="Steel Dragon", folder="metallic4", tier=4, chassis="metallic",
         alignment="Lawful Good", color="#8a9aa6", icon="dragon-head", abil={"int": 2, "cha": 2},
         breath=("Acid Breath", "cone", ["acid"], "dex", "a cloud of acidic gas"),
         breath2=("Debilitating Gas", "con", "be &Reference[poisoned] for 1 minute. A creature can repeat the saving throw at "
                  "the end of each of its turns, ending the effect on itself on a success.", "poisoned"),
         di=["acid"], traits=[CHANGE_SHAPE,
             ("City Dweller", "{DR} has advantage on Charisma checks made to pass as a humanoid while in a humanoid form.", 1)],
         languages=["elvish", "dwarvish"], env="Urban",
         lore="Steel dragons love cities. They live among humanoids in disguise, often for centuries, as scholars, "
              "merchants or judges, and they defend the freedom of their adopted homes fiercely.",
         lair=["The dragon calls on its allies; one creature of its choice within 120 feet can use its reaction to make "
               "one weapon attack.",
               "Acidic mist fills a 20-foot sphere: DC 15 Constitution saving throw or take 10 (3d6) acid damage.",
               "Doors and shutters within 60 feet slam shut and lock."]),
    # ---------------------------------------------------------------- catastrophic
    dict(key="blizzard", name="Blizzard Dragon", folder="catastrophic", tier=3, chassis="chromatic",
         alignment="Chaotic Evil", color="#bfe3f2", icon="dragon-spiral", abil={"con": 2},
         breath=("Blizzard Breath", "cone", ["cold"], "con", "a howling blizzard"),
         di=["cold"], traits=[ICE_WALK,
             ("Whiteout", "Snow swirls around {DR}: the area within 10 feet of it is lightly obscured.", 1)],
         languages=["primordial"], env="Arctic, Planar",
         lore="Catastrophic dragons are living disasters born from the raw elements. Blizzard dragons bury villages in "
              "snow and freeze rivers solid as they pass, and they care nothing for treasure, only destruction.",
         lair=["Snow falls in a 40-foot sphere; the area is heavily obscured and difficult terrain.",
               "Hail strikes a 20-foot square: DC 15 Dexterity saving throw or take 10 (3d6) cold damage.",
               "Each creature within 60 feet must succeed on a DC 15 Constitution saving throw or gain 1 level of "
               "exhaustion from the cold."]),
    dict(key="earthquake", name="Earthquake Dragon", folder="catastrophic", tier=4, chassis="chromatic",
         alignment="Chaotic Evil", color="#6b4f2a", icon="dragon-spiral", abil={"str": 2, "dex": -2},
         breath=("Earthquake Breath", "cone", ["thunder"], "dex",
                 "a shockwave through the ground", "A creature that fails the save is also knocked &Reference[prone]."),
         di=["thunder"], move={"burrow": 1}, senses={"tremorsense": 60},
         traits=[("Tremor Step", "Each time {DR} lands or moves on the ground, the ground within 10 feet of it becomes "
                  "difficult terrain until the start of its next turn.", 1)],
         languages=["primordial"], env="Mountain, Planar",
         lore="Earthquake dragons shake the earth simply by walking on it. They collapse cities and mountains alike, "
              "and the cracks they leave can be followed for miles.",
         lair=["The ground heaves; each creature on the ground within 120 feet must succeed on a DC 15 Dexterity saving "
               "throw or fall &Reference[prone].",
               "A fissure opens in a 60-foot line, 10 feet wide: DC 15 Dexterity saving throw or fall in, taking 10 "
               "(3d6) bludgeoning damage.",
               "Rubble falls in a 20-foot sphere: DC 15 Dexterity saving throw or take 10 (3d6) bludgeoning damage."]),
    dict(key="tempest", name="Tempest Dragon", folder="catastrophic", tier=4, chassis="chromatic",
         alignment="Chaotic Evil", color="#4b6a8a", icon="dragon-spiral", abil={"dex": 2},
         breath=("Tempest Breath", "line", ["lightning", "thunder"], "dex",
                 "a storm-bolt", "Half the damage is lightning and half is thunder."),
         di=["lightning", "thunder"],
         traits=[("Storm Aura", "At the start of each of {DR}'s turns, each creature within 10 feet of it takes 5 (1d10) "
                  "lightning damage.", 1)],
         languages=["primordial"], env="Coastal, Planar",
         lore="Tempest dragons are storms with wings. Wherever they fly, thunderheads gather, and lightning follows "
              "them into the hearts of cities.",
         lair=["Lightning strikes a point within 120 feet: each creature within 5 feet must make a DC 15 Dexterity "
               "saving throw, taking 14 (4d6) lightning damage on a failure.",
               "Thunder booms; each creature within 60 feet must succeed on a DC 15 Constitution saving throw or be "
               "&Reference[deafened] until initiative count 20 on the next round.",
               "Wind gusts; each flying creature other than the dragon must succeed on a DC 15 Strength saving throw "
               "or be pushed 20 feet."]),
    dict(key="volcanic", name="Volcanic Dragon", folder="catastrophic", tier=5, chassis="chromatic",
         alignment="Chaotic Evil", color="#a12d0f", icon="dragon-spiral", abil={"con": 2},
         breath=("Lava Breath", "cone", ["fire"], "dex", "a spray of molten lava"),
         di=["fire"], move={"burrow": 1},
         traits=[("Molten Blood", "When a creature within 5 feet of {DR} hits it with a melee attack, molten blood "
                  "splashes the attacker, dealing 5 (1d10) fire damage.", 1)],
         languages=["primordial"], env="Volcano, Planar",
         lore="Volcanic dragons sleep in magma chambers beneath mountains and wake in eruptions. When they rise, "
              "rivers of lava follow, and the sky darkens with ash for days.",
         lair=["Lava erupts in a 10-foot radius: DC 15 Dexterity saving throw or take 14 (4d6) fire damage.",
               "Ash fills a 30-foot sphere; the area is heavily obscured.",
               "Volcanic gas spreads; each creature within 60 feet must succeed on a DC 15 Constitution saving throw "
               "or be &Reference[poisoned] until initiative count 20 on the next round."]),
    dict(key="void", name="Void Dragon", folder="catastrophic", tier=5, chassis="chromatic",
         alignment="Neutral Evil", color="#2a2148", icon="dragon-spiral", abil={"int": 2, "str": -2},
         breath=("Void Breath", "cone", ["necrotic"], "con", "a cone of starless cold void"),
         breath2=("Unmaking Breath", "cha", "have its connection to the world weakened: it is &Reference[incapacitated] until the "
                  "end of its next turn.", "incapacitated"),
         di=["necrotic", "cold"], ci=["frightened"], senses={"truesight": 60},
         traits=[("Starless", "{DR} doesn't need to breathe, and it can fly through the void between stars.", 0),
                 ("Lightless Aura", "Nonmagical light within 30 feet of {DR} is extinguished.", 2)],
         languages=["deep speech"], env="Planar",
         lore="Void dragons come from the cold spaces between the stars. They are alien and hungry, drawn to the "
              "light and warmth of worlds, and they leave behind only emptiness.",
         lair=["Darkness fills a 30-foot sphere; even creatures with darkvision can't see through it.",
               "Gravity fails in a 20-foot sphere; creatures there float 10 feet up until initiative count 20 on the "
               "next round.",
               "One creature the dragon can see must succeed on a DC 15 Charisma saving throw or take 14 (4d6) "
               "necrotic damage."]),
    # ---------------------------------------------------------------- other classic dragons
    dict(key="cloud", name="Cloud Dragon", folder="other", tier=4, chassis="metallic",
         alignment="Neutral", color="#cfd8e3", icon="wyvern", abil={"dex": 2},
         breath=("Frost Cloud", "cone", ["cold"], "con", "a freezing cloud"),
         di=["cold"],
         traits=[("Mist Form", "As an action, {DR} can turn into a cloud of mist or back. In mist form it has a flying "
                  "speed of 30 feet, can hover, can't attack, and has resistance to nonmagical damage.", 1)],
         languages=["auran"], env="Mountain, Coastal",
         lore="Cloud dragons live above the highest peaks in castles of mist. They are reclusive and moody, and "
              "they shroud their homes in fog to keep visitors away. Their scales are white-silver, tinged with pink "
              "at the edges like a sunrise.",
         lair=["Fog fills the lair; everything more than 20 feet from the dragon is heavily obscured.",
               "Wind gusts; each creature of the dragon's choice within 60 feet must succeed on a DC 15 Strength saving "
               "throw or be pushed 15 feet.",
               "Freezing rain falls; each creature within 60 feet must succeed on a DC 15 Constitution saving throw or "
               "take 7 (2d6) cold damage."]),
    dict(key="mist", name="Mist Dragon", folder="other", tier=3, chassis="metallic",
         alignment="Neutral", color="#9db7c2", icon="wyvern", abil={"wis": 2},
         breath=("Scalding Mist", "cone", ["fire"], "con", "a cloud of scalding mist"),
         di=["fire"], move={"swim": 1}, traits=[AMPHIBIOUS,
             ("Mist Form", "As an action, {DR} can turn into a cloud of mist or back. In mist form it has a flying speed of "
              "30 feet, can hover, can't attack, and has resistance to nonmagical damage.", 1)],
         languages=["aquan"], env="Coastal, Forest",
         lore="Mist dragons live near waterfalls and misty coasts. They are solitary and thoughtful, and they spend "
              "years in mist form, drifting and dreaming. They become dangerous only when disturbed.",
         lair=["Mist fills a 30-foot sphere; the area is heavily obscured.",
               "Scalding steam rises from the water: each creature in a 20-foot square must succeed on a DC 15 "
               "Constitution saving throw or take 10 (3d6) fire damage.",
               "The dragon teleports to a space in mist within 60 feet."]),
    dict(key="song", name="Song Dragon", folder="other", tier=2, chassis="metallic",
         alignment="Chaotic Good", color="#a8c6e0", icon="wyvern", abil={"cha": 2},
         breath=("Lightning Breath", "cone", ["lightning"], "dex", "a cloud of crackling electricity"),
         breath2=("Paralyzing Gas", "con", "be &Reference[paralyzed] until the end of its next turn.", "paralyzed"),
         di=["lightning"], traits=[CHANGE_SHAPE,
             ("Silver Tongue", "{DR} has advantage on Charisma (Performance) checks and on Charisma checks to "
              "pass as a humanoid.", 0)],
         languages=["elvish"], env="Urban, Forest",
         lore="Song dragons love the company of humanoids and spend much of their lives in disguise as bards and "
              "travelers. They are sociable and curious, with silver scales that shift to pale blue.",
         lair=["Music fills the lair; each creature of the dragon's choice within 60 feet must succeed on a DC 15 "
               "Wisdom saving throw or be &Reference[charmed] until initiative count 20 on the next round.",
               "Static crackles; one creature within 60 feet must succeed on a DC 15 Dexterity saving throw or take "
               "10 (3d6) lightning damage.",
               "Up to three creatures of the dragon's choice gain advantage on their next ability check."]),
    dict(key="fang", name="Fang Dragon", folder="other", tier=3, chassis="chromatic",
         alignment="Neutral Evil", color="#5a4a3a", icon="wyvern", abil={"str": 2, "cha": -2},
         breath=None,
         dr=["bludgeoning", "piercing", "slashing"],
         traits=[("Draining Bite", "When {DR} hits a creature with its Bite, the target must succeed on a DC {DC:con} "
                  "Constitution saving throw or have its hit point maximum reduced by an amount equal to the damage "
                  "taken. The reduction lasts until the creature finishes a long rest.", 0),
                 ("Bony Hide", "{DR} has no breath weapon; instead its hide is covered in bony spikes. A creature that "
                  "grapples it or hits it with an unarmed strike takes 5 (1d10) piercing damage.", 0)],
         languages=[], env="Hill, Mountain",
         lore="Fang dragons have no breath weapon, and they make up for it with teeth. They are spiteful and "
              "territorial, and they drain the strength of their prey with every bite. Their hides are gray-brown and "
              "studded with bony plates.",
         lair=["Bone spikes erupt in a 20-foot square: DC 15 Dexterity saving throw or take 10 (3d6) piercing damage.",
               "The dragon makes one Bite attack.",
               "Each creature of the dragon's choice within 60 feet must succeed on a DC 15 Wisdom saving throw or be "
               "&Reference[frightened] until initiative count 20 on the next round."]),
]
