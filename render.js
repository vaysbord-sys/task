/* ============================================================
   render.js — the app engine (Builder agent)
   ============================================================ */
const state = { view:"today", chan:"all", q:"" };
const M = document.getElementById("main");
const $ = s => document.querySelector(s);

/* ---------- helpers ---------- */
const chanTag = c => c==="web3" ? `<span class="tag t-w3"><span class="dot"></span>Web3</span>`
  : c==="web2" ? `<span class="tag t-w2"><span class="dot"></span>Web2</span>` : "";
const eraLabel = e => e==="classic" ? "Timeless" : "Modern";
const matchChan = c => state.chan==="all" || c==="all" || c===state.chan;
const esc = s => (s||"").replace(/<[^>]+>/g,"");
const hay = (...xs) => esc(xs.join(" ")).toLowerCase();
const matchQ = txt => !state.q || txt.toLowerCase().includes(state.q.toLowerCase());

/* ---------- modal ---------- */
function openModal(html){ $("#modal").innerHTML = `<div class="grab"></div>`+html; $("#modalBg").classList.add("open"); document.body.style.overflow="hidden"; }
function closeModal(){ $("#modalBg").classList.remove("open"); document.body.style.overflow=""; }
function detailHTML(d, head){
  let h = head||"";
  if(d.what) h += `<p>${d.what}</p>`;
  (d.sections||[]).forEach(s=>{ h+=`<h4>${s.h}</h4><ul>${s.b.map(b=>`<li>${b}</li>`).join("")}</ul>`; });
  if(d.reading) h+=`<h4>Study further</h4><ul>${d.reading.map(r=>`<li>${r}</li>`).join("")}</ul>`;
  return h;
}

/* ---------- views ---------- */
function viewToday(){
  const sigs = DATA.signals.filter(s=>matchChan(s.c) && matchQ(hay(s.title,s.body,s.tags.join(" "))));
  let h = `<div class="view">
    <div class="kicker">Today · ${fmtDate(DATA.asOf)}</div>
    <div class="h1">The brief</div>
    <div class="digest"><div class="kicker">${DATA.digest.title}</div><p style="color:var(--t2);font-size:.9rem;line-height:1.6;margin:0">${DATA.digest.body}</p></div>
    <div class="sec-h"><h2>Signals worth your time</h2><span class="cnt">${sigs.length}</span></div>`;
  h += sigs.length ? sigs.map(sigCard).join("") : empty("No signals match your filter.");
  h += `<div class="footer-note"><b>How this stays current.</b> ${DATA.review.feeds}
    <div class="review-stamp">✓ Reviewed by the Critic agent · curated ${fmtDate(DATA.asOf)}</div></div>`;
  h += `</div>`;
  M.innerHTML = h;
}
function sigCard(s){
  const idx = DATA.signals.indexOf(s);
  return `<div class="signal" onclick="openSignal(${idx})" style="cursor:pointer">
    <div class="sig-icon">${s.icon}</div>
    <div style="flex:1">
      <h3>${s.title}</h3><p>${s.body}</p>
      <div class="sig-meta">${chanTag(s.c)}
        <span class="score ${s.hot?'hot':''}">${s.hot?'🔥 ':''}signal ${s.score}</span>
        ${s.tags.map(t=>`<span class="tag t-mut">${t}</span>`).join("")}</div>
    </div></div>`;
}
function openSignal(idx){
  const s = DATA.signals[idx]; if(!s) return;
  openModal(`<div class="mtags">${chanTag(s.c)}<span class="tag t-mut">signal ${s.score}/100</span>${s.tags.map(t=>`<span class="tag t-mut">${t}</span>`).join("")}</div>
    <h2>${s.icon} ${s.title}</h2><p>${s.body}</p>
    <h4>Why it should change what you do</h4>
    <p>This is a directional signal, not financial or investment advice. Treat the score as "how much attention this deserves from a CMO," weigh it against your own positioning, and pull the relevant <b>Play</b> and <b>Cases</b> from this hub to act on it.</p>`);
}

function viewLearn(){
  const mods = DATA.modules.filter(m=>matchChan(m.c) && matchQ(hay(m.title,m.blurb,m.track,(m.points||[]).join(" "))));
  const tracks = ["Foundations","Web3 channel","Web2 channel"];
  let h = `<div class="view"><div class="kicker">Curriculum</div><div class="h1">Learn marketing</div>
    <div class="sub">A working CMO's curriculum. Foundations apply everywhere; then two distinct channels — Web3 and Web2 — each with their own playbook. Tap any module to go deep.</div>`;
  tracks.forEach(tr=>{
    const list = mods.filter(m=>m.track===tr);
    if(!list.length) return;
    h += `<div class="sec-h"><h2>${tr}</h2><span class="cnt">${list.length}</span></div><div class="grid g2">`;
    h += list.map(modCard).join("");
    h += `</div>`;
  });
  if(!mods.length) h+=empty("No modules match your filter.");
  h += `</div>`;
  M.innerHTML = h;
}
function modCard(m){
  return `<div class="card mod" onclick="openMod('${m.num}')">
    <div class="case-tags">${chanTag(m.c)||`<span class="tag t-mut">Core</span>`}<span class="num">MODULE ${m.num}</span></div>
    <h3>${m.title}</h3><p>${m.blurb}</p>
    <ul class="points">${m.points.map(p=>`<li>${p}</li>`).join("")}</ul>
    <div class="meta"><span class="tag t-mut">Tap to read →</span></div></div>`;
}
function openMod(num){
  const m = DATA.modules.find(x=>x.num===num); if(!m) return;
  openModal(`<div class="mtags">${chanTag(m.c)||`<span class="tag t-mut">Foundations</span>`}<span class="tag t-mut">Module ${m.num}</span><span class="tag t-mut">${m.track}</span></div>
    <h2>${m.title}</h2>${detailHTML(m.detail)}`);
}

