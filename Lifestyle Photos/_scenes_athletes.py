"""
Athlon Rub - Set A: 12 athlete lifestyle photographs, no product in frame.

Deliberately spread across combat, field, court, endurance, strength and
artistic sport so the set covers the brand's whole "all-sports" claim, and
across body types, ages, genders and ethnicities so it reads as a real roster
rather than one model in twelve outfits.

Each scene names: who, what they are doing, where, and what the camera is
doing. Nothing else - the style blocks in _style.py carry the look.

CLIENT DIRECTION APPLIED
------------------------
- Facilities are CLEAN and WELL KEPT. The first pass read as derelict
  warehouses and condemned gyms; these athletes train in properly maintained
  rings, halls and courts. Street and outdoor settings still appear (running,
  cycling, the neighbourhood basketball court) but they are in good repair.
- Swimming was dropped. A water sport is the wrong read for a topical oil,
  so A10 is now indoor volleyball, which keeps the court coverage.
"""

ATHLETES = [
    {
        "id": "A01",
        "slug": "muay-thai-knee",
        "scene": (
            "A woman in her late twenties, lean and heavily muscled through the "
            "shoulders and obliques, training Muay Thai. She is mid-knee strike "
            "into a heavy bag, one hand clamped on the bag, her weight fully "
            "committed and her rear heel lifted. Cotton hand wraps, ankle "
            "supports, sports bra and Thai shorts, all soaked through. Her hair "
            "is tied back and coming loose. A well-run Muay Thai gym in good "
            "condition: clean rubber matting, a properly maintained ring behind "
            "her with taut red ropes and clean white canvas, neat rows of "
            "hanging bags, sound walls, good light. Camera is low and close on "
            "her right side, focus locked on her face and the line of her ribs; "
            "the bag and the ring go soft."
        ),
    },
    {
        "id": "A02",
        "slug": "boxer-ropes",
        "scene": (
            "A Black male boxer in his early thirties, welterweight build, "
            "between rounds. He is leaning back into the corner ropes with both "
            "arms slung over them, chest heaving, mouth open, head tipped back "
            "and eyes closed. Hands still taped with white gauze, damp at the "
            "knuckles. Sweat sheets down his chest and drips off his chin onto "
            "the canvas. A clean, well-run boxing club behind him: taut white "
            "ring canvas underfoot, evenly wrapped ropes, neat rows of hanging "
            "bags, a corner stool. Camera is outside the ropes at his eye level, "
            "one rope crossing low through the frame slightly out of focus; his "
            "face is the only sharp thing in the picture."
        ),
    },
    {
        "id": "A03",
        "slug": "soccer-slide",
        "scene": (
            "A young Latino soccer player, wiry and quick, sliding into a tackle "
            "on a soaked pitch under floodlights at night. His trailing leg "
            "carves a spray of water and torn grass into the air, jersey pulled "
            "sideways, both hands out for balance, jaw set. Studded boots caked "
            "in mud, shin guards showing above the socks. A well-kept floodlit "
            "pitch: even grass, crisp white markings, a modern stand reduced to "
            "a soft dark band behind. Camera is at pitch level, panning with "
            "him, so the grass in the foreground streaks and his face and "
            "shoulders stay sharp."
        ),
    },
    {
        "id": "A04",
        "slug": "gymnast-bars",
        "scene": (
            "A 16-year-old female artistic gymnast, small and compact at about "
            "150 cm with very developed shoulders and lats, swinging under the "
            "high bar of a set of uneven bars. Both hands are locked in leather "
            "dowel grips on the bar, arms straight overhead, body in a long "
            "straight hollow line with legs together and toes pointed, swinging "
            "through the bottom of the arc, chalk dust puffing off the bar. She "
            "wears a plain long-sleeved competition leotard, and chalk is caked "
            "into her palms, wrists and the front of it. Unmistakably a modern, "
            "well-kept gymnastics hall: the LOW BAR of the same apparatus "
            "clearly visible below and behind her, the tensioned guy cables "
            "running down to the floor, a blue foam pit and neatly stacked crash "
            "mats. Camera is below and to the side looking up, focus on her "
            "hands and face."
        ),
    },
    {
        "id": "A05",
        "slug": "sprinter-blocks",
        "scene": (
            "A muscular male sprinter in the SET position in metal starting "
            "blocks on a synthetic running track at first light. The blocks are "
            "clearly visible: an aluminium rail bolted to the track with two "
            "angled foot pedals, both of his spiked feet braced hard into them, "
            "rear knee off the ground. Hips high above his shoulders, arms "
            "locked vertical, fingertips bridged on the white start line, head "
            "down. Plain compression shorts and singlet. Breath visible in the "
            "cold air. He is on a well-kept red-brown eight-lane track with "
            "crisp white lane lines running away behind him and an empty "
            "grandstand soft in the distance. Camera is on the ground in the "
            "next lane, level with his hands, focus on the tendons of his "
            "forearm and the side of his face."
        ),
    },
    {
        "id": "A06",
        "slug": "runner-cold-morning",
        "scene": (
            "A woman in her forties, long-distance runner, mid-stride on a wet "
            "back road on a cold grey morning. Breath steaming, hair pulled back "
            "and damp, a plain long-sleeve top pushed up the forearms, tights, "
            "road shoes throwing a fine mist off the tarmac. Her expression is "
            "inward and working, not performing. Bare trees and low fog reduce "
            "the background to soft grey bands. Camera tracks her from "
            "three-quarters front at hip height, shutter just slow enough that "
            "her trailing foot smears."
        ),
    },
    {
        "id": "A07",
        "slug": "olympic-lift",
        "scene": (
            "An Asian woman in her late twenties, thick through the back and "
            "quads, catching a clean in the bottom of a front squat. Elbows "
            "driven high, bar racked hard across her deltoids, bar whip still "
            "visible, plates flexing. Chalk on her hands, thighs and the front "
            "of her shirt, a leather belt cinched tight, knee sleeves rolled "
            "down. A serious, well-kept strength gym: clean rubber platform, "
            "neatly racked bumper plates, chalk bowl, a rack out of focus "
            "behind. Camera is low and front-on but offset, focus on her face "
            "and the bar across her shoulders."
        ),
    },
    {
        "id": "A08",
        "slug": "bjj-grapple",
        "scene": (
            "Two men grappling in Brazilian jiu-jitsu gis on the mat, both "
            "utterly spent. The one on top is passing guard with a cross-collar "
            "grip, knuckles white in the fabric; the one underneath is framing "
            "with a forearm, face pressed sideways into the mat, eyes hard."
            "Both men are straining, jaws clenched, neither of them calm or"
            "smiling. One wears a white "
            "gi and one a royal blue gi, both unmistakably jiu-jitsu gis - heavy woven cotton jackets with"
            "thick padded lapels, sleeves ending at the wrist and a coloured"
            "belt knotted at the waist - dark with sweat and pulled out of"
            "shape, and the clean mat streaked wet where they have been "
            "rolling. A modern academy in good order: clean unmarked tatami, a "
            "mirrored wall soft in the background. Camera is on the mat itself "
            "at head height a metre away, focus on the top man's grip and the "
            "bottom man's eyes."
        ),
    },
    {
        "id": "A09",
        "slug": "basketball-outdoor",
        "scene": (
            "A tall young man driving baseline on a resurfaced outdoor court at "
            "dusk. He is low, ball pushed out ahead on the dribble, off arm up "
            "to shield, shoulder dropped into contact, sweat flying off his "
            "hairline. Plain reversible tank, long shorts, high-tops gripping "
            "and squealing on the surface. A well-kept neighbourhood court: "
            "proper white net, true rim, freshly painted lines, clean fencing, "
            "and the last orange light on the buildings behind, all soft. "
            "Camera is low on the baseline looking up, focus on his face and the "
            "hand on the ball."
        ),
    },
    {
        "id": "A10",
        "slug": "volleyball-block",
        "scene": (
            "A women's indoor volleyball middle blocker airborne at the top of a block jump, both feet clearly off the"
            "floor and her hands and forearms reaching above the height of the"
            "net tape, arms pressed together and angled over the net, fingers"
            "spread and tensed, eyes tracking the ball, shoulders and calves"
            "loaded. "
            "Knee pads pushed down, jersey riding up, tape on two fingers, sweat "
            "at her hairline and along her forearms. A clean modern sports hall: "
            "pale polished maple floor with crisp painted lines, a taut white "
            "net, a padded post and an empty bank of bleachers soft behind. "
            "Camera is low on the far side of the net looking up along the tape, "
            "focus on her hands and face."
        ),
    },
    {
        "id": "A11",
        "slug": "tennis-clay-serve",
        "scene": (
            "A male tennis player at full extension on a serve on a well-"
            "maintained red clay court in flat afternoon light. Racquet arm "
            "driving up and through, back arched, front foot dragging a small "
            "plume of clay off the baseline, the ball a small hard shape above "
            "him. Clay dust is ground into his socks, shoes and the side of his "
            "shorts, and his shirt is stuck to his back. Freshly swept clay, "
            "crisp white lines, and a clean dark green windscreen and fence as a "
            "soft band behind. Camera is low behind the baseline to one side, "
            "focus on his torso and face."
        ),
    },
    {
        "id": "A12",
        "slug": "cyclist-climb",
        "scene": (
            "A road cyclist out of the saddle grinding up a steep mountain "
            "switchback, bike rocking under him, forearms locked on the hoods, "
            "head down and turned slightly so his face is readable. Jersey "
            "unzipped to the sternum and stuck to his chest, salt crust drying "
            "white at the temples and on the straps, road grit up the calves. "
            "Clean tarmac, a crash barrier and a hazy valley drop away behind "
            "him, all soft. Camera is roadside and low, panning with him, so the "
            "tarmac streaks and his face and hands stay sharp."
        ),
    },
]
