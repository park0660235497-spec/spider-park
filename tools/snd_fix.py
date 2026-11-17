import sys
F = sys.argv[1]; s = open(F, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit(f'COUNT {c}!={n}: {a[:140]}')
    s = s.replace(a, b)

# quieter UI clicks
rep("  const VOL = .32;", "  const VOL = .15;")

# ---- tone: louder, longer, with a short metallic strike overtone
rep("""  function tone(fs, dur){ SFX.tick(); if(SFX.muted) return null; const c = ac(); if(!c) return null; const out = []; fs.forEach(f=>{ const o = c.createOscillator(), g = c.createGain(); o.type = 'sine'; o.frequency.value = f; g.gain.setValueAtTime(0, c.currentTime); g.gain.linearRampToValueAtTime(.12, c.currentTime + .02); g.gain.exponentialRampToValueAtTime(.0005, c.currentTime + dur); o.connect(g); g.connect(c.destination); o.start(); o.stop(c.currentTime + dur + .05); out.push({o, g}); }); return out; }""",
"""  function tone(fs, dur, pk){ if(SFX.muted) return null; const c = ac(); if(!c) return null; const out = [], t0 = c.currentTime, v = pk || .35;
    fs.forEach(f=>{ const o = c.createOscillator(), g = c.createGain(); o.type = 'sine'; o.frequency.value = f; g.gain.setValueAtTime(0, t0); g.gain.linearRampToValueAtTime(v, t0 + .01); g.gain.setTargetAtTime(v*.55, t0 + .05, 1.2); g.gain.setTargetAtTime(0, t0 + dur*.55, dur*.18); o.connect(g); g.connect(c.destination); o.start(); o.stop(t0 + dur + .4); out.push({o, g, v});
      const o2 = c.createOscillator(), g2 = c.createGain(); o2.type = 'sine'; o2.frequency.value = f*6.27; g2.gain.setValueAtTime(v*.22, t0); g2.gain.exponentialRampToValueAtTime(.0003, t0 + .35); o2.connect(g2); g2.connect(c.destination); o2.start(); o2.stop(t0 + .4); });
    return out; }""")

# ---- part 1: 8 forks, longer tube, louder resonance
rep("const TT = TABLE_Y + 1.25, TX = -.3, TL = 1.0, EC = .012, FK = [512, 384], RX = .45;",
    "const TT = TABLE_Y + 1.32, TX = -.3, TL = 1.12, LMAX = TL - .05, EC = .012, FK = [256, 288, 320, 341, 384, 427, 480, 512], RX = .45, RING1 = 12, RING3 = 9;")
rep("if(x > .96) break;", "if(x > LMAX) break;")
rep("s.L = Math.max(.03, Math.min(.96, Math.round(L*1000)/1000)); checkRes(tol);", "s.L = Math.max(.03, Math.min(LMAX, Math.round(L*1000)/1000)); checkRes(tol);")
rep("s.L = Math.max(.03, Math.min(.96, Math.round((TT - pt.y + .03)*1000)/1000)); updP1(); }", "s.L = Math.max(.03, Math.min(LMAX, Math.round((TT - pt.y + .03)*1000)/1000)); updP1(); }")
rep("for(let c=0;c<=100;c++){ const y = 4 + c*(h - 8)/100,", "for(let c=0;c<=110;c++){ const y = 4 + c*(h - 8)/110,")
rep("x.fillRect(0, y - 1, L, 2); if(c%10===0 && c) x.fillText(String(c), 30, y + 7); } });", "x.fillRect(0, y - 1, L, 2); if(c%10===0 && c) x.fillText(String(c), 30, y + 7); } });\n    const TLR = 1.10;")
rep("W.add(at(box(.105, TL + .02, .012, mat(0xE8D9A8)), TX + .125, TT - TL/2, .012)); W.add(at(new THREE.Mesh(new THREE.PlaneGeometry(.1, TL), new THREE.MeshStandardMaterial({map:st, roughness:.7})), TX + .125, TT - TL/2, .02));",
    "W.add(at(box(.105, TLR + .02, .012, mat(0xE8D9A8)), TX + .125, TT - TLR/2, .012)); W.add(at(new THREE.Mesh(new THREE.PlaneGeometry(.1, TLR), new THREE.MeshStandardMaterial({map:st, roughness:.7})), TX + .125, TT - TLR/2, .02));")
# fork rack
rep("    P.air = Array.from({length:44},", """    // rack holding the 8 tuning forks: tap one to mount it on the tube
    const rk = new THREE.Group(), RW = .96; rk.add(at(box(RW, .07, .16, WOOD(0xB07A4A)), 0, .035, 0)); P.rk = [];
    P.rkTex = canvasTex(1024, 96, ()=>{}); const lp = new THREE.Mesh(new THREE.PlaneGeometry(RW, .09), new THREE.MeshBasicMaterial({map:P.rkTex, transparent:true})); lp.position.set(0, .04, .0805); rk.add(lp);
    FK.forEach((f,k)=>{ const g = makeFork(.15); g.scale.setScalar(.85); g.userData.id = 'rk:' + f; g.position.set(-RW/2 + RW/16 + k*RW/8, .07, 0); g.add(hitBox(.12,.5,.25,.15)); rk.add(g); P.rk.push(g); });
    rk.position.set(.05, TABLE_Y, .62); rk.rotation.y = -.12; W.add(rk);
    P.labels.push({obj:rk, dy:.42, text:()=>'ชุดส้อมเสียง (แตะเพื่อเลือก)'});
    P.air = Array.from({length:44},""")
rep("  function updP1(){ const s = P.s; if(!P.water) return;", """  function drawRack(){ if(!P.rkTex) return; const c = P.rkTex.userData.c, x = c.getContext('2d'), w = c.width, h = c.height; x.clearRect(0,0,w,h);
    FK.forEach((f,k)=>{ const cx = (k + .5)*w/8, on = f===P.s.f; x.fillStyle = on ? '#F2994A' : 'rgba(255,255,255,.92)'; x.beginPath(); x.roundRect ? x.roundRect(cx - 54, 10, 108, 76, 18) : x.rect(cx - 54, 10, 108, 76); x.fill(); x.fillStyle = on ? '#fff' : '#1C2236'; x.font = '700 40px sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(String(f), cx, 50); });
    P.rkTex.needsUpdate = true; (P.rk || []).forEach(g=>g.visible = g.userData.id !== 'rk:' + P.s.f); }
  function pickFork(f){ const s = P.s; if(!FK.includes(f) || s.f===f) return; s.f = f; s.ring = 0; stopTone(P.snd); P.snd = null; drawRack(); SFX.pick(); P.say = `ติดตั้งส้อมเสียง ${f} Hz แล้ว แตะส้อมเสียงบนท่อเพื่อเคาะ แล้วปรับระดับน้ำหาตำแหน่งดังที่สุดครับ`; }
  function updP1(){ const s = P.s; if(!P.water) return; if(P.rkF !== s.f){ P.rkF = s.f; drawRack(); }""")
rep("s.ring = 6; stopTone(P.snd); P.snd = tone([s.f], 6);", "s.ring = RING1; stopTone(P.snd); P.snd = tone([s.f], RING1, .6);")
rep("const was = s.ring > 0; s.ring = Math.max(0, s.ring - dt); const env = Math.min(1, s.ring/3), a = amp1();",
    "const was = s.ring > 0; s.ring = Math.max(0, s.ring - dt); const env = Math.pow(s.ring/RING1, .8), a = amp1();")
rep("g.gain.setTargetAtTime((.01 + .2*a)*env, AC.currentTime, .03); }); }", "g.gain.setTargetAtTime((.1 + .5*a)*env, AC.currentTime, .04); }); }")
rep("const on = s.ring > 0, a = amp1()*Math.min(1, s.ring/3),", "const on = s.ring > 0, a = amp1()*Math.min(1, s.ring/4),")
rep("a = s.ring > 0 ? amp1()*Math.min(1, s.ring/3) : 0, bars", "a = s.ring > 0 ? amp1()*Math.min(1, s.ring/4) : 0, bars")
rep("""    else if(v==='fk') act(()=>{ s.f = s.f===FK[0] ? FK[1] : FK[0]; s.ring = 0; stopTone(P.snd); P.snd = null; P.say = `เปลี่ยนเป็นส้อมเสียง ${s.f} Hz แล้ว เคาะใหม่ครับ`; });""",
    """    else if(v==='fk') act(()=>pickFork(FK[(FK.indexOf(s.f) + 1) % FK.length]));
    else if(v.startsWith('fk:')) act(()=>pickFork(+v.slice(3)));""")
rep("if(d.id==='fork') action('hit'); else if(d.id && d.id.startsWith('fk')) action('hit3'); };",
    "if(d.id==='fork') action('hit'); else if(d.id && d.id.startsWith('rk:')) action('fk:' + d.id.slice(3)); else if(d.id && d.id.startsWith('fk')) action('hit3'); };")

# ---- part 3: longer ring, live monitor (1 s window), counting consistent
rep("s.ring = 4; stopTone(P.snd); P.snd = tone([FA, fBn()], 4); s.heard[s.clay ? 'c' : 'n'] = 1; s.last = {fb, clay:s.clay}; drawMon();",
    "s.ring = RING3; stopTone(P.snd); P.snd = tone([FA, fBn()], RING3, .3); s.heard[s.clay ? 'c' : 'n'] = 1; s.last = {fb, clay:s.clay}; P.sw = {t0:P.tt, clay:s.clay}; drawMon();")
rep("const env = Math.min(1, s.ring/2), fb = s.last ? s.last.fb : 0, e2 = env*Math.abs(Math.cos(Math.PI*fb*(4 - s.ring)));",
    "const env = Math.pow(s.ring/RING3, .7), fb = s.last ? s.last.fb : 0, e2 = env*Math.abs(Math.cos(Math.PI*fb*(RING3 - s.ring)));")
rep("const fbv = P.s.last ? P.s.last.fb : 0, e = Math.abs(Math.cos(Math.PI*fbv*(4 - P.s.ring)));", "const fbv = P.s.last ? P.s.last.fb : 0, e = Math.abs(Math.cos(Math.PI*fbv*(RING3 - P.s.ring)));")
# live monitor drawing
rep("""      x.strokeStyle = col; x.lineWidth = 2; x.beginPath(); for(let px=0;px<=w-40;px++){ const t = px/(w - 40), e = Math.abs(Math.cos(Math.PI*fb*t)), yv = mid + 6 + Math.sin(t*2*Math.PI*90)*e*(hh/2 - 30); px ? x.lineTo(20 + px, yv) : x.moveTo(20 + px, yv); } x.stroke(); };""",
"""      const lv = P.sw && s.ring > 0 && P.sw.clay===(name!=='A + B'), el = lv ? P.tt - P.sw.t0 : 1e9, cur = lv ? el % 1 : -1, env = lv ? .35 + .65*Math.pow(s.ring/RING3, .7) : 1, ph = lv ? P.tt*55 : 0;
      x.strokeStyle = col; x.lineWidth = 2; x.globalAlpha = lv && el < 1 ? .25 : 1; x.beginPath(); for(let px=0;px<=w-40;px++){ const t = px/(w - 40), e = Math.abs(Math.cos(Math.PI*fb*t)), yv = mid + 6 + Math.sin(t*2*Math.PI*90 + ph)*e*(hh/2 - 30)*env; px ? x.lineTo(20 + px, yv) : x.moveTo(20 + px, yv); } x.stroke(); x.globalAlpha = 1;
      if(lv){ if(el < 1){ x.lineWidth = 2.5; x.beginPath(); for(let px=0;px<=(w-40)*cur;px++){ const t = px/(w - 40), e = Math.abs(Math.cos(Math.PI*fb*t)), yv = mid + 6 + Math.sin(t*2*Math.PI*90 + ph)*e*(hh/2 - 30)*env; px ? x.lineTo(20 + px, yv) : x.moveTo(20 + px, yv); } x.stroke(); }
        const cx = 20 + (w - 40)*cur; x.strokeStyle = 'rgba(255,255,255,.85)'; x.lineWidth = 2; x.beginPath(); x.moveTo(cx, y0 + 34); x.lineTo(cx, y0 + hh - 4); x.stroke(); } };""")
rep("x.fillText('0', 20, h - 10); x.fillText('เวลา 1 วินาที', w/2, h - 10); x.fillText('1 s', w - 30, h - 10); P.mtex.needsUpdate = true; }",
    "x.fillText('0', 24, h - 10); x.fillText('เวลา 1 วินาที (นับยอดใน 1 วินาที)', w/2, h - 10); x.fillText('1 s', w - 30, h - 10); P.mtex.needsUpdate = true; }")
# animate monitor while ringing (throttled)
rep("P.fks.forEach(g=>vib(g.userData.f, env, P.tt));", "P.fks.forEach(g=>vib(g.userData.f, env, P.tt)); P.mT = (P.mT || 0) + dt; if(P.mT > .05 && (s.ring > 0 || P.mLive)){ P.mT = 0; drawMon(); P.mLive = s.ring > 0; }")
# scope in result panel: 1 s, same as monitor
rep("for(let k=0;k<=4;k++) x.fillText((k*.5).toFixed(1) + (k===4 ? ' s' : ''), Math.min(w - 22, Math.max(18, k*w/4)), h - 8);",
    "for(let k=0;k<=4;k++) x.fillText((k*.25).toFixed(2).replace(/0$/,'') + (k===4 ? ' s' : ''), Math.min(w - 22, Math.max(22, k*w/4)), h - 8);")
rep("for(let i=0;i<w;i+=2){ const t = i/w*2, e = Math.abs(Math.cos(Math.PI*l.fb*t))", "for(let i=0;i<w;i+=2){ const t = i/w, e = Math.abs(Math.cos(Math.PI*l.fb*t))")
rep("res = `<h2>กราฟเสียงรวม 2 วินาที${", "res = `<h2>กราฟเสียงรวม 1 วินาที${")
rep("else if(Math.abs(x - 2*fb) < .05 || Math.abs(x - fb*2) < .05 || Math.abs(x - fb/2) < .05) P.warn = 'กราฟยาว 2 วินาทีครับ นับจังหวะดังแล้วหารด้วย 2';",
    "else if(Math.abs(x - fb/2) < .05) P.warn = 'กราฟยาว 1 วินาทีครับ นับยอดทั้งหมดในกราฟ';")
rep("P.warn = hint(['นับยอดสว่างของกราฟใน 1 วินาที (2 ช่องตาราง) ครับ', 'f_b = จำนวนจังหวะดังต่อวินาที ดูกราฟอีกครั้งครับ']);",
    "P.warn = hint(['นับยอดของเส้นสีฟ้าบนจอ (กราฟยาว 1 วินาที) ครับ', 'ความถี่บีตส์ = จำนวนจังหวะดังต่อวินาที ดูกราฟอีกครั้งครับ']);")
open(F, 'w', encoding='utf-8').write(s); print('snd ok')
