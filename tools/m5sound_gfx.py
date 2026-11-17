import sys
F = '/home/claude/spider-park/site/lab/m5-sound.html'
s = open(F, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit(f'COUNT {c}!={n}: {a[:110]}')
    s = s.replace(a, b)
def block(start, end, new):
    global s
    i = s.index(start); j = s.index(end, i); s = s[:i] + new + s[j:]

# ---- shared models
block("  function makeFork(h){", "  function vib(g, a, t){", r"""  function woodTex(){ if(woodTex.t) return woodTex.t; woodTex.t = canvasTex(256, 256, (x)=>{ x.fillStyle = '#C89A62'; x.fillRect(0,0,256,256); let sd = 4; const r = ()=>{ sd = (sd*9301+49297)%233280; return sd/233280; };
      for(let y=0;y<256;y+=5){ x.strokeStyle = `rgba(90,55,20,${(.10 + r()*.2).toFixed(2)})`; x.lineWidth = 1 + r()*2.5; x.beginPath(); const ph = r()*6; x.moveTo(0,y); for(let q=0;q<=256;q+=16) x.lineTo(q, y + Math.sin(q/40 + ph)*2.5); x.stroke(); } }); return woodTex.t; }
  const WOOD = (c=0xFFFFFF) => new THREE.MeshStandardMaterial({map:woodTex(), roughness:.6, color:c});
  const RUBBER = () => mat(0x23262F, {roughness:.9});
  function makeFork(h){ const g = new THREE.Group(), m = METAL(); g.add(at(cyl(.014,.014,.16, m, 12), 0, h + .08, 0)); g.add(at(sph(.022, m, 12), 0, h + .17, 0));
    const br = new THREE.Mesh(new THREE.TorusGeometry(.04,.013,10,20,Math.PI), m); br.position.set(0, h, 0); br.rotation.z = Math.PI; br.scale.y = .001; g.add(br); g.add(at(box(.106,.026,.026, m), 0, h, 0));
    const pr = [-1,1].map(k=>{ const p = new THREE.Group(); p.add(at(box(.022, h, .026, m), 0, 0, 0)); p.add(at(cyl(.011,.011,.026, m, 10), 0, -h/2, 0)); p.children[1].rotation.x = Math.PI/2; p.position.set(k*.04, h/2, 0); g.add(p); return p; }); g.userData.pr = pr; g.userData.h = h; return g; }
  function makeMallet(){ const g = new THREE.Group(); const hd = cyl(.035,.035,.1, RUBBER(), 16); hd.rotation.z = Math.PI/2; hd.position.y = .3; g.add(hd); g.add(at(cyl(.011,.013,.3, WOOD(), 10), 0,.15,0)); return g; }
  function swing(m, t){ if(!m) return; const u = m.userData, k = u.t0==null ? 1 : (t - u.t0)/.32; if(k >= 1){ u.t0 = null; m.position.copy(u.restPos); m.rotation.set(Math.PI/2, 0, .4); return; } m.position.copy(u.hitPos); m.rotation.set(0, 0, .35 + .43*Math.sin(k*Math.PI)); }
""")
# ---- audio respects mute + strike click
rep("  function tone(fs, dur){ const c = ac(); if(!c) return null;", "  function tone(fs, dur){ SFX.tick(); if(SFX.muted) return null; const c = ac(); if(!c) return null;")

# ---- part 1
block("  function buildP1(){ const W = R.world;", "  function hit1(){", r"""  function buildP1(){ const W = R.world, DK = mat(0x2B3050, {roughness:.45, metalness:.3});
    const bs = box(.56,.035,.42, DK); bs.position.set(TX - .02, TABLE_Y + .0175, 0); W.add(bs); [[-.25,-.18],[.25,-.18],[-.25,.18],[.25,.18]].forEach(([x,z])=>W.add(at(cyl(.03,.03,.012, RUBBER(), 10), TX - .02 + x, TABLE_Y + .006, z)));
    W.add(at(cyl(.018,.018, TT - TABLE_Y + .1, METAL(), 12), TX - .2, (TT + TABLE_Y + .1)/2, -.12)); W.add(at(sph(.024, METAL(), 10), TX - .2, TT + .1, -.12));
    [TT - .15, TT - .8].forEach(y=>{ const c = new THREE.Group(); c.add(at(box(.05,.05,.05, DK), -.2,0,-.12)); const arm = cyl(.01,.01,.24, METAL(), 8); arm.rotation.z = Math.PI/2; arm.rotation.y = -.55; arm.position.set(-.1,0,-.06); c.add(arm); const rg = new THREE.Mesh(new THREE.TorusGeometry(.072,.009,8,24), METAL()); rg.rotation.x = Math.PI/2; c.add(rg); const kn = cyl(.014,.014,.05, RUBBER(), 8); kn.rotation.x = Math.PI/2; kn.position.set(-.2,0,-.075); c.add(kn); c.position.set(TX, y, 0); W.add(c); });
    W.add(at(cyl(.065,.065, TL, GLASS(.22), 32, true), TX, TT - TL/2, 0));
    [TT, TT - TL].forEach(y=>{ const r = new THREE.Mesh(new THREE.TorusGeometry(.065,.005,8,32), GLASS(.55)); r.rotation.x = Math.PI/2; r.position.set(TX, y, 0); W.add(r); });
    W.add(at(cyl(.03,.012,.06, GLASS(.4), 16), TX, TT - TL - .03, 0));
    P.water = cyl(.058,.058,1, TRANS(0x4FA3EA,.62), 28); W.add(P.water);
    P.wtop = cyl(.058,.058,.004, new THREE.MeshStandardMaterial({color:0xBFE3FF, transparent:true, opacity:.85, roughness:.05, envMap:ENVMAP, envMapIntensity:1.4}), 28); W.add(P.wtop);
    const st = canvasTex(64, 1024, (x,w,h)=>{ x.fillStyle = '#FFF6D8'; x.fillRect(0,0,w,h); x.fillStyle = '#1C2236'; x.font = '700 20px sans-serif'; for(let c=0;c<=100;c++){ const y = 4 + c*(h - 8)/100, L = c%10 ? (c%5 ? 12 : 20) : 30; x.fillRect(0, y - 1, L, 2); if(c%10===0 && c) x.fillText(String(c), 30, y + 7); } });
    W.add(at(box(.105, TL + .02, .012, mat(0xE8D9A8)), TX + .125, TT - TL/2, .012)); W.add(at(new THREE.Mesh(new THREE.PlaneGeometry(.1, TL), new THREE.MeshStandardMaterial({map:st, roughness:.7})), TX + .125, TT - TL/2, .02));
    P.labels.push({obj:P.water, dy:.0, text:()=>`L = ${(P.s.L*100).toFixed(1)} cm`});
    const rv = new THREE.Group(); rv.userData.id = 'res'; rv.add(cyl(.13,.1,.24, GLASS(.28), 28, true)); rv.add(at(cyl(.118,.095,.15, TRANS(0x4FA3EA,.6), 24), 0,-.04,0)); rv.add(at(cyl(.1,.1,.012, GLASS(.45), 24), 0,-.12,0));
    const rim = new THREE.Mesh(new THREE.TorusGeometry(.13,.007,8,28), GLASS(.6)); rim.rotation.x = Math.PI/2; rim.position.y = .12; rv.add(rim); rv.add(at(cyl(.02,.02,.05, GLASS(.4), 12), 0,-.15,0));
    const hd = new THREE.Mesh(new THREE.TorusGeometry(.06,.01,8,16,Math.PI), mat(0xF2994A,{roughness:.5})); hd.rotation.z = -Math.PI/2; hd.position.set(.14,0,0); rv.add(hd);
    rv.add(hitBox(.5,.55,.5,0)); W.add(rv); P.rv = rv;
    P.labels.push({obj:rv, dy:.25, text:()=>'ถังน้ำ (ลากขึ้นลง)'});
    P.hose = new THREE.Mesh(new THREE.BufferGeometry(), RUBBER()); P.hose.castShadow = true; W.add(P.hose);
    const fk = makeFork(.28); fk.userData.id = 'fork'; fk.add(hitBox(.3,.6,.3,.25)); fk.position.set(TX, TT + .04, 0); W.add(fk); P.fork = fk;
    P.mal = makeMallet(); P.mal.userData.restPos = V(TX + .42, TABLE_Y + .045, .22); P.mal.userData.hitPos = V(TX + .26, TT + .06, 0); W.add(P.mal); swing(P.mal, 0);
    P.labels.push({obj:fk, dy:.62, text:()=>`ส้อมเสียง ${P.s.f} Hz`});
    P.air = Array.from({length:44}, (_,k)=>{ const m = sph(.0085, new THREE.MeshBasicMaterial({color:0xF2994A, transparent:true, opacity:.85}), 6); m.userData = {u:(k + .5)/44, a:k*2.399, r:.012 + ((k*37)%29)/29*.036}; W.add(m); return m; });
    P.rg = rings(3, 0xF2994A);
    shadowAll(W); updP1();
  }
  function updP1(){ const s = P.s; if(!P.water) return; const wy = TT - s.L, bot = TT - TL; P.water.scale.y = Math.max(.001, wy - bot); P.water.position.set(TX, (wy + bot)/2, 0); P.wtop.position.set(TX, wy, 0);
    const ry = Math.max(TABLE_Y + .22, Math.min(TT + .1, wy + .03)); P.rv.position.set(RX, ry, 0);
    const cv = new THREE.CatmullRomCurve3([V(TX, bot - .06, 0), V(TX, TABLE_Y + .09, .06), V((TX + RX)/2, TABLE_Y + .03, .14), V(RX, TABLE_Y + .1, .06), V(RX, ry - .17, 0)]); P.hose.geometry.dispose(); P.hose.geometry = new THREE.TubeGeometry(cv, 36, .013, 8, false); }
  function airP1(t){ const s = P.s; if(!P.air) return; const on = s.ring > 0, a = amp1()*Math.min(1, s.ring/3), k = 2*Math.PI/lamT();
    P.air.forEach(m=>{ const u = m.userData, d = u.u*s.L, base = TT - d; const disp = on ? a*.03*Math.cos(k*(d + EC) - k*(s.L + EC) + Math.PI/2)*Math.sin(t*14) : 0;
      m.position.set(TX + Math.cos(u.a)*u.r, base + disp, Math.sin(u.a)*u.r); m.material.opacity = on ? .35 + .55*Math.min(1, a*1.6) : .22; }); }
""")
rep("  function hit1(){ const s = P.s; s.ring = 6;", "  function hit1(){ const s = P.s; if(P.mal) P.mal.userData.t0 = P.tt; s.ring = 6;")

# ---- part 2
block("    P.spk = [0,1].map(k=>{", "    P.labels.push({obj:P.spk[0], dy:.8,", r"""    P.spk = [0,1].map(k=>{ const g = new THREE.Group(); g.add(at(box(.42,.62,.4, WOOD(0x9A6A48)), 0,.31,0)); g.add(at(box(.012,.58,.36, mat(0x1A1C24,{roughness:.8})), .212,.31,0));
      const sur = new THREE.Mesh(new THREE.TorusGeometry(.13,.016,10,28), RUBBER()); sur.rotation.y = Math.PI/2; sur.position.set(.222,.25,0); g.add(sur);
      const cn = new THREE.Mesh(new THREE.ConeGeometry(.125,.07,28,1,true), mat(0x3A3F4E,{roughness:.6, side:THREE.DoubleSide})); cn.rotation.z = Math.PI/2; cn.position.set(.19,.25,0); g.add(cn);
      const cap = sph(.04, mat(0x15171D,{roughness:.35}), 14); cap.scale.x = .5; cap.position.set(.175,.25,0); g.add(cap); g.userData.cn = cn; g.userData.cap = cap;
      const tr = new THREE.Mesh(new THREE.TorusGeometry(.05,.01,8,20), METAL()); tr.rotation.y = Math.PI/2; tr.position.set(.222,.49,0); g.add(tr); const td = sph(.035, mat(0x2A2D38,{roughness:.3}), 12); td.scale.x = .45; td.position.set(.215,.49,0); g.add(td);
      [[-.16,-.15],[.16,-.15],[-.16,.15],[.16,.15]].forEach(([x,z])=>g.add(at(cyl(.025,.03,.02, RUBBER(), 10), x,.01,z)));
      g.position.set(XS0 - .2, y, k ? -.55 : 0); W.add(g); return g; });
""")
block("    const mt = new THREE.Group(); mt.userData.id = 'meter';", "    P.labels.push({obj:mt, dy:1.05,", r"""    const mt = new THREE.Group(); mt.userData.id = 'meter'; [0,1,2].forEach(q=>{ const l = cyl(.009,.012,.34, RUBBER(), 6); const a = q/3*Math.PI*2; l.position.set(Math.cos(a)*.09,.15,Math.sin(a)*.09); l.rotation.set(Math.sin(a)*.55, 0, -Math.cos(a)*.55); mt.add(l); });
    mt.add(at(cyl(.016,.016,.3, METAL(), 10), 0,.43,0)); mt.add(at(cyl(.03,.03,.04, RUBBER(), 12), 0,.3,0));
    mt.add(at(box(.15,.3,.06, mat(0xF2994A,{roughness:.45})), 0,.72,0)); mt.add(at(box(.13,.1,.012, mat(0x20242E)), 0,.76,.032)); mt.add(at(cyl(.02,.03,.08, mat(0x20242E), 12), 0,.9,0));
    [[-.035,.63],[.035,.63],[0,.6]].forEach(([x,yy])=>mt.add(at(cyl(.014,.014,.012, mat(0xFFFFFF), 10), x,yy,.032))); mt.children.slice(-3).forEach(b=>b.rotation.x = Math.PI/2);
    const mic = sph(.055, mat(0x2A2A2E,{roughness:1}), 16); mic.position.set(0,.97,0); mt.add(mic);
    P.dtex = canvasTex(256,128,()=>{}); mt.add(at(new THREE.Mesh(new THREE.PlaneGeometry(.118,.085), new THREE.MeshBasicMaterial({map:P.dtex})), 0,.76,.0385)); mt.add(hitBox(.55,1.15,.55,.5)); W.add(mt); P.meter = mt;
""")
rep("    P.labels.push({obj:mt, dy:1.05, text:()=>`r = ${P.s.r.toFixed(1)} m`});\n    P.rg = rings(4, 0xF2994A);\n    updP2();",
    "    P.labels.push({obj:mt, dy:1.12, text:()=>`r = ${P.s.r.toFixed(1)} m`});\n    P.rg = rings(6, 0xF2994A);\n    shadowAll(W); updP2();")
rep("c.fillStyle = '#C8E6C9'; c.fillRect(0,0,256,128); c.fillStyle = '#1B3A20'; c.font = '700 60px monospace'; c.textAlign = 'center'; c.fillText(beta(s.r, s.n).toFixed(1), 128, 88);",
    "c.fillStyle = '#0E1A12'; c.fillRect(0,0,256,128); c.fillStyle = '#7CFFA0'; c.font = '700 64px monospace'; c.textAlign = 'center'; c.fillText(beta(s.r, s.n).toFixed(1), 128, 80); c.font = '600 26px sans-serif'; c.fillStyle = '#56C97A'; c.fillText('dB', 128, 116);")

# ---- part 3
block("    P.fks = [XA, XB].map((x,k)=>{", "    P.clay = sph(", r"""    P.fks = [XA, XB].map((x,k)=>{ const g = new THREE.Group(); g.userData.id = 'fk' + k; const wd = WOOD(0xC88A5C);
      g.add(at(box(.7,.02,.32, wd), 0,.29,0)); g.add(at(box(.7,.02,.32, wd), 0,.03,0)); g.add(at(box(.7,.28,.02, wd), 0,.16,.15)); g.add(at(box(.7,.28,.02, wd), 0,.16,-.15)); g.add(at(box(.02,.28,.3, wd), -.34,.16,0));
      g.add(at(box(.66,.24,.28, mat(0x2B1A10,{roughness:1})), -.015,.16,0)); [[-.28,-.12],[.28,-.12],[-.28,.12],[.28,.12]].forEach(([fx,fz])=>g.add(at(cyl(.025,.025,.02, RUBBER(), 10), fx,.01,fz)));
      const f = makeFork(.42); f.position.set(-.05,.3,0); g.add(f); g.userData.f = f; g.add(at(cyl(.03,.035,.02, METAL(), 12), -.05,.31,0)); g.add(hitBox(.8,1.2,.5,.5));
      if(k) g.rotation.y = Math.PI; g.position.set(x, TABLE_Y, 0); W.add(g); return g; });
    P.mal = makeMallet(); W.add(P.mal);
""")
rep("P.clay.position.set(-.05 + .04, .3 + .3, .03); P.fks[1].add(P.clay);", "P.clay.scale.set(1.1,.8,1); P.clay.position.set(-.05 - .04, .3 + .36, .0); P.fks[1].add(P.clay);")
rep("    P.rg = rings(4, 0xE25555);\n    updP3();", "    P.rg = rings(5, 0xE25555);\n    shadowAll(W); updP3();")
rep("  function hit3(){ const s = P.s, fb = Math.abs(FA - fBn()); s.ring = 4;", "  function hit3(){ const s = P.s, fb = Math.abs(FA - fBn()); if(P.mal) P.mal.userData.t3 = P.tt; s.ring = 4;")

# ---- tick
rep("        vib(P.fork, env, P.tt); if(P.snd && AC)", "        vib(P.fork, env, P.tt); airP1(P.tt); swing(P.mal, P.tt); if(P.snd && AC)")
rep("      else if(P.i===1 && P.spk){ runRings(P.rg, P.tt, true, .15, .9, r=>{ r.rotation.y = Math.PI/2; r.position.set(XS0 + .05, TABLE_Y + .4, 0); }); }",
    "      else if(P.i===1 && P.spk){ runRings(P.rg, P.tt, true, .15, 1.6, r=>{ r.rotation.y = Math.PI/2; const f = (P.tt*.8 + r.userData.ph) % 1; r.position.set(XS0 + .05 + f*1.1, TABLE_Y + .25, 0); r.material.opacity = .5*(1 - f)*(1 - f); });\n        const pu = Math.sin(P.tt*38)*.012; P.spk.forEach(g=>{ g.userData.cn.position.x = .19 + pu; g.userData.cap.position.x = .175 + pu; }); }")
rep("        P.fks.forEach(g=>vib(g.userData.f, env, P.tt));", "        P.fks.forEach(g=>vib(g.userData.f, env, P.tt)); if(P.mal){ const u = P.mal.userData, k = u.t3==null ? 1 : (P.tt - u.t3)/.5; if(k >= 1){ u.t3 = null; P.mal.position.set(-.15, TABLE_Y + .04, .5); P.mal.rotation.set(Math.PI/2, 0, 1.2); } else { const sd = k < .5 ? -1 : 1, q = Math.sin((k < .5 ? k : k - .5)*2*Math.PI); P.mal.position.set(sd*(XB - .32), TABLE_Y + .42, 0); P.mal.rotation.set(0, 0, -sd*(.8 + q*.4)); } }")
# Lab api: mute stops running tone
rep("    stop(){ SFX.amb({}); if(R){ R.active = false; if(R.ro) R.ro.disconnect(); } },", "    stop(){ SFX.amb({}); if(P) stopTone(P.snd); if(R){ R.active = false; if(R.ro) R.ro.disconnect(); } },\n    muted(m){ if(m && P){ stopTone(P.snd); P.snd = null; } },")
rep("    {pos:V(1.5,2.1,4.1), tgt:V(0.05,.95,0)},", "    {pos:V(1.2,1.95,3.3), tgt:V(0.02,.95,0)},")
rep("    {pos:V(-.9,2.6,6.2), tgt:V(-.9,.5,0)},", "    {pos:V(-.65,2.1,5.3), tgt:V(-.65,.55,0)},")
rep("const el = R.renderer.domElement, a = el.clientWidth/Math.max(1, el.clientHeight); if(a < 1){ const k = Math.min(1.25, .8/a);", "const el = R.renderer.domElement, a = el.clientWidth/Math.max(1, el.clientHeight), c = CAMS[P.i]; if(a < (c.na || .8)/1.02){ const k = Math.min(c.nk || 1.25, (c.na || .8)/a);")
rep("{pos:V(-.65,2.1,5.3), tgt:V(-.65,.55,0)},", "{pos:V(-.65,2.1,5.3), tgt:V(-.65,.55,0), na:1.25, nk:1.75},")
rep("    {pos:V(0,1.7,3.8), tgt:V(0,.6,0)}", "    {pos:V(0,1.7,3.8), tgt:V(0,.6,0), na:1.02, nk:1.45}")
rep("P.labels.push({obj:fk, dy:.62, text:()=>`ส้อมเสียง ${P.s.f} Hz`});", "P.labels.push({obj:fk, dy:.5, text:()=>`ส้อมเสียง ${P.s.f} Hz`});")
rep("{pos:V(1.2,1.95,3.3), tgt:V(0.02,.95,0)},", "{pos:V(1.2,2.0,3.3), tgt:V(0.02,1.02,0), na:.86},")
open(F, 'w', encoding='utf-8').write(s)
print('sound gfx ok')