function viewCases(){
  let cs = DATA.cases.filter(c=>matchChan(c.c) && matchQ(hay(c.title,c.brand,c.body,c.vert,c.tags.join(" "))));
  if(state.caseFilter && state.caseFilter!=="all") cs = cs.filter(c=>c.era===state.caseFilter);
  let h = `<div class="view"><div class="kicker">Case library</div><div class="h1">Cases</div>
    <div class="sub">The best campaigns and plays, dissected. Timeless classics next to modern moves — across Web3 and Web2, from AI and consumer to betting and fantasy. Every case ends in a transferable lesson.</div>
    <div class="filters">
      ${["all","classic","modern"].map(f=>`<button class="fbtn ${(state.caseFilter||'all')===f?'on':''}" onclick="setCaseFilter('${f}')">${f==='all'?'All eras':eraLabel(f)}</button>`).join("")}
    </div>`;
  h += cs.length ? `<div class="grid g2">${cs.map(caseCard).join("")}</div>` : empty("No cases match your filter.");
  h += `</div>`;
  M.innerHTML = h;
}
function caseCard(c){
  const idx = DATA.cases.indexOf(c);
  return `<div class="card" onclick="openCase(${idx})">
    <div class="case-tags">${chanTag(c.c)}<span class="tag t-era">${eraLabel(c.era)}</span><span class="tag t-mut">${c.vert}</span></div>
    <div class="case-t">${c.title}</div>
    <div class="case-brand">${c.brand} · ${c.year}</div>
    <div class="case-body">${c.body}</div>
    <div class="lesson"><b>The lesson</b>${c.lesson}</div></div>`;
}
function openCase(idx){
  const c = DATA.cases[idx]; if(!c) return;
  const head = `<div class="case-brand" style="margin-bottom:14px">${c.brand} · ${c.year} · ${c.vert}</div>`;
  openModal(`<div class="mtags">${chanTag(c.c)}<span class="tag t-era">${eraLabel(c.era)}</span>${c.tags.map(t=>`<span class="tag t-mut">${t}</span>`).join("")}</div>
    <h2>${c.title}</h2>${head}${detailHTML(c.detail)}
    <div class="lesson" style="margin-top:18px"><b>The transferable lesson</b>${c.lesson}</div>`);
}

function viewPlays(){
  const ps = DATA.plays.filter(p=>matchChan(p.c) && matchQ(hay(p.vert,p.title,p.steps.join(" "),(p.examples||[]).join(" "))));
  let h = `<div class="view"><div class="kicker">Playbooks</div><div class="h1">Plays</div>
    <div class="sub">Tactical, ready-to-run playbooks by vertical — AI, consumer, sport tech, betting/gambling/fantasy, and token launches. Pull one when you need to act, not just learn.</div>
    <div class="grid g2">`;
  h += ps.length ? ps.map(playCard).join("") : empty("No plays match your filter.");
  h += `</div></div>`;
  M.innerHTML = h;
}
function playCard(p){
  const idx = DATA.plays.indexOf(p);
  return `<div class="card" onclick="openPlay(${idx})">
    <div class="play-h"><div class="play-ic" style="background:${p.color}22;color:${p.color}">${p.icon}</div>
      <div><h3>${p.title}</h3><div class="vert">${p.vert} ${p.c==='web3'?'· Web3':''}</div></div></div>
    <ul class="points">${p.steps.slice(0,3).map(s=>`<li>${s}</li>`).join("")}</ul>
    <div class="meta" style="margin-top:10px"><span class="tag t-mut">${p.steps.length} moves · tap →</span></div></div>`;
}
function openPlay(idx){
  const p = DATA.plays[idx]; if(!p) return;
  openModal(`<div class="mtags">${p.c==='web3'?chanTag('web3'):`<span class="tag t-mut">All channels</span>`}<span class="tag t-mut">${p.vert}</span></div>
    <h2>${p.icon} ${p.title}</h2>
    <h4>The moves</h4><ul>${p.steps.map(s=>`<li>${s}</li>`).join("")}</ul>
    <h4>Study these</h4><p>${p.examples.map(e=>`<b>${e}</b>`).join(" · ")} — find them in the Cases tab.</p>`);
}

