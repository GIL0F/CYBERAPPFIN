#!/usr/bin/env python3
"""Monta anatomia.html: a página única "Anatomia da Cyberappfin".

Junta numa rolagem só:
  - a abertura e a anatomia das 7 camadas (ferramentas/anatomia-base.html);
  - o mapa da topologia com o fluxo dos pacotes, a simulação, o DR e todas as
    telas de processo, copiados da apresentação (jornada.html).

O conteúdo vem da jornada.html: se um texto ou IP mudar lá, rode de novo:
    python3 ferramentas/montar-pagina-unica.py
"""
import pathlib, re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
base = (RAIZ / 'ferramentas' / 'anatomia-base.html').read_text(encoding='utf-8')
jornada = (RAIZ / 'jornada.html').read_text(encoding='utf-8')

def entre(txt, ini, fim, incluir=False):
    a = txt.index(ini); b = txt.index(fim, a + len(ini))
    return txt[a:b + len(fim)] if incluir else txt[a + len(ini):b]

# ---------- partes do protótipo-base ----------
css_base = entre(base, '<style>', '</style>')
js_base = entre(base, '<script>', '</script>')
abertura = entre(base, '<section class="abre">', '</section>', True)
anatomia = entre(base, '<section id="anatomia"', '</section>', True)

css_base = (css_base
    .replace('.legenda{', '.legenda-times{').replace('.legenda div', '.legenda-times div').replace('.legenda i', '.legenda-times i')
    .replace('.palco{ position:sticky; top:0; height:100vh;', '.palco{ position:sticky; top:var(--topo); height:calc(100vh - var(--topo));')
    .replace('#figura{ width:100%; height:94vh;', '#figura{ width:100%; height:calc(100vh - var(--topo) - 6vh);')
    .replace('max-height:92vh; overflow:auto;', 'max-height:calc(100vh - var(--topo) - 6vh); overflow:auto;'))
abertura = abertura.replace('<section class="abre">', '<section class="abre" id="inicio">').replace('class="legenda"', 'class="legenda-times"')

# ---------- motor do mapa e conteúdo da apresentação ----------
js_j = entre(jornada, '<script>', '</script>')
nucleo = entre(js_j, "const NS = 'http://www.w3.org/2000/svg';", '/* ---------- navegação ---------- */')
nucleo = "const NS = 'http://www.w3.org/2000/svg';" + nucleo
assert nucleo.count("const svg = document.getElementById('mapa');") == 1
nucleo = nucleo.replace("const svg = document.getElementById('mapa');", '')
# o foco (apagar o que não importa) passa a valer só para este mapa
for a, b in [("document.body.classList.remove('focando')", "svg.classList.remove('focando')"),
             ("document.body.classList.add('focando')", "svg.classList.add('focando')")]:
    assert nucleo.count(a) == 1, a
    nucleo = nucleo.replace(a, b)
incidente = entre(js_j, 'async function rodarIncidente', '\nfunction ir(')
incidente = 'async function rodarIncidente' + incidente

motor = f"""
/* =====================================================================
   Motor do mapa — copiado da jornada.html por ferramentas/montar-pagina-unica.py
   Cada chamada cria um mapa independente dentro do <svg> recebido.
   ===================================================================== */
function criarMapa(svg){{
{nucleo}
{incidente}
  function aplicar(i){{
    const p = PARADAS[i];
    limparAnimacoes(); resetIncidente();
    camera(p.cam || MUNDO); focar(p.foco);
    const minha = geracao;
    setTimeout(() => {{
      if(minha !== geracao) return;
      if(p.anim) p.anim();
      if(p.incidente !== undefined) rodarIncidente(p.incidente);
      if(p.dr !== undefined) rodarDR(p.dr);
    }}, 950);
  }}
  function parar(){{ limparAnimacoes(); resetIncidente(); }}
  return {{ PARADAS, aplicar, parar }};
}}
"""

