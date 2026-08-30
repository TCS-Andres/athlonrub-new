"""
Athlon Rub - shared photographic style blocks for the lifestyle image system.

WHY THIS FILE EXISTS
--------------------
The single hardest requirement on this shoot is "it cannot look AI". Every
clause below is load-bearing against a specific tell that gives generated
photography away:

  CAMERA   - a real lens at a real aperture, so the model renders one plane of
             focus with honest falloff instead of the everything-sharp,
             everything-glowing look.
  LIGHT    - one big soft source plus deep unlit shadow. AI defaults to flat
             omnidirectional fill, which reads as CGI.
  SKIN     - pores, blemishes, asymmetry, real sweat. Smooth skin is tell #1.
  GRADE    - muted and desaturated with lifted blacks. The orange-and-teal
             "cinematic" push is tell #2.
  CAPTURE  - grain, vignette, slight CA, highlight roll-off. Clean digital
             perfection is tell #3.
  FRAMING  - reportage, off-centre, caught mid-action. Centred hero poses
             staring down the barrel are tell #4.

Matches the reference set the client supplied: gritty gym / warehouse
interiors, hard-training athletes, sweat, muted grade, shallow depth.
"""

# ---------------------------------------------------------------------------
# The camera and the light. Kept first because whatever leads the prompt
# dominates the render.
# ---------------------------------------------------------------------------
CAMERA = (
    "Shot on a Canon EOS R5 with an 85mm f/1.4 prime wide open at f/1.6, "
    "ISO 800, 1/400s, handheld at roughly chest height. Real editorial sports "
    "photography from a working photojournalist, not an advertisement. "
    "Genuinely shallow depth of field: one narrow plane is sharp and "
    "everything in front of and behind it falls off smoothly into soft, "
    "un-busy bokeh with no outlining or halos. "
)

LIGHT = (
    "Lighting is one large soft directional source - daylight through a big "
    "clean, well-kept gym window - raking in from camera left at about 45 degrees. "
    "The shadow side of the body goes genuinely dark and stays uncorrected, "
    "with only a faint bounce off the floor. A thin specular rim separates the "
    "far shoulder and jaw from the background. The day outside is overcast, so "
    "the light is soft and directional but never direct sun - no hard sunbeams, "
    "no shafts of light crossing the room, no warm golden-hour cast. No fill "
    "light, no rim light kickers, no coloured gels, no studio strobe look. "
)

GRADE = (
    "Colour grade is muted, desaturated and neutral-cool: grey-green shadows, "
    "warm but restrained skin highlights, whites that roll off instead of "
    "clipping, and shadows that carry real density and fall to a true black "
    "point without going milky, washed out or flat. Contrast is held in the "
    "midtones so muscle separation and fabric weave stay readable. Absolutely "
    "no HDR, no clarity or structure slider, no orange-and-teal cinematic "
    "push, no bloom, no glow. "
)

# ---------------------------------------------------------------------------
# The skin, the sweat and the room. This is the block that actually kills the
# uncanny look, so it is the longest and the most specific.
# ---------------------------------------------------------------------------
REALISM = (
    "Uncompromising photographic realism in the skin: visible open pores, fine "
    "peach fuzz along the jaw and forearm, uneven blotchy tone, small "
    "blemishes and old scars, freckles, razor bumps, capillary flush at the "
    "cheekbones, faint tan lines, chapped lips, forearm and temple veins "
    "standing up from exertion. The face is asymmetrical the way real faces "
    "are - one eye a little different from the other, a nose that is not "
    "straight, teeth that are not uniform. "
    "Sweat behaves physically: beads sit in the pores on the forehead and "
    "upper lip, larger drops run down the temple and sternum following "
    "gravity, damp patches darken the fabric at chest, spine and waistband, "
    "and hair is wet at the hairline with flyaway strands stuck flat to the "
    "forehead while others frizz loose. Fabric behaves like real fabric: soft "
    "creases and memory folds, worn elastic, pilled cotton, sweat darkening "
    "the weave unevenly. "
    "THE FACILITY IS CURRENT, CLEAN AND WELL MAINTAINED - a serious gym that "
    "is properly looked after, not a derelict one. Ring canvas is taut, clean "
    "and white; ropes are tight and evenly wrapped; mats are unmarked; floors "
    "are swept; paint is sound; equipment is in good order and correctly "
    "racked. Realism in the room comes from honest use, not decay: chalk dust "
    "on a platform, a folded towel over a rail, shoe scuffs on a clean floor. "
    "Explicitly NOT wanted: peeling or chipped paint, water stains, rust, "
    "cracked concrete, broken or grimy windows, duct-taped equipment, bare "
    "unfinished walls, an abandoned-warehouse or condemned-building look. "
)

CAPTURE = (
    "Reportage framing - slightly off-centre, a little loose, the subject "
    "caught mid-effort and not performing for the lens. Fine natural sensor "
    "grain, mild optical vignetting, a trace of chromatic aberration in the "
    "brightest speculars, very slight motion blur in the fastest-moving limb. "
    "Straight out of camera with only a light grade - not retouched. "
)

# ---------------------------------------------------------------------------
# Negatives. Named failure modes, not vague adjectives.
# ---------------------------------------------------------------------------
NEGATIVE = (
    "CRITICAL - this must never read as AI-generated, 3D-rendered or "
    "illustrated. No plastic, waxy, airbrushed or poreless skin, no smoothed "
    "or symmetrical face, no perfect white teeth, no glowing skin, no "
    "over-sharpened halos, no CGI sheen. No haze machine, no floating "
    "particles, no lens flare. No stock-photo grin, no thumbs up, no hero pose "
    "facing the camera dead centre. Anatomy strictly correct: five fingers per "
    "hand, thumbs placed right, joints bending the correct way, two arms and "
    "two legs, ears and teeth correctly formed. "
)

NO_BRANDING = (
    "All athletic clothing, wraps, gloves, shoes and equipment are plain and "
    "completely unbranded. No text, no lettering, no numbers, no logos, no "
    "signage, no watermark and no caption anywhere in the frame. "
)


def build(scene: str, branding: str = NO_BRANDING) -> str:
    """Assemble a full prompt. Scene first, then camera, light, grade, realism."""
    return " ".join(
        p.strip() for p in (scene, CAMERA, LIGHT, GRADE, REALISM, CAPTURE, branding, NEGATIVE)
    )