function viewPeople(){
  const ppl = DATA.people.filter(p=>matchChan(p.c) && matchQ(hay(p.name,p.role,p.why,(p.follow||[]).join(" "))));
  const groups = [["web3","Web3 & onchain"],["web2","Web2, tech & growth"]];
  let h = `<div class="view"><div class="kicker">Who to follow</div><div class="h1">People</div>
    <div class="sub">The most instructive voices in marketing — the operators, founders, and thinkers shaping both channels. Each card says exactly what to learn from them.</div>`;
  groups.forEach(([c,label])=>{
    if(state.chan!=="all" && state.chan!==c) return;
    const list = ppl.filter(p=>p.c===c);
    if(!list.length) return;
    h += `<div class="sec-h"><h2>${label}</h2><span class="cnt">${list.length}</span></div><div class="grid g2">${list.map(personCard).join("")}</div>`;
  });
  if(!ppl.length) h+=empty("No people match your filter.");
  h += `</div>`;
  M.innerHTML = h;
}
function personCard(p){
  return `<div class="card person">
    <div class="avi" style="background:${p.color}">${p.init}</div>
    <div style="flex:1">
      <h3>${p.name} ${chanTag(p.c)}</h3>
      <div class="handle">${p.handle}</div>
      <div class="role">${p.role}</div>
      <div class="why">${p.why}</div>
      <div class="meta" style="display:flex;gap:5px;flex-wrap:wrap;margin-top:9px">${p.follow.map(f=>`<span class="tag t-mut">${f}</span>`).join("")}</div>
    </div></div>`;
}

function empty(msg){ return `<div class="empty"><div class="e-ic">◌</div>${msg}</div>`; }
function fmtDate(s){ try{ return new Date(s+"T00:00:00").toLocaleDateString(undefined,{month:"short",day:"numeric",year:"numeric"}); }catch(e){ return s; } }

/* ---------- routing ---------- */
const VIEWS = { today:viewToday, learn:viewLearn, cases:viewCases, plays:viewPlays, people:viewPeople };
function go(v){
  state.view = v;
  document.querySelectorAll(".navbtn").forEach(b=>b.classList.toggle("on", b.dataset.v===v));
  VIEWS[v](); M.scrollTop = 0;
}
function setChan(c){
  state.chan = c;
  document.querySelectorAll("#chan button").forEach(b=>b.classList.toggle("on", b.dataset.c===c));
  VIEWS[state.view]();
}
function setCaseFilter(f){ state.caseFilter=f; viewCases(); }
let searchT;
function onSearch(v){ state.q=v.trim(); clearTimeout(searchT); searchT=setTimeout(()=>VIEWS[state.view](),140); }

/* ---------- theme ---------- */
const THEMES=["black","light","paper"];
function cycleTheme(){
  const cur=document.documentElement.getAttribute("data-theme");
  const next=THEMES[(THEMES.indexOf(cur)+1)%THEMES.length];
  document.documentElement.setAttribute("data-theme",next);
  try{ localStorage.setItem("signal-theme",next); }catch(e){}
  const tc={black:"#0a0a0c",light:"#ececed",paper:"#13110d"}[next];
  document.querySelector('meta[name=theme-color]').setAttribute("content",tc);
}
try{ const t=localStorage.getItem("signal-theme"); if(t) document.documentElement.setAttribute("data-theme",t); }catch(e){}

/* ---------- PWA install (Add to Home Screen) ---------- */
const manifest = {
  name:"The Signal — Marketing Hub", short_name:"The Signal", start_url:".", display:"standalone",
  background_color:"#0a0a0c", theme_color:"#0a0a0c",
  icons:[{src:"data:image/svg+xml,"+encodeURIComponent(`<svg xmlns='http://www.w3.org/2000/svg' width='512' height='512'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='%237C5CFF'/><stop offset='1' stop-color='%23FF7A45'/></linearGradient></defs><rect width='512' height='512' rx='112' fill='url(%23g)'/><text x='50%25' y='54%25' font-size='300' text-anchor='middle' dominant-baseline='middle' fill='white' font-family='sans-serif'>◎</text></svg>`),sizes:"512x512",type:"image/svg+xml"}]
};
try{
  const blob=new Blob([JSON.stringify(manifest)],{type:"application/json"});
  const link=document.createElement("link"); link.rel="manifest"; link.href=URL.createObjectURL(blob); document.head.appendChild(link);
}catch(e){}
let deferredPrompt;
window.addEventListener("beforeinstallprompt",e=>{ e.preventDefault(); deferredPrompt=e; const b=$("#installBtn"); if(b) b.style.display="grid"; });
$("#installBtn").addEventListener("click",async()=>{ if(!deferredPrompt) return; deferredPrompt.prompt(); await deferredPrompt.userChoice; deferredPrompt=null; $("#installBtn").style.display="none"; });

/* ---------- boot ---------- */
go("today");
