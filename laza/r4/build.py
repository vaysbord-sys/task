"""Builds laza/r4/index.html (Round 4, YONEX-style full-screen slides). Old round (r3) lives at laza/r4/old/."""
import pathlib, html, json

HERE = pathlib.Path(__file__).parent
B = "https://d8j0ntlcm91z4.cloudfront.net/user_2xojXnccJM2OM83CuOEuH3U88is/hf_20260929_"
I = json.loads((HERE / "images.json").read_text())
u = lambda k: B + I[k]
e = html.escape
D = json.loads((HERE / "directions.json").read_text())

def img(k, alt):
    return f'<img loading="lazy" src="{u(k)}" alt="{e(alt)}">'

def full(k, title, text, pos="left"):
    return f'''<section class="slide full rv"><div class="bg">{img(k, title)}</div>
<div class="cap {pos}"><h3>{e(title)}</h3><p>{e(text)}</p></div></section>'''

def one(x):
    k, t, s = x
    return f'<figure class="rv"><div class="ph">{img(k, t)}</div><figcaption><h3>{e(t)}</h3><p>{e(s)}</p></figcaption></figure>'

def pair(a, b):
    return f'<section class="slide pair"><div class="wrap two">{one(a)}{one(b)}</div></section>'

def direction(d):
    k = lambda s: d["pre"] + s
    c = d["cap"]
    pal = "".join(
        f'<div class="chip"><div class="c" style="background:{h}{";border:1px solid rgba(0,0,0,.1)" if light else ""}"></div><b>{n}</b><span>{h} · {r}</span></div>'
        for n, h, r, light in d["pal"])
    src = lambda s: (f' <a href="{s}" target="_blank" rel="noopener">source</a>') if s else ""
    roots = "".join(f"<li>{e(t)}{src(s)}</li>" for t, s in d["roots"])
    voice = "".join(f"<li>{e(v)}</li>" for v in d["voice"])
    disp, text, ar, sample, arsample = d["type"]
    x = lambda key: (k(c[key][0]), c[key][1], c[key][2])
    return f'''
<div id="{d["id"]}" class="dir {d["cls"]}">
<section class="slide full hero rv"><div class="bg">{img(k(c["01"][0]), d["name"])}</div>
  <div class="cap left big"><p class="eb">Direction {d["n"]} · {e(d["atmos"])}</p><h2 class="dname">{d["name"]}</h2><p class="dline">{e(d["line"])}</p><p>{e(c["01"][2])}</p></div></section>

<section class="slide text rv"><div class="wrap cols">
  <div><p class="eb">Roots · research</p><ul class="roots">{roots}</ul><p class="lens">{e(d["lens"])}</p></div>
  <div><p class="eb">What it means for Laza</p><p class="so">{e(d["so"])}</p></div></div></section>

<section class="slide text rv"><div class="wrap">
  <p class="eb">Logo · a one-color wordmark and a three-color symbol</p>
  <div class="logos"><figure><div class="lg" style="background:{d["wm_bg"]}">{img("W" + d["n"], d["name"] + " wordmark")}</div><figcaption>{e(d["wm_note"])}</figcaption></figure>
  <figure><div class="lg sq" style="background:{d["sym_bg"]}">{img(d["sym"], d["name"] + " symbol")}</div><figcaption>{e(d["sym_note"])}</figcaption></figure></div></div></section>

<section class="slide text rv"><div class="wrap">
  <p class="eb">Color · {e(d["scheme"])}</p><div class="pal">{pal}</div><p class="small">{e(d["contrast"])}</p>
  <div class="ty"><p class="d" style="font-family:'{disp}',serif">{e(sample)}</p><p class="ar" lang="ar" dir="rtl" style="font-family:'{ar}',sans-serif">{arsample}</p></div>
  <p class="small">Display {disp} · Text {text} · Arabic {ar} (native proof pending)</p></div></section>

{full(*x("11"), "right")}
{full(*x("02"), "left")}
{full(*x("12"), "right")}
{pair(x("03"), x("04"))}
{pair(x("05"), x("06"))}
{pair(x("07"), x("08"))}

<section class="slide text rv"><div class="wrap cols"><div><p class="eb">Voice</p><ul class="vo">{voice}</ul></div>
  <div><p class="eb">Service</p><p class="so">{e(d["service"])}</p></div></div></section>
</div>'''

tpl = (HERE / "template.html").read_text()
out = tpl.replace("<!--DIRECTIONS-->", "".join(direction(d) for d in D))
for d in D:
    out = out.replace("HERO_" + d["id"], u(d["pre"] + d["cap"]["01"][0]))
(HERE / "index.html").write_text(out)
print("ok", len(out))