pagina_js = r"""
/* =====================================================================
   Página única: capítulos montados a partir das paradas da apresentação
   ===================================================================== */
const CAPS = [
  { id:'organizacao', rot:'02', nome:'Organização', titulo:'Como nos organizamos', partes:[{ salas:[2] }] },
  { id:'topologia', rot:'03', nome:'Topologia', titulo:'A topologia e o fluxo dos pacotes', partes:[{ mapa:[3, 4, 5, 6, 7, 8, 9, 17, 18, 19, 20] }] },
  { id:'deteccao', rot:'04', nome:'Detecção', titulo:'Detecção: Wazuh, IA e firewall', partes:[{ salas:[10, 11, 12, 13, 14, 15, 16, 21] }] },
  { id:'incidente', rot:'05', nome:'Incidente', titulo:'Um incidente, do clique ao ticket', partes:[{ mapa:[22, 23, 24, 25, 26, 27] }, { salas:[28, 29, 30, 31, 32, 33] }] },
  { id:'continuidade', rot:'06', nome:'Continuidade', titulo:'Backup, BIA e recuperação', partes:[{ salas:[35, 36, 37, 38, 39, 40] }, { mapa:[34, 41, 42, 43, 44, 45, 46] }, { salas:[47, 48, 49, 50, 51, 52] }] },
  { id:'grc', rot:'07', nome:'GRC', titulo:'Governança e riscos', partes:[{ salas:[53, 54] }] }
];

// as cores do conteúdo foram feitas para fundo escuro: no papel claro, viram tons legíveis
const CLARO = { 'color:#4ADE80':'color:#15803D', 'color:#F87171':'color:#B91C1C', 'color:#8DB6F9':'color:#1D4ED8', 'color:#FB923C':'color:#C2410C',
  'color:#FCA5A5':'color:#B91C1C', 'color:#FACC15':'color:#A16207', 'color:#F5D08A':'color:#92400E',
  'background:#3A1C21':'background:#FEE2E2', 'background:#33270F':'background:#FEF3C7', 'background:#1C2F42':'background:#E5E7EB' };
const claro = html => Object.entries(CLARO).reduce((h, [a, b]) => h.split(a).join(b), html || '');
const nota = t => t ? `<details class="nota"><summary>Notas do apresentador</summary><p>${t}</p></details>` : '';

const DADOS = criarMapa(document.createElementNS(NS, 'svg')).PARADAS;
const capitulos = document.getElementById('capitulos');
const blocos = [];

function artigoSala(n){
  const p = DADOS[n - 1];
  const a = document.createElement('article');
  a.className = 'sala-sec';
  a.innerHTML = `<header class="sala-cab"><span class="quem" style="background:${p.cor}">${p.quem || 'Cyberappfin'}</span>
      <h3>${p.titulo}</h3>${p.sub ? `<p class="sala-sub">${p.sub}</p>` : ''}</header>
    <div class="sala-corpo">${claro(p.sala)}</div>${nota(p.notas)}`;
  return a;
}

function blocoMapa(paradas){
  const N = paradas.length;
  const b = document.createElement('div');
  b.className = 'mapa-bloco';
  b.style.height = `calc(${N} * 70vh + 100vh)`;
  b.innerHTML = `<div class="mapa-palco">
      <div class="mapa-moldura"><svg class="mapa" viewBox="0 0 1600 920" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Mapa da topologia da Cyberappfin"></svg></div>
      <aside class="cartao mapa-cartao" aria-live="polite">
        <span class="fase"></span><div class="barra" aria-hidden="true"><i></i></div>
        <nav class="m-nav" aria-label="Ir para um passo"></nav>
        <span class="quem"></span><h3 class="m-titulo"></h3><p class="m-sub"></p>
        <div class="m-html"></div><div class="m-nota"></div>
      </aside></div>`;
  const svg = b.querySelector('svg');
  const mapa = criarMapa(svg);
  const q = s => b.querySelector(s);
  const nav = q('.m-nav');
  paradas.forEach((n, k) => {
    const bt = document.createElement('button');
    bt.textContent = String(k + 1).padStart(2, '0');
    bt.setAttribute('aria-label', `Passo ${k + 1}: ${DADOS[n - 1].titulo}`);
    bt.addEventListener('click', () => irPasso(k));
    nav.appendChild(bt);
  });
  let atual = -1, visivel = false;
  function total(){ return b.offsetHeight - innerHeight; }
  function irPasso(k){ scrollTo({ top:b.offsetTop + (k + .5) / N * total(), behavior:REDUZIR ? 'auto' : 'smooth' }); }
  function mostrar(k){
    const p = mapa.PARADAS[paradas[k] - 1];
    mapa.aplicar(paradas[k] - 1);
    q('.fase').textContent = `Passo ${k + 1} de ${N}`;
    const quem = q('.quem'); quem.textContent = p.quem || 'Cyberappfin'; quem.style.background = p.cor;
    q('.m-titulo').textContent = p.titulo;
    q('.m-sub').textContent = p.sub || '';
    q('.m-html').innerHTML = claro(p.html);
    q('.m-nota').innerHTML = nota(p.notas);
    [...nav.children].forEach((x, i) => x.classList.toggle('ativo', i === k));
    atual = k;
  }
  function render(){
    if(!visivel) return;
    const p = Math.min(1, Math.max(0, (scrollY - b.offsetTop) / total()));
    q('.barra i').style.width = (p * 100).toFixed(1) + '%';
    const k = Math.min(N - 1, Math.floor(p * N));
    if(k !== atual) mostrar(k);
  }
  new IntersectionObserver(([e]) => {
    visivel = e.isIntersecting;
    if(visivel) render(); else { mapa.parar(); atual = -1; }
  }).observe(b);
  blocos.push(render);
  return b;
}

const REDUZIR = matchMedia('(prefers-reduced-motion: reduce)').matches;
CAPS.forEach(c => {
  const sec = document.createElement('section');
  sec.className = 'cap'; sec.id = c.id; sec.dataset.nome = c.nome;
  sec.innerHTML = `<header class="cap-cab"><span class="fig">CAP_${c.rot} · ${c.nome}</span><h2>${c.titulo}</h2></header>`;
  c.partes.forEach(parte => {
    if(parte.salas) parte.salas.forEach(n => sec.appendChild(artigoSala(n)));
    if(parte.mapa) sec.appendChild(blocoMapa(parte.mapa));
  });
  capitulos.appendChild(sec);
});

let pedidoMapa = false;
addEventListener('scroll', () => { if(!pedidoMapa){ pedidoMapa = true; requestAnimationFrame(() => { blocos.forEach(f => f()); pedidoMapa = false; }); } }, { passive:true });
addEventListener('resize', () => blocos.forEach(f => f()));

// menu do topo: marca o capítulo em que a leitura está
const links = [...document.querySelectorAll('.topo-nav a[href^="#"]')];
new IntersectionObserver(es => es.forEach(e => {
  if(!e.isIntersecting) return;
  links.forEach(l => l.classList.toggle('ativo', l.getAttribute('href') === '#' + e.target.id));
}), { rootMargin:'-45% 0px -50% 0px' }).observe(document.getElementById('anatomia'));
document.querySelectorAll('.cap, #inicio, #fim').forEach(s => new IntersectionObserver(es => es.forEach(e => {
  if(!e.isIntersecting) return;
  links.forEach(l => l.classList.toggle('ativo', l.getAttribute('href') === '#' + e.target.id));
}), { rootMargin:'-45% 0px -50% 0px' }).observe(s));
"""

