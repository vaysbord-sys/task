"""Builds laza/r4/index.html (Round 4). Old round (r3) is copied to laza/r4/old/ for the toggle."""
import pathlib, shutil, html, json

HERE = pathlib.Path(__file__).parent
B = "https://d8j0ntlcm91z4.cloudfront.net/user_2xojXnccJM2OM83CuOEuH3U88is/hf_20260929_"
I = json.loads((HERE / "images.json").read_text())
u = lambda k: B + I[k]
e = html.escape

D = [
 dict(id="oasis", n="01", name="Oasis", cls="E", was="Earthy",
  atmos="A desert oasis, and the inside of a Dubai chocolate bar",
  lens="Arabic-contemporary lens · storytelling in the spirit of Mythology",
  line="Rest here.",
  roots=[("Caravans stopped at oases to replenish water and food; Al-Ahsa, the world's largest, holds about 2.5 million date palms.", "https://whc.unesco.org/en/list/1563/"),
         ("Kunafa's origin is disputed (Palestine, Egypt, Syria); a common account places it in the 10th-century Fatimid court. Nablus is the touchstone.", "https://www.cadburydessertscorner.com/articles/tracing-the-origins-of-kunafa-the-popular-middle-eastern-dessert"),
         ("Fix Dessert Chocolatier launched the pistachio-kunafa bar in Dubai in 2021; one TikTok passed 80M+ views and the founder reports 30,000 orders in an hour.", "https://officialfixdessertchocolatier.com/blogs/news/who-is-sarah-hamouda-meet-the-woman-behind-dubais-viral-chocolate-bar")],
  so="Laza becomes the oasis on 5th Avenue: the 2am rest stop where water and something sweet arrive before you ask. The wordmark stretches like a kashida stroke, a caravan road. The symbol is dune, water and sun. The WOW is a counter built like a cross-section of the chocolate bar: layers you can see, a crunch you can hear.",
  wm="23557141-3920-4659-920e-09c7a9ef3627", wm_bg="#EFE2CC", sym="S1", sym_bg="#EFE2CC",
  wm_note="Kashida stretch between z and a · one color: Clay",
  sym_note="Dune · water · sun, in three colors",
  pal=[("Clay","#C4623A","Primary",1),("Sand","#EFE2CC","Ground",0),("Saffron","#F2A93B","Warm lead",0),("Olive","#7A7D4A","Secondary",1),("Date","#5A3A29","Text",1),("Oak","#B98A5E","Material",0)],
  scheme="Analogous warms (clay, saffron, date) with an olive counterpoint.", contrast="Date on Sand 7.9:1 · Clay on Sand 3.2:1, display only.",
  type=("Young Serif","Hanken Grotesk","Readex Pro","Warm from the tray.","دافئة من الصينية"),
  voice=["Rest here.","Water first. Then kunafa.","We pull it from the oven when it's ready, not when the timer says."],
  service="Every guest gets a glass of water and one date on arrival, the oasis welcome. Linen shirts in sand, aprons in olive."),
 dict(id="teta", n="02", name="Teta", cls="O", was="Arabic",
  atmos="Grandma's kitchen, and a Turkish esnaf lokanta",
  lens="Brooklyn lens · human, neighborhood-proud, in the spirit of Red Antler",
  line="Teta says: eat.",
  roots=[("'Ahlan wa sahlan' joins ahl (family) and sahl (easy path): you are family, and may your way be easy.", "https://speakrealarabic.com/post/ahlan-wa-sahlan-meaning-levantine-arabic"),
         ("Hospitality (karam) is treated as a sacred obligation, rooted in the Bedouin ethic of caring for travelers.", "https://www.arabiclanguageonline.com/blog/arabic-coffee-culture/"),
         ("The esnaf lokantası is a tradesmen's canteen with a steam table of ready dishes, often family-run, with staff of 20 or more years. The principle is that you should feel at home.", "https://www.theguideistanbul.com/istanbul-lokanta-culture/")],
  so="Teta (grandmother) feeds you before you ask, and the lokanta keeps the trays warm and visible. The brand is a name-tag, not a crest: a friendly Ruq'ah-cut wordmark with one diamond dot, and a three-petal ma'amoul flower pressed into plates and aprons. The room is the tray wall, loud and warm, tiled like a kitchen.",
  wm="0bb8da4e-442f-4657-a6c3-791e9044b941", wm_bg="#F7F0E3", sym="S2", sym_bg="#F7F0E3",
  wm_note="Ruq'ah teardrop terminals and one nuqta dot · one color: Pomegranate",
  sym_note="Three-petal ma'amoul flower, in three colors",
  pal=[("Pomegranate","#B7283A","Primary",1),("Ivory","#F7F0E3","Ground",0),("Indigo Tile","#23408E","Blue",1),("Saffron","#F4B23E","Warm lead",0),("Rosewater","#F2B8C2","Tint",0),("Oak","#A8774D","Material",0)],
  scheme="Triadic: red, yellow and blue. Indigo always sits with oak and saffron.", contrast="Indigo on Ivory 8.4:1 · Pomegranate on Ivory 5.5:1.",
  type=("Libre Caslon Display","Instrument Sans","Aref Ruqaa","Ahlan, come in.","أهلاً وسهلاً"),
  voice=["Teta says: eat.","A second plate, whether you asked or not.","No one leaves hungry. It's a rule."],
  service="Guests are served first and regulars greeted by name. Pomegranate aprons with indigo trim carry the petal embroidered on the chest."),
 dict(id="aegean", n="03", name="Aegean", cls="L", was="Ultramarine + Violet",
  atmos="The Turkish coastline, from Bodrum to Kaş",
  lens="Northern-European lens · restraint in the spirit of Koto",
  line="Beyond the sea. Open till 2am.",
  roots=[("'Ultramarine' is Middle Latin for 'beyond the sea'. The pigment came from lapis mined in Badakhshan, Afghanistan, and was once worth more than gold in Europe.", "https://storiedcolors.com/color/ultramarine/"),
         ("In Bodrum, walls are whitewashed against insects and windows painted blue against the evil eye, with bougainvillea over the doors.", "https://www.hurriyetdailynews.com/bodrums-white-against-insects-blue-against-the-evil-eye-117393"),
         ("Maraş dondurma is stretchy ice cream made with salep and mastic. Its vendors turn serving into a playful street show.", "https://www.cnn.com/travel/maras-dondurma-turkish-ice-cream")],
  so="The blue has come a long way, and Laza's has too, from the Levant to Astoria. A heavy, calm, generously spaced wordmark with one crescent-cut counter; a symbol where a wave curls into a scoop. The ritual is the stretch-and-flip at the ice-cream counter, modernized: striped linen, not a costume.",
  wm="86de6be2-64a3-4911-8ffe-0564b8e1d562", wm_bg="#EEE9FF", sym="S3", sym_bg="#EEE9FF",
  wm_note="Crescent-cut counter in the final a · one color: Ultramarine",
  sym_note="Wave into scoop, a petal and a sun, in three colors",
  pal=[("Ultramarine","#2438D6","Primary",1),("Lilac","#EEE9FF","Ground",0),("Violet","#7A4DF2","Bougainvillea",1),("Apricot","#FF8A3D","Warm lead",0),("Lapis Ink","#1B1F5E","Text",1),("Oak","#B8875A","Material",0)],
  scheme="Split-complementary: blue-violet against apricot, grounded by oak.", contrast="Ultramarine on Chalk 7.3:1 · Lapis Ink on Apricot 6.4:1.",
  type=("Archivo","Geist","Alexandria","Open till 2. Obviously.","مفتوح حتى الثانية"),
  voice=["Beyond the sea. Open till 2am.","Stretch it. Flip it. Eat it.","The lights go violet at eleven."],
  service="A stretch-and-flip moment at the ice-cream counter. Ultramarine-and-white striped linen shirts with an apricot neckerchief."),
 dict(id="island", n="04", name="Island", cls="B", was="Blue",
  atmos="A tropical island, on Brooklyn hours",
  lens="LA lens · sunny, social and content-first in the spirit of Media.Monks",
  line="Island time. Brooklyn hours.",
  roots=[("Tiki began in 1933–34 in Hollywood and Oakland as a fantasy tropics, and is now widely critiqued as cultural appropriation. So no masks, no totems, no pseudo-Polynesian type.", "https://en.wikipedia.org/wiki/Tiki_culture"),
         ("Mango kunafa (kataifi, mango, cream, rose syrup) is an established modern twist, spread on TikTok and Instagram.", "https://amiraspantry.com/knafeh-mango-cream/"),
         ("Island time means slowness and sun. Laza's version is the unhurried 20-minute hang Moose asked for. (inference)", "")],
  so="The escape is the fruit, the light and the pace, not a costume. A bubbly, heavy, well-spaced wordmark whose l curls like a Naskh stroke. A symbol of mango, leaf and sun. Oak decking and cornflower tile make the room feel like 2pm by the water, all year.",
  wm="c2f3771f-3d59-41eb-93f0-5f06812711f4", wm_bg="#FBF7F0", sym="S4", sym_bg="#FBF7F0",
  wm_note="Naskh-curl l, bubbly terminals · one color: Cornflower",
  sym_note="Mango · leaf · sun, in three colors",
  pal=[("Cornflower","#4F86E8","Primary",1),("Cream","#FBF7F0","Ground",0),("Mango","#FFB627","Warm lead",0),("Coral","#FF6F59","Secondary",0),("Deep Blue","#1F3A7A","Text",1),("Oak","#B8875A","Material",0)],
  scheme="Split-complementary: blue against mango and coral.", contrast="Deep Blue on Cream 10.1:1 · Cornflower on Cream 3.3:1, display only.",
  type=("Gloock","Instrument Sans","El Messiri","Pick a side, or take both.","حلو يا حلو"),
  voice=["Island time. Brooklyn hours.","Cold froyo, hot kunafa. Pick a side, or take both.","Bring a friend. Split nothing."],
  service="Nobody rushes you. Fruit-forward specials. Cornflower camp-collar shirts with mango aprons."),
]

