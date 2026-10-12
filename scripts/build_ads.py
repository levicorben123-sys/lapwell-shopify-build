"""Build the Lapwell TikTok ads (1080x1920, 15 s, no audio; add a sound inside TikTok).

Each ad = 4 licensed Pexels b-roll clips with a caption (2.5 s each) + a 5 s product end card built from the
supplier photos of a LIVE product, with its real price and the store address.
Run:  python scripts/build_ads.py            (writes ads/v2/*.mp4 and *_preview.jpg)
Edit the ADS list when products or prices change.
"""
import os, subprocess, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = os.path.join(ROOT, "tools", "ffmpeg.exe")
OUT = os.path.join(ROOT, "ads", "v2")
PROD = os.path.join(ROOT, "mockup", "img", "prod")
VID = os.path.join(ROOT, "videos")
FONT = "C\\:/Windows/Fonts/segoeuib.ttf"
INK, SALMON = "0x15302b", "0xef7d5d"
CLIP_S, CARD_S = 2.5, 5.0

ADS = [
    {"name": "fountain_ad_v2", "clips": [
        ("hydration/kitten-drinking-water-from-faucet_pexels-35247531.mp4", 1.0, "Your cat only drinks\nfrom the tap?"),
        ("hydration/cat-drinking-from-faucet-kitchen-sink_pexels-27895556.mp4", 0.5, "It isn't being weird."),
        ("hydration/adorable-cat-drinking-water-from-bowl_pexels-39284290.mp4", 2.0, "Lots of cats like\nmoving water"),
        ("hydration/calico-cat-drinking-water_pexels-37679493.mp4", 2.0, "A fountain keeps it\nflowing all day"),
     ], "title": "Stainless steel fountain, 3.2 L", "price": "$39.99  ·  free US shipping",
     "photos": ["steel-fountain-1.jpg", "steel-fountain-6.jpg"]},
    {"name": "grooming_kit_ad_v2", "clips": [
        ("grooming/cat-cleaning-itself-on-couch_pexels-11366754.mp4", 2.0, "Cat fur on\neverything you own?"),
        ("grooming/person-brushing-a-cat_pexels-8944053.mp4", 2.0, "A two-minute brush\na few times a week"),
        ("grooming/grooming-a-cat-masked_pexels-6131044.mp4", 3.0, "Catches the loose fur\nbefore your couch does"),
        ("grooming/relaxed-cat-grooming-on-bed-sunlight_pexels-36242518.mp4", 1.0, "Yours might end up\nloving it"),
     ], "title": "Grooming Kit: self-cleaning\nbrush + LED nail clipper", "price": "$41.99  ·  free US shipping",
     "photos": ["slicker-brush-1.jpg", "nail-clipper-2.jpg"]},
    {"name": "cozy_kit_ad_v2", "clips": [
        ("calming/person-petting-cat-on-bed_pexels-18980939.mp4", 0.5, "Where does your cat\nactually sleep?"),
        ("calming/white-orange-cat-laying-on-bed_pexels-8719250.mp4", 2.0, "Your bed?\nProbably."),
        ("calming/cozy-cat-relaxing-in-soft-blanket_pexels-30588697.mp4", 2.0, "Give them a soft spot\nof their own"),
        ("calming/calm-tabby-resting-in-sunlight_pexels-34971445.mp4", 5.0, "and somewhere sunny\nto watch the world"),
     ], "title": "Cozy Kit: raised sofa bed\n+ window hammock", "price": "$79.99  ·  free US shipping",
     "photos": ["sofa-bed-1.jpg", "window-hammock-1.jpg"]},
]


def run(args):
    subprocess.run([FF, "-loglevel", "error", "-y", *args], check=True)


def txtfile(tmp, name, text):
    p = os.path.join(tmp, name)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return p.replace("\\", "/").replace(":", "\\:")


