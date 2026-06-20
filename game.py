import random, sys, os, textwrap

def play_game():
    RED = '\033[31m'
    BLACK_BG = '\033[40m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    def border(text, width=72, double=False):
        try:
            import shutil
            term_width = shutil.get_terminal_size().columns
            width = min(width, term_width - 2) if term_width > 20 else width
        except:
            pass

        wrap_width = width - 4
        if wrap_width < 10:
            wrap_width = 10

        wrapped_lines = []
        for line in text.split('\n'):
            if line == '':
                wrapped_lines.append('')
            else:
                wrapped_lines.extend(textwrap.wrap(line, width=wrap_width) or [''])

        max_len = max(len(line) for line in wrapped_lines) if wrapped_lines else 0
        box_width = max(max_len + 4, width)

        tl = '╔' if double else '┌'
        tr = '╗' if double else '┐'
        bl = '╚' if double else '└'
        br = '╝' if double else '┘'
        hz = '═' if double else '─'
        vt = '║' if double else '│'

        top = tl + hz * (box_width - 2) + tr
        bottom = bl + hz * (box_width - 2) + br
        middle = ''
        for line in wrapped_lines:
            middle += f"{vt} {line.ljust(max_len)} {vt}\n"
        return f"{top}\n{middle}{bottom}"

    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_first_name(full_name):
        return full_name.split()[0]

    clear_screen()
    print(RED + BLACK_BG + BOLD + border(
        "The Red Affair\n\n"
        "A greasy spoon-dive at the edge of the Pillars of Creation. No sound travels\n"
        "through the vacuum of space, but the constant debris, gas, and radiation that\n"
        "beats on the clear polymerate windows makes it sound like the whine of creation\n"
        "on a loop like a scratched magneto-disc.\n"
        "The air scrubber is on the fritz, but that's not why it's so stuffy in here,\n"
        "or why the coffee tastes perhaps a little more than just recycled. A body is\n"
        "cooling in the back, and it's your job to figure out why.\n\n"
        "Outside the porthole: The Grand Void, silence only ever punctuated by\n"
        "the occasional existential scream of a dying star, planet, or god.\n\n"
        "The airlock is sealed. The unmanned aerospace police drone is forty hours out.\n"
        "Somewhere in this fluorescent flickering palisade of sin, a killer waits.",
        double=True
    ) + RESET)
    print()
    input("Press Enter to begin...")
    clear_screen()

    player_name = input(f"{RED}{BLACK_BG}Your name, detective, if you subscribe to such niceties: {RESET}").strip()
    if not player_name:
        player_name = "Myla-Dean"
    print(f"\n{RED}{BLACK_BG}The name's {player_name}. Licensed to poke around in other people's misery.\n")
    print(f"The universe doesn't care. But you should, and here you are.{RESET}\n")

    LEANINGS = ["communist", "fascist", "liberal", "anarchist"]
    print(f"{RED}{BLACK_BG}Before we begin – your, um- political leanings?")
    print("(It matters as much as anything matters in a pressurized tin can. Turns out? Quite a lot.)")
    print("1. Communist – Strong and welcoming. The people united will never be defeated.")
    print("2. Fascist – Order above all. Strength through unity. Terrifying.")
    print("3. Liberal – The free market solves everything. Adorable.")
    print("4. Anarchist – No gods, no masters, no parking tickets. Chaotic.")
    while True:
        choice = input(f"Choose your delusion (1-4): {RESET}").strip()
        if choice == '1':
            player_lean = "communist"
            break
        elif choice == '2':
            player_lean = "fascist"
            break
        elif choice == '3':
            player_lean = "liberal"
            break
        elif choice == '4':
            player_lean = "anarchist"
            break
        else:
            print("Oh, come on. Don't tell me you're one of those ''radical centrist'' types. You're -you're not, are you?")
    print(f"\nA {player_lean} detective. The universe adjusts its expectations accordingly. You probably should as well.\n")
    input("Press Enter to step in through the airlock...and into the lockdown.")
    clear_screen()

    RESERVED_KEY_THX1138 = "thatcher"

    shuffled_leans = LEANINGS.copy()
    random.shuffle(shuffled_leans)
    suspect_leans = {
        "marcus": shuffled_leans[0],
        "napoleon": shuffled_leans[1],
        "cleopatra": shuffled_leans[2],
        RESERVED_KEY_THX1138: shuffled_leans[3]
    }

    suspect_descriptions = {
        "marcus": (
            "Aiden Adams slumps against the cash register like any employee who's\n"
            "realized the universe hates him, his boss tolerates him, and his mother only may have liked him. His beard is\n"
            "the kind that's seen everything in the perpetual nightlife scene that lures in honeys, hicks, hacks, hackers, and horrors– mostly horrors. He wears a diner uniform standard: black button-up, black pants, red tie, that way you never see it stained with what might be coffee or might be the remnants of a collapsed college student. His eyes are deep wells of calm resignation, the kind you\n"
            "develop when you've watched people die, or maybe even the kind you develop when you're why people die. A syntharette sits crooked behind his ear, and one glows between his lips, because even in space, some men can't let go\n"
            "of their addictions."
        ),
        "napoleon": (
            'Bladovich "Blake" Jughashvili occupies a booth like he\'s planning a wedding alone,\n'
            "and he intends to crash it. ''Heart of Gold, Head of Lead'', reads a sententia in\n"
            "obscure Na-Min lettering emblazoned across his neck from behind and under his ear\n"
            "down towards his chin. He's buff, but still shorter than you'd expect,\n"
            "shorter than he'd like, and shorter than he would willingly admit. The pompadour\n"
            "adds a few inches to his height, but not his dignity. His hands are on the table,\n"
            "shaking like someone who's completely innocent, and scared out of their wits; maybe\n"
            "someone who's guilty, and just wasn't cut out for murder and secret keeping. The\n"
            "napkins scattered around him are covered in various bodily fluids, all from his\n"
            "face. For what? Nobody knows. Probably not even him."
        ),
        "cleopatra": (
            "Alice Oliverae stands by the back door with the bearing of a woman who's\n"
            "met every goal she laid out in life and found them wanting. Her kohl-rimmed eyes and obsidian rimmed glasses have witnessed the fall of rivals and the rise of ever disappointing replacements. Gold bangles clink on her wrists with every gesture, her outfit is outlandish but somehow still tame. Gold, makeup, and two pins in long stockings made up with gold thread that just doesn't end. She doesn't occupy space so much as allow it the remarkable privilege of containing her."
        ),
        RESERVED_KEY_THX1138: (
            "Nyx Singénero lounges about the back office like they've already been cleared by the investigation. Their posture is a monument to the conviction that they are right and you are merely an inconvenience. The synthjade and anodized chain around their neck catches the flickering white-washed light\n"
            "and glares in tandem with Nyx right at you with what feels like spite, but may be mild annoyance. Their hair is an auburn tinted burgundy, pulled into a bun and held in place with chopsticks placed with unwavering certainty. When they speak,\n"
            "their voice has the texture of gravel being crushed into smaller, more compliant gravel. They smell like an ashtray and sound like every smoke they've ever had left enough tar behind to preserve the mesozoic.  There's something in their eyes – not warmth,\n"
            "exactly, but the cold fusion of absolute conviction. Their feet are on their desk at the end of two crossed legs, but they don't seem to be waiting for you to speak. They seem to already know what you're going to say. Maybe they just know everything."
        )
    }

    suspects = {
        "marcus": {
            "name": "Aiden Adams",
            "alive": True, "hostile": False, "detained": False, "defeated": False,
            "hp": 25,
            "motive": "Personal differences about the appropriate use of power – the kind that end in firings, perhaps even body bags.",
            "guilty": False,
            "lean": suspect_leans["marcus"],
            "characteristics": ["stoic", "bearded", "calm", "philosophical"],
            "curses": ["chem-sucker", "sinkhook", "fucking pig", "federal gangster", "murder jockey"],
            "exonerated": False
        },
        "napoleon": {
            "name": 'Bladovich "Blake" Jughashvili',
            "alive": True, "hostile": False, "detained": False, "defeated": False,
            "hp": 25,
            "motive": "Turns out they used to date, maybe it was a bad breakup, maybe the kind that leaves blood on the cutting room floor.",
            "guilty": False,
            "lean": suspect_leans["napoleon"],
            "characteristics": ["short", "intense", "militaristic", "ambitious"],
            "curses": ["synthrot", "neural-plushie", "prescription grade fool", "leakskull", "spiritual hernia"],
            "exonerated": False
        },
        "cleopatra": {
            "name": "Alice Oliverae",
            "alive": True, "hostile": False, "detained": False, "defeated": False,
            "hp": 25,
            "motive": "Breakdowns in business negotiations, making 'hostile takeover' mean exactly what it sounds like.",
            "guilty": False,
            "lean": suspect_leans["cleopatra"],
            "characteristics": ["regal", "serpentine", "charismatic", "patient"],
            "curses": ["joy thief", "state ghoul", "cashcop", "moonboot-licker", "chitterlings egg"],
            "exonerated": False
        },
        RESERVED_KEY_THX1138: {
            "name": "Nyx Singénero",
            "alive": True, "hostile": False, "detained": False, "defeated": False,
            "hp": 25,
            "motive": "She stood up for herself against Nyx's bullying. Sometimes putting your foot down brings the rest of you along for at least six feet more.",
            "guilty": True,
            "lean": suspect_leans[RESERVED_KEY_THX1138],
            "characteristics": ["detached", "strong", "unusual", "calculating"],
            "curses": ["state sponsored thug", "gas-cow", "auctioneer of justice", "unbelievably fucking stupid asshole", "viscera venture capitalist"],
            "exonerated": False
        }
    }

    suspect_aliases = {
        "marcus": "marcus",
        "aiden": "marcus",
        "adams": "marcus",
        "aiden adams": "marcus",
        "napoleon": "napoleon",
        "bladovich": "napoleon",
        "blake": "napoleon",
        "jughashvili": "napoleon",
        "blake jughashvili": "napoleon",
        "bladovich jughashvili": "napoleon",
        "cleopatra": "cleopatra",
        "alice": "cleopatra",
        "oliverae": "cleopatra",
        "alice oliverae": "cleopatra",
        RESERVED_KEY_THX1138: RESERVED_KEY_THX1138,
        "nyx": RESERVED_KEY_THX1138,
        "singénero": RESERVED_KEY_THX1138,
        "nyx singénero": RESERVED_KEY_THX1138,
    }

    def resolve_suspect(name):
        if not name:
            return None
        name = name.strip().lower()
        return suspect_aliases.get(name)

    revealed_characteristic = {
        "marcus": "detached",
        "napoleon": "strong",
        "cleopatra": "unusual",
        RESERVED_KEY_THX1138: None
    }

    locations = {
        "counter": {
            "desc": (
                "THE COUNTER – A scratched carbonite slab that's seen more elbows than a\n"
                "gala dance floor with Fred Astaire and Bob Fosse. The cash register is smashed open, PCB, chits, change, and Valerian Draughma spilled across the floor like so many things have been over the years, leaving a sticky film beneath your shoes.\n"
                "The entrance is sealed with a field of plasma that hums something like a funeral dirge. Maybe you're imagining that last bit, but visually, audibly, and tactically if you must, you do know the field is there.\n\n"
                + suspect_descriptions["marcus"]
            ),
            "items": [],
            "suspect": "marcus",
            "searchable": ["aiden_alibi"]
        },
        "dining": {
            "desc": (
                "THE DINING AREA – Booths line the walls placed in opposition with a white table between them, and the walls undecorated except for the art deco murals that fill the otherwise unremarkable space; one to each wall. Upholstered in synthleather and what was once blue vinyl, they are now\n"
                "faded and cracking across every surface except one patch now the color of dried blood and and what was once, presumably, someone's personality. Napkins, sauce, seasoning, and marmalade are strewn across one tabletop, the rest being various gradations of clean, none of which seem hygienic. The jukebox is stuck on a single song – an avant garde noise album, now academically classical hundreds of years later and light-years away, but it vibrates your fillings.\n\n"
                + suspect_descriptions["napoleon"]
            ),
            "items": [],
            "suspect": "napoleon",
            "searchable": ["blake_alibi"],
            "hidden_revolver": True
        },
        "kitchen": {
            "desc": (
                "THE KITCHEN – Stainless steel griddles that haven't been stainless since\n"
                "the most recent Big Bang. A food can full of what's either canned food or\n"
                "cleaning solvents sits atop the griddle. The back door is hermetically sealed,\n"
                "its porthole showing nothing but the indifferent void. Every kitchen has its\n"
                "secrets, but you feel something extra weighing down the ether in this one.\n"
                "You intend to find what it is, whatever it takes, and whoever's responsible.\n\n"
                + suspect_descriptions["cleopatra"]
            ),
            "items": ["candlestick"],
            "suspect": "cleopatra",
            "searchable": ["alice_alibi"]
        },
        "office": {
            "desc": (
                "THE BACK OFFICE – A cramped drywall cage full of stale smoke and broken promises of raises, promotions, and staff openings. The body of a man lies sprawled on the floor, like a taxidermy rug by the world's laziest psychopath. A single gunshot wound to the temple. It's neat, professional, and almost polite. Blood has pooled in the cracks of a linoleum floor that screamed despair and desperation long before it became\n"
                "a crime scene. The smell is...complex. You draw in the bouquet like the seasoned professional you are.  Gunpowder, iron, acetone, and something sweet all separate as components in your mind through a mastery in the art of olfactory reverse-engineering.  A torn sheet of paper flutters near the desk.\n\n"
                + suspect_descriptions[RESERVED_KEY_THX1138]
            ),
            "items": ["poison vial"],
            "suspect": RESERVED_KEY_THX1138,
            "searchable": ["nyx_message"],
            "body_examinable": True
        }
    }

    current_location = "counter"
    inventory = []
    handcuffs = 2
    clues = set()
    evidence_collected = 0
    body_examined = False
    revolver_found = False
    game_over = False
    traits_revealed = set()
    trust = {}
    nyx_escape_offered = False
    talk_history = {}
    countenance_used = False
    required_incriminating = 3
    for s in suspects:
        trust[s] = 1 if suspects[s]["lean"] == player_lean else 0

    player = {
        "hp": 30,
        "max_hp": 30,
        "level": 1,
        "xp": 0,
        "xp_to_next": 3,
        "base_damage": 5.0,
        "regular_hit_chance": 0.20,
        "special_hit_chance": 0.10
    }

    incriminating = {"nyx_message", "unknown_revolver", "aiden_footprint", "blake_witness", "alice_witness"}

    MISLEADING_CLUES = {
        "marcus": ["aiden_says_alice_promoted", "aiden_says_alice_paycheck", "aiden_says_victim_angry"],
        "cleopatra": ["alice_blake_screenshots", "alice_victim_msg_afraid", "alice_victim_cant_stay_home"],
        "napoleon": ["blake_nyx_bully", "blake_nyx_called_out", "blake_victim_distant"],
        RESERVED_KEY_THX1138: ["nyx_aiden_resented", "nyx_alice_promoted_over_victim", "nyx_victim_didnt_want_return"]
    }

    def hud():
        print(RED + BLACK_BG + "╔══ HUD ═══════════════════════════════════════════╗")
        print(f"║ Location: {current_location.ljust(8)}  Cuffs: {handcuffs}/2    HP: {player['hp']}/{player['max_hp']}   ║")
        print("╚══════════════════════════════════════════════════╝" + RESET)

    def add_evidence(ev_id):
        global evidence_collected
        if ev_id not in clues:
            clues.add(ev_id)
            evidence_collected += 1
            print(f"{RED}📋 Evidence: {ev_id} ({evidence_collected}/8){RESET}")
            player["xp"] += 1
            if player["xp"] >= player["xp_to_next"]:
                level_up()

    def remove_evidence(ev_id):
        global evidence_collected
        if ev_id in clues:
            clues.remove(ev_id)
            evidence_collected -= 1
            print(f"{RED}📋 Evidence lost: {ev_id} ({evidence_collected}/8){RESET}")

    def level_up():
        player["level"] += 1
        player["xp"] = 0
        player["xp_to_next"] += 2
        player["max_hp"] += 5
        player["hp"] = player["max_hp"]
        player["base_damage"] += 0.5
        reg_increase = random.randint(5, 10) / 100.0
        spec_increase = random.randint(5, 10) / 100.0
        player["regular_hit_chance"] = min(player["regular_hit_chance"] + reg_increase, 0.95)
        player["special_hit_chance"] = min(player["special_hit_chance"] + spec_increase, 0.95)
        print(f"{RED}🎉 LEVEL UP! Level {player['level']}. HP: {player['hp']}/{player['max_hp']}{RESET}")

    def trust_change(sus, amount):
        trust[sus] = max(0, min(3, trust[sus] + amount))
        if amount > 0:
            print(f"Trust with {get_first_name(suspects[sus]['name'])} up ({trust[sus]}/3)")
        elif amount < 0:
            print(f"Trust with {get_first_name(suspects[sus]['name'])} down ({trust[sus]}/3)")

    def reveal_characteristic(sus):
        if sus == RESERVED_KEY_THX1138:
            print(f"{get_first_name(suspects[sus]['name'])} lights a smoke in their hand and waves dismissively: 'The killer? I have no idea. I was contemplating things that actually mattered.'")
            return
        trait = revealed_characteristic[sus]
        if trait not in traits_revealed:
            traits_revealed.add(trait)
            print(f"{get_first_name(suspects[sus]['name'])} leans in: 'The killer was definitely {trait}. I just know it. I mean, they'd have to be to do something like that.'")
            print(f"   (Clue: {trait})")
        else:
            print(f"{get_first_name(suspects[sus]['name'])} already told you. You weren't listening...were you...?")

    def check_traits():
        if len(traits_revealed) >= 3:
            killer_traits = suspects[RESERVED_KEY_THX1138]["characteristics"]
            if sum(1 for t in traits_revealed if t in killer_traits) >= 3:
                return True
        return False

    def describe_location():
        loc = locations[current_location]
        desc = loc["desc"]
        if current_location == "dining" and revolver_found:
            desc += "\nThe napkin dispenser is empty – you already liberated its secret."
        if current_location == "office" and "nyx_message" in clues:
            desc += "\nThe torn paper is gone. Its absence feels louder than its presence."
        if current_location == "office" and not body_examined:
            desc += "\nThe body waits. Patient as only the dead can be."
        sus_key = loc.get("suspect")
        if sus_key:
            s = suspects[sus_key]
            if s["exonerated"]:
                desc += f"\n\n{get_first_name(s['name'])} is here, but they've been completely exonerated. Not worth your time."
            elif s["alive"] and not s["detained"] and not s["defeated"]:
                desc += f"\n\n{get_first_name(s['name'])} is here. Trust: {trust[sus_key]}/3 – fragile as a soap bubble."
                desc += f"\nPolitical lean: {s['lean']}"
            elif s["detained"]:
                desc += f"\n\n{get_first_name(s['name'])} is handcuffed, radiating silent fury."
            elif s["defeated"]:
                desc += f"\n\n{get_first_name(s['name'])} is unconscious, dreaming whatever dreams a bruised ego conjures."
        print(border(desc, width=68))

    def move(direction):
        global current_location
        if direction in locations:
            current_location = direction
            clear_screen()
            hud()
            describe_location()
        else:
            print("Not a room. Try: counter, dining, kitchen, office.")

    def search():
        global revolver_found
        loc = locations[current_location]
        if current_location == "dining" and loc.get("hidden_revolver") and not revolver_found:
            revolver_found = True
            inventory.append("revolver")
            print("In Plain View: cold metal made for someone with even colder blood; a revolver. It's definitely recently fired – the barrel still whispers gunpowder to anyone who will pay attention.")
            add_evidence("unknown_revolver")
            return
        if current_location == "office" and "nyx_message" not in clues:
            inventory.append("torn thesis")
            add_evidence("nyx_message")
            print(f"Torn paper. {suspects[RESERVED_KEY_THX1138]['name']}'s handwriting. Hard to make out what was said here, but by the looks of phrases like \"per my last query\", \"as you can see\", and at least one use of the word asinine in the corner like a watermark where the rip begins at the bottom – this is clearly an angry letter preceded by at least a couple more.")
            return
        if current_location == "counter" and "aiden_alibi" not in clues:
            print("Payphone log. Aiden was on a call at time of death. It's hard to be in two places at once, but you've seen stranger things.")
            add_evidence("aiden_alibi")
            trust_change("marcus", 1)
            return
        if current_location == "dining" and "blake_alibi" not in clues:
            print("Time-stamped napkin. Blake's scribblings. He was here all evening writing some sort of...polemic? Seems pretty unlikely he's your man.")
            add_evidence("blake_alibi")
            trust_change("napoleon", 1)
            return
        if current_location == "kitchen" and "alice_alibi" not in clues:
            print("Bus ticket stub. The schedule readout on your personal device confirms Alice would have arrived just before the shot, maybe even just after. Well, that dog just don't hunt.")
            add_evidence("alice_alibi")
            trust_change("cleopatra", 1)
            return
        print("Nothing. Nothing worth mentioning anyway, just grease, despair, and the miasma of mystery.")

    def examine(item):
        global body_examined
        if item == "body" and current_location == "office":
            if not body_examined:
                body_examined = True
                print("The victim appears to be between the ages of 25 and 30. Feminine. Clothes are in tact, the wallet is in hand. From the look of it, it doesn't seem it ever left her fist. She's approximately 5 feet tall. Her makeup is done, smeared only from the blood. For a brief moment, you wonder what foundation she used. You've only ever heard of makeup smudging in old films.\n\nThe victim's face: mild surprise. Death wasn't so much terrifying as much as it was rude. Between the eyes is a bullet wound: neat, centered, professional even. Someone knew what they were doing.")
            else:
                print("The body remains. It hasn't changed. Corpses rarely do.")
        else:
            print(f"You give the {item} a good look over. It's definitely a {item}. What were you expecting?")

    def take(item):
        loc = locations[current_location]
        if item in loc["items"]:
            loc["items"].remove(item)
            inventory.append(item)
            print(f"Pocketed: {item}. Maybe you can find some use for it, or just a keep it as a souvenir of this...establishment.")
        else:
            print("It's not here. Maybe it was never here. Maybe nothing is.")

    def talk(sus):
        global nyx_escape_offered
        if not sus:
            print("Who did you want to talk to? Try: Aiden, Blake, Alice, Nyx (or their last names).")
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' is not a person here. Try: Aiden Adams, Blake Jughashvili, Alice Oliverae, Nyx Singénero.")
            return
        s = suspects[sus]
        if s["exonerated"]:
            print("They've been completely cleared. Anything they say is now officially irrelevant.")
            return
        if not s["alive"] or s["defeated"]:
            print("They're beyond conversation. The void has claimed their attention.")
            return
        if s["detained"]:
            print("The cuffs have a way of making people uncooperative.")
            return
        if s["hostile"]:
            print(f"{get_first_name(s['name'])} fixes you with a stare that could curdle deuterium. No conversation today.")
            return
        if locations[current_location].get("suspect") != sus:
            print(f"{get_first_name(s['name'])} isn't here. Space is big. This diner is small. Try the right room.")
            return

        print(f"\n{RED}You approach {get_first_name(s['name'])}. The air shifts.{RESET}")
        print(f"Trust: {trust[sus]}/3 | Lean: {s['lean']}")
        if trust[sus] == 3 and revealed_characteristic[sus] not in traits_revealed:
            reveal_characteristic(sus)

        if sus == RESERVED_KEY_THX1138 and trust[sus] == 3 and not nyx_escape_offered:
            nyx_escape_offered = True
            print(f"\nNyx gives you a long, appraising look. There's something there that you only realize as their lips part and they issue an appeal to your better, perhaps your worst, nature, 'You know, detective... we could help each other.' Your blood runs cold and your heart beats a little faster. You know what they're asking, the only question is whether or not you will.")
            choice = input("Let Nyx escape? (y/n): ").strip().lower()
            if choice == 'y':
                nyx_escape_ending()
                return
            else:
                print("Nyx shrugs. 'Your loss, detective.' The moment passes, but you will never forget it.")

        while True:
            print("\nWhat do you say?")
            options = ["alibi", "motive"]
            if sus == RESERVED_KEY_THX1138 and "nyx_message" in clues:
                options.append("the torn paper")
            if sus == RESERVED_KEY_THX1138 and revolver_found:
                options.append("the revolver")
            if sus == "marcus" and "aiden_footprint" not in clues:
                options.append("anything odd outside")
            if sus == "napoleon" and "blake_witness" not in clues:
                options.append("did you see anything")
            if sus == "cleopatra" and "alice_witness" not in clues:
                options.append("the argument")
            for i, opt in enumerate(options, 1):
                print(f"{i}. Ask about {opt}")
            print("0. Step away")
            choice = input("> ").strip()
            if choice == "0":
                break
            if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
                print("That dog don't hunt. Try something else.")
                continue
            topic = options[int(choice)-1]
            talk_key = (sus, topic)

            if talk_key in talk_history:
                print(f"You've already gone over that with {get_first_name(s['name'])}. Nothing new to add.")
                continue

            talk_history[talk_key] = True
            curse = random.choice(s["curses"]) if s["curses"] else ""

            if topic == "alibi":
                if sus == "marcus":
                    print(f"'You {curse}! Check the payphone log. I was talking to my mother in Serduz on Proxima B. It's not that complicated.'")
                    if "aiden_alibi" not in clues:
                        add_evidence("aiden_alibi")
                        trust_change("marcus", 1)
                elif sus == "napoleon":
                    print("'Wait, where is it? It's not in my pocket, but I swear, I was writing at that time. I even wrote the time I began. There's a napkin around here somewhere on it that proves my innocence, I promise you!'")
                    if "blake_alibi" not in clues:
                        add_evidence("blake_alibi")
                        trust_change("napoleon", 1)
                elif sus == "cleopatra":
                    print(f"'What, little ol' me? Well, my bus ticket clears me. Check it yourself. Hey, why not call the Transit Authority and confirm the ticket too?'")
                    if "alice_alibi" not in clues:
                        add_evidence("alice_alibi")
                        trust_change("cleopatra", 1)
                elif sus == RESERVED_KEY_THX1138:
                    print(f"'Working. Office. Alone. Is that a crime?' *Muttering '{curse}' under breath. Syntharette twitching.")
            elif topic == "motive":
                print(f"'{s['motive']}' Said like it's clearly obvious. Maybe it is.")
                trust_change(sus, -1)
            elif topic == "the torn paper":
                print(f"{get_first_name(s['name'])} glances at the scrap. 'Mine. Obviously. I'm not sure what you expect to do with it, detective.'")
                if sus == RESERVED_KEY_THX1138:
                    print(f"They snatch it back before you can put it away. '{curse}!'")
                    trust_change(sus, -1)
                    if "nyx_message" in inventory:
                        inventory.remove("nyx_message")
            elif topic == "the revolver":
                if sus == RESERVED_KEY_THX1138:
                    print(f"For a moment, but just a moment, something flickers; their face an old neon sign on its last leg that hardly says anything completely. 'Never seen it before, detective.' The lie is obvious, but not why.")
                    trust_change(sus, -1)
            elif topic == "anything odd outside" and sus == "marcus":
                print("'I saw some track out the back porthole. They're too big to be mine, I know that. I know a lot of things. It's a curse sometimes.'")
                add_evidence("aiden_footprint")
                trust_change("marcus", 1)
            elif topic == "did you see anything" and sus == "napoleon":
                print("'I heard someone that was leaving the office after the bang. They had strong posture, I think, because of the sound the footsteps made.'")
                add_evidence("blake_witness")
                trust_change("napoleon", 1)
            elif topic == "the argument" and sus == "cleopatra":
                print(f"'I heard loud voices from the office. {suspects[RESERVED_KEY_THX1138]['name']} and the victim. Nothing civil about it, but then, when are *they* ever civil? '")
                add_evidence("alice_witness")
                trust_change("cleopatra", 1)

    def threaten(sus):
        if not sus:
            print("Who are you trying to intimidate?")
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' doesn't match any suspect. Try: Aiden, Blake, Alice, Nyx.")
            return
        s = suspects[sus]
        if s["exonerated"]:
            print("Exonerated. Even you aren't cruel enough to threaten them now.")
            return
        if not s["alive"] or s["defeated"]:
            print("Beyond intimidation. The void has already claimed that privilege.")
            return
        if s["detained"]:
            print("Cuffed. Threatening them now is just poor sportsmanship.")
            return
        if locations[current_location].get("suspect") != sus:
            print("Threatening the air. Bold. Ineffective.")
            return
        curse = random.choice(s["curses"]) if s["curses"] else ""
        print(f"You invade {get_first_name(s['name'])}'s space. The tension rises and the pressure is on.")
        if sus == "marcus":
            print(f"He cracks. 'Fine! I saw {suspects[RESERVED_KEY_THX1138]['name']} near the office right before the gunshot, you jerk! Now back off!! Please?!'")
            trust_change("marcus", 1)
        elif sus == "napoleon":
            print("He doesn't flinch. 'Intimidation is a crude tool. I prefer kindness.' You feel vaguely embarrassed and a little ashamed.")
        elif sus == "cleopatra":
            print("She laughs. Your ego dissolves. 'You dare intimidate me?' Her voice carries a weight that could crush a songbird. Trust completely evaporates.")
            for s2 in suspects:
                if s2 != sus:
                    trust_change(s2, -1)
        elif sus == RESERVED_KEY_THX1138:
            print(f"Their face hardens into something between complete disdain and total disregard. 'No proof, no case, no hope, detective.' They seem much more hostile now. Congratulations.")
            s["hostile"] = True

    def detain(sus):
        global handcuffs
        if handcuffs <= 0:
            print("You reach for your cuffs and find no more.")
            return
        if not sus:
            print("Cuff whom?")
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' isn't a suspect. Try: Aiden, Blake, Alice, Nyx.")
            return
        s = suspects[sus]
        if s["exonerated"]:
            print("They've been cleared. You'd be arresting an innocent person – wait, you've done that before.")
            return
        if not s["alive"] or s["defeated"] or s["detained"]:
            print("You've already detained this one. Another set of cuffs would be redundant, don't you think?")
            return
        if locations[current_location].get("suspect") != sus:
            print("They're not in here and ain't telekinetic. Not yet, anyway.")
            return
        handcuffs -= 1
        s["detained"] = True
        print(f"Click-click-click-click. {get_first_name(s['name'])} now sports a used set of state-issued jewelry. {handcuffs} remaining.")

    def fight(sus):
        if not sus:
            print("Fight who? The existential void?")
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' isn't a suspect. Try: Aiden, Blake, Alice, Nyx.")
            return
        s = suspects[sus]
        if s["exonerated"]:
            print("They've been exonerated. Even you have standards.")
            return
        if not s["alive"] or s["defeated"]:
            print("Already on the floor. Kicking them now is excessive.")
            return
        if s["detained"]:
            print("Cuffed and harmless. What are you, a bully?")
            return
        if locations[current_location].get("suspect") != sus:
            print("Shadowboxing. Very existential. Very pointless.")
            return
        curse = random.choice(s["curses"]) if s["curses"] else ""
        print(f"\n{RED}⚔ The air is electric. You and {get_first_name(s['name'])} circle the area like binary stars on a collision course. There may yet be another murder. At least it'll be easy to solve.{RESET}")
        while player["hp"] > 0 and s["hp"] > 0:
            print(f"\nYour HP: {player['hp']}/{player['max_hp']} | {get_first_name(s['name'])} HP: {s['hp']}")
            print("1. Calculated strike  2. Desperate swing  3. Tactical retreat")
            act = input("> ").strip()
            if act == "3":
                print("Discretion is the most fundamental component of not dying. You retreat, hoping they forgive this trespass.")
                return
            elif act == "1":
                dmg = int(round(player["base_damage"]))
                s["hp"] -= dmg
                print(f"Clean hit. {dmg} damage. Good work.")
            elif act == "2":
                roll = random.random()
                if roll < player["special_hit_chance"]:
                    dmg_float = player["base_damage"] * 1.25
                    dmg = int(round(dmg_float))
                    s["hp"] -= dmg
                    print(f"Lucky break, detective. You land a devastating blow! {dmg} damage.")
                elif roll < player["special_hit_chance"] + player["regular_hit_chance"]:
                    dmg = int(round(player["base_damage"]))
                    s["hp"] -= dmg
                    print(f"Wild-eyed, but effective. Be careful, detective. {dmg} damage.")
                else:
                    print("Your swing goes wide! No damage.")
            else:
                print("Indecision could cost your life. No damage.")
            if s["hp"] <= 0:
                s["hp"] = 0
                s["defeated"] = True
                print(f"{get_first_name(s['name'])} collapses, eyes rolled back and lips muttering '{curse}' before their animus fades.")
                check_total_carnage()
                return
            edmg = random.randint(3, 6)
            player["hp"] -= edmg
            print(f"{get_first_name(s['name'])} strikes back. {edmg} damage. You see murder in their eyes.")
            if player["hp"] <= 0:
                player["hp"] = 0
                print("Darkness rolls over you. The void encompasses your vision bit by bit. Somewhere, a jukebox plays your funeral dirge, and no one realizes it. Game over, detective.")
                sys.exit(0)

    def check_total_carnage():
        if all(suspects[k]["defeated"] for k in suspects):
            ending_carnage()

    def accuse(sus):
        global handcuffs
        if not sus:
            print("Accuse who? Make up your mind, detective.")
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' doesn't match anyone. Try: Aiden, Blake, Alice, Nyx.")
            return
        if sus != RESERVED_KEY_THX1138 and suspects[RESERVED_KEY_THX1138]["detained"]:
            secret_ending()
            return
        if sus != RESERVED_KEY_THX1138:
            ending_fail()
            return

        if len(clues.intersection(incriminating)) < required_incriminating:
            print(f"{get_first_name(suspects[RESERVED_KEY_THX1138]['name'])} smirks. 'Let's say I did. Who in Existence would believe you? You've got nothing on me.'")
            return

        if suspects[RESERVED_KEY_THX1138]["detained"]:
            ending_correct()
            return

        print(f"\nYou point at {get_first_name(suspects[RESERVED_KEY_THX1138]['name'])}. 'You.' The word hangs like a bullet; slipping behind their eyes and through their mental folds as the realization dawns on them. You're pointing at them, and you're not backing down.")
        print(f"You both notice at the same time: they're unrestrained. '{player_name}, you absolute fool!' They lunge.")
        fight(RESERVED_KEY_THX1138)
        if suspects[RESERVED_KEY_THX1138]["defeated"] and not suspects[RESERVED_KEY_THX1138]["detained"]:
            if handcuffs > 0:
                handcuffs -= 1
                suspects[RESERVED_KEY_THX1138]["detained"] = True
                print(f"You slap the cuffs on {get_first_name(suspects[RESERVED_KEY_THX1138]['name'])}. {handcuffs} remaining. Justice never tasted so bloody and sweet. Good job, detective. They're sure to tell stories of this one at the station.")
            else:
                print("You don't have any cuffs left, but they're out cold. The police drone will handle it. Probably. You light a smoke and watch over them making sure they're still breathing ready to issue another state-sanctioned beat-down if necessary.")
            ending_correct()
        elif suspects[RESERVED_KEY_THX1138]["defeated"] and suspects[RESERVED_KEY_THX1138]["detained"]:
            ending_correct()
        else:
            print("They slip your grasp and bolt out the door like greased lightning. The airlock cycles. By the time you reach it, they're a silhouette against the stars. You'll never catch up to them, and may never find them again. It's a 24 carat run of bad luck, or maybe just bad decision making gilded with pyrite excuses.")
            ending_fail()

    def secret_ending():
        global game_over
        print(f"\nWrong accusation. You made the wrong bet. Very wrong.")
        print(f"Behind you: a soft click. You spin. {get_first_name(suspects[RESERVED_KEY_THX1138]['name'])}, one wrist free, working on the other.")
        print(f"'Did you really think these standard restraints could hold me?' They smile. The predator turns prey, but it dawns on you they're damn good at being either.")
        print(f"'Entertaining, {player_name}. Truly. But I have a schedule to keep, and you have a new problem to explain.'")
        print("They're gone before you can move. The airlock cycles. Moments later the police drone arrives to an empty office and a restaurant full of fools. Too bad, detective. They'll definitely tell this story although you'd certainly wish they wouldn't.")
        print(f"\n{RED}GAME OVER{RESET}")
        game_over = True
        sys.exit(0)

    def nyx_escape_ending():
        global game_over
        print("Nyx parts their lips once more to reveal their toxic solvent-based smile. Their eyes flash the recognition that's only ever shared between two predators in league with each other. You immediately begin to consider how you'll spin this to the police drone. You scratch your notepad with fervor and get to work destroying the evidence. Why you did this, only you'll ever know, and let's hope it doesn't haunt you any longer than it takes to finish a bottle of absinthe. Few things ever do.\n\nGAME OVER")
        game_over = True
        sys.exit(0)

    def ending_correct():
        global game_over
        k = suspects[RESERVED_KEY_THX1138]
        print(f"\n{RED}Everything clicks into place. The whole crooked design.{RESET}")
        print(f"'{get_first_name(k['name'])}, in the office, with the revolver. Victim killed in cold blood. For ego? For fun? For the oldest reason there ever was: because you could.'")
        print(f"{get_first_name(k['name'])} deflates like a punctured flight suit. 'Yes, you meddling {random.choice(k['curses'])}. Fine! I did it. And I'd do it again. I'd do it all again without a second damn thought.'")
        print("The confession hangs in the air, hideous and undeniable. You make your notes.")
        for sus in suspects:
            if sus == RESERVED_KEY_THX1138: continue
            s = suspects[sus]
            if s["alive"] and not s["defeated"] and not s["exonerated"]:
                curse = random.choice(s["curses"]) if s["curses"] else "sprocket-head"
                print(f"{get_first_name(s['name'])} stares. 'Them? All along? That...makes sense...'")
        print("\nMoments later, the police drone docks with a hydraulic hiss. Justice arrives on autopilot, but it lands, as it is wont to do, in your hands. Good job, detective. You're sure to get a bonus for this one.\n")
        print(f"{RED}Game Over.{RESET}")
        game_over = True
        sys.exit(0)

    def ending_fail():
        global game_over
        k = suspects[RESERVED_KEY_THX1138]
        print("\nYour accusation shatters against the truth like glass against bulkhead.")
        print(f"{get_first_name(k['name'])} has no skeletons in their closet, at least none that are people. 'Poor {player_name}. So close. Yet so... not.'")
        print("The killer's out the back before the drone docks. By the time authorities arrive: you're trembling with frustration, confusion, and shame.")
        for sus in suspects:
            if sus != RESERVED_KEY_THX1138:
                s = suspects[sus]
                if s["alive"] and not s["defeated"] and not s["exonerated"]:
                    print(f"{get_first_name(s['name'])} shakes their head. This failure has left them feeling betrayed and more importantly, to you anyway, disappointed.")
        print(f"The drone files its report. Somewhere in a distant solar system, it moves across the desk of your superiors, and with that your reputation shrinks further. You're sure to catch hell for this one, {player_name}.\n")
        print(f"{RED}GAME OVER{RESET}")
        game_over = True
        sys.exit(0)

    def ending_carnage():
        global game_over
        print("You look back across the bar. Everyone's dead. Dead folk tell no tales, but there's sure to be plenty living who watch your live-streamed execution. The detective who went completely mad and committed mass murder. Good job, I guess, detective. Maybe you'll solve a case in the next life.\n\nGAME OVER")
        game_over = True
        sys.exit(0)

    def countenance():
        global countenance_used, handcuffs, required_incriminating
        if countenance_used:
            print("You've already called upon your Countenance. The moment has passed.")
            return
        countenance_used = True

        if player_lean == "liberal":
            sus_key = locations[current_location].get("suspect")
            if not sus_key or suspects[sus_key]["exonerated"] or trust[sus_key] < 3:
                print("The required trust isn't there. The moment fades, wasted.")
                return
            print("You flash a fat stack of credits, multiple denominations, multiple forms of currency, all tied together with a rubber band. You ask, gently, with this new tool of persuasion.")
            s = suspects[sus_key]
            for ev in MISLEADING_CLUES.get(sus_key, []):
                add_evidence(ev)
            print(f"{get_first_name(s['name'])} spills everything they know about another patron. The evidence is bought and paid for, but cash quantity doesn't always mean product quality.")
        elif player_lean == "fascist":
            sus_key = locations[current_location].get("suspect")
            if not sus_key:
                print("Nobody here to interrogate. The Countenance fizzles uselessly.")
                return
            s = suspects[sus_key]
            if s["exonerated"]:
                print("They've been exonerated. No point.")
                return
            print("You flash your badge and strike the federal salute pose. Their visage softens greatly as you threaten to throw them, their family, and anyone they've ever loved into a deep dark mine with no escape, benefits, or unions to speak of.")
            if sus_key != RESERVED_KEY_THX1138:
                others = [k for k in suspects if k != sus_key and k != RESERVED_KEY_THX1138]
                if random.random() < 0.8:
                    pair = [RESERVED_KEY_THX1138, random.choice(others)]
                else:
                    pair = random.sample(others, 2)
                names = [get_first_name(suspects[k]['name']) for k in pair]
                print(f"{get_first_name(s['name'])} leans in: 'Ok! Ok! Look, it's either {names[0]} or {names[1]}. I'm sure of it.'")
            else:
                innocents = [k for k in suspects if k != RESERVED_KEY_THX1138]
                pair = random.sample(innocents, 2)
                names = [get_first_name(suspects[k]['name']) for k in pair]
                print(f"Nyx smirks. 'If you must know, I suspect {names[0]} or {names[1]}.'")
        elif player_lean == "communist":
            handcuffs += 1
            print("You speak into your cufflinks, whether anyone notices or not is immaterial. A commissar materialises from the ventilation shaft, slaps a fresh pair of cuffs into your palm, and vanishes. This is sure to be useful. (+1 cuffs)")
        elif player_lean == "anarchist":
            candidates = [k for k in suspects if k != RESERVED_KEY_THX1138 and not suspects[k]["exonerated"]]
            if not candidates:
                print("Everyone not guilty is already cleared. The gesture does nothing.")
                return
            chosen = random.choice(candidates)
            suspects[chosen]["exonerated"] = True
            print("You start beating your chest and call for everyone to rally where you stand. You make an impassioned speech detailing the nature of liberty, law, justice, and outline flaws in the current galactic justice system. In the chaos, a few things happen, and you struggle to keep track of what happens when.")
            print(f"{get_first_name(suspects[chosen]['name'])} is completely exonerated. All evidence tied to them evaporates like mist.")
            prefixes = {
                "marcus": ["aiden_alibi", "aiden_footprint"],
                "napoleon": ["blake_alibi", "blake_witness"],
                "cleopatra": ["alice_alibi", "alice_witness"]
            }
            for clue in prefixes.get(chosen, []):
                if clue in clues:
                    remove_evidence(clue)
                    if clue in incriminating:
                        required_incriminating = max(0, required_incriminating - 1)
                        print(f"(Required incriminating evidence now {required_incriminating})")
        else:
            print("Your Countenance manifests in an unexpected way. Nothing happens.")

    def show_inventory():
        ev_list = '\n'.join(f' - {e}' for e in sorted(clues)) if clues else "You've got nothing. The void stares back. Don't blink."
        print(border(f"Inventory: {', '.join(inventory) if inventory else 'empty pockets'}\nCuffs: {handcuffs}/2\nHP: {player['hp']}/{player['max_hp']}\n\nEvidence ({evidence_collected}/8):\n{ev_list}", width=68))

    EASTER_EGG_PHRASE = "Im an existentialist-absurdist-gnostic-agnostic-secular-true path unitarian-marxist-leninist-maoist multi-level marketer."

    shortcuts = {
        'g': 'go', 'l': 'look', 's': 'search', 'e': 'examine', 't': 'talk',
        'th': 'threaten', 'd': 'detain', 'f': 'fight', 'a': 'accuse',
        'i': 'inventory', 'inv': 'inventory', 'h': 'help', '?': 'help',
        'q': 'quit', 'x': 'examine', 'c': 'countenance'
    }

    def expand_command(raw):
        raw = raw.strip()
        if not raw:
            return None
        if raw.lower() == EASTER_EGG_PHRASE.lower():
            print(border("You realize once today is over, tomorrow will never come. Red will fade to black, and you will wake up in another reality, as another person, and this experience may never truly grow roots and flourish in your psyche. You will simply move onto the next life.", width=68))
            return None
        parts = raw.split()
        first = parts[0].lower()
        if first in shortcuts:
            if first in ('g', 'go'):
                return f"go {' '.join(parts[1:])}" if len(parts) > 1 else "go"
            elif first in ('t', 'talk'):
                return f"talk {' '.join(parts[1:])}" if len(parts) > 1 else "talk"
            elif first in ('th', 'threaten'):
                return f"threaten {' '.join(parts[1:])}" if len(parts) > 1 else "threaten"
            elif first in ('d', 'detain'):
                return f"detain {' '.join(parts[1:])}" if len(parts) > 1 else "detain"
            elif first in ('f', 'fight'):
                return f"fight {' '.join(parts[1:])}" if len(parts) > 1 else "fight"
            elif first in ('a', 'accuse'):
                return f"accuse {' '.join(parts[1:])}" if len(parts) > 1 else "accuse"
            elif first in ('e', 'x', 'examine'):
                return f"examine {' '.join(parts[1:])}" if len(parts) > 1 else "examine"
            elif first in ('l', 'look'):
                return "look"
            elif first in ('s', 'search'):
                return "search"
            elif first in ('i', 'inv', 'inventory'):
                return "inventory"
            elif first in ('h', '?'):
                return "help"
            elif first == 'q':
                return "quit"
            elif first == 'c':
                return "countenance"
        return raw

    def help_text():
        print(border("""
Commands (shortcut):
  go <place>       (g)  – move between rooms
  look             (l)  – survey current location
  search           (s)  – rummage for hidden clues
  examine <obj>    (e/x)– inspect something closely
  take <item>           – pocket an item
  talk <suspect>   (t)  – interrogate a patron
  threaten <suspect>(th)– apply pressure (may backfire)
  detain <suspect> (d)  – apply handcuffs (2 pairs)
  fight <suspect>  (f)  – resort to violence
  accuse <suspect> (a)  – point the finger
  inventory        (i)  – check pockets and evidence
  countenance      (c)  – use your one-time political ability
  help             (h/?)– this list
  quit             (q)  – abandon the case
Rooms: counter, dining, kitchen, office
Suspects: Aiden Adams, Alice Oliverae, Blake Jughashvili, Nyx Singénero
          (use first name, last name, or full name)
""", width=68))

    clear_screen()
    hud()
    describe_location()
    while not game_over:
        hud()
        raw = input(f"{RED}> {RESET}").strip()
        if not raw:
            continue
        expanded = expand_command(raw)
        if not expanded:
            continue
        parts = expanded.split()
        verb = parts[0]
        noun = " ".join(parts[1:]) if len(parts) > 1 else ""

        if verb == "go":
            move(noun)
        elif verb == "look":
            clear_screen()
            hud()
            describe_location()
        elif verb == "search":
            search()
        elif verb == "examine":
            examine(noun)
        elif verb == "take":
            take(noun)
        elif verb == "talk":
            talk(noun)
        elif verb == "threaten":
            threaten(noun)
        elif verb == "detain":
            detain(noun)
        elif verb == "fight":
            fight(noun)
        elif verb == "accuse":
            accuse(noun)
        elif verb == "countenance":
            countenance()
        elif verb == "inventory":
            show_inventory()
        elif verb == "help":
            help_text()
        elif verb == "quit":
            print("You step back through the airlock. For now, the case remains unsolved; one day going cold. The stars don't care. Neither do you.")
            sys.exit(0)
        else:
            print("Unrecognized command. This must be your first homicide detail. Type 'help' or 'h' for assistance.")

if __name__ == "__main__":
    play_game()