css_pagina = r"""
  /* ===================== página única ===================== */
  :root{ --topo:58px; }
  body{ padding-top:var(--topo); }
  section[id], .cap{ scroll-margin-top:var(--topo); }
  .abre{ min-height:calc(100vh - var(--topo)); }
  .topo-nav{ position:fixed; top:0; left:0; right:0; height:var(--topo); z-index:50; display:flex; align-items:center; gap:6px; padding:0 2vw;
             background:var(--papel); border-bottom:var(--borda); overflow-x:auto; }
  .topo-nav a{ flex-shrink:0; font:800 13px 'JetBrains Mono', monospace; letter-spacing:.08em; text-transform:uppercase; color:var(--tinta);
               text-decoration:none; padding:8px 11px; border:2px solid transparent; }
  .topo-nav a:hover{ border-color:var(--tinta); }
  .topo-nav a.ativo{ background:var(--tinta); color:#fff; }
  .topo-nav a:focus-visible{ outline:3px solid var(--soc); outline-offset:2px; }
  .topo-nav .marca{ font-family:'Space Grotesk', sans-serif; font-size:17px; letter-spacing:-.01em; margin-right:auto; border:var(--borda); background:var(--soc); padding:5px 10px; }
  .topo-nav .marca.ativo{ background:var(--soc); color:var(--tinta); }

  .cap{ padding:12vh 5vw 4vh; border-top:var(--borda); }
  .cap-cab{ display:flex; flex-direction:column; gap:2vh; margin-bottom:6vh; }
  .cap-cab h2{ font-size:clamp(44px, 6vw, 110px); line-height:.9; letter-spacing:-.04em; text-transform:uppercase; max-width:18ch; }
  .sala-sec{ margin:0 auto 12vh; max-width:1500px; display:flex; flex-direction:column; gap:22px; }
  .sala-cab{ display:flex; flex-direction:column; gap:10px; }
  .sala-cab h3{ font-size:clamp(30px, 3vw, 54px); line-height:1; letter-spacing:-.02em; text-transform:uppercase; }
  .sala-sub{ font-size:clamp(16px, 1.15vw, 20px); color:var(--cinza); font-weight:500; }
  .quem{ align-self:flex-start; font:800 13px 'JetBrains Mono', monospace; letter-spacing:.12em; text-transform:uppercase; border:var(--borda); padding:5px 10px; color:var(--tinta); }
  .nota{ border:2px dashed var(--tinta); background:#fff; padding:10px 14px; font-size:15px; line-height:1.5; }
  .nota summary{ cursor:pointer; font:800 12px 'JetBrains Mono', monospace; letter-spacing:.12em; text-transform:uppercase; }
  .nota p{ margin-top:8px; color:#333; }

  /* ---------- blocos de mapa (rolagem) ---------- */
  .mapa-bloco{ position:relative; margin:0 -5vw 10vh; }
  .mapa-palco{ position:sticky; top:var(--topo); height:calc(100vh - var(--topo)); display:grid; grid-template-columns:minmax(0, 1.55fr) minmax(340px, 1fr);
               gap:2vw; padding:2.5vh 3vw; align-items:center; }
  .mapa-moldura{ height:calc(100vh - var(--topo) - 5vh); border:var(--borda); background:#fff; box-shadow:var(--sombra); overflow:hidden; }
  svg.mapa{ width:100%; height:100%; display:block; }
  .mapa-cartao{ max-height:calc(100vh - var(--topo) - 5vh); }
  .m-titulo{ font-size:clamp(24px, 2.1vw, 38px); line-height:1.02; letter-spacing:-.02em; text-transform:uppercase; }
  .m-sub{ font-size:15px; color:var(--cinza); font-weight:500; }
  .m-nav{ display:flex; flex-wrap:wrap; gap:6px; }
  .m-nav button{ font:800 14px 'JetBrains Mono', monospace; border:var(--borda); background:#fff; color:var(--tinta); padding:6px 9px; cursor:pointer; }
  .m-nav button.ativo{ background:var(--tinta); color:#fff; }
  .m-nav button:focus-visible{ outline:3px solid var(--soc); outline-offset:2px; }
  .m-html{ display:flex; flex-direction:column; gap:10px; font-size:clamp(15px, 1.05vw, 18px); line-height:1.45; font-weight:500; }
  .m-html h3{ font:800 12px 'JetBrains Mono', monospace; letter-spacing:.12em; text-transform:uppercase; color:var(--cinza); margin-top:4px; }
  .m-html table{ width:100%; border-collapse:collapse; font-size:14px; }
  .m-html th{ text-align:left; font:800 11px 'JetBrains Mono', monospace; letter-spacing:.08em; text-transform:uppercase; border-bottom:3px solid var(--tinta); padding:5px 6px; }
  .m-html td{ padding:5px 6px; border-bottom:1px solid #11111133; vertical-align:top; }
  .m-html tr.dest td{ background:#FEF3C7; } .m-html tr.perigo td{ background:#FEE2E2; }
  .m-html ul{ list-style:none; display:flex; flex-direction:column; gap:6px; }
  .m-html li{ padding-left:20px; position:relative; }
  .m-html li::before{ content:""; position:absolute; left:0; top:.45em; width:10px; height:10px; background:var(--cor, var(--tinta)); border:2px solid var(--tinta); }
  .cards{ display:grid; grid-template-columns:1fr 1fr; gap:10px; }
  .card{ border:var(--borda); background:#fff; padding:10px 12px; display:flex; flex-direction:column; gap:2px; border-top:8px solid var(--cor, var(--tinta)); }
  .card .n{ font:700 26px 'Space Grotesk', sans-serif; line-height:1.05; }
  .card .l{ font:600 12px 'JetBrains Mono', monospace; color:var(--cinza); }
  .aviso{ border:var(--borda); background:#FEF3C7; padding:8px 12px; font-weight:600; font-size:15px; }
  .chips{ display:flex; flex-wrap:wrap; gap:6px; }
  .chip{ border:2px solid var(--tinta); background:#fff; padding:3px 9px; font:700 13px 'JetBrains Mono', monospace; }
  .passos{ display:flex; flex-direction:column; gap:7px; counter-reset:p; }
  .passo{ display:flex; gap:10px; align-items:flex-start; color:var(--cinza); }
  .passo::before{ counter-increment:p; content:counter(p); flex-shrink:0; width:26px; height:26px; border:2px solid var(--tinta); background:#fff; color:var(--tinta);
                  display:flex; align-items:center; justify-content:center; font:800 13px 'JetBrains Mono', monospace; }
  .passo.ativo{ color:var(--tinta); } .passo.ativo::before{ background:var(--cp, var(--dmz)); }
  .passo.feito{ color:var(--tinta); } .passo.feito::before{ content:"✓"; background:#DCFCE7; }
  .passo b{ color:var(--tinta); }

  /* ---------- mapa no papel (o motor desenha em cores de fundo escuro; aqui elas viram o estilo cru) ---------- */
  svg.mapa text{ font-family:'JetBrains Mono', monospace; fill:var(--tinta); }
  svg.mapa .t-title{ font-family:'Space Grotesk', sans-serif; font-weight:700; }
  svg.mapa .t-mono, svg.mapa .t-muted{ fill:var(--cinza); font-weight:600; }
  svg.mapa pattern path{ stroke:#11111114; }
  svg.mapa .no{ transition:opacity .45s ease; }
  svg.mapa.focando .no{ opacity:.28; } svg.mapa.focando .no.foco{ opacity:1; }
  svg.mapa .lig{ fill:none; stroke:var(--tinta); stroke-width:2.5; } svg.mapa .lig.trac{ stroke-dasharray:7 7; }
  svg.mapa .barramento{ fill:none; stroke:var(--tinta); stroke-width:7; stroke-linecap:square; }
  svg.mapa rect[fill="#12263A"], svg.mapa rect[fill="#10283A"]{ fill:#fff; stroke:var(--tinta); stroke-width:3; }
  svg.mapa rect[fill="#16354C"]{ fill:#CCFBF1; stroke:var(--tinta); stroke-width:2.5; }
  svg.mapa text[fill="#5EEAD4"]{ fill:#0F766E; }
  svg.mapa rect[fill="#101B27"]{ fill:#F1EFE8; stroke:var(--tinta); stroke-width:2.5; }
  svg.mapa rect[fill="#15222F"]{ fill:#fff; stroke:var(--tinta); stroke-width:2; }
  svg.mapa text[fill="#AFC1D2"]{ fill:var(--tinta); }
  svg.mapa rect[fill="#0F1D2B"]{ fill:#fff; stroke:var(--tinta); stroke-width:3; stroke-opacity:1; }
  svg.mapa rect[fill="#16283A"]{ fill:#fff; stroke:var(--tinta); stroke-width:2; }
  svg.mapa text.t-title[fill="#EAB308"]{ fill:#A16207; } svg.mapa text.t-title[fill="#22C55E"]{ fill:#15803D; }
  svg.mapa text.t-title[fill="#14B8A6"]{ fill:#0F766E; } svg.mapa text.t-title[fill="#F59E0B"]{ fill:#B45309; }
  svg.mapa .host rect{ transition:fill .3s, stroke .3s; }
  svg.mapa .host.alerta rect{ fill:#FEE2E2 !important; stroke:#B91C1C !important; stroke-width:3; }
  svg.mapa .host.ok rect{ fill:#DCFCE7 !important; stroke:#15803D !important; stroke-width:3; }
  svg.mapa text[fill="#F87171"]{ fill:#B91C1C; } svg.mapa text[fill="#4ADE80"]{ fill:#15803D; }
  svg.mapa text[fill="#FCD34D"]{ fill:#A16207; } svg.mapa text[fill="#7DD3FC"]{ fill:#1D4ED8; }
  svg.mapa .host.link{ cursor:pointer; } svg.mapa .host.link:focus{ outline:none; }
  svg.mapa .host.link:focus-visible rect{ stroke:var(--soc) !important; stroke-width:4; }
  svg.mapa .pulso{ animation:pulso 1.4s ease-in-out infinite; }
  @keyframes pulso{ 0%,100%{ opacity:1 } 50%{ opacity:.35 } }

  /* ---------- componentes das telas de processo, no estilo cru ---------- */
  .sala-corpo{ font-size:16px; }
  .s-corpo{ display:flex; flex-direction:column; gap:22px; }
  .s-txt{ font-size:clamp(16px, 1.15vw, 20px); line-height:1.5; font-weight:500; } .s-txt b{ font-weight:700; }
  .s-rot{ font:800 13px 'JetBrains Mono', monospace; letter-spacing:.12em; text-transform:uppercase; color:var(--cinza); }
  .s-aviso{ align-self:flex-start; border:var(--borda); background:#FEF3C7; padding:9px 14px; font-weight:600; }
  .linha{ display:grid; gap:18px; }
  .bloco{ position:relative; background:#fff; border:var(--borda); box-shadow:6px 6px 0 0 var(--tinta); padding:24px 18px 18px; display:flex; flex-direction:column; gap:8px; }
  .bloco::before{ content:""; position:absolute; left:0; top:0; right:0; height:8px; background:var(--cor, var(--brand)); border-bottom:3px solid var(--tinta); }
  .bloco h4{ font-size:clamp(18px, 1.4vw, 24px); line-height:1.15; }
  .bloco p{ font-size:clamp(14px, 1vw, 17px); line-height:1.45; font-weight:500; }
  .bloco .grande{ font:700 clamp(34px, 3.2vw, 56px)/1 'Space Grotesk', sans-serif; }
  .bloco .rot{ font:800 12px 'JetBrains Mono', monospace; letter-spacing:.1em; text-transform:uppercase; color:var(--cinza); }
  .bloco .rodape{ margin-top:auto; padding-top:10px; border-top:2px dashed var(--tinta); font-size:15px; }
  .chips2{ display:flex; flex-wrap:wrap; gap:8px; }
  .chips2 span{ border:2px solid var(--tinta); background:#fff; padding:5px 11px; font:700 14px 'JetBrains Mono', monospace; }
  .tempo{ display:grid; grid-template-columns:repeat(var(--n), 1fr); gap:10px; position:relative; }
  .tempo::before{ content:""; position:absolute; left:4%; right:4%; top:22px; height:3px; background:var(--tinta); }
  .etapa{ display:flex; flex-direction:column; align-items:center; text-align:center; gap:8px; position:relative; }
  .etapa .bola{ width:46px; height:46px; display:flex; align-items:center; justify-content:center; font:700 18px 'Space Grotesk', sans-serif;
                background:var(--cor, var(--brand)); border:var(--borda); box-shadow:3px 3px 0 0 var(--tinta); }
  .etapa h4{ font-size:16px; line-height:1.2; } .etapa p{ font-size:14px; color:var(--cinza); line-height:1.35; }
  .org{ display:flex; flex-direction:column; align-items:center; }
  .org .chefe{ border:var(--borda); background:#FEF3C7; padding:12px 22px; text-align:center; box-shadow:5px 5px 0 0 var(--tinta); }
  .org .chefe h4{ font-size:20px; } .org .chefe p{ font-size:14px; }
  .org .tronco{ width:3px; height:22px; background:var(--tinta); }
  .org .ramos{ display:grid; grid-template-columns:repeat(6, 1fr); gap:12px; width:100%; position:relative; padding-top:22px; }
  .org .ramos::before{ content:""; position:absolute; top:0; left:8.3%; right:8.3%; height:3px; background:var(--tinta); }
  .org .membro{ border:var(--borda); border-top:8px solid var(--cor); background:#fff; padding:12px; position:relative; }
  .org .membro::before{ content:""; position:absolute; top:-30px; left:50%; width:3px; height:22px; background:var(--tinta); }
  .org .membro h4{ font-size:16px; margin-bottom:4px; } .org .membro p{ font-size:14px; line-height:1.35; }
  .escada{ display:grid; grid-template-columns:repeat(5, 1fr); gap:14px; align-items:end; }
  .escada .bloco:nth-child(2){ margin-bottom:22px; } .escada .bloco:nth-child(3){ margin-bottom:44px; }
  .escada .bloco:nth-child(4){ margin-bottom:66px; } .escada .bloco:nth-child(5){ margin-bottom:88px; }
  .escada .rodape b{ color:var(--tinta); }
  .relogio{ display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; padding:4px 0; }
  .relogio div{ display:flex; flex-direction:column; gap:2px; }
  .relogio b{ font:700 clamp(18px, 1.6vw, 28px)/1.05 'Space Grotesk', sans-serif; white-space:nowrap; }
  .relogio span{ font:800 11px 'JetBrains Mono', monospace; letter-spacing:.1em; color:var(--cinza); }
  .calor, .marcos{ display:grid; grid-template-columns:minmax(140px, 15%) repeat(5, 1fr); gap:6px; }
  .calor .cab{ font:800 12px 'JetBrains Mono', monospace; letter-spacing:.06em; text-transform:uppercase; text-align:center; padding:6px 0; }
  .calor .srv{ font-weight:700; display:flex; align-items:center; }
  .calor .cel{ border:2px solid var(--tinta); padding:10px 4px; text-align:center; font-weight:700; font-size:15px; }
  .calor .n2{ background:#FACC15; } .calor .n3{ background:#FB923C; } .calor .n4{ background:#F87171; }
  .marcos p{ font-size:14px; line-height:1.4; border-top:3px solid var(--tinta); padding-top:8px; }
  .mitiga{ display:grid; grid-template-columns:minmax(140px, 13%) minmax(190px, 27%) 1fr; gap:6px; }
  .mitiga .cab{ font:800 12px 'JetBrains Mono', monospace; letter-spacing:.08em; text-transform:uppercase; color:var(--cinza); padding:4px 8px; }
  .mitiga .pil{ font:700 18px 'Space Grotesk', sans-serif; display:flex; align-items:center; padding:10px; border:var(--borda); border-left:10px solid var(--grc); background:#fff; }
  .mitiga .imp{ display:flex; align-items:center; background:#FEE2E2; border:var(--borda); padding:10px 12px; font-size:15px; line-height:1.4; }
  .mitiga .acoes{ display:flex; flex-wrap:wrap; gap:6px; align-content:center; border:var(--borda); background:#fff; padding:8px 10px; }
  .mitiga .acoes span{ border:2px solid var(--tinta); background:#DCFCE7; padding:3px 10px; font-size:14px; font-weight:600; }
  .mitiga .acoes span.pend{ background:#FEF3C7; }
  .acoes span.pend::before, .legenda b.pend::before{ content:""; display:inline-block; width:.72em; height:.72em; margin-right:.4em; vertical-align:-.05em; border-radius:50%;
    border:2px solid currentColor; background:linear-gradient(90deg, currentColor 50%, transparent 50%); box-sizing:border-box; }
  .legenda{ display:flex; gap:18px; font-size:15px; color:var(--cinza); } .legenda b{ color:#15803D; } .legenda b.pend{ color:#A16207; }
  .ordem .bloco{ flex-direction:row; align-items:flex-start; gap:14px; }
  .ordem .num{ font:700 clamp(28px, 2.4vw, 42px)/1 'Space Grotesk', sans-serif; min-width:1.1em; }
  .fluxo{ display:flex; align-items:stretch; gap:8px; }
  .fluxo .passo2{ flex:1; border:var(--borda); border-top:8px solid var(--cor, var(--grc)); background:#fff; padding:10px; display:flex; flex-direction:column; gap:4px; }
  .fluxo .passo2 b{ font:700 16px 'Space Grotesk', sans-serif; } .fluxo .passo2 span{ font-size:13px; color:var(--cinza); }
  .fluxo .seta2{ align-self:center; font-weight:800; font-size:22px; }
  .check{ list-style:none; display:grid; grid-template-columns:1fr 1fr; gap:0 18px; }
  .check li{ font-size:15px; padding-left:24px; position:relative; line-height:1.9em; border-bottom:1px solid #BFD3EC; color:#2B3440; }
  .check li::before{ content:""; position:absolute; left:2px; top:.55em; width:12px; height:12px; border:2px solid #3B7D52; background:#fff; }
  .prancheta{ position:relative; background:linear-gradient(160deg, #7A5232, #5C3B22); padding:30px 14px 14px; border:var(--borda); box-shadow:6px 6px 0 0 var(--tinta); }
  .prancheta .clip{ position:absolute; top:-12px; left:50%; transform:translateX(-50%); width:120px; height:30px; background:linear-gradient(180deg, #E8EDF2, #9AA6B2 55%, #C9D1D9); border:2px solid var(--tinta); }
  .prancheta .papel{ background-color:#FBF8EF; padding:14px 18px 12px 46px; background-image:linear-gradient(90deg, transparent 33px, #F2A8A8 33px, #F2A8A8 35px, transparent 35px); }
  .prancheta .papel .rot{ display:block; color:#7C5A3A; padding-bottom:6px; border-bottom:1px solid #BFD3EC; font:800 12px 'JetBrains Mono', monospace; letter-spacing:.1em; text-transform:uppercase; }
  .doc{ background:#fff; border:var(--borda); box-shadow:6px 6px 0 0 var(--tinta); padding:18px; display:flex; flex-direction:column; gap:8px; }
  .doc .cod{ font:700 12px 'JetBrains Mono', monospace; color:var(--cinza); } .doc h4{ font-size:19px; line-height:1.2; } .doc p{ font-size:14px; line-height:1.45; }
  .doc .selo2{ align-self:flex-start; margin-top:auto; font:800 12px 'JetBrains Mono', monospace; padding:4px 10px; border:2px solid var(--tinta); }
  .ticket{ display:grid; grid-template-columns:minmax(250px, 27%) 1fr; gap:18px; align-items:start; }
  .tk-cab{ border:var(--borda); border-top:8px solid var(--soc); background:#fff; box-shadow:6px 6px 0 0 var(--tinta); padding:18px; display:flex; flex-direction:column; gap:10px; }
  .tk-cab .cod{ font:800 14px 'JetBrains Mono', monospace; } .tk-cab h4{ font-size:22px; line-height:1.15; }
  .tk-cab dl{ display:grid; grid-template-columns:auto 1fr; gap:4px 12px; font-size:15px; } .tk-cab dt{ color:var(--cinza); } .tk-cab dd{ font-weight:700; }
  .tk-cab .kpi{ display:grid; grid-template-columns:1fr 1fr; gap:8px; }
  .tk-cab .kpi div{ border:2px solid var(--tinta); background:#F0FDF4; padding:8px; }
  .tk-cab .kpi b{ display:block; font:700 28px/1.1 'Space Grotesk', sans-serif; color:#15803D; } .tk-cab .kpi span{ font-size:12px; color:var(--cinza); display:block; }
  .tk-linha, .cadeia{ display:flex; flex-direction:column; gap:6px; }
  .tk-ev{ display:grid; grid-template-columns:5.6em 9.5em 1fr; gap:12px; align-items:baseline; border:2px solid var(--tinta); border-left:8px solid var(--cor); background:#fff; padding:8px 12px; }
  .tk-ev .h{ font:700 15px 'JetBrains Mono', monospace; } .tk-ev .f{ font:800 12px 'JetBrains Mono', monospace; letter-spacing:.08em; text-transform:uppercase; }
  .tk-ev p{ font-size:15px; line-height:1.4; font-weight:500; }
  .vks{ display:grid; gap:16px; align-items:stretch; }
  .vk{ border:var(--borda); border-top:8px solid var(--cor); background:#fff; box-shadow:5px 5px 0 0 var(--tinta); padding:14px; display:flex; flex-direction:column; gap:10px; min-width:0; }
  .vk-top{ display:flex; gap:12px; align-items:center; }
  .vk-n{ flex-shrink:0; width:38px; height:38px; display:flex; align-items:center; justify-content:center; font:700 17px 'Space Grotesk', sans-serif; background:var(--cor); border:2px solid var(--tinta); }
  .vk h4{ font-size:clamp(17px, 1.3vw, 22px); line-height:1.15; } .vk .pq{ font-size:15px; line-height:1.4; }
  .vk-cmd{ display:flex; flex-direction:column; gap:4px; }
  .vk-cmd .os{ font:800 11px 'JetBrains Mono', monospace; letter-spacing:.1em; text-transform:uppercase; color:var(--cinza); margin-top:4px; }
  .vk-cmd code{ display:block; font:600 14px/1.4 'JetBrains Mono', monospace; background:var(--tinta); color:#D1FAE5; padding:6px 10px; white-space:pre-wrap; word-break:break-word; }
  .vk-cmd code::before{ content:"$ "; color:#6B7280; }
  .vk-cmd code.txt{ background:#F3F4F6; color:var(--tinta); font-family:'Space Grotesk', sans-serif; border:2px solid var(--tinta); } .vk-cmd code.txt::before{ content:"▸ "; color:var(--tinta); }
  .vk-cmd code.cmt{ color:#9CA3AF; } .vk-cmd code.cmt::before{ content:""; }
  .vk .ok, .vk .x{ font-size:14px; line-height:1.4; padding:8px 12px; border:2px solid var(--tinta); font-weight:500; }
  .vk .ok{ background:#DCFCE7; margin-top:auto; } .vk .x{ background:#FEF3C7; } .vk .ok b, .vk .x b{ font-weight:800; }
  .regras{ width:100%; border-collapse:separate; border-spacing:0 5px; }
  .regras th{ text-align:left; font:800 11px 'JetBrains Mono', monospace; letter-spacing:.08em; text-transform:uppercase; color:var(--cinza); padding:2px 10px; }
  .regras td{ background:#fff; padding:7px 10px; font-size:14px; line-height:1.3; border-top:2px solid var(--tinta); border-bottom:2px solid var(--tinta); }
  .regras td:first-child{ border-left:2px solid var(--tinta); font:700 14px 'JetBrains Mono', monospace; color:#1D4ED8; }
  .regras td:last-child{ border-right:2px solid var(--tinta); white-space:nowrap; } .regras td.det{ font-weight:700; }
  .regras tr.corr td{ background:#F0FDF4; }
  .niv{ display:inline-flex; justify-content:center; min-width:2.2em; padding:2px 8px; border:2px solid var(--tinta); font-weight:800; }
  .trat{ display:inline-block; padding:2px 9px; border:2px solid var(--tinta); font-size:13px; font-weight:700; }
  .trat.L{ background:#E5E7EB; } .trat.C{ background:#FEF3C7; } .trat.X{ background:#FEE2E2; } .trat.A{ background:#DBEAFE; }
  .tag-corr{ display:inline-block; margin-left:8px; padding:1px 7px; border:2px solid var(--tinta); background:#DCFCE7; font:800 10px 'JetBrains Mono', monospace; letter-spacing:.06em; vertical-align:1px; }
  .wz-fluxo{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
  .wz-fluxo .nodo{ border:var(--borda); border-top:8px solid var(--cor); background:#fff; padding:8px 14px; font:700 17px 'Space Grotesk', sans-serif; }
  .wz-fluxo .nodo small{ display:block; font-weight:500; font-size:12px; color:var(--cinza); }
  .wz-fluxo .seta3{ font-weight:800; font-size:22px; }
  .roteiro{ counter-reset:r; display:flex; flex-direction:column; gap:6px; }
  .roteiro li{ list-style:none; counter-increment:r; display:flex; gap:12px; align-items:flex-start; border:2px solid var(--tinta); background:#fff; padding:8px 12px; font-size:15px; line-height:1.4; }
  .roteiro li::before{ content:counter(r); flex-shrink:0; width:26px; height:26px; background:var(--soc); border:2px solid var(--tinta); font:800 13px 'JetBrains Mono', monospace; display:flex; align-items:center; justify-content:center; }
  .conclusao{ border:var(--borda); background:#DCFCE7; padding:12px 16px; font-size:16px; }
  .status-chip{ align-self:flex-start; border:2px solid var(--tinta); background:#FEF3C7; padding:5px 12px; font-weight:700; font-size:14px; }
  .amb{ display:flex; flex-wrap:wrap; gap:10px; }
  .amb-link, .doc-link{ display:inline-flex; gap:8px; align-items:baseline; align-self:flex-start; text-decoration:none; color:var(--tinta);
    font:800 14px 'JetBrains Mono', monospace; text-transform:uppercase; letter-spacing:.04em; background:#BFDBFE; border:var(--borda); box-shadow:4px 4px 0 0 var(--tinta); padding:8px 12px; }
  .doc-link{ background:var(--grc); }
  .amb-link small, .doc-link small{ font-weight:500; text-transform:none; opacity:.8; }
  .amb-link:hover, .doc-link:hover, .amb-link:focus-visible, .doc-link:focus-visible{ transform:translate(2px, 2px); box-shadow:2px 2px 0 0 var(--tinta); outline:none; }
  .demo .vk-n{ font-size:19px; }

  @media (max-width:900px){
    .mapa-palco{ grid-template-columns:1fr; grid-template-rows:46vh auto; }
    .mapa-moldura{ height:46vh; }
    .mapa-cartao{ max-height:44vh; }
    .linha, .vks, .ticket, .escada, .org .ramos, .tempo{ grid-template-columns:1fr !important; }
    .escada .bloco{ margin-bottom:0 !important; }
    .calor, .marcos, .mitiga{ overflow-x:auto; }
    .fluxo{ flex-direction:column; }
  }
"""