def clip_segment(tmp, i, src, start, caption):
    out = os.path.join(tmp, f"seg{i}.mp4")
    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"
    for n, line in enumerate(caption.split("\n")):
        t = txtfile(tmp, f"cap{i}_{n}.txt", line)
        vf += (f",drawtext=fontfile='{FONT}':textfile='{t}':fontsize=68:fontcolor=white:"
               "borderw=3:bordercolor=black@0.55:shadowx=0:shadowy=3:shadowcolor=black@0.5:"
               f"x=(w-text_w)/2-40:y=390+{n}*86")  # TikTok safe zone: below top tabs, left of buttons
    run(["-ss", str(start), "-t", str(CLIP_S), "-i", os.path.join(VID, src), "-an", "-vf", vf,
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20",
         "-video_track_timescale", "15360", out])
    return out


def card_segment(tmp, ad):
    half = CARD_S / len(ad["photos"])
    parts = []
    title_lines = ad["title"].split("\n")
    t_titles = [txtfile(tmp, f"title{n}.txt", l) for n, l in enumerate(title_lines)]
    # Everything stays inside TikTok's safe zone: y 260-1480 (top tabs above, username/caption below),
    # centered on x=500 (like/share buttons sit on the right edge).
    cx = "(w-text_w)/2-40"
    title_y = 350
    photo_y = title_y + 66 * len(title_lines) + 30
    P = 700                                   # photo size
    price_y = photo_y + P + 30
    t_price = txtfile(tmp, "price.txt", ad["price"])
    for k, ph in enumerate(ad["photos"]):
        out = os.path.join(tmp, f"card{k}.mp4")
        frames = int(half * 30)
        flt = (f"[1:v]scale={2*P}:{2*P},zoompan=z='1+0.0009*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
               f"d={frames}:s={P}x{P}:fps=30[ph];"
               f"[0:v][ph]overlay=(W-w)/2-40:{photo_y}[b];"
               f"[b]drawtext=fontfile='{FONT}':text='Lapwell':fontsize=60:fontcolor={SALMON}:x={cx}:y=265,"
               + "".join(f"drawtext=fontfile='{FONT}':textfile='{t}':fontsize=52:fontcolor=white:"
                         f"x={cx}:y={title_y + 66 * n}," for n, t in enumerate(t_titles)) +
               f"drawbox=x=150:y={price_y}:w=700:h=100:color={SALMON}:t=fill,"
               f"drawtext=fontfile='{FONT}':textfile='{t_price}':fontsize=48:fontcolor=white:x={cx}:y={price_y + 24},"
               f"drawtext=fontfile='{FONT}':text='getlapwell.com':fontsize=60:fontcolor=white:x={cx}:y={price_y + 125}[v]")
        run(["-f", "lavfi", "-t", str(half), "-i", f"color=c={INK}:s=1080x1920:r=30",
             "-loop", "1", "-t", str(half), "-i", os.path.join(PROD, ph),
             "-filter_complex", flt, "-map", "[v]", "-t", str(half),
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "20",
             "-video_track_timescale", "15360", out])
        parts.append(out)
    return parts


def build(ad):
    with tempfile.TemporaryDirectory() as tmp:
        segs = [clip_segment(tmp, i, *c) for i, c in enumerate(ad["clips"])]
        segs += card_segment(tmp, ad)
        lst = os.path.join(tmp, "list.txt")
        with open(lst, "w") as f:
            f.writelines(f"file '{s.replace(os.sep, '/')}'\n" for s in segs)
        out = os.path.join(OUT, ad["name"] + ".mp4")
        run(["-f", "concat", "-safe", "0", "-i", lst, "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p",
             "-preset", "medium", "-crf", "19", "-movflags", "+faststart", out])
        # preview: one frame every 2.5 s
        run(["-i", out, "-vf", "select='not(mod(n\\,75))',scale=216:384,tile=6x1", "-frames:v", "1",
             os.path.join(OUT, ad["name"] + "_preview.jpg")])
        print("built", out)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for ad in ADS:
        build(ad)
