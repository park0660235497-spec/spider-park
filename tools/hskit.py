"""Shared upgrade kit for ม.4-6 (uni shell) labs: sound, graphics environment, mobile dock.
usage: python3 hskit.py <file.html>"""
import sys
SP = '/tmp/claude-0/-home-claude/47ceed5a-d5ff-5a5d-a420-b3a8b09a223d/scratchpad/'
F = sys.argv[1]
s = open(F, encoding='utf-8').read()
if 'const SFX = (function' in s: sys.exit('already patched: ' + F)
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit(f'COUNT {c}!={n} in {F}: {a[:110]}')
    s = s.replace(a, b)

# ---------- CSS ----------
CSS = """#dockbar{flex:1 1 100%;display:none;padding:10px;background:var(--surface);border:1px solid var(--line2);border-top:0;border-radius:0 0 var(--r-lg) var(--r-lg);box-sizing:border-box;min-width:0}
#dockbar.on{display:block}
#dockbar #dock .btn{min-height:48px!important;font-size:15.5px!important;padding:0 14px!important;flex:1 1 auto;justify-content:center;border-radius:12px}
#dockbar #dock .status{min-height:48px;display:inline-flex;align-items:center;justify-content:center;flex:1 1 auto;border:1.5px solid var(--line2);font-size:15.5px;border-radius:12px;box-sizing:border-box}
.stage.hasbar{border-radius:var(--r-lg) var(--r-lg) 0 0!important}
@media (pointer:coarse){.btn.sm{min-height:44px}.chip{min-height:44px}.ibtn{min-width:44px;min-height:44px}#pCtrl input,#helper input{font-size:16px!important;min-height:46px}.calc button{min-height:44px}}
@media (max-width:600px){.bubble .msg{font-size:13.5px;padding:8px 12px;line-height:1.45}.bubble{left:8px;right:8px;bottom:8px}.labels div{font-size:11px;padding:2px 8px}.camctl{top:8px;right:8px;gap:6px}.reschip{top:8px;left:8px;right:60px;max-width:none;width:auto;justify-content:space-between}.reschip .v{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
"""
k = s.rfind("</style>"); assert k > 0; s = s[:k] + CSS + s[k:]

# ---------- SFX ----------
SFX = open(SP + 'sfx_block.js', encoding='utf-8').read()
rep("/* ---------- PDF ---------- */", SFX + "\n/* ---------- PDF ---------- */")
rep("""  const act = a.dataset.act, v = a.dataset.v;
  if(act==='go') go(v);""", """  const act = a.dataset.act, v = a.dataset.v;
  if(act==='sfx'){ const m = SFX.toggle(); a.innerHTML = m ? SND_OFF : SND_ON; a.setAttribute('aria-label', m ? 'เปิดเสียง' : 'ปิดเสียง'); toast(m ? 'ปิดเสียงแล้ว' : 'เปิดเสียงแล้ว'); if(typeof Lab!=='undefined' && Lab.muted) Lab.muted(m); return; }
  if(act==='ans' || act==='pred') SFX.pick(); else if(!(act==='lab' && /^(cam|z(in|out))/.test(String(v)))) SFX.click();
  if(act==='go') go(v);""")
rep('data-v="camReset" aria-label="มุมมองเริ่มต้น">${ICON.cube}</button>', 'data-v="camReset" aria-label="มุมมองเริ่มต้น">${ICON.cube}</button>\n          <button class="ibtn" type="button" data-act="sfx" aria-label="${SFX.muted ? \'เปิดเสียง\' : \'ปิดเสียง\'}">${SFX.muted ? SND_OFF : SND_ON}</button>')
rep("st.a[k] = o; if(o!==q.a){ st.w[k] = (st.w[k] || 0) + 1; } else toast(", "st.a[k] = o; if(o!==q.a){ st.w[k] = (st.w[k] || 0) + 1; SFX.bad(); } else SFX.ok(), toast(")
rep("    return ch;\n  }\n  function refresh(){", "    if(ch) SFX.ok();\n    return ch;\n  }\n  function refresh(){")
rep("S.labDone[P.i] = true; P.celebrate = true; toast(", "S.labDone[P.i] = true; P.celebrate = true; SFX.done(); toast(")
rep("    try { S.ps = S.ps || {}; S.ps[P.i] = JSON.parse(JSON.stringify(P.s)); } catch(e){}\n    save(); refreshUI();",
    "    try { S.ps = S.ps || {}; S.ps[P.i] = JSON.parse(JSON.stringify(P.s)); } catch(e){}\n    if(P.warn && P.warn !== P.lastWarn) SFX.bad(); P.lastWarn = P.warn;\n    save(); refreshUI();")
