"""
Athlon Rub - Set B: 12 athlete lifestyle photographs with the product in frame.

Same photographic world as Set A. The product is present the way a real bottle
is present on a real shoot - on the bench, in a hand, in the bag - not floated
in like a packshot.

FOUR THINGS CARRY THIS SET
--------------------------
1. SCALE. The commonest way an AI product shot dies is the bottle rendering at
   the wrong size against the human body, and the first pass ran large on every
   SKU. Each spec below therefore carries hard dimensions, a hand anchor, a
   phone anchor AND an explicit instruction to err small, because the model
   reasons about size far better from "a hand around it covers half its height"
   than from millimetres.
2. THE PRODUCT IS AN OIL. Per client direction it is not an aerosol and does
   not atomise: the pump pushes out a slow, dense amber oil that is poured into
   the palm and rubbed into the muscle. No mist, no spray cone, no droplets in
   the air. The OIL block below is what the shots are actually about.
3. LABEL FIDELITY. Told that most of the label should be illegible, the model
   redesigned it outright - round crests, dark labels, invented hierarchy. The
   LABEL block therefore leads with "copy the reference exactly", guards the
   two things it got wrong (the label is white, the crest is a shield), and
   demotes the fine-print note to a closing clause.
4. INTEGRATION. Shared lighting, a grounded contact shadow and real wear. The
   composited-packshot look is the giveaway on product-in-scene, so it is named
   and forbidden - as is the bottle glowing like a lamp, which it did once.

Reference photographs of each SKU are attached to the request as image_input,
so the label is copied rather than invented.
"""

# ---------------------------------------------------------------------------
# SKU specifications. Real dimensions, each paired with body-scale anchors and
# a bias toward rendering small.
# ---------------------------------------------------------------------------
SKU = {
    "100": (
        "THE PRODUCT: a single Athlon Rub 100 ml / 3.4 fl oz bottle, exactly as "
        "in the attached reference photograph. A squat amber-brown translucent "
        "PET bottle with a black pump dispenser and a smoke-tinted clear "
        "over-cap. "
        "SCALE, CRITICAL - THIS IS A SMALL BOTTLE: 135 mm (5.3 inches) tall "
        "including the pump and over-cap, 46 mm (1.8 inches) across. It is "
        "SHORTER THAN A SMARTPHONE. A closed adult hand hides almost all of it, "
        "with only the pump head showing above the index finger. Held against a "
        "forearm it barely reaches past the wrist. "
    ),
    "250": (
        "THE PRODUCT: a single Athlon Rub 250 ml / 8.5 fl oz bottle, exactly as "
        "in the attached reference photograph. A slim amber-brown translucent "
        "PET cylinder with a black pump dispenser and a smoke-tinted clear "
        "over-cap. "
        "SCALE, CRITICAL - THIS IS A MID-SIZE PERSONAL BOTTLE, NOT A LARGE "
        "ONE: 195 mm (7.7 inches) tall including the pump and over-cap, 52 mm "
        "(2 inches) across. About one and a third times the length of a "
        "smartphone. A hand wrapped around its middle covers roughly half its "
        "height and the fingers reach three quarters of the way around. It is "
        "clearly shorter than an adult forearm, and stood beside a boxing glove "
        "it is only a little taller than the glove is long. "
    ),
    "500": (
        "THE PRODUCT: a single Athlon Rub 500 ml / 17 fl oz bottle, exactly as "
        "in the attached reference photograph. An amber-brown translucent "
        "boston-round bottle with a sloping shoulder and a black ribbed screw "
        "cap - no pump on this size. "
        "SCALE: this is the largest of the three, 210 mm (8.3 inches) tall "
        "including the cap and 82 mm (3.2 inches) across the widest part of the "
        "body - a wine-bottle body needing a full hand to wrap around it. Still "
        "a shelf-size bottle, never a salon jug or a gallon container. "
    ),
}

# The failure was one-directional every time, so the correction is too.
SCALE_BIAS = (
    "SIZE ERROR TO AVOID, IMPORTANT: generated product shots consistently "
    "render this bottle TOO LARGE against the body and against the props "
    "around it. Deliberately err on the small side. If the bottle looks "
    "imposing, oversized or hero-scaled next to a hand, a glove, a bench or a "
    "gym bag, it is wrong - shrink it. "
)

