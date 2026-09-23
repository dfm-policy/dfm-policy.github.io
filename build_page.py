#!/usr/bin/env python3
"""Generates index.html for the DFMP project page (video-first)."""
from pathlib import Path

OUT = Path(__file__).with_name("index.html")
M = "static/dfmp"
TITLE = "Discrete Flow Matching Policy"
SUBTITLE = "Learning to Act in Discrete Space"

SIM = [("lift", "Lift"), ("can", "Can"), ("square", "Square"), ("toolhang", "Tool Hang"),
       ("transport", "Transport"), ("pusht", "Push-T"), ("blockpush", "Block Push"), ("kitchen", "Kitchen")]

COMPARE = {
    "stacking": dict(title="Cup Stacking", speed="3&times;",
                     rows=[("fm", "Flow Matching", "10 steps", "Misses the first cup and never re-grasps it."),
                           ("dp", "Diffusion Policy", "100 steps",
                            "Pauses at every action chunk and reacts too late when the stacked cups wobble."),
                           ("dfmp", "DFMP", "10 steps", "Misses once, re-grasps the cup and completes the stack.")]),
    "placing": dict(title="Cup Placing", speed="3&times;",
                    rows=[("fm", "Flow Matching", "10 steps",
                           "Never finds a working grasp and pushes the cup until the arm leaves its range."),
                          ("dp", "Diffusion Policy", "100 steps", "Finds a grasp, but slowly, stuttering between action chunks."),
                          ("dfmp", "DFMP", "10 steps", "Goes straight for the handle and finishes quickly.")]),
}

ABSTRACT = (
    "It is well established that discrete representations offer a natural framework for capturing multimodal structure "
    "and modeling transitions in continuous signals. Building on this idea, we introduce Discrete Flow Matching Policy "
    "(DFMP), a method for learning continuous robot actions in a discrete space. DFMP formulates action generation as a "
    "continuous-time Markov chain over action tokens, combining three desirable properties: (i) multimodal behavior "
    "modeling through probabilistic branching among tokens, (ii) fast inference through few-step sampling, and (iii) "
    "stable optimization through a flow-matching objective. To bridge discrete representations and continuous control, "
    "we systematically compare action tokenization schemes, analyze their trade-offs, and identify an effective scheme "
    "for real-world robot policies. Experiments across a broad range of simulated manipulation benchmarks and two "
    "real-world robot deployments demonstrate strong task performance and improved scalability and robustness relative "
    "to continuous-space baselines. These results support DFMP as a principled framework for efficient and robust "
    "visuomotor policy learning.")


def poster(src):
    return src.replace("/videos/", "/posters/").replace(".mp4", ".jpg")


def loop_vid(src):
    return (f"<video data-autoplay muted loop playsinline preload='none' poster='{poster(src)}'>"
            f"<source src='{src}' type='video/mp4'></video>")


def real_vid(base):
    # H.264 .mp4 next to the original .mov if present (plays everywhere), otherwise the .mov
    return (f"<video data-autoplay muted loop playsinline preload='metadata' controls>"
            f"<source src='{base}.mp4' type='video/mp4'><source src='{base}.mov'></video>")


def sim_grid():
    return "".join(f"<figure class='sim'>{loop_vid(f'{M}/videos/sim/{k}.mp4')}<figcaption>{n}</figcaption></figure>"
                   for k, n in SIM)


def compare_block(key):
    c = COMPARE[key]
    panels = "".join(f"""
      <figure class="cmp-panel{' ours' if slug == 'dfmp' else ''}">
        <div class="media">
          <video data-group="{key}" muted playsinline preload="none" poster="{M}/posters/compare/{key}_{slug}.jpg"><source src="{M}/videos/compare/{key}_{slug}.mp4" type="video/mp4"></video>
          <span class="tag">{name} <em>{steps}</em></span><span class="speed">{c['speed']}</span>
        </div>
        <figcaption>{note}</figcaption>
      </figure>""" for slug, name, steps, note in c["rows"])
    return f"""
  <div class="cmp" data-cmp="{key}">
    <div class="cmp-head"><h3>{c['title']}</h3>
      <button class="replay" data-replay="{key}" type="button">&#8635; Replay together</button></div>
    <div class="cmp-grid">{panels}
    </div>
  </div>"""