rep("    stop(){ if(R){ R.active = false; if(R.ro) R.ro.disconnect(); } },", "    stop(){ SFX.amb({}); if(R){ R.active = false; if(R.ro) R.ro.disconnect(); } },")

# ---------- mobile dock ----------
rep("""  function dock(html){ const st = $('#stage'); if(!st) return; let d = $('#dock'); if(!d){ d = document.createElement('div'); d.id = 'dock'; d.style.cssText = 'position:absolute;top:10px;left:10px;right:64px;z-index:4;display:flex;flex-wrap:wrap;gap:6px;align-items:center'; st.appendChild(d); }
    if(d.dataset.h !== html){ d.innerHTML = html; d.dataset.h = html; } const hn = $('.hint', st); if(hn) hn.style.display = html ? 'none' : ''; }""",
"""  function dock(html){ const st = $('#stage'); if(!st) return; let d = $('#dock'); if(!d){ d = document.createElement('div'); d.id = 'dock'; st.appendChild(d); }
    const below = st.clientWidth < 700 && !st.classList.contains('full') && !document.body.classList.contains('fullon'); let bar = $('#dockbar');
    if(below && !bar){ bar = document.createElement('div'); bar.id = 'dockbar'; st.insertAdjacentElement('afterend', bar); }
    const host = below ? bar : st, mode = below ? 'b' : 's';
    if(d.parentNode !== host || d.dataset.m !== mode){ host.appendChild(d); d.dataset.m = mode; d.style.cssText = below ? 'display:flex;flex-wrap:wrap;gap:8px;align-items:stretch' : 'position:absolute;top:10px;left:10px;right:64px;z-index:4;display:flex;flex-wrap:wrap;gap:6px;align-items:center'; }
    if(bar){ const on = below && !!html; bar.classList.toggle('on', on); st.classList.toggle('hasbar', on); if(on){ const g = parseFloat(getComputedStyle(st.parentNode).rowGap) || 0; bar.style.marginTop = (-g - 1) + 'px'; } }
    if(d.dataset.h !== html){ d.innerHTML = html; d.dataset.h = html; } const hn = $('.hint', st); if(hn) hn.style.display = html ? 'none' : ''; }""")
rep("st.style.setProperty('--docky', ((d && d.offsetHeight ? d.offsetTop + d.offsetHeight : 52) + 10) + 'px');",
    "st.style.setProperty('--docky', ((d && d.offsetHeight && d.parentNode===st ? d.offsetTop + d.offsetHeight : 52) + 10) + 'px');")

# ---------- graphics environment ----------
rep("  const METAL = () => mat(0xB9C0CE, {metalness:.8, roughness:.3});", "  let ENVMAP = null;\n  const METAL = () => mat(0xC9CFDA, {metalness:.9, roughness:.22, envMap:ENVMAP, envMapIntensity:1});")
rep("  const GLASS = (op=.2) => new THREE.MeshStandardMaterial({color:0xDCEBFB, transparent:true, opacity:op, roughness:.05,", "  const GLASS = (op=.2) => new THREE.MeshStandardMaterial({color:0xDCEBFB, transparent:true, opacity:op, roughness:.05, envMap:ENVMAP, envMapIntensity:1.6, metalness:.1,")
rep("      const scene = new THREE.Scene(); scene.background = new THREE.Color(0xEDF1FA);",
"""      const scene = new THREE.Scene(); scene.background = new THREE.Color(0xEDF1FA);
      try{ renderer.physicallyCorrectLights = false;
        const bg = canvasTex(16, 256, (x)=>{ const g = x.createLinearGradient(0,0,0,256); g.addColorStop(0,'#CFDcF6'); g.addColorStop(.55,'#E9EEF9'); g.addColorStop(1,'#F6F2EC'); x.fillStyle = g; x.fillRect(0,0,16,256); }); scene.background = bg;
        const ec = canvasTex(512, 256, (x)=>{ const g = x.createLinearGradient(0,0,0,256); g.addColorStop(0,'#FFFFFF'); g.addColorStop(.42,'#DCE6F7'); g.addColorStop(.5,'#B9C2D6'); g.addColorStop(.62,'#8E8676'); g.addColorStop(1,'#5E564A'); x.fillStyle = g; x.fillRect(0,0,512,256);
          x.fillStyle = 'rgba(255,255,255,.95)'; [[40,30,90,60],[200,20,70,70],[330,34,110,50],[450,26,50,64]].forEach(r=>x.fillRect(...r)); x.fillStyle = 'rgba(255,236,200,.6)'; x.fillRect(120,50,40,30); });
        ec.mapping = THREE.EquirectangularReflectionMapping; const pm = new THREE.PMREMGenerator(renderer); ENVMAP = pm.fromEquirectangular(ec).texture; pm.dispose(); ec.dispose();
      }catch(_){ }""")
rep("      scene.add(new THREE.HemisphereLight(0xffffff, 0xC9D3EC, .85));\n      const sun = new THREE.DirectionalLight(0xffffff, .85); sun.position.set(4, 9, 6); sun.castShadow = true;\n      sun.shadow.mapSize.set(1024,1024);",
"""      scene.add(new THREE.HemisphereLight(0xffffff, 0xC9D3EC, .85));
      const sun = new THREE.DirectionalLight(0xFFF6E8, .85); sun.position.set(4, 9, 6); sun.castShadow = true;
      const fill = new THREE.DirectionalLight(0xBFD4FF, .22); fill.position.set(-6, 4, -5); scene.add(fill);
      { const coarse = window.matchMedia && matchMedia('(pointer:coarse)').matches; sun.shadow.radius = 3;
        const fl = new THREE.Mesh(new THREE.CircleGeometry(70, 48), new THREE.MeshStandardMaterial({map:canvasTex(512, 512, (x)=>{ x.fillStyle = '#A8A297'; x.fillRect(0,0,512,512); x.strokeStyle = 'rgba(120,112,100,.35)'; x.lineWidth = 3; for(let k=0;k<=512;k+=128){ x.beginPath(); x.moveTo(k,0); x.lineTo(k,512); x.moveTo(0,k); x.lineTo(512,k); x.stroke(); } }), roughness:.9}));
        fl.material.map.wrapS = fl.material.map.wrapT = THREE.RepeatWrapping; fl.material.map.repeat.set(36,36); fl.rotation.x = -Math.PI/2; fl.position.y = -2.6; fl.receiveShadow = false; scene.add(fl);
        scene.fog = new THREE.Fog(0xDCE3F2, 22, 75);
        const lm = mat(0x5A4630, {roughness:.7}); [[-4.4,-2.5],[4.4,-2.5],[-4.4,2.5],[4.4,2.5]].forEach(([x,z])=>{ const l = box(.22, 2.5, .22, lm, x, -1.45, z); scene.add(l); });
        scene.add(box(9.1,.32,.08, lm, 0, -.42, 2.62)); scene.add(box(9.1,.32,.08, lm, 0, -.42, -2.62));
        sun.shadow.mapSize.set(coarse ? 1024 : 2048, coarse ? 1024 : 2048); }""")
open(F, 'w', encoding='utf-8').write(s)
print('kit ok', F)