SHOTS = [("01","Interior · people hanging out","wide"),("02","The WOW moment",""),("03","What the team wears",""),("04","Cups · to-go and froyo",""),
         ("05","Plates and cookware",""),("06","Merch",""),("07","Advertising",""),("08","Storefront","wide")]

def fig(k, cap, cls=""):
    return f'<figure class="{cls}"><div class="im"><img loading="lazy" src="{u(k)}" alt="{e(cap)}"></div><figcaption>{e(cap)}</figcaption></figure>'

BORDER = ";border:1px solid rgba(0,0,0,.08)"
LIGHT = ("#EFE2CC","#F7F0E3","#EEE9FF","#FBF7F0")

def section(d, i):
    base = str(i + 1)
    k = lambda s: base + "0" + s
    pal = "".join(f'<div class="chip"><div class="c" style="background:{h};color:{"#fff" if dark else "#1a1a1a"}{BORDER if h in LIGHT else ""}"></div><b>{n}</b><span>{h}</span><em>{r}</em></div>' for n,h,r,dark in d["pal"])
    src = lambda s: (' <a href="' + s + '" target="_blank" rel="noopener">source</a>') if s else ""
    roots = "".join("<li>" + e(t) + src(s) + "</li>" for t, s in d["roots"])
    disp, text, ar, sample, arsample = d["type"]
    voice = "".join(f"<li>{e(v)}</li>" for v in d["voice"])
    return f'''
<section id="{d["id"]}" class="dir {d["cls"]}"><div class="wrap">
  <div class="dhead"><div><p class="dnum">DIRECTION {d["n"]} · {e(d["atmos"]).upper()}</p><h2 class="dname">{d["name"]}</h2><p class="lens">{e(d["lens"])} · evolved from round 3 "{d["was"]}"</p></div><p class="dline">{e(d["line"])}</p></div>

  <div class="blk"><div><p class="eb">Roots</p><p class="why">Research, then the idea it gives us.</p></div>
    <div class="roots"><ul>{roots}</ul><p class="so">{e(d["so"])}</p></div></div>

  <div class="blk"><div><p class="eb">Logo</p><p class="why">The wordmark is lettering in one color, thick and well spaced, with one Arabic cue. The symbol is three colors and built to work at 16 px.</p></div>
    <div class="logos">
      <figure><div class="im logo" style="background:{d["wm_bg"]}"><img src="{u('W'+d['n'])}" alt="{d["name"]} wordmark"></div><figcaption>{e(d["wm_note"])}</figcaption></figure>
      <figure><div class="im logo sq" style="background:{d["sym_bg"]}"><img src="{u(d["sym"])}" alt="{d["name"]} symbol"></div><figcaption>{e(d["sym_note"])}</figcaption></figure>
    </div></div>

  <div class="blk"><div><p class="eb">Color + type</p><p class="why">{e(d["scheme"])}</p></div>
    <div><div class="pal">{pal}</div><p class="small">{e(d["contrast"])}</p>
    <div class="ty"><p class="d" style="font-family:'{disp}',serif">{e(sample)}</p><p class="ar" lang="ar" dir="rtl" style="font-family:'{ar}',sans-serif">{arsample}</p></div>
    <p class="small">Display {disp} · Text {text} · Arabic {ar} (native proof pending)</p></div></div>

  <div class="blk"><div><p class="eb">Space + people</p><p class="why">Where the 20-minute hang happens, and who looks after you.</p></div>
    <div class="g g-space">{fig(k("1"),"Interior · people hanging out","wide")}{fig(k("2"),"The WOW moment")}{fig(k("3"),"What the team wears")}</div></div>
  <p class="svc">{e(d["service"])}</p>

  <div class="blk"><div><p class="eb">Objects</p><p class="why">Cups, tableware and merch, all carrying the real mark.</p></div>
    <div class="g g-obj">{fig(k("4"),"Cups · to-go and froyo")}{fig(k("5"),"Plates and cookware")}{fig(k("6"),"Merch")}</div></div>

  <div class="blk"><div><p class="eb">Out in the world</p><p class="why">Advertising and the street.</p></div>
    <div class="g g-out">{fig(k("7"),"Advertising")}{fig(k("8"),"Storefront","wide")}</div></div>

  <div class="blk"><div><p class="eb">Voice</p><p class="why">Short, sensory, specific.</p></div><div class="vo"><ul>{voice}</ul></div></div>
</div></section>'''

tpl = (HERE / "template.html").read_text()
out = tpl.replace("<!--DIRECTIONS-->", "".join(section(d, i) for i, d in enumerate(D)))
for k in ("101","201","301","401"):
    out = out.replace("IMG" + k, u(k))
(HERE / "index.html").write_text(out)
old = HERE / "old"; old.mkdir(exist_ok=True)
o = (HERE.parent / "r3" / "index.html").read_text()
o = o.replace('<b>LAZA · R3</b>', '<b>LAZA · R3</b><span style="display:flex;border:1px solid #161616;border-radius:99px;overflow:hidden;flex:none"><a href="../" style="padding:6px 14px;font:500 12px IBM Plex Mono,monospace;color:#161616">New</a><a href="./" aria-current="page" style="padding:6px 14px;font:500 12px IBM Plex Mono,monospace;background:#161616;color:#fff">Old</a></span>')
(old / "index.html").write_text(o)
print("ok", len(out))
