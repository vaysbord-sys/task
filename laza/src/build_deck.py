"""Builds laza/index.html: a full-screen slide deck (YONEX round-3 format) from src/blocks.json + src/plan*.svg."""
import json, re, pathlib

HERE = pathlib.Path(__file__).parent
B = json.loads((HERE / "blocks.json").read_text())
PLAN = {i: (HERE / f"plan{i}.svg").read_text() for i in range(1, 5)}

CONCEPTS = [
    dict(id="blue-hour", n="01", key="c1", cls="A", name="Blue Hour.", pillar="Light is the brand",
         line="“Stay for the good part.”", bg="#F4F8FD", fg="#16306B", accent="#7FB2F0",
         wow="The Sky", wow_txt="A continuous lacquered barrel vault in Laza Sky, lit from a hidden cove programmed to the store's hours: clear daylight blue at 2pm, blue hour at 8pm, deep blue with warm table light at 1am. The room changes every visit, needs no sign, and works in any footprint.",
         wow_list=["Mirror-chrome bar front that reflects the vault", "Three oak “bleacher” steps: day-club seating, not a laptop café", "Sky glazed-tile path from door to counter", "Terry-and-chrome stools, a nod to the tennis project"]),
    dict(id="ahlan", n="02", key="c2", cls="B", name="Ahlan.", pillar="Hospitality is the brand",
         line="“Come as you are. Leave sweeter.”", bg="#F8F7F3", fg="#0F3550", accent="#4FB0E0",
         wow="The Pull Bar", wow_txt="A long, open kunafa counter at the entrance, clad in handmade Tile Blue glaze with a chrome top. Trays come out, get flipped, and the cheese is pulled under one warm spotlight, in front of you. A slowly turning chrome turntable of whole trays sits in the window.",
         wow_list=["Long shared oak sofra tables: strangers sit together", "Built-in perimeter majlis bench with Rose Syrup cushions", "Scalloped chrome edges on tables and awning", "The host greets every guest with “ahlan”"]),
    dict(id="pool-club", n="03", key="c3", cls="C", name="Pool Club.", pillar="Architecture is the brand",
         line="“Everyone's a member.”", bg="#FFFFFF", fg="#1F5FA8", accent="#A9DDF3",
         wow="The Pit", wow_txt="A sunken oval conversation pit about 45 cm deep, lined in pale pool tile with a Deep End band and chrome pool-ladder rails. About 18 guests sit facing each other, so the social energy comes built in. A level seating ring on the rim keeps it accessible.",
         wow_list=["Blue-and-white cabana awning over the counter", "Deck-oak counter with chrome edge", "Terry cushions, ladder-rail door pulls", "Free membership card: five punches pays out a kunafa"]),
    dict(id="radio", n="04", key="c4", cls="D", name="Laza Radio.", pillar="Music is the brand",
         line="“Good mood, on air till 2am.”", bg="#F3F4FA", fg="#1A1F4A", accent="#6C8CFF",
         wow="The Record Wall", wow_txt="An oak wall of about 1,500 records with two big speakers and a built-in booth behind a chrome counter with a periwinkle top. Guest selectors on Fridays, one Laza Radio stream in every store, and an ON AIR box that lights at 2pm and goes dark at 2am.",
         wow_list=["Oak acoustic-slat ceiling washed in Frequency Blue", "Close small tables, room to move", "Menu as a tracklist: side A kunafa + crepes, side B froyo + drinks", "Crew jacket doubles as the merch hero"]),
]

def figs(gal):
    out = []
    for m in re.finditer(r'<figure[^>]*>(.*?)</figure>', gal, re.S):
        inner = m.group(1)
        img = re.search(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"', inner)
        cap = re.search(r'<figcaption>(.*?)</figcaption>', inner)
        if img:
            out.append((img.group(1), img.group(2), cap.group(1) if cap else ""))
    return out

def views(items, title, c, part=""):
    cells = "".join(
        f'<figure class="v{i}"><img loading="lazy" src="{src}" alt="{alt}" data-cap="{cap}"><figcaption>{cap}</figcaption></figure>'
        for i, (src, alt, cap) in enumerate(items))
    return f'''<section class="slide {c["cls"]}" data-key="{c["key"]}"><div class="in">
<div class="shead"><span class="eb">{c["n"]} · {title}{part}</span><span class="eb dim">{c["name"].rstrip(".")}</span></div>
<div class="views n{len(items)}">{cells}</div></div></section>'''

def concept(c):
    b = B[c["id"]]
    hero = re.search(r'src="([^"]+)"[^>]*alt="([^"]*)"', b["hero"])
    items = figs(b["gal"])
    s = []
    s.append(f'''<section class="slide cover-c {c["cls"]}" data-key="{c["key"]}"><img class="full" src="{hero.group(1)}" alt="{hero.group(2)}">
<div class="cover-ov"><span class="eb light">Concept {c["n"]} · {c["pillar"]}</span><h2 class="cname">{c["name"]}</h2><p class="cline">{c["line"]}</p></div></section>''')
    s.append(f'''<section class="slide {c["cls"]}" data-key="{c["key"]}"><div class="in two">
<div><span class="eb">{c["n"]} · The idea</span>{b["idea"].replace('<div><p class="idea">','<p class="idea">').replace('</p></div>','</p>')}<p class="cline in-line">{c["line"]}</p></div>
{b["facts"]}</div></section>''')
    s.append(f'''<section class="slide {c["cls"]}" data-key="{c["key"]}"><div class="in">
<div class="shead"><span class="eb">{c["n"]} · Identity</span><span class="eb dim">Logo · color · voice</span></div>
<div class="idgrid">{b["stage"]}{b["pal"]}</div>{b["voice"]}</div></section>''')
    lis = "".join(f"<li>{x}</li>" for x in c["wow_list"])
    s.append(f'''<section class="slide {c["cls"]}" data-key="{c["key"]}"><div class="in">
<div class="shead"><span class="eb">{c["n"]} · Space</span><span class="eb dim">The WOW moment</span></div>
<div class="space"><div class="plan">{PLAN[int(c["n"])]}</div><div><h3 class="wow">{c["wow"]}</h3><p>{c["wow_txt"]}</p><ul>{lis}</ul></div></div></div></section>''')
    if len(items) > 6:
        s.append(views(items[:5], "Views", c, " · 1/2"))
        s.append(views(items[5:], "Views", c, " · 2/2"))
    else:
        s.append(views(items, "Views", c))
    return "\n".join(s)

tpl = (HERE / "deck_template.html").read_text()
html = tpl.replace("<!--CONCEPTS-->", "\n".join(concept(c) for c in CONCEPTS))
(HERE.parent / "index.html").write_text(html)
print("wrote", len(html), "bytes")
