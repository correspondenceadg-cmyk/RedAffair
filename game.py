import random, sys, os, textwrap

sfx_queue = None
cheat_unlimited_cuffs = False
cheat_god_mode = False
cheat_infinite_countenance = False

def play_game():
    RED = '\033[31m'
    BLACK_BG = '\033[40m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    GRAY = '\033[90m'

    TOTAL_NON_MISLEADING = 21 

    def clear_screen():
        print("##CLEARSCREEN##")

    def get_first_name(full_name):
        return full_name.split()[0]

    clear_screen()
    print(RED + BLACK_BG + BOLD +
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
        "Somewhere in this fluorescent flickering palisade of sin, a killer waits."
    + RESET)
    print()
    input("Press Enter to begin...")
    clear_screen()

    player_name = input(f"{RED}{BLACK_BG}Your name, detective, if you subscribe to such niceties: {RESET}").strip()
    if not player_name:
        player_name = "Myla-Dean"
    print(f"\n{RED}{BLACK_BG}The name's {player_name}. Licensed to poke around in other people's misery.\n")
    print(f"The universe doesn't care. But you should, and here you are.{RESET}\n")

    LEANINGS = ["communist", "fascist", "liberal", "anarchist",
                "communist", "fascist", "liberal"]
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
        "janitor": shuffled_leans[3],
        "cook": shuffled_leans[4],
        "patron": shuffled_leans[5],
        RESERVED_KEY_THX1138: shuffled_leans[6]
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
        ),
        "janitor": "Elliot Luka sweeps the floor with the resigned air of a man who knows that Sisyphus is content, if only because he is Sisyphus. His stained speedsuit and calloused hands speak of endless circuits against invasive pathogens, pests, and careless spills. He rarely speaks, but his eyes flick toward every sound. He's squirrely, yet composed enough that most wouldn't notice. You do.",
        "cook": "Adeline Malovega stands over the carbon steel griddle, eyes locked a thousand miles through the cook-top beyond the floor. The murder has shut down her kitchen and, apparently, her mind. Tattoos flow around her forearms past her biceps into unique sleeves, the true meaning of which only she would know. Her hair is up in a bun with a hairnet wrapped around her brow and lips that twitch as she breaks her catatonia to notice you.",
        "patron": "Alexander Hemlock sits in the corner booth, a cup of cold black coffee before him. His hands tremble, but his eyes are sharp – possibly nerves, possibly a neurodisease. He’s been here since before the murder, and the staff treat him like furniture; not a beautiful armoire, but a living‑room coffee table that’s never seen a coaster and is as replaceable as it is functional."
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
        },
        "janitor": {
            "name": "Elliot Luka",
            "alive": True, "hostile": False, "detained": False, "defeated": False,
            "hp": 25,
            "motive": "The victim accused him of stealing a valuable ring. He was written up, his pay docked, and spent his next several days searching for it, even on his day off, even after everyone assumed he was merely pretending to look.",
            "guilty": False,
            "lean": suspect_leans["janitor"],
            "characteristics": ["quiet", "observant", "nervous", "diligent"],
            "curses": ["cheese dick", "pig bitch", "evolved yeast infection", "bureaucratic non-entity", "nosey fucking freak"],
            "exonerated": False
        },
        "cook": {
            "name": "Adeline Malovega",
            "alive": True, "hostile": False, "detained": False, "defeated": False,
            "hp": 25,
            "motive": "The victim was her landlord, often demanding rent when she ate, sometimes three weeks in a row. Some people just can't stand a leech. Can you relate?",
            "guilty": False,
            "lean": suspect_leans["cook"],
            "characteristics": ["reliable", "frenetic", "avoidant", "unpredictable"],
            "curses": ["Mr. Jerk", "death-jockey", "short-order disappointment", "needle-dick double bitch", "space-pig"],
            "exonerated": False
        },
        "patron": {
            "name": "Alexander Hemlock",
            "alive": True, "hostile": False, "detained": False, "defeated": False,
            "hp": 25,
            "motive": "He has none, but his whereabouts are unaccounted for by anyone else but him. He claims to have used the bathroom just before the incident, but others claim they didn't see him actually walk that direction, but instead out the front door.",
            "guilty": False,
            "lean": suspect_leans["patron"],
            "characteristics": ["forgetful", "blasé", "lonely", "old-fashioned"],
            "curses": ["pussywillow", "cuck", "achey half-dead punk", "idiot child", "gun sucking piss sniffing shitheel"],
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
        "elliot": "janitor",
        "luka": "janitor",
        "elliot luka": "janitor",
        "adeline": "cook",
        "malovega": "cook",
        "adeline malovega": "cook",
        "alex": "patron",
        "alexander": "patron",
        "hemlock": "patron",
        "alexander hemlock": "patron",
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
        "janitor": "calculating",
        "cook": "frenetic",
        "patron": "unusual",
        RESERVED_KEY_THX1138: None
    }

    # -- Dynamic expansions --
    freezer_unlocked = False
    freezer_cleaver_found = False
    bathroom_panel_revealed = False
    revolver_found = False
    bullet_found_in_office = False
    label_taken = False

    locations = {
        "counter": {
            "desc": (
                "THE COUNTER – A scratched carbonite slab that's seen more elbows than a\n"
                "gala dance floor with Fred Astaire and Bob Fosse. The cash register is smashed open, PCB, chits, change, and Valerian Draughma spilled across the floor like so many things have been over the years, leaving a sticky film beneath your shoes.\n"
                "The entrance is sealed with a field of plasma that hums something like a funeral dirge. Maybe you're imagining that last bit, but visually, audibly, and tactically if you must, you do know the field is there.\n\n"
                + suspect_descriptions["marcus"] + "\n\n" + suspect_descriptions["janitor"]
            ),
            "items": [],
            "suspects": ["marcus", "janitor"],
            "searchable": ["aiden_alibi", "luka_alibi"]
        },
        "dining": {
            "desc": (
                "THE DINING AREA – Booths line the walls placed in opposition with a white table between them, and the walls undecorated except for the art deco murals that fill the otherwise unremarkable space; one to each wall. Upholstered in synthleather and what was once blue vinyl, they are now\n"
                "faded and cracking across every surface except one patch now the color of dried blood and and what was once, presumably, someone's personality. Napkins, sauce, seasoning, and marmalade are strewn across one tabletop, the rest being various gradations of clean, none of which seem hygienic. The jukebox is stuck on a single song – an avant garde noise album, now academically classical hundreds of years later and light-years away, but it vibrates your fillings.\n\n"
                + suspect_descriptions["napoleon"] + "\n\n" + suspect_descriptions["patron"]
            ),
            "items": [],
            "suspects": ["napoleon", "patron"],
            "searchable": ["blake_alibi", "hemlock_missing"],
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
                + suspect_descriptions["cleopatra"] + "\n\n" + suspect_descriptions["cook"] +
                "\nA corkboard hangs beside the back door, pinned with old schedules, a faded menu, and a flier."
            ),
            "items": ["candlestick", "label"],
            "suspects": ["cleopatra", "cook"],
            "searchable": ["alice_alibi", "adeline_timestamps"],
            "examinables": ["corkboard", "freezer"]
        },
        "office": {
            "desc": (
                "THE BACK OFFICE – A cramped drywall cage full of stale smoke and broken promises of raises, promotions, and staff openings. "
                "A torn sheet of paper flutters near the desk.\n\n"
                + suspect_descriptions[RESERVED_KEY_THX1138]
            ),
            "items": ["poison vial", "ring_or_id"],
            "suspects": [RESERVED_KEY_THX1138],
            "searchable": ["nyx_message"],
            "body_examinable": False,
            "bullet_found": False
        },
        "bathroom": {
            "desc": (
                "THE BATHROOM – A cramped, flicker-lit cubicle. The air smells of cheap disinfectant and stale regret. "
                "The victim lies here. She’s propped against the wall like someone sat her down for a chat she’ll never finish. "
                "A single gunshot wound to the temple – neat, professional, almost polite. "
                "Blood has pooled in the cracks of a linoleum floor that screamed despair long before it became a crime scene."
            ),
            "items": [],
            "suspects": [],
            "searchable": [],
            "body_examinable": True,
            "datachip_found": False
        },
        "freezer": {
            "desc": "FREEZER – A cramped sub-zero storage locker. Frost creeps over plastic crates and a half-empty case of synth-crab.",
            "items": [],
            "suspects": [],
            "searchable": [],
            "body_examinable": False
        }
    }

    ring_or_id = random.choice(["signet ring", "galactic_id"])
    locations["office"]["items"].remove("ring_or_id")
    locations["office"]["items"].append(ring_or_id)

    current_location = "counter"
    inventory = ["notepad"]
    handcuffs = 3
    clues = set()
    body_examined = False
    game_over = False
    traits_revealed = set()
    trust = {}
    nyx_escape_offered = False
    nyx_escaped = False
    corruption_planted = None
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
        RESERVED_KEY_THX1138: ["nyx_aiden_resented", "nyx_alice_promoted_over_victim", "nyx_victim_didnt_want_return"],
        "janitor": ["luka_says_cook_threatened", "luka_says_patron_was_outside", "luka_says_ring_was_planted"],
        "cook": ["adeline_says_janitor_stole_ring", "adeline_says_alice_argued", "adeline_says_victim_was_armed"],
        "patron": ["hemlock_says_blake_threatened", "hemlock_says_airlock_heard", "hemlock_says_nyx_was_calm"]
    }

    MISLEADING_DIALOGUE = {
        "luka_says_cook_threatened": "'That cook... I heard her say she'd shut Marsha up for good.'",
        "luka_says_patron_was_outside": "'The old man? He went outside right before the shot. I swear I heard the airlock cycle.'",
        "luka_says_ring_was_planted": "'The ring... I think someone else took it, or maybe she lost it. I'm being framed. Marsha was a bitch anyway.'",
        "adeline_says_janitor_stole_ring": "'Elliot? He's been obsessed with that ring. Probably sold it to cover his debts.'",
        "adeline_says_alice_argued": "'Alice and Marsha had a screaming match. Something about a promotion, or a client...I don't really remember.'",
        "adeline_says_victim_was_armed": "'Marsha carried a small knife. She wasn't defenceless. She was ruthless and cruel. I'm not surprised she got got.'",
        "hemlock_says_blake_threatened": "'That short fellow? He was muttering threats under his breath all evening.'",
        "hemlock_says_airlock_heard": "'I heard the airlock hiss. Someone came or went right before the bang.'",
        "hemlock_says_nyx_was_calm": "'Nyx? They were the calmest person in the room when it happened. Suspiciously calm.'",
        "aiden_says_alice_promoted": "'Alice never got the promotion that she wanted. That's motive enough.'",
        "aiden_says_alice_paycheck": "'Alice's paycheck was docked because of Marsha. She was furious. At least, that's how I remember it.'",
        "aiden_says_victim_angry": "'Marsha was angry at everyone. It was only a matter of time. I don't know what it was, but she was in a dark place, and she always made that everyone else's problem too.'",
        "alice_blake_screenshots": "'Blake sent threatening messages to Marsha. I have screenshots. Here, let me send them to you.'",
        "alice_victim_msg_afraid": "'Marsha told me she was scared to be here. I'm not sure why she was here, but she was.'",
        "alice_victim_cant_stay_home": "'Marsha said she couldn't stay in her apartment anymore. Someone was harassing her.'",
        "blake_nyx_bully": "'Nyx bullied Marsha constantly. It was psychological warfare. I don't know if they were together or if Nyx was just holding her hostage.'",
        "blake_nyx_called_out": "'Nyx was called out by Marsha in front of everyone. Humiliated. She didn't react, but we all know she was waiting for the right moment.'",
        "blake_victim_distant": "'Marsha had become distant lately. She knew something was coming. I tried to reach out to her. She just wouldn't let me.'",
        "nyx_aiden_resented": "'Aiden resented Marsha for reporting him to management. He had plenty run-ins with her, and every one was something he'd whine about like a school-girl.'",
        "nyx_alice_promoted_over_victim": "'Alice leapfrogged Marsha for that promotion. She'd waited years for that spot, and she didn't think Alice deserved it.'",
        "nyx_victim_didnt_want_return": "'Marsha didn't want to come back here. She knew it wasn't safe. She just couldn't stay in her apartment either, I'm sure you've heard the rumors, right? How Blake was terrorizing her?'"
    }

    MOTIVE_GOSSIP = {
        "marcus": ("cleopatra", "'I heard that Alice had a breakdown in business negotiations. Something about a hostile takeover that went south.'", "marcus_gossip_cleopatra"),
        "napoleon": ("marcus", "'Aiden? He had personal differences with Marsha over the use of power. I heard he was close to being fired.'", "napoleon_gossip_marcus"),
        "cleopatra": ("napoleon", "'Blake used to date Marsha. Bad breakup. I'm talking the kind that leaves blood on the cutting room floor.'", "cleopatra_gossip_napoleon"),
        "janitor": ("cook", "'That cook... I overheard her saying Marsha was her landlord. Always demanding rent. She called her a leech.'", "janitor_gossip_cook"),
        "cook": ("janitor", "'Elliot? Marsha accused him of stealing a ring. He spent days looking for it, even after everyone thought he was faking.'", "cook_gossip_janitor"),
        "patron": ("thatcher", "'Nyx... Marsha stood up to them once. I mean Marsha, I mean. She didn't back down. Nyx hates being challenged.'", "patron_gossip_thatcher"),
        RESERVED_KEY_THX1138: ("patron", "'Hemlock? He claims he was in the bathroom, but I saw him go out the front door. He's hiding something.'", "nyx_gossip_patron")
    }

    CONFRONT_DIALOGUE = {
        "marcus": "'I... I didn't mean to cause trouble. She just pushed too hard, okay? But that doesn't mean I killed her!'",
        "napoleon": "'Yeah, we dated. So what? It ended badly. That doesn't make me a murderer!'",
        "cleopatra": "'Hostile takeover? Please. My hands are clean. I was on a bus when it happened!'",
        "janitor": "'The ring? I never stole it! She was a liar. I was just trying to find it to clear my name!'",
        "cook": "'So she was my landlord. So what? I didn't kill her over rent. That's insane.'",
        "patron": "'I went to the bathroom. The airlock? I don't know what you're talking about. I'm old, not stupid.'",
        RESERVED_KEY_THX1138: "'You've got nothing. I've been in this office the whole time. Ask anyone who actually matters.'"
    }

    EVIDENCE_DESCRIPTIONS = {
        "aiden_alibi": "Payphone log. Aiden was on a call at time of death.",
        "luka_alibi": "Wet floor sign and pristine sheen near the counter. Elliot's alibi.",
        "blake_alibi": "Time-stamped napkin. Blake's scribblings from all evening.",
        "blake_alibi_confirmed": "Blake's alibi verified via handwriting scan. Consistent.",
        "hemlock_missing": "Old coffee receipt, hours before the murder. Doesn't confirm his whereabouts.",
        "alice_alibi": "Bus ticket stub. Alice arrived just before or after the shot.",
        "alice_alibi_confirmed": "Alice's alibi verified by transit database. Legitimate ticket.",
        "adeline_timestamps": "Stock bucket label with timestamped order docket. Adeline's alibi.",
        "adeline_alibi_confirmed": "Adeline's alibi verified by freezer logs. She was in the freezer at time of death.",
        "nyx_message": "Torn paper. Nyx's handwriting. An angry letter to the victim.",
        "unknown_revolver": "A revolver, recently fired. The murder weapon.",
        "aiden_footprint": "Tracks outside the back porthole. Too big to be Aiden's.",
        "blake_witness": "Someone with strong posture left the office after the bang.",
        "alice_witness": "Loud argument from the office. Nyx and the victim.",
        "luka_swept": "Someone walked towards the office with a determined stride.",
        "adeline_heard": "Loud argument from the office. A woman's voice and someone calm.",
        "hemlock_yelling": "Heated yelling near the office. Words were unclear.",
        "cook_landlord": "Adeline revealed the victim was her landlord.",
        "marcus_gossip_cleopatra": "Aiden says Alice had a breakdown in business negotiations.",
        "napoleon_gossip_marcus": "Blake says Aiden had personal differences with the victim over power.",
        "cleopatra_gossip_napoleon": "Alice says Blake and the victim had a bad breakup.",
        "janitor_gossip_cook": "Elliot says Adeline's landlord was the victim, always demanding rent.",
        "cook_gossip_janitor": "Adeline says Elliot was accused of stealing a ring and searched for days.",
        "patron_gossip_thatcher": "Hemlock says Nyx was challenged by the victim and hates being defied.",
        "nyx_gossip_patron": "Nyx says Hemlock went out the front door, not the bathroom.",
        "aiden_says_alice_promoted": "Aiden claims Alice never got the promotion she wanted.",
        "aiden_says_alice_paycheck": "Aiden says Alice's paycheck was docked because of Marsha.",
        "aiden_says_victim_angry": "Aiden says Marsha was angry at everyone.",
        "alice_blake_screenshots": "Alice claims Blake sent threatening messages to Marsha.",
        "alice_victim_msg_afraid": "Alice says Marsha was scared to be here.",
        "alice_victim_cant_stay_home": "Alice says Marsha couldn't stay in her apartment.",
        "blake_nyx_bully": "Blake says Nyx bullied Marsha constantly.",
        "blake_nyx_called_out": "Blake says Nyx was humiliated by Marsha publicly.",
        "blake_victim_distant": "Blake says Marsha had become distant lately.",
        "nyx_aiden_resented": "Nyx says Aiden resented Marsha for reporting him.",
        "nyx_alice_promoted_over_victim": "Nyx says Alice leapfrogged Marsha for a promotion.",
        "nyx_victim_didnt_want_return": "Nyx says Marsha didn't want to come back.",
        "luka_says_cook_threatened": "Elliot says Adeline threatened to shut Marsha up.",
        "luka_says_patron_was_outside": "Elliot says Hemlock went outside right before the shot.",
        "luka_says_ring_was_planted": "Elliot says the ring was planted to frame him.",
        "adeline_says_janitor_stole_ring": "Adeline says Elliot stole the ring.",
        "adeline_says_alice_argued": "Adeline says Alice and Marsha had a screaming match.",
        "adeline_says_victim_was_armed": "Adeline says Marsha carried a knife.",
        "hemlock_says_blake_threatened": "Hemlock says Blake was muttering threats.",
        "hemlock_says_airlock_heard": "Hemlock says he heard the airlock hiss.",
        "hemlock_says_nyx_was_calm": "Hemlock says Nyx was suspiciously calm.",
        "bullet_casing": "A spent bullet casing found in the office. Matches the revolver calibre.",
        "datachip": "A datachip from a loose panel in the bathroom. Contains encrypted communications.",
        "bloody_cleaver": "A bloody cleaver in the freezer. A grisly red herring.",
        "cleaver_analysis": "Scanner shows the blood is lab-meat juice, not human.",
    }

    # -- Evidence implication/exoneration labels --
    EVIDENCE_IMPLICATION = {
        "aiden_alibi": (["Unknown"], ["Aiden"]),
        "luka_alibi": (["Unknown"], ["Elliot"]),
        "blake_alibi": (["Unknown"], ["Blake"]),
        "blake_alibi_confirmed": (["Unknown"], ["Blake"]),
        "hemlock_missing": (["Unknown"], ["Alexander"]),
        "alice_alibi": (["Unknown"], ["Alice"]),
        "alice_alibi_confirmed": (["Unknown"], ["Alice"]),
        "adeline_timestamps": (["Unknown"], ["Adeline"]),
        "adeline_alibi_confirmed": (["Unknown"], ["Adeline"]),
        "nyx_message": (["Nyx"], []),
        "unknown_revolver": (["Nyx", "Unknown"], []),
        "aiden_footprint": (["Unknown"], ["Aiden"]),
        "blake_witness": (["Nyx"], []),
        "alice_witness": (["Nyx"], []),
        "luka_swept": (["Nyx"], []),
        "adeline_heard": (["Nyx"], []),
        "hemlock_yelling": (["Nyx"], []),
        "cook_landlord": (["Adeline"], []),
        "marcus_gossip_cleopatra": (["Alice"], []),
        "napoleon_gossip_marcus": (["Aiden"], []),
        "cleopatra_gossip_napoleon": (["Blake"], []),
        "janitor_gossip_cook": (["Adeline"], []),
        "cook_gossip_janitor": (["Elliot"], []),
        "patron_gossip_thatcher": (["Nyx"], []),
        "nyx_gossip_patron": (["Alexander"], []),
        "aiden_says_alice_promoted": (["Alice"], []),
        "aiden_says_alice_paycheck": (["Alice"], []),
        "aiden_says_victim_angry": (["Unknown"], []),
        "alice_blake_screenshots": (["Blake"], []),
        "alice_victim_msg_afraid": (["Unknown"], []),
        "alice_victim_cant_stay_home": (["Unknown"], []),
        "blake_nyx_bully": (["Nyx"], []),
        "blake_nyx_called_out": (["Nyx"], []),
        "blake_victim_distant": (["Unknown"], []),
        "nyx_aiden_resented": (["Aiden"], []),
        "nyx_alice_promoted_over_victim": (["Alice"], []),
        "nyx_victim_didnt_want_return": (["Unknown"], []),
        "luka_says_cook_threatened": (["Adeline"], []),
        "luka_says_patron_was_outside": (["Alexander"], []),
        "luka_says_ring_was_planted": (["Elliot"], []),
        "adeline_says_janitor_stole_ring": (["Elliot"], []),
        "adeline_says_alice_argued": (["Alice"], []),
        "adeline_says_victim_was_armed": (["Unknown"], []),
        "hemlock_says_blake_threatened": (["Blake"], []),
        "hemlock_says_airlock_heard": (["Unknown"], []),
        "hemlock_says_nyx_was_calm": (["Nyx"], []),
        "bullet_casing": (["Nyx"], []),
        "datachip": (["Nyx"], []),
        "bloody_cleaver": (["Unknown"], []),
        "cleaver_analysis": (["Unknown"], []),
    }

    # -- Evidence aliases (including merged meta-clues) --
    EVIDENCE_ALIASES = {
        "payphone log": "aiden_alibi", "phone log": "aiden_alibi", "log": "aiden_alibi", "payphone": "aiden_alibi", "p log": "aiden_alibi",
        "wet floor sign": "luka_alibi", "floor sign": "luka_alibi", "sheen": "luka_alibi", "wet floor": "luka_alibi",
        "time-stamped napkin": "blake_alibi", "napkin": "blake_alibi", "blake's napkin": "blake_alibi",
        "blake confirmed": "blake_alibi_confirmed",
        "coffee receipt": "hemlock_missing", "receipt": "hemlock_missing", "old receipt": "hemlock_missing",
        "bus ticket stub": "alice_alibi", "ticket stub": "alice_alibi", "bus ticket": "alice_alibi", "ticket": "alice_alibi", "bus stub": "alice_alibi", "b ticket": "alice_alibi", "bts": "alice_alibi",
        "alice confirmed": "alice_alibi_confirmed",
        "stock bucket": "adeline_timestamps", "order docket": "adeline_timestamps", "docket": "adeline_timestamps", "label": "adeline_timestamps",
        "adeline's alibi confirmed": "adeline_alibi_confirmed", "freezer log": "adeline_alibi_confirmed",
        "torn paper": "nyx_message", "nyx's letter": "nyx_message", "letter": "nyx_message",
        "revolver": "unknown_revolver", "gun": "unknown_revolver", "weapon": "unknown_revolver",
        "footprint": "aiden_footprint", "tracks": "aiden_footprint", "outside tracks": "aiden_footprint",
        "strong posture witness": "blake_witness", "posture witness": "blake_witness",
        "argument witness": "alice_witness", "argument": "alice_witness",
        "determined stride": "luka_swept", "stride": "luka_swept",
        "adeline heard": "adeline_heard", "woman's voice": "adeline_heard",
        "hemlock yelling": "hemlock_yelling", "yelling": "hemlock_yelling",
        "landlord motive": "cook_landlord", "landlord": "cook_landlord",
        "bullet casing": "bullet_casing", "casing": "bullet_casing",
        "datachip": "datachip", "chip": "datachip",
        "bloody cleaver": "bloody_cleaver", "cleaver": "bloody_cleaver",
        "cleaver analysis": "cleaver_analysis",

        # Merged gossip aliases
        "alice's motive": ["aiden_says_alice_promoted", "nyx_alice_promoted_over_victim"],
        "alice's paycheck": ["aiden_says_alice_paycheck"],
        "marsha's anger": ["aiden_says_victim_angry"],
        "blake screenshots": ["alice_blake_screenshots"],
        "marsha scared": ["alice_victim_msg_afraid"],
        "marsha left apartment": ["alice_victim_cant_stay_home"],
        "nyx bullying": ["blake_nyx_bully"],
        "nyx called out": ["blake_nyx_called_out"],
        "marsha and blake distant": ["blake_victim_distant"],
        "aiden resented marsha": ["nyx_aiden_resented"],
        "marsha didn't want return": ["nyx_victim_didnt_want_return"],
        "cook threatened": ["luka_says_cook_threatened"],
        "patron outside": ["luka_says_patron_was_outside"],
        "ring planted": ["luka_says_ring_was_planted"],
        "janitor stole ring": ["adeline_says_janitor_stole_ring"],
        "alice argued": ["adeline_says_alice_argued"],
        "marsha armed": ["adeline_says_victim_was_armed"],
        "blake threatened": ["hemlock_says_blake_threatened"],
        "airlock heard": ["hemlock_says_airlock_heard"],
        "nyx calm": ["hemlock_says_nyx_was_calm"],
    }

    # -- Evidence verification lines (scanner/database flavor) --
    EVIDENCE_VERIFY = {
        "aiden_alibi": "You scan the payphone log. Seconds later you get a ping, and unsurprisingly it is a real log. Why anyone would fake a payphone log, or more to the point, how, you don't know, but it never hurts to be careful.",
        "luka_alibi": None,
        "blake_alibi": "You scan the napkin and upload it to the handwriting database. Moments later, you get a confirmation that it is in fact Blake's handwriting. This is definitely his work, although you still can't verify the timestamp.",
        "blake_alibi_confirmed": "Blake's alibi holds up under scrutiny. The handwriting matches and the timeline is plausible.",
        "hemlock_missing": "You know a diner receipt when you see it, although that still doesn't account for Hemlock's whereabouts.",
        "alice_alibi": "You scan the bus ticket. Instantly, you get a ping confirming the legitimacy. It's definitely an officially issued ticket. Although, it never hurts to be careful.",
        "alice_alibi_confirmed": "The transit database confirms Alice was on that bus. Her alibi is airtight.",
        "adeline_timestamps": "You scan the label and compare it to the handwriting database. It's definitely a match for Adeline.",
        "adeline_alibi_confirmed": "Freezer logs confirm Adeline was inside at the time of death. She's exonerated.",
        "nyx_message": "You scan the letter fragment. Unfortunately, the database isn't able to get enough of the message to fully confirm or deny the match to Nyx. You'll have to think on this.",
        "unknown_revolver": "You scan the weapon for fingerprints, but nothing shows up. Curiously, not even the gunshot residue that normally accompanies a fired weapon is present. It's been thoroughly cleaned, probably by the killer.",
        "aiden_footprint": "You squint your eyes. There isn't much you can do from this side of the door, and you aren't equipped to go for a space-walk. You'll have to think on this.",
        "blake_witness": None,
        "alice_witness": None,
        "luka_swept": None,
        "adeline_heard": None,
        "hemlock_yelling": None,
        "cook_landlord": None,
        "marcus_gossip_cleopatra": None,
        "napoleon_gossip_marcus": None,
        "cleopatra_gossip_napoleon": None,
        "janitor_gossip_cook": None,
        "cook_gossip_janitor": None,
        "patron_gossip_thatcher": None,
        "nyx_gossip_patron": None,
        "aiden_says_alice_promoted": None,
        "aiden_says_alice_paycheck": None,
        "aiden_says_victim_angry": None,
        "alice_blake_screenshots": None,
        "alice_victim_msg_afraid": None,
        "alice_victim_cant_stay_home": None,
        "blake_nyx_bully": None,
        "blake_nyx_called_out": None,
        "blake_victim_distant": None,
        "nyx_aiden_resented": None,
        "nyx_alice_promoted_over_victim": None,
        "nyx_victim_didnt_want_return": None,
        "luka_says_cook_threatened": None,
        "luka_says_patron_was_outside": None,
        "luka_says_ring_was_planted": None,
        "adeline_says_janitor_stole_ring": None,
        "adeline_says_alice_argued": None,
        "adeline_says_victim_was_armed": None,
        "hemlock_says_blake_threatened": None,
        "hemlock_says_airlock_heard": None,
        "hemlock_says_nyx_was_calm": None,
        "bullet_casing": "You open the revolver, pull out the casing, and drop it into the slot. It's a perfect fit. This bullet was definitely fired from this gun. That much is obvious.",
        "datachip": "You plug the chip into your scanner and wait for the data to transfer. A few seconds later a notification appears:\n\"ENCRYPTED DATA\"\nYou select the option to decrypt. There's no telling when, or even if, this will finish anytime soon. You put everything away and take a deep breath. Just as your hands return to your sides, you hear a ping and pull your scanner back out of your pocket to see the screen\nEst. Decryption: 13h47m18s\nWell, that's not good. You'll have to figure something else out after all.",
        "bloody_cleaver": "You scan the cleaver, first for DNA then for prints. The prints match Adeline. She definitely handled it.",
        "cleaver_analysis": "Further analysis confirms the blood is lab‑meat juice, not human. Adeline's story checks out.",
    }

    # -- Tamper/plant actions --
    TAMPER_ACTIONS = {
        "aiden_alibi": ("destroy", "You tear up the payphone log and drop it into the trash. Who cares? Not you."),
        "luka_alibi": ("destroy", "You drag your shoes across the floor leaving streaks. The floor is no longer clean. Maybe it was never clean."),
        "blake_alibi": ("destroy", "You tear the napkin to shreds and toss it into the trash. It's not like it'll make a difference. You're the one who makes the difference."),
        "hemlock_missing": ("destroy", "You snap open your lighter and flick. Holding the receipt over the flame causes it to flash into a puff of smoke. It's not like it was that important anyway."),
        "alice_alibi": ("destroy", "You snap open your lighter and flick the wheel. The ticket-stub burns to a crispy carbon finish and its ashes scatter across the diner. Who cares?"),
        "adeline_timestamps": ("destroy", "You wipe the bucket with a wet rag. The label dissolves almost instantly. It's like it was never there."),
        "adeline_alibi_confirmed": ("destroy", "You tear the sheet into tiny pieces and stuff them into your pocket. As far as you're concerned, there never was a log sheet."),
        "nyx_message": ("destroy", "You eat the scrap of paper quickly, swallowing with some difficulty, but you get it down. The only way to get it back would require cops to do the one thing they never do: truly investigate one of their own."),
        "unknown_revolver": ("plant", "You plant the revolver on {suspect} carefully and quietly. Whenever the police drone gets here, it'll be they who goes down for it."),
        "bullet_casing": ("plant", "You plant the spent round on {suspect}. It may not be enough, but it's something. You just need a conviction, not necessarily justice."),
        "bloody_cleaver": ("plant", "You plant the cleaver on {suspect}. It may not be enough, but it's something. After all, you only need a conviction, not necessarily justice."),
        "datachip": ("destroy", "You smash the data chip on the ground beneath your heel. Pieces scatter in every direction. If it wasn't unusable before, it sure as shit is now."),
        "alice_blake_screenshots": ("destroy", "You delete the screenshots. It's not like you cared about any of that drama anyway."),
    }

    def evidence_display_name(clue_id):
        return EVIDENCE_DESCRIPTIONS.get(clue_id, clue_id).split('.')[0].strip()

    def is_misleading(clue_id):
        for v in MISLEADING_CLUES.values():
            if clue_id in v:
                return True
        return False

    def hud():
        print(RED + BLACK_BG + "╔══ HUD ═══════════════════════════════════════════╗")
        print(f"║ Location: {current_location.ljust(8)}  Cuffs: {handcuffs}/3    HP: {player['hp']}/{player['max_hp']}   ║")
        print(f"║ Evidence: {len(clues)}/{TOTAL_NON_MISLEADING}                            ║")
        print("╚══════════════════════════════════════════════════╝" + RESET)

    def add_evidence(ev_id):
        if ev_id not in clues:
            clues.add(ev_id)
            print(f"{RED}📋 Evidence: {evidence_display_name(ev_id)} ({len(clues)}/{TOTAL_NON_MISLEADING}){RESET}")
            player["xp"] += 1
            if player["xp"] >= player["xp_to_next"]:
                level_up()

    def remove_evidence(ev_id):
        if ev_id in clues:
            clues.remove(ev_id)
            print(f"{RED}📋 Evidence lost: {evidence_display_name(ev_id)} ({len(clues)}/{TOTAL_NON_MISLEADING}){RESET}")

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
        if sfx_queue: sfx_queue.put('lvlup')

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
        if current_location == "office":
            if bullet_found_in_office:
                desc += "\nA spent bullet casing glints under the desk."
        if current_location == "bathroom" and body_examined:
            desc += "\nThe body remains, patient as only the dead can be."
            if bathroom_panel_revealed:
                desc += "\nA loose panel behind the toilet hints at secrets."
        sus_keys = loc.get("suspects", [])
        for sus_key in sus_keys:
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
        print(desc)

    def move(direction):
        nonlocal current_location
        if direction == "freezer":
            if not freezer_unlocked:
                print("The freezer door is locked tight. Maybe there's a reason to check in here...")
                return
        if direction in locations:
            current_location = direction
            clear_screen()
            hud()
            describe_location()
        else:
            print("Not a room. Try: counter, dining, kitchen, office, bathroom, freezer.")

    def search():
        nonlocal revolver_found, bullet_found_in_office, bathroom_panel_revealed, freezer_unlocked, freezer_cleaver_found, label_taken
        loc = locations[current_location]
        if current_location == "dining" and loc.get("hidden_revolver") and not revolver_found:
            revolver_found = True
            inventory.append("revolver")
            print("In Plain View: cold metal made for someone with even colder blood; a revolver. It's definitely recently fired – the barrel still whispers gunpowder to anyone who will pay attention.")
            add_evidence("unknown_revolver")
            return
        if current_location == "office" and revolver_found and not bullet_found_in_office:
            bullet_found_in_office = True
            print("A spent bullet casing, half hidden beneath the desk. It matches the revolver's calibre.")
            add_evidence("bullet_casing")
            return
        if current_location == "bathroom" and bathroom_panel_revealed and not locations["bathroom"]["datachip_found"]:
            locations["bathroom"]["datachip_found"] = True
            print("You pry open the loose panel. Inside: a datachip, cold and unmarked.")
            add_evidence("datachip")
            inventory.append("datachip")
            return
        if current_location == "freezer":
            if not freezer_cleaver_found and "cook_landlord" in talk_history:
                freezer_cleaver_found = True
                print("Buried under synth-crab: a cleaver stained with something dark and ominous.")
                add_evidence("bloody_cleaver")
                return
            elif "adeline_timestamps" in clues and "adeline_alibi_confirmed" not in clues:
                add_evidence("adeline_alibi_confirmed")
                print("A log sheet on the freezer door confirms Adeline was inside at the time of the murder. Solid alibi.")
                return
        if current_location == "counter" and "aiden_alibi" not in clues:
            print("Payphone log. Aiden was on a call at time of death. It's hard to be in two places at once, but you've seen stranger things.")
            add_evidence("aiden_alibi")
            trust_change("marcus", 1)
            return
        if current_location == "counter" and "luka_alibi" not in clues:
            print("A wet floor sign and a pristine sheen near the counter. Elliot's work, no doubt.")
            add_evidence("luka_alibi")
            trust_change("janitor", 1)
            return
        if current_location == "dining" and "blake_alibi" not in clues:
            print("Time-stamped napkin. Blake's scribblings. He was here all evening writing some sort of...polemic? Seems pretty unlikely he's your man.")
            add_evidence("blake_alibi")
            trust_change("napoleon", 1)
            return
        if current_location == "dining" and "hemlock_missing" not in clues:
            print("An old coffee receipt. The timestamp is hours before the murder, but it doesn't confirm his whereabouts during.")
            add_evidence("hemlock_missing")
            trust_change("patron", 1)
            return
        if current_location == "kitchen" and "alice_alibi" not in clues:
            print("Bus ticket stub. The schedule readout on your personal device confirms Alice would have arrived just before the shot, maybe even just after. Well, that dog just don't hunt.")
            add_evidence("alice_alibi")
            trust_change("cleopatra", 1)
            return
        if current_location == "kitchen" and "adeline_timestamps" not in clues:
            print("A stock bucket with a timestamped order docket. Adeline's alibi checks out, at least on the surface.")
            add_evidence("adeline_timestamps")
            trust_change("cook", 1)
            freezer_unlocked = True
            print("Adeline hands you the freezer key. 'Here, have a look if you want.'")
            return
        if current_location == "office" and "nyx_message" not in clues:
            inventory.append("torn thesis")
            add_evidence("nyx_message")
            print(f"Torn paper. {suspects[RESERVED_KEY_THX1138]['name']}'s handwriting. Hard to make out... clearly an angry letter preceded by at least a couple more.")
            return
        print("Nothing. Nothing worth mentioning anyway, just grease, despair, and the miasma of mystery.")

    def examine(item):
        nonlocal body_examined, bathroom_panel_revealed
        if item == "body" and current_location == "bathroom":
            if not body_examined:
                body_examined = True
                print("The victim appears to be between the ages of 25 and 30. Feminine. Clothes are in tact, the wallet is in hand. From the look of it, it doesn't seem it ever left her fist. She's approximately 5 feet tall. Her makeup is done, smeared only from the blood. For a brief moment, you wonder what foundation she used. You've only ever heard of makeup smudging in old films.\n\nThe victim's face: mild surprise. Death wasn't so much terrifying as much as it was rude. Between the eyes is a bullet wound: neat, centered, professional even. Someone knew what they were doing.")
            else:
                print("The body remains. It hasn't changed. Corpses rarely do.")
                if not bathroom_panel_revealed and trust["janitor"] >= 3:
                    bathroom_panel_revealed = True
                    print("You notice something new: a loose panel behind the toilet. The janitor must have mentioned it.")
            return
        if item == "corkboard" and current_location == "kitchen":
            print("The corkboard is a collage of fading schedules, a yellowed menu, and a crisp flier for 'Reyes Properties'. The same name as on the victim's ID, if you've seen it.")
            if "galactic_id" in inventory or "signet ring" in inventory:
                print("The connection clicks: the victim owned the complex where Adeline lives.")
            return
        if item == "freezer" and current_location == "kitchen":
            if freezer_unlocked:
                print("The walk-in freezer hums softly. You can now enter it properly. Try 'go freezer'.")
            else:
                print("The walk-in freezer door is locked. You'd need a reason to open it.")
            return
        if item in ["signet ring", "galactic_id"] and item in locations[current_location]["items"]:
            if item == "signet ring":
                print("A heavy silver ring, engraved with the initials E.R. It feels cold and important.")
            else:
                print("The ID reads 'E. Reyes' with a photo of the victim. The address lists a building complex owned by a shell company.")
            inventory.append(item)
            locations[current_location]["items"].remove(item)
            return
        if item == "poison vial" and item in locations[current_location]["items"]:
            print("A small vial of clear liquid. It smells faintly of almonds. Cyanide, maybe. Or just bad coffee syrup.")
            inventory.append(item)
            locations[current_location]["items"].remove(item)
            return
        if item == "notepad":
            show_notepad()
            return

        # Evidence lookup via aliases
        ev_id = EVIDENCE_ALIASES.get(item.lower())
        if ev_id is None:
            if item in EVIDENCE_DESCRIPTIONS:
                ev_id = item
        if ev_id:
            desc = EVIDENCE_DESCRIPTIONS.get(ev_id, "No description.")
            impl, exon = EVIDENCE_IMPLICATION.get(ev_id, (["Unknown"], []))
            impl_str = ", ".join(impl) if impl else "None"
            exon_str = ", ".join(exon) if exon else "None"
            print(f"{desc}\nImplicates: {impl_str}\nExonerates: {exon_str}")
            verify = EVIDENCE_VERIFY.get(ev_id)
            if verify is not None:
                print(verify)
                # Auto-add confirmed alibis if scanner verifies them
                if ev_id == "blake_alibi" and "blake_alibi_confirmed" not in clues:
                    add_evidence("blake_alibi_confirmed")
                if ev_id == "alice_alibi" and "alice_alibi_confirmed" not in clues:
                    add_evidence("alice_alibi_confirmed")
            return
        print(f"You give the {item} a good look over. It's definitely a {item}. What were you expecting?")

    def show_notepad():
        if not clues:
            print("The notepad is empty. Nothing to review yet.")
        else:
            print("─── NOTEPAD ───")
            # Group by meta-clue for display
            shown_meta = set()
            for c in sorted(clues):
                # find meta key if this is a sub-clue
                meta = None
                for alias, ids in EVIDENCE_ALIASES.items():
                    if isinstance(ids, list) and c in ids:
                        meta = alias
                        break
                if meta:
                    if meta not in shown_meta:
                        shown_meta.add(meta)
                        name = meta
                        sources = [evidence_display_name(sc) for sc in ids if sc in clues]
                        combined_desc = f"  • {name}  [Sources: {', '.join(sources)}]"
                        if any(is_misleading(sc) for sc in ids):
                            combined_desc = f"  {GRAY}• {name} (suspicious)  [Sources: {', '.join(sources)}]{RESET}"
                        print(combined_desc)
                else:
                    name = evidence_display_name(c)
                    impl, exon = EVIDENCE_IMPLICATION.get(c, (["Unknown"], []))
                    impl_str = ", ".join(impl) if impl else "None"
                    exon_str = ", ".join(exon) if exon else "None"
                    line = f"  • {name}  [Implicates: {impl_str}; Exonerates: {exon_str}]"
                    if is_misleading(c):
                        line = f"  {GRAY}• {name} (suspicious)  [Implicates: {impl_str}; Exonerates: {exon_str}]{RESET}"
                    print(line)
            print("───────────────")

    def take(item):
        loc = locations[current_location]
        if item == "label" and "label" in loc["items"]:
            loc["items"].remove("label")
            inventory.append("label")
            print("You peel the label off the container. Hopefully, Adeline won't notice. She seems harmless, but if she isn't, she's truly unstable.")
            return
        if item in loc["items"]:
            loc["items"].remove(item)
            inventory.append(item)
            print(f"Pocketed: {item}. Maybe you can find some use for it, or just a keep it as a souvenir of this...establishment.")
            if sfx_queue: sfx_queue.put('take')
        else:
            print("It's not here. Maybe it was never here. Maybe nothing is.")

    def talk(sus):
        nonlocal nyx_escape_offered, freezer_unlocked
        if not sus:
            print("Who did you want to talk to? Try: Aiden, Blake, Alice, Nyx, Elliot, Adeline, Alexander (or their last names).")
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' is not a person here. Try: Aiden Adams, Blake Jughashvili, Alice Oliverae, Nyx Singénero, Elliot Luka, Adeline Malovega, Alexander Hemlock.")
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
        loc_suspects = locations[current_location].get("suspects", [])
        if sus not in loc_suspects:
            print(f"{get_first_name(s['name'])} isn't here. Space is big. This diner is small. Try the right room.")
            return

        print(f"\n{RED}You approach {get_first_name(s['name'])}. The air shifts.{RESET}")
        print(f"Trust: {trust[sus]}/3 | Lean: {s['lean']}")
        if trust[sus] == 3 and revealed_characteristic[sus] not in traits_revealed:
            reveal_characteristic(sus)

        if sus == "cook" and trust[sus] >= 2:
            if "cook_landlord" not in talk_history:
                talk_history["cook_landlord"] = True
                print(f"{get_first_name(s['name'])} suddenly blurts out: 'Marsha... she was my landlord. Always hounding me for rent. Can you believe it?'")
                freezer_unlocked = True

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
            if sus == "janitor" and "luka_swept" not in clues:
                options.append("the floor")
            if sus == "cook" and "adeline_heard" not in clues:
                options.append("the office")
            if sus == "patron" and "hemlock_yelling" not in clues:
                options.append("the noise")

            gossip_clue = None
            for speaker, (target, _, clue_id) in MOTIVE_GOSSIP.items():
                if target == sus and clue_id in clues:
                    gossip_clue = clue_id
                    break
            if gossip_clue:
                options.append(f"confront {get_first_name(suspects[sus]['name'])}")

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

            if talk_key in talk_history and topic != f"confront {get_first_name(suspects[sus]['name'])}":
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
                elif sus == "janitor":
                    print("'I was mopping the floor by the counter the whole time. I always do the bathrooms thrice a day; morning, after lunch rush, closing. Check the floor, see the sheen? Notice the wet floor sign. It’s still up.'")
                    if "luka_alibi" not in clues:
                        add_evidence("luka_alibi")
                        trust_change("janitor", 1)
                elif sus == "cook":
                    print("'I was prepping vegetables when the shit hit the fan. The stock bucket label is all time‑stamped. Please, take the label and check it out. Alice and I were chatting after she finished her call.'")
                    freezer_unlocked = True
                    print("She hands you the freezer key.")
                    if "adeline_timestamps" not in clues:
                        add_evidence("adeline_timestamps")
                        trust_change("cook", 1)
                elif sus == "patron":
                    print("'I’ve been sitting here all evening. The staff can confirm I never left this booth except to drain the old lead pipe.'")
                    if "hemlock_missing" not in clues:
                        add_evidence("hemlock_missing")
                        trust_change("patron", 1)
                elif sus == RESERVED_KEY_THX1138:
                    print(f"'Working. Office. Alone. Is that a crime?' *Muttering '{curse}' under breath. Syntharette twitching.")
            elif topic == "motive":
                if sus in MOTIVE_GOSSIP:
                    target, gossip_text, clue_id = MOTIVE_GOSSIP[sus]
                    print(f"{get_first_name(suspects[sus]['name'])} leans in: {gossip_text}")
                    if clue_id not in clues:
                        add_evidence(clue_id)
                    trust_change(sus, 1)
                else:
                    print(f"{get_first_name(suspects[sus]['name'])} stays silent on that topic.")
            elif topic == "the torn paper":
                print(f"{get_first_name(s['name'])} glances at the scrap. 'Mine. Obviously. I'm not sure what you expect to do with it, detective.'")
                if sus == RESERVED_KEY_THX1138:
                    print(f"They snatch it back before you can put it away. '{curse}!'")
                    trust_change(sus, -1)
                    if "torn thesis" in inventory:
                        inventory.remove("torn thesis")
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
                print(f"'I heard loud voices from the office. {suspects[RESERVED_KEY_THX1138]['name']} and Marsha. Nothing civil about it, but then, when are *they* ever civil? '")
                add_evidence("alice_witness")
                trust_change("cleopatra", 1)
            elif topic == "the floor" and sus == "janitor":
                print("'Someone walked towards the office with a determined stride. Strong, purposeful. Not a casual stroll.'")
                add_evidence("luka_swept")
                trust_change("janitor", 1)
            elif topic == "the office" and sus == "cook":
                print("'I heard a loud argument from the office. A woman’s voice, and someone responding calmly. Chilling.'")
                add_evidence("adeline_heard")
                trust_change("cook", 1)
            elif topic == "the noise" and sus == "patron":
                print("'There was yelling near the office. I couldn’t make out the words, but it was heated.'")
                add_evidence("hemlock_yelling")
                trust_change("patron", 1)
            elif topic.startswith("confront "):
                if sus in CONFRONT_DIALOGUE:
                    print(f"{get_first_name(suspects[sus]['name'])} stares at you: {CONFRONT_DIALOGUE[sus]}")
                    trust_change(sus, -1)
                else:
                    print("They just stare at you, unmoved.")

    def threaten(sus):
        if not sus:
            print("Who are you trying to intimidate?")
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' doesn't match any suspect. Try: Aiden, Blake, Alice, Nyx, Elliot, Adeline, Alexander.")
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
        loc_suspects = locations[current_location].get("suspects", [])
        if sus not in loc_suspects:
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
        elif sus == "janitor":
            print(f"He stammers. 'Okay! Okay! I saw {suspects[RESERVED_KEY_THX1138]['name']} go into the office just before it happened. Please don't hurt me!'")
            trust_change("janitor", 1)
        elif sus == "cook":
            print("She stares through you. 'Threats? In my kitchen? You're either brave or stupid.' She doesn't break, but you see a flicker of fear.")
        elif sus == "patron":
            print("He chuckles. 'Son, I've been threatened by people twice your size and half your nerve. You'll need to do better.'")
        elif sus == RESERVED_KEY_THX1138:
            print(f"Their face hardens into something between complete disdain and total disregard. 'No proof, no case, no hope, detective.' They seem much more hostile now. Congratulations.")
            s["hostile"] = True

    def detain(sus):
        nonlocal handcuffs
        if not cheat_unlimited_cuffs and handcuffs <= 0:
            print("You reach for your cuffs and find no more.")
            return
        if not sus:
            print("Cuff whom?")
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' isn't a suspect. Try: Aiden, Blake, Alice, Nyx, Elliot, Adeline, Alexander.")
            return
        s = suspects[sus]
        if s["exonerated"]:
            print("They've been cleared. You'd be arresting an innocent person – wait, you've done that before.")
            return
        if not s["alive"] or s["defeated"] or s["detained"]:
            print("You've already detained this one. Another set of cuffs would be redundant, don't you think?")
            return
        loc_suspects = locations[current_location].get("suspects", [])
        if sus not in loc_suspects:
            print("They're not in here and ain't telekinetic. Not yet, anyway.")
            return
        if not cheat_unlimited_cuffs:
            handcuffs -= 1
        s["detained"] = True
        remaining = "∞" if cheat_unlimited_cuffs else handcuffs
        print(f"Click-click-click-click. {get_first_name(s['name'])} now sports a used set of state-issued jewelry. {remaining} remaining.")
        if sfx_queue: sfx_queue.put('cuffs')

    def fight(sus):
        if not sus:
            print("Fight who? The existential void?")
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' isn't a suspect. Try: Aiden, Blake, Alice, Nyx, Elliot, Adeline, Alexander.")
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
        loc_suspects = locations[current_location].get("suspects", [])
        if sus not in loc_suspects:
            print("Shadowboxing. Very existential. Very pointless.")
            return
        curse = random.choice(s["curses"]) if s["curses"] else ""
        print(f"\n{RED}⚔ The air is electric. You and {get_first_name(s['name'])} circle the area like binary stars on a collision course. There may yet be another murder. At least it'll be easy to solve.{RESET}")
        if sfx_queue: sfx_queue.put('fight')
        while player["hp"] > 0 and s["hp"] > 0:
            if cheat_god_mode:
                player["hp"] = player["max_hp"]
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
                if sfx_queue: sfx_queue.put('hit')
            elif act == "2":
                roll = random.random()
                if roll < player["special_hit_chance"]:
                    dmg_float = player["base_damage"] * 1.25
                    dmg = int(round(dmg_float))
                    s["hp"] -= dmg
                    print(f"Lucky break, detective. You land a devastating blow! {dmg} damage.")
                    if sfx_queue: sfx_queue.put('hit')
                elif roll < player["special_hit_chance"] + player["regular_hit_chance"]:
                    dmg = int(round(player["base_damage"]))
                    s["hp"] -= dmg
                    print(f"Wild-eyed, but effective. Be careful, detective. {dmg} damage.")
                    if sfx_queue: sfx_queue.put('hit')
                else:
                    print("Your swing goes wide! No damage.")
                    if sfx_queue: sfx_queue.put('miss')
            else:
                print("Indecision could cost your life. No damage.")
            if s["hp"] <= 0:
                s["hp"] = 0
                s["defeated"] = True
                print(f"{get_first_name(s['name'])} collapses, eyes rolled back and lips muttering '{curse}' before their animus fades.")
                check_total_carnage()
                return
            edmg = random.randint(3, 6)
            if cheat_god_mode:
                edmg = 0
            player["hp"] -= edmg
            print(f"{get_first_name(s['name'])} strikes back. {edmg} damage. You see murder in their eyes.")
            if player["hp"] <= 0:
                player["hp"] = 0
                print("Darkness rolls over you. The void encompasses your vision bit by bit. Somewhere, a jukebox plays your funeral dirge, and no one realizes it. Game over, detective.")
                if sfx_queue: sfx_queue.put('gameover')
                sys.exit(0)

    def check_total_carnage():
        if all(suspects[k]["defeated"] for k in suspects):
            ending_carnage()

    def tamper(item, suspect=None):
        nonlocal corruption_planted
        # Determine if item is an alias or direct ID
        ev_id = EVIDENCE_ALIASES.get(item.lower())
        if ev_id is None:
            if item in EVIDENCE_DESCRIPTIONS:
                ev_id = item
        if ev_id is None or ev_id not in TAMPER_ACTIONS:
            print("That item can't be tampered with.")
            return
        action_type, msg = TAMPER_ACTIONS[ev_id]
        if action_type == "destroy":
            if ev_id in clues:
                remove_evidence(ev_id)
            else:
                print("You don't have that evidence.")
                return
            print(msg)
        elif action_type == "plant":
            if not suspect:
                print("You need to specify a suspect to plant on. Use 'tamper revolver on Alice'")
                return
            resolved = resolve_suspect(suspect)
            if not resolved:
                print("Invalid suspect.")
                return
            # Remove item from inventory if present, or mark as planted
            if ev_id == "unknown_revolver" and "revolver" in inventory:
                inventory.remove("revolver")
            elif ev_id == "bullet_casing" and "bullet_casing" not in inventory:
                print("You don't have the bullet casing.")
                return
            elif ev_id == "bloody_cleaver" and "bloody_cleaver" not in inventory:
                print("You don't have the cleaver.")
                return
            # Set corruption planted
            corruption_planted = resolved
            print(msg.format(suspect=get_first_name(suspects[resolved]['name'])))

    def accuse(sus):
        nonlocal handcuffs, corruption_planted
        if not sus:
            print("Accuse who? Make up your mind, detective.")
            return
        if sus.startswith("tamper "):
            parts = sus[7:].split(" on ")
            if len(parts) == 2 and parts[1].strip():
                tamper(parts[0].strip(), parts[1].strip())
            else:
                tamper(parts[0].strip())
            return
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print(f"'{sus}' doesn't match anyone. Try: Aiden, Blake, Alice, Nyx, Elliot, Adeline, Alexander.")
            return
        if sfx_queue: sfx_queue.put('accuse')
        if sus == "cook" and not suspects["cook"]["exonerated"] and not suspects["cook"]["detained"] and not suspects["cook"]["defeated"]:
            print("Adeline's eyes widen. 'You think it was me? No, no, no...' She bolts for the back door!")
            print("She escapes into the void before you can react. The case just got harder.")
            suspects["cook"]["alive"] = False
            suspects["cook"]["escaped"] = True
            return
        if nyx_escaped and corruption_planted and sus == corruption_planted:
            corruption_ending()
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
            if cheat_unlimited_cuffs or handcuffs > 0:
                if not cheat_unlimited_cuffs:
                    handcuffs -= 1
                suspects[RESERVED_KEY_THX1138]["detained"] = True
                rem = "∞" if cheat_unlimited_cuffs else handcuffs
                print(f"You slap the cuffs on {get_first_name(suspects[RESERVED_KEY_THX1138]['name'])}. {rem} remaining. Justice never tasted so bloody and sweet. Good job, detective. They're sure to tell stories of this one at the station.")
            else:
                print("You don't have any cuffs left, but they're out cold. The police drone will handle it. Probably. You light a smoke and watch over them making sure they're still breathing ready to issue another state-sanctioned beat-down if necessary.")
            ending_correct()
        elif suspects[RESERVED_KEY_THX1138]["defeated"] and suspects[RESERVED_KEY_THX1138]["detained"]:
            ending_correct()
        else:
            print("They slip your grasp and bolt out the door like greased lightning. The airlock cycles. By the time you reach it, they're a silhouette against the stars. You'll never catch up to them, and may never find them again. It's a 24 carat run of bad luck, or maybe just bad decision making gilded with pyrite excuses.")
            ending_fail()

    def secret_ending():
        nonlocal game_over
        if sfx_queue: sfx_queue.put('gameover')
        print(f"\nWrong accusation. You made the wrong bet. Very wrong.")
        print(f"Behind you: a soft click. You spin. {get_first_name(suspects[RESERVED_KEY_THX1138]['name'])}, one wrist free, working on the other.")
        print(f"'Did you really think these standard restraints could hold me?' They smile. The predator turns prey, but it dawns on you they're damn good at being either.")
        print(f"'Entertaining, {player_name}. Truly. But I have a schedule to keep, and you have a new problem to explain.'")
        print("They're gone before you can move. The airlock cycles. Moments later the police drone arrives to an empty office and a restaurant full of fools. Too bad, detective. They'll definitely tell this story although you'd certainly wish they wouldn't.")
        print(f"\n{RED}GAME OVER{RESET}")
        game_over = True
        sys.exit(0)

    def nyx_escape_ending():
        nonlocal nyx_escaped
        print("Nyx parts their lips once more to reveal their toxic solvent-based smile. Their eyes flash the recognition that's only ever shared between two predators in league with each other. You immediately begin to consider how you'll spin this to the police drone. But perhaps there's another way...")
        nyx_escaped = True
        suspects[RESERVED_KEY_THX1138]["alive"] = False
        suspects[RESERVED_KEY_THX1138]["exonerated"] = False
        print("Nyx vanishes through the back office. The airlock cycles. You're alone with the mess and a choice.")
        print("You can plant the revolver on someone and accuse them to close the case. Dirty, but effective.")

    def corruption_ending():
        nonlocal game_over
        if sfx_queue: sfx_queue.put('gameover')
        print(f"You plant the revolver and make your accusation. The frame holds. The police drone accepts your report without question.")
        print("A dirty cop ending. Justice is served cold, and you're the one holding the freezer door open.")
        print(f"{RED}GAME OVER – CORRUPTION ENDING{RESET}")
        game_over = True
        sys.exit(0)

    def ending_correct():
        nonlocal game_over
        if sfx_queue: sfx_queue.put('jaildoor')
        k = suspects[RESERVED_KEY_THX1138]
        print(f"\n{RED}Everything clicks into place. The whole crooked design.{RESET}")
        print(f"'{get_first_name(k['name'])}, in the office, with the revolver. Marsha Stone killed in cold blood. For ego? For fun? For the oldest reason there ever was: because you could.'")
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
        nonlocal game_over
        if sfx_queue: sfx_queue.put('gameover')
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
        nonlocal game_over
        if sfx_queue: sfx_queue.put('gameover')
        print("You look back across the bar. Everyone's dead. Dead folk tell no tales, but there's sure to be plenty living who watch your live-streamed execution. The detective who went completely mad and committed mass murder. Good job, I guess, detective. Maybe you'll solve a case in the next life.\n\nGAME OVER")
        game_over = True
        sys.exit(0)

    def countenance():
        nonlocal countenance_used, handcuffs, required_incriminating
        if not cheat_infinite_countenance and countenance_used:
            print("You've already called upon your Countenance. The moment has passed.")
            return
        countenance_used = True

        if player_lean == "liberal":
            sus_keys = locations[current_location].get("suspects", [])
            valid_sus = None
            for key in sus_keys:
                if not suspects[key]["exonerated"] and trust[key] >= 3:
                    valid_sus = key
                    break
            if not valid_sus:
                print("The required trust isn't there. The moment fades, wasted.")
                return
            print("You flash a fat stack of credits, multiple denominations, multiple forms of currency, all tied together with a rubber band. You ask, gently, with this new tool of persuasion.")
            s = suspects[valid_sus]
            print(f"{get_first_name(s['name'])} spills everything they know about another patron. The evidence is bought and paid for, but cash quantity doesn't always mean product quality.")
            for ev in MISLEADING_CLUES.get(valid_sus, []):
                add_evidence(ev)
                dialogue = MISLEADING_DIALOGUE.get(ev, f"'{ev}'")
                print(f"   {get_first_name(s['name'])} says: {dialogue}")
        elif player_lean == "fascist":
            sus_keys = locations[current_location].get("suspects", [])
            valid_sus = None
            for key in sus_keys:
                if not suspects[key]["exonerated"]:
                    valid_sus = key
                    break
            if not valid_sus:
                print("Nobody here to interrogate. The Countenance fizzles uselessly.")
                return
            s = suspects[valid_sus]
            if s["exonerated"]:
                print("They've been exonerated. No point.")
                return
            print("You flash your badge and strike the federal salute pose. Their visage softens greatly as you threaten to throw them, their family, and anyone they've ever loved into a deep dark mine with no escape, benefits, or unions to speak of.")
            if valid_sus != RESERVED_KEY_THX1138:
                others = [k for k in suspects if k != valid_sus and k != RESERVED_KEY_THX1138]
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
                "cleopatra": ["alice_alibi", "alice_witness"],
                "janitor": ["luka_alibi", "luka_swept"],
                "cook": ["adeline_timestamps", "adeline_heard"],
                "patron": ["hemlock_missing", "hemlock_yelling"]
            }
            for clue in prefixes.get(chosen, []):
                if clue in clues:
                    remove_evidence(clue)
                    if clue in incriminating:
                        required_incriminating = max(0, required_incriminating - 1)
                        print(f"(Required incriminating evidence now {required_incriminating})")
        else:
            print("Your Countenance manifests in an unexpected way. Nothing happens.")
        if cheat_infinite_countenance:
            countenance_used = False

    def show_inventory():
        ev_list = '\n'.join(f' - {evidence_display_name(e)}' for e in sorted(clues)) if clues else "You've got nothing. The void stares back. Don't blink."
        print(f"Inventory: {', '.join(inventory) if inventory else 'empty pockets'}\nCuffs: {handcuffs}/3\nHP: {player['hp']}/{player['max_hp']}\n\nEvidence ({len(clues)}/{TOTAL_NON_MISLEADING}):\n{ev_list}")

    # -- Theory command --
    def theory(sus):
        resolved = resolve_suspect(sus)
        if resolved:
            sus = resolved
        if sus not in suspects:
            print("Unknown suspect for theory.")
            return
        s = suspects[sus]
        name = get_first_name(s['name'])
        print(f"{name}.")
        # Motives
        if sus in MOTIVE_GOSSIP:
            target, gossip_text, _ = MOTIVE_GOSSIP[sus]
            print(f"Known motives: {s['motive']} (Also: {gossip_text})")
        else:
            print(f"Known motives: {s['motive']}")
        # Evidence for/against
        evidence_for = []
        evidence_against = []
        for ev_id in clues:
            if ev_id in EVIDENCE_IMPLICATION:
                impl, exon = EVIDENCE_IMPLICATION[ev_id]
                if name in impl:
                    evidence_for.append(evidence_display_name(ev_id))
                if name in exon:
                    evidence_against.append(evidence_display_name(ev_id))
        print(f"Evidence for {name}: {', '.join(evidence_for) if evidence_for else 'none'}")
        print(f"Evidence against {name}: {', '.join(evidence_against) if evidence_against else 'none'}")
        # Alibi
        alibi_map = {
            "marcus": "aiden_alibi",
            "napoleon": "blake_alibi",
            "cleopatra": "alice_alibi",
            "janitor": "luka_alibi",
            "cook": "adeline_timestamps",
            "patron": "hemlock_missing",
            RESERVED_KEY_THX1138: None
        }
        alibi_id = alibi_map.get(sus)
        if alibi_id and alibi_id in clues and not is_misleading(alibi_id):
            print("Alibi: Yes")
        elif alibi_id is None:
            print("Alibi: None presented")
        else:
            print("Alibi: No")

    EASTER_EGG_PHRASE = "Im an existentialist-absurdist-gnostic-agnostic-secular-true path unitarian-marxist-leninist-maoist multi-level marketer."

    shortcuts = {
        'g': 'go', 'l': 'look', 's': 'search', 'e': 'examine', 't': 'talk',
        'th': 'threaten', 'd': 'detain', 'f': 'fight', 'a': 'accuse',
        'i': 'inventory', 'inv': 'inventory', 'h': 'help', '?': 'help',
        'q': 'quit', 'x': 'examine', 'c': 'countenance', 'r': 'read',
        'v': 'theory', 'tamper': 'tamper'
    }

    def expand_command(raw):
        raw = raw.strip()
        if not raw:
            return None
        if raw.lower() == EASTER_EGG_PHRASE.lower():
            print("You realize once today is over, tomorrow will never come. Red will fade to black, and you will wake up in another reality, as another person, and this experience may never truly grow roots and flourish in your psyche. You will simply move onto the next life.")
            return None
        parts = raw.split()
        first = parts[0].lower()
        if first in shortcuts:
            shortcut = shortcuts[first]
            if shortcut == 'go':
                return f"go {' '.join(parts[1:])}" if len(parts) > 1 else "go"
            elif shortcut == 'talk':
                return f"talk {' '.join(parts[1:])}" if len(parts) > 1 else "talk"
            elif shortcut == 'threaten':
                return f"threaten {' '.join(parts[1:])}" if len(parts) > 1 else "threaten"
            elif shortcut == 'detain':
                return f"detain {' '.join(parts[1:])}" if len(parts) > 1 else "detain"
            elif shortcut == 'fight':
                return f"fight {' '.join(parts[1:])}" if len(parts) > 1 else "fight"
            elif shortcut == 'accuse':
                return f"accuse {' '.join(parts[1:])}" if len(parts) > 1 else "accuse"
            elif shortcut == 'examine':
                return f"examine {' '.join(parts[1:])}" if len(parts) > 1 else "examine"
            elif shortcut == 'look':
                return "look"
            elif shortcut == 'search':
                return "search"
            elif shortcut == 'inventory':
                return "inventory"
            elif shortcut == 'help':
                return "help"
            elif shortcut == 'quit':
                return "quit"
            elif shortcut == 'countenance':
                return "countenance"
            elif shortcut == 'read':
                return "read notepad"
            elif shortcut == 'theory':
                return f"theory {' '.join(parts[1:])}" if len(parts) > 1 else "theory"
            elif shortcut == 'tamper':
                return f"tamper {' '.join(parts[1:])}" if len(parts) > 1 else "tamper"
        return raw

    def help_text():
        print("""
Commands (shortcut):
  go <place>       (g)  – move between rooms (includes freezer if unlocked)
  look             (l)  – survey current location
  search           (s)  – rummage for hidden clues
  examine <obj>    (e/x)– inspect something closely
  take <item>           – pocket an item (including label)
  talk <suspect>   (t)  – interrogate a patron
  threaten <suspect>(th)– apply pressure (may backfire)
  detain <suspect> (d)  – apply handcuffs (3 pairs, or unlimited with cheat)
  fight <suspect>  (f)  – resort to violence
  accuse <suspect> (a)  – point the finger
  tamper <item> on <suspect> – plant evidence
  tamper <item>         – destroy evidence
  theory <suspect> (v)  – summarise suspect
  inventory        (i)  – check pockets and evidence
  countenance      (c)  – use your political ability
  help             (h/?)– this list
  quit             (q)  – abandon the case
  read notepad     (r)  – review collected evidence (grouped, with implications)
Rooms: counter, dining, kitchen, office, bathroom, freezer (after unlocking)
Suspects: Aiden Adams, Blake Jughashvili, Alice Oliverae, Nyx Singénero,
          Elliot Luka, Adeline Malovega, Alexander Hemlock
          (use first name, last name, or full name)
""")

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
        elif verb == "read":
            show_notepad()
        elif verb == "theory":
            theory(noun)
        elif verb == "tamper":
            accuse(f"tamper {noun}")
        else:
            print("Unrecognized command. This must be your first homicide detail. Type 'help' or 'h' for assistance.")

if __name__ == "__main__":
    play_game()