CSS = r"""
:root{--bg:#faf7f2;--card:#fff;--ink:#1f2328;--muted:#6b6b6b;--line:#e8e1d7;--accent:#e07a48;--accent-ink:#b4532a;
--ours:#4f8f3a;--radius:14px;--shadow:0 1px 2px rgba(31,35,40,.06),0 4px 16px rgba(31,35,40,.06)}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 "Noto Sans",system-ui,-apple-system,"Segoe UI",sans-serif}
h1,h2,h3,.btn,nav a,.eyebrow,.tag,.replay{font-family:"Poppins","Noto Sans",system-ui,sans-serif}
a{color:var(--accent-ink)}video{display:block;max-width:100%}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
header.hero{padding:68px 0 0;text-align:center}
.eyebrow{display:inline-block;font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--accent-ink);
background:#fbe9df;border-radius:999px;padding:5px 14px;margin-bottom:22px}
h1{font-size:clamp(34px,5.2vw,56px);line-height:1.12;font-weight:700;margin:0 auto 8px;letter-spacing:-.015em}
.subtitle{font-family:"Poppins",sans-serif;font-size:clamp(20px,2.6vw,28px);font-weight:500;color:var(--accent);margin:0 0 18px}
.authors{font-size:19px;color:var(--muted);margin-bottom:24px}
.btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 20px;border-radius:999px;background:var(--ink);color:#fff;
text-decoration:none;font-size:15px;font-weight:500}
.btn svg{width:17px;height:17px}.btn.off{background:#d9d3ca;color:#5b5750;cursor:default}
.tldr{max-width:780px;margin:30px auto 0;font-size:19px;color:#3b3f45}
.main-video{margin-top:34px}
.main-video video{width:100%;border-radius:var(--radius);background:#000;box-shadow:var(--shadow)}
nav.toc{position:sticky;top:0;z-index:10;background:rgba(250,247,242,.9);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);margin-top:40px}
nav.toc .wrap{display:flex;gap:22px;justify-content:center;overflow-x:auto;padding-top:12px;padding-bottom:12px;scrollbar-width:none}
nav.toc a{color:var(--muted);text-decoration:none;font-size:14.5px;font-weight:500;white-space:nowrap}
nav.toc a:hover,nav.toc a.on{color:var(--ink)}
section{padding:60px 0 4px;scroll-margin-top:64px}
h2{font-size:32px;font-weight:700;margin:0 0 8px;letter-spacing:-.01em}
.lead{font-size:17.5px;color:var(--muted);max-width:820px;margin:0 0 22px}
h3{font-size:21px;font-weight:600;margin:0}
.card{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);padding:24px 26px}
.abstract{margin:0;text-align:justify;hyphens:auto}
figure{margin:0}figcaption{font-size:15px;color:#3b3f45;line-height:1.5}
.task-head{margin:24px 0 10px}
.pair{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.pair video{width:100%;border-radius:12px;background:#000;aspect-ratio:16/9;object-fit:cover}
.pair figcaption{margin-top:8px}
.cmp{margin-top:26px}
.cmp-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px}
.replay{font-size:14px;font-weight:500;border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 14px;cursor:pointer}
.replay:hover{border-color:var(--ink)}
.cmp-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.cmp-panel{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden}
.cmp-panel.ours{outline:2px solid var(--ours)}
.cmp-panel .media{position:relative;background:#000}
.cmp-panel video{width:100%;aspect-ratio:16/9;object-fit:cover}
.cmp-panel figcaption{padding:12px 16px 16px}
.tag{position:absolute;left:10px;top:10px;background:rgba(31,35,40,.82);color:#fff;font-size:13px;font-weight:600;border-radius:999px;padding:3px 11px}
.tag em{font-style:normal;font-weight:400;opacity:.8}
.cmp-panel.ours .tag{background:var(--ours)}
.speed{position:absolute;right:10px;bottom:10px;background:rgba(31,35,40,.82);color:#fff;font:600 12px "Poppins",sans-serif;border-radius:999px;padding:2px 9px}
.sim-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.sim video{width:100%;aspect-ratio:1;object-fit:cover;border-radius:12px;background:#eee}
.sim figcaption{text-align:center;margin-top:6px;font-size:14.5px;color:var(--muted)}
.mm{display:grid;gap:14px}
.mm figure{background:#fff;border-radius:var(--radius);box-shadow:var(--shadow);padding:14px}
.mm video{width:100%}
.mm figcaption{margin-bottom:6px;font-family:"Poppins",sans-serif;font-weight:600;font-size:15px}
.mm figcaption span{font-weight:400;color:var(--muted)}
footer{margin-top:72px;padding:28px 0 40px;border-top:1px solid var(--line);color:var(--muted);font-size:14px;text-align:center}
@media (max-width:900px){.cmp-grid{grid-template-columns:1fr}nav.toc .wrap{justify-content:flex-start}}
@media (max-width:560px){body{font-size:16px}header.hero{padding-top:48px}.pair{grid-template-columns:1fr}
.sim-grid{grid-template-columns:repeat(2,1fr)}h2{font-size:26px}section{padding-top:46px}.abstract{text-align:left}}
"""