# ---------------------------------------------------------------------------
# What actually comes out of the bottle. Client correction: this is an oil.
# ---------------------------------------------------------------------------
OIL = (
    "HOW THE PRODUCT BEHAVES - THIS IS AN OIL, NOT A SPRAY: Athlon Rub is a "
    "dense amber-golden oil, a liquid serum with real body to it, closer to a "
    "warm massage oil than a lotion and nothing like an aerosol. The pump "
    "pushes it out slowly. THERE IS NEVER A SPRAY CONE, NEVER ATOMISED MIST, "
    "NEVER AIRBORNE DROPLETS. "
    "USE VERY LITTLE OIL - THIS IS THE MOST COMMON MISTAKE IN THIS IMAGE. The "
    "dose is small: a coin-sized pool in a cupped palm, no more. By the time "
    "we see the skin it is essentially already rubbed in, and all that remains "
    "is a light satin sheen that follows the shape of the muscle and catches "
    "one soft highlight along the muscle belly, with the surrounding skin "
    "still matte and dry. "
    "Explicitly NOT wanted: a thick syrupy or honey-like slick, a glossy "
    "varnished or laminated coating, a wet-look plastic shine, oil running, "
    "dripping, beading or pooling on a limb, a poured stream in mid-air, or a "
    "whole arm or leg glazed amber. If the skin looks sticky, candied or "
    "shrink-wrapped, there is far too much. "
    "The action shown is always the RUB - pressing and working the oil into "
    "the muscle with the flat of the hand, the heel of the palm or the thumb, "
    "the skin visibly dragging and releasing under the pressure. "
)

# ---------------------------------------------------------------------------
# The label. Copy first, guard second, blur last.
# ---------------------------------------------------------------------------
LABEL = (
    "THE LABEL - HIGHEST PRIORITY IN THIS IMAGE: reproduce the label from the "
    "attached reference photograph exactly. Same artwork, same layout, same "
    "proportions, same hierarchy, same wording, same colours. Do not redesign "
    "it, do not simplify it, do not rearrange it, do not resize its elements "
    "and do not substitute a different mark. "
    "For reference, it is a matte WHITE wrap-around label - it must read as "
    "clean bright white and stay one of the brightest values in the frame, "
    "never grey, cream, dark, tinted or transparent - covering roughly the "
    "middle half of the bottle's height and carrying, top to bottom: "
    "a pointed heraldic SHIELD crest, shield-shaped with a notched crown and a "
    "point at the bottom, never a circle, oval, roundel or round badge, in deep "
    "forest green - clearly green, never black or navy - outlined in gold, with "
    "a gold diagonal band and a gold star across it; "
    "beneath it the wordmark ATHLON in large dark forest-green condensed "
    "capitals, with RUB directly under it, much smaller and letterspaced, "
    "flanked left and right by a thin gold rule; "
    "below that the line ALL - SPORTS RUB in small letterspaced dark green "
    "capitals; below that two short centred lines of tiny type reading "
    "POWERING PERFORMANCE AND RECOVERY; and across the bottom of the label a "
    "dark green and near-black panel carrying three tiny gold icons, a small "
    "gold-outlined badge and the volume marking. "
    "The micro-type inside that bottom panel is genuinely finer than an 85mm "
    "lens resolves at this distance, so let it settle into soft printed "
    "texture rather than inventing words for it - but the shield, ATHLON, RUB "
    "and ALL - SPORTS RUB are crisp, correct and exactly as referenced. "
)

# ---------------------------------------------------------------------------
# Integration. Names the composited-packshot failure mode and forbids it.
# ---------------------------------------------------------------------------
INTEGRATION = (
    "THE BOTTLE IS A REAL OBJECT IN THIS ROOM. It is lit by the same single "
    "window as everything else, so its highlight sits on the same side, its "
    "shadow falls in the same direction and at the same length, and it lays "
    "down a soft grounded contact shadow where it touches the surface. The "
    "amber plastic transmits a little of that light where the source passes "
    "through it, so the liquid reads warm on the lit side and goes almost "
    "black on the shadow side, and the room reflects faintly across its "
    "shoulder. It is never itself a light source: it does not glow from "
    "within, is not internally lit or lamp-like, and casts no light onto the "
    "surfaces around it. "
    "It has been used: fingerprints on the plastic, a slight scuff at the "
    "label edge, a couple of dried amber drips down the side below the pump. "
    "It obeys the same plane of focus as everything else - if it is not the "
    "nearest thing to the lens then it is softly out of focus, never "
    "artificially sharpened. It must not look composited, cut out, floating, "
    "tilted onto a surface it is not touching, or lit by a separate studio "
    "light. "
)

PRODUCT_BRANDING = (
    "The Athlon Rub label is the ONLY text, lettering or branding anywhere in "
    "the frame. All clothing, wraps, gloves, shoes, towels, bags and equipment "
    "are plain and completely unbranded - no other logos, no signage, no "
    "numbers, no watermark, no caption. "
)