nav = """<nav class="topo-nav" aria-label="Capítulos">
  <a class="marca" href="#inicio">Cyberappfin</a>
  <a href="#anatomia">Anatomia</a><a href="#organizacao">Organização</a><a href="#topologia">Topologia</a>
  <a href="#deteccao">Detecção</a><a href="#incidente">Incidente</a><a href="#continuidade">Continuidade</a>
  <a href="#grc">GRC</a><a href="#fim">Documentos</a>
</nav>"""

fim = """<section class="fim" id="fim">
  <span class="fig">FIG_FIM · documentos completos (abrem em outra aba)</span>
  <h2>Quer o detalhe? Está tudo aqui.</h2>
  <div class="links">
    <a class="amarelo" href="drp.html" target="_blank" rel="noopener">Plano de recuperação (DRP) ↗</a>
    <a href="regras-wazuh.html" target="_blank" rel="noopener">Catálogo de regras do Wazuh ↗</a>
    <a href="runbook-tecnico.html" target="_blank" rel="noopener">Runbook técnico ↗</a>
    <a href="dashboards/" target="_blank" rel="noopener">Dashboards do Grafana ↗</a>
    <a href="jornada.html" target="_blank" rel="noopener">Versão em slides (projetor) ↗</a>
  </div>
  <p class="mono" style="font-weight:700"><a href="#inicio" style="box-shadow:none; border:none; padding:0; background:none; text-decoration:underline">↑ Voltar ao início</a></p>
</section>"""

head = entre(base, '<!doctype html>', '<style>', True)
head = head.replace('<title>Anatomia da Cyberappfin</title>', '<title>Anatomia da Cyberappfin</title>')
head = head.replace('content="As sete camadas do ambiente da Cyberappfin, desmontadas, e o caminho de um pacote por elas."',
                    'content="A Cyberappfin numa página só: as camadas do ambiente, a topologia com o fluxo dos pacotes, a resposta a incidentes e a recuperação."')

html = f"""{head}{css_base}{css_pagina}</style>
</head>
<body>
{nav}
{abertura}
{anatomia}
<div id="capitulos"></div>
{fim}
<script>
{js_base}
</script>
<script>
{motor}
{pagina_js}
</script>
</body>
</html>
"""
(RAIZ / 'anatomia.html').write_text(html, encoding='utf-8')
print('anatomia.html gerado:', len(html), 'bytes')