JS = r"""
(function(){
  const io = new IntersectionObserver(es => es.forEach(e => {
    const v = e.target;
    if (e.isIntersecting) { if (v.preload === 'none') v.preload = 'auto'; v.play().catch(()=>{}); } else v.pause();
  }), {threshold: 0.25});
  document.querySelectorAll('video[data-autoplay]').forEach(v => io.observe(v));

  // comparison rows: start together, restart together once every clip has ended
  const groups = {};
  document.querySelectorAll('video[data-group]').forEach(v => (groups[v.dataset.group] ||= []).push(v));
  function restart(g){ groups[g].forEach(v => { v.preload = 'auto'; v.currentTime = 0; v.play().catch(()=>{}); }); }
  Object.entries(groups).forEach(([g, vs]) => {
    let timer = null, visible = false;
    vs.forEach(v => v.addEventListener('ended', () => {
      if (vs.every(x => x.ended) && visible) { clearTimeout(timer); timer = setTimeout(() => restart(g), 1500); }
    }));
    new IntersectionObserver(es => es.forEach(e => {
      visible = e.isIntersecting;
      if (visible) restart(g); else { clearTimeout(timer); vs.forEach(v => v.pause()); }
    }), {threshold: 0.35}).observe(document.querySelector(`[data-cmp="${g}"]`));
  });
  document.querySelectorAll('[data-replay]').forEach(b => b.addEventListener('click', () => restart(b.dataset.replay)));

  const links = [...document.querySelectorAll('nav.toc a')];
  const so = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) links.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id));
  }), {rootMargin: '-45% 0px -50% 0px'});
  links.forEach(a => { const s = document.querySelector(a.getAttribute('href')); if (s) so.observe(s); });
})();
"""

ICON_PAPER = "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'><path d='M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z'/><path d='M14 3v6h6'/></svg>"
ICON_CODE = "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'><path d='m16 18 6-6-6-6M8 6l-6 6 6 6'/></svg>"

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-F28Q22D1LS"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-F28Q22D1LS');
  </script>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{TITLE}: {SUBTITLE}</title>
  <meta name="description" content="{TITLE}: {SUBTITLE}">
  <meta name="keywords" content="discrete flow matching, visuomotor policy, imitation learning, learning from demonstration, bimanual manipulation, robotics">
  <meta property="og:title" content="{TITLE}: {SUBTITLE}">
  <meta property="og:description" content="Continuous robot actions as discrete tokens, generated by a continuous-time Markov chain in 10 steps.">
  <meta property="og:image" content="{M}/posters/overview.jpg">
  <link rel="icon" href="./favicon.ico?">
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>{CSS}</style>
</head>
<body>