PRODUCTS = [
    {
        "id": "B01", "slug": "muaythai-ring-apron", "sku": "250",
        "scene": (
            "A woman in her late twenties in Muay Thai kit, wrapped hands and "
            "ankle supports, sitting on the edge of a clean boxing ring apron "
            "with her legs hanging over, working oil into her own shin and calf "
            "with the heel of her hand, head down and watching what she is "
            "doing, chest still heaving. The Athlon Rub bottle stands upright on "
            "the apron beside her hip, close to the camera and slightly left, "
            "her wraps coiled next to it. A well-kept Muay Thai gym behind: taut "
            "red ropes, clean white canvas, neat rows of bags. Camera is just "
            "below apron height a metre away, focus on the bottle and her near "
            "hand, her face soft behind it."
        ),
    },
    {
        "id": "B02", "slug": "cornerman-oil-shoulder", "sku": "250",
        "scene": (
            "A cornerman's weathered hands working Athlon Rub oil into the "
            "deltoid and upper trapezius of a Black male boxer sitting on a "
            "corner stool between rounds. The cornerman's right palm is pressed "
            "flat and driving down across the muscle, the skin dragging under "
            "it, a light satin sheen worked over the muscle, the skin around it"
            "still matte. His left hand steadies the "
            "boxer's arm, and the open bottle stands on the ring apron just "
            "behind them. The boxer's taped hands rest on his knees, head "
            "forward, breathing hard. A clean, well-run club: taut ropes, neat "
            "bags soft behind. Camera is over the boxer's opposite shoulder, "
            "focus on the cornerman's hand and the oiled deltoid."
        ),
    },
    {
        "id": "B03", "slug": "bench-wraps-gloves", "sku": "250",
        "scene": (
            "A quiet still life on a clean, solid wooden gym bench: the Athlon "
            "Rub bottle standing upright, a pair of plain unbranded leather "
            "boxing gloves slumped beside it, a neatly rolled coil of cotton "
            "hand wraps, a folded towel and a skipping rope. The bottle is only "
            "a little taller than a glove is long - keep that relationship "
            "exact. Everything sits in soft window light with shadows running "
            "away to the right. Twelve feet behind, an athlete works a bag in a "
            "clean, well-equipped gym, reduced to a dark moving shape. Camera is "
            "at bench height, close, focus on the label and the nearest glove, "
            "the athlete far out of focus."
        ),
    },
    {
        "id": "B04", "slug": "runner-curb-calf", "sku": "100",
        "scene": (
            "A woman in her forties, a distance runner, sitting on a kerb at the "
            "end of a wet road session with one leg extended, both thumbs "
            "pressed into her calf working oil down the muscle, her head bent to "
            "watch. The calf carries only a faint sheen where the oil has been worked"
            "in, the skin above and below it matte. The small Athlon Rub bottle stands on the kerb "
            "beside her hip, its pump head just clearing her fingers when she "
            "reaches for it - it is a small bottle, shorter than a phone. Damp "
            "hair pulled back, long-sleeve top pushed up the forearms, road "
            "shoes, breath still visible. Wet tarmac and bare trees soft behind. "
            "Camera is on the road at kerb level, focus on her hands and calf, "
            "her face soft above."
        ),
    },
    {
        "id": "B05", "slug": "soccer-hamstring-touchline", "sku": "250",
        "scene": (
            "A young Latino soccer player lying back on the grass at the "
            "touchline after a match, one knee raised, while a physio's oiled "
            "hands press and glide along his hamstring, the muscle moving under the pressure and the skin carrying only a"
            "faint satin sheen. His kit is "
            "soaked and grass-stained, socks pushed down. The Athlon Rub bottle "
            "stands upright in the grass in the near foreground beside the "
            "physio's kneeling shin, blades of grass crossing its base, standing "
            "no taller than the physio's hand is long. A well-kept floodlit "
            "pitch falls away soft behind. Camera is on the ground a metre from "
            "the bottle, focus on the bottle and the physio's hands."
        ),
    },
    {
        "id": "B06", "slug": "gymnast-chalk-floor", "sku": "100",
        "scene": (
            "A 16-year-old gymnast sitting on the floor of a clean modern "
            "training hall next to the chalk bowl, working the last of the oil into her wrist and forearm with her"
            "opposite thumb, the skin dragging under it and only a faint sheen"
            "left. "
            "The small Athlon Rub bottle stands upright on the floor beside her "
            "knee, a film of chalk dust on its shoulder, next to a pair of "
            "leather dowel grips and a roll of tape - it is small, no taller "
            "than her hand is long. Her palms are chalked and callused. Uneven "
            "bars, neatly stacked mats and a blue foam pit soft behind under "
            "high window light. Camera is on the floor at her level, focus on "
            "the bottle and her hands."
        ),
    },
    {
        "id": "B07", "slug": "lifter-oil-palm", "sku": "250",
        "scene": (
            "An Asian woman in her late twenties, a weightlifter, standing on a "
            "clean rubber platform with the Athlon Rub bottle held in her "
            "chalked left hand and her right palm cupped beneath the pump, a "
            "thick amber bead of oil landing in the hollow of her palm and "
            "starting to spread. She is looking down at her palm, not at the "
            "camera. Chalk prints transfer onto the amber plastic where her "
            "fingers wrap it, and her hand covers about half the bottle's "
            "height. A leather belt, knee sleeves rolled down, shirt dark with "
            "sweat. A loaded barbell rests on the platform behind her, plates "
            "and rack falling soft. Camera is chest height just off-axis, focus "
            "on the bottle and her cupped palm."
        ),
    },
    {
        "id": "B08", "slug": "open-gym-bag", "sku": "100",
        "scene": (
            "An open canvas gym duffel on a clean locker-room bench, seen from "
            "just above and to the side, its contents spilling: the small Athlon "
            "Rub bottle lying on its side half out of the bag with its label "
            "rolled toward the camera so the wordmark reads upright and the "
            "right way round, a coiled skipping rope, a roll of athletic tape, "
            "balled-up hand wraps and a folded towel. The bottle is short - it "
            "spans only about a third of the bag's opening. A solid wooden "
            "bench, clean lockers behind, a soft band of window light across the "
            "bag. Camera is close and handheld looking down at about 40 degrees, "
            "focus on the bottle label, the far end of the bag soft."
        ),
    },
    {
        "id": "B09", "slug": "therapy-table-quad", "sku": "500",
        "scene": (
            "A sports therapist's oiled forearms driving down the quadriceps of "
            "an athlete lying face-up on a clean treatment table in a bright, "
            "well-kept therapy room. The skin visibly drags and releases under the pressure and the"
            "thigh carries a light even sheen, not a gloss. The "
            "large Athlon Rub bottle stands on a small steel trolley in the near "
            "foreground with a folded white towel, its black screw cap off and "
            "resting beside it, a little oil pooled at the neck. Clean tiled "
            "wall and cabinetry soft behind. Camera is at table height beside "
            "the trolley, focus on the bottle and the therapist's forearms."
        ),
    },
    {
        "id": "B10", "slug": "basketball-courtside", "sku": "250",
        "scene": (
            "A tall young basketball player sitting forward on the courtside "
            "bench of a clean modern indoor gym, elbows on knees, working oil "
            "into the front of his thigh with the heel of his hand, jersey dark "
            "with sweat, a towel over his shoulder. The Athlon Rub bottle stands "
            "on the bench slats beside his hip in the near foreground, upright, "
            "reaching only to about mid-shin on him where he sits. Pale polished "
            "maple floor with crisp painted lines, a hoop and empty bleachers "
            "soft behind. Camera is at bench height a half metre from the "
            "bottle, focus on the bottle and his working hand, his face soft."
        ),
    },
    {
        "id": "B11", "slug": "cyclist-post-ride-bench", "sku": "100",
        "scene": (
            "A road cyclist sitting sideways on a bench just off the road at the "
            "end of a long climb, one leg up on the seat, one hand pressing the oil down the length of his calf, which"
            "carries only a faint sheen. The small Athlon Rub bottle stands on "
            "the bench slats beside his helmet and mitts, small enough that the "
            "helmet dwarfs it. Jersey unzipped to the sternum and stuck to his "
            "chest, salt dried white at his temples, road grit up his calves. "
            "His bike leans out of focus against the bench end, hazy valley "
            "beyond. Camera is at bench height a half metre from the bottle, "
            "focus on the bottle and his working hand."
        ),
    },
    {
        "id": "B12", "slug": "forearm-rub-macro", "sku": "250",
        "scene": (
            "A tight close-up of an athlete working Athlon Rub oil into their "
            "own forearm. The far hand's thumb is pressed hard into the muscle "
            "and drawing along it, the skin bunching ahead of the thumb and the oil already spread into a thin satin sheen that follows the"
            "shape of the flexors and catches a single soft highlight, with no"
            "visible liquid sitting on the skin. The forearm fills the lower third "
            "of the frame: raised veins, damp hair, a bruise fading yellow-"
            "green, an old scar, the edge of a cotton hand wrap at the wrist. "
            "The bottle stands just behind the forearm, upright, already "
            "softening out of focus. A clean gym interior reduces to soft shape "
            "beyond. Camera is very close at forearm level, focus on the skin "
            "where the thumb is pressing."
        ),
    },
]