<header class="hero">
  <div class="wrap">
    <div class="eyebrow">Anonymous submission &middot; under review</div>
    <h1>{TITLE}</h1>
    <p class="subtitle">{SUBTITLE}</p>
    <div class="authors">Anonymous Authors</div>
    <div class="btns">
      <span class="btn off" title="Available after review">{ICON_PAPER} Paper (under review)</span>
      <span class="btn off" title="Coming soon">{ICON_CODE} Code (coming soon)</span>
    </div>
    <p class="tldr">DFMP represents continuous robot actions as discrete tokens and generates them with a continuous-time
      Markov chain: it keeps several valid behaviors and needs only 10 generation steps.</p>
  </div>
  <div class="wrap main-video" id="video">
    <video controls preload="metadata" playsinline poster="{M}/posters/overview.jpg">
      <source src="{M}/videos/overview.mp4" type="video/mp4"></video>
  </div>
</header>

<nav class="toc"><div class="wrap">
  <a href="#abstract">Abstract</a><a href="#real">Real robot</a><a href="#comparison">Comparison</a>
  <a href="#recovery">Recovery</a><a href="#multimodality">Multimodality</a><a href="#simulation">Simulation</a>
</div></nav>

<main class="wrap">

<section id="abstract">
  <h2>Abstract</h2>
  <div class="card"><p class="abstract">{ABSTRACT}</p></div>
</section>

<section id="real">
  <h2>Real-robot rollouts</h2>
  <p class="lead">Uncut autonomous runs of DFMP on a bimanual Franka setup. Between trials, the operator only resets the cups.</p>
  <div class="task-head"><h3>Cup Stacking</h3></div>
  <div class="pair">{real_vid('./stacking/cup_stacking1')}{real_vid('./stacking/cup_stacking2')}</div>
  <div class="task-head"><h3>Cup Placing</h3></div>
  <div class="pair">{real_vid('./placing/cup_placing1')}{real_vid('./placing/cup_placing2')}</div>
</section>

<section id="comparison">
  <h2>Flow Matching vs Diffusion Policy vs DFMP</h2>
  <p class="lead">The best policy of each method on the same task. Clips in a row play in sync.</p>
  {compare_block('stacking')}
  {compare_block('placing')}
</section>

<section id="recovery">
  <h2>Recovery</h2>
  <p class="lead">When a grasp fails, DFMP re-attempts it and still completes the task.</p>
  <div class="pair">
    <figure>{loop_vid(f'{M}/videos/recovery/stacking.mp4')}<figcaption>Cup Stacking: the grasp on the last cup misses; DFMP retries and completes the stack.</figcaption></figure>
    <figure>{loop_vid(f'{M}/videos/recovery/placing.mp4')}<figcaption>Cup Placing: the first grasp tips the cup over; DFMP re-grasps it and places it in the rack.</figcaption></figure>
  </div>
</section>

<section id="multimodality">
  <h2>Multimodal behavior</h2>
  <p class="lead">200 Push-T rollouts per policy from one shared initial state; colour marks time. Flow Matching and
    Diffusion Policy follow a single route, while DFMP spreads over several.</p>
  <div class="mm">
    <figure><figcaption>Initial state 1 <span>&middot; first 120 steps</span></figcaption>{loop_vid(f'{M}/videos/multimodal/pusht_fig5_state.mp4')}</figure>
    <figure><figcaption>Initial state 2 <span>&middot; 200 steps</span></figcaption>{loop_vid(f'{M}/videos/multimodal/pusht_second_state.mp4')}</figure>
  </div>
</section>

<section id="simulation">
  <h2>Simulation rollouts</h2>
  <p class="lead">DFMP on eight simulated tasks from Robomimic, Push-T, UR3 Block Push and Franka Kitchen (2&times; speed).</p>
  <div class="sim-grid">{sim_grid()}</div>
</section>

</main>

<footer><div class="wrap">This page is anonymized for double-blind review.</div></footer>
<script>{JS}</script>
</body>
</html>
"""

OUT.write_text(HTML)
print("wrote", OUT, len(HTML), "bytes")
