// Real-tap test on Android Chrome emulation (Pixel 7): every dock button, ดูผล, rotate/zoom, 3D taps/drags, normal + fullscreen.
const {open} = require('./rt.js');
const fs = require('fs');
const [file, key, np, nq, specFile, tag, onlyParts] = process.argv.slice(2);
const SPEC = require(specFile);
(async()=>{
  const T = await open(file, key, +np, 'm', +nq); const p = T.p; const issues = []; const log = (...a)=>console.log(...a);
  const cam = async()=>JSON.stringify(await p.evaluate(()=>__cam()));
  const vp = p.viewportSize();
  const visibleIn = async sel => p.evaluate((sel)=>{ const el = document.querySelector(sel); if(!el) return 'missing'; const cs = getComputedStyle(el); if(cs.display==='none' || cs.visibility==='hidden' || el.hidden) return 'hidden'; const b = el.getBoundingClientRect(); if(b.width < 20 || b.height < 20) return 'tiny'; if(b.bottom > innerHeight + 2 || b.top < -2 || b.right > innerWidth + 2 || b.left < -2) return `offscreen ${Math.round(b.top)},${Math.round(b.bottom)} / ${innerHeight}`; const cx = b.left + b.width/2, cy = b.top + Math.min(b.height/2, 30); const t = document.elementFromPoint(cx, cy); if(t && !el.contains(t)) return 'covered by ' + (t.id || t.className || t.tagName); return 'ok'; }, sel);
  const objPt = async (expr, dy) => p.evaluate(([expr, dy])=>{ const P = __P(); const o = eval(expr); if(!o) return null; return __scr(o, dy); }, [expr, dy || 0]);
  for(const [pi, part] of SPEC.parts.entries()){
    if(onlyParts && !onlyParts.includes(String(pi))) continue;
    await T.part(pi); log(`\n=== part ${pi + 1} ===`);
    for(const mode of ['normal', 'full']){
      if(mode==='full'){ const fb = await p.$('#fullBtn'); await T.tap(fb); await p.waitForTimeout(700); }
      const st = await p.evaluate(()=>document.getElementById('stage').classList.contains('full')); if((mode==='full') !== st) issues.push(`p${pi+1} ${mode}: fullscreen state ${st}`);
      // dock buttons (real taps)
      const dvs = await p.$$eval('#dock [data-v]', els=>els.map(e=>e.dataset.v));
      for(const v of dvs){ if((part.skip || []).includes(v)) continue; const el = await p.$(`#dock [data-v="${v}"]`); if(!el) continue; const vis = await el.isVisible(); if(!vis){ issues.push(`p${pi+1} ${mode}: dock ${v} not visible`); continue; }
        const bb = await el.boundingBox(); if(bb.y + bb.height > vp.height + 1 || bb.y < 0){ if(mode==='full') issues.push(`p${pi+1} ${mode}: dock ${v} offscreen`); }
        const before = await p.evaluate(()=>JSON.stringify(__P().s) + document.getElementById('bubbleMsg').textContent);
        await T.tap(el); await p.waitForTimeout(150);
        const after = await p.evaluate(()=>JSON.stringify(__P().s) + document.getElementById('bubbleMsg').textContent);
        if(before===after && !(part.noop || []).includes(v)) issues.push(`p${pi+1} ${mode}: dock ${v} had no effect`); }
      // result chip
      const chip = await p.$('#resChip:not([hidden]) [data-act="resopen"]');
      if(chip){ await T.tap(chip); await p.waitForTimeout(400); const r = await visibleIn('#pRes'); if(r!=='ok') issues.push(`p${pi+1} ${mode}: ดูผล panel ${r}`); await T.shot(`rt-${tag}-p${pi+1}-${mode}-res.png`);
        const h = await p.$('#pRes h2'); if(h){ await T.tap(h); await p.waitForTimeout(300); } const c2 = await visibleIn('#resChip'); if(c2!=='ok') issues.push(`p${pi+1} ${mode}: chip after close ${c2}`); }
      else issues.push(`p${pi+1} ${mode}: no ดูผล chip`);
      // 3D actions (from the default camera)
      await T.fire('lab','camReset'); await p.waitForTimeout(400);
      for(const a of (part.obj || [])){
        const pt = await objPt(a.o, a.dy);
        const cov = pt ? await p.evaluate(([x,y])=>{ const t = document.elementFromPoint(x,y); return t && t.tagName==='CANVAS' ? '' : (t ? (t.id || t.className || t.tagName) : 'none'); }, [pt.x, pt.y]) : '';
        if(cov){ issues.push(`p${pi+1} ${mode}: obj ${a.o} covered by ${cov}`); continue; } if(!pt){ issues.push(`p${pi+1} ${mode}: obj ${a.o} missing`); continue; }
        if(pt.x < 0 || pt.x > vp.width || pt.y < 0 || pt.y > vp.height){ issues.push(`p${pi+1} ${mode}: obj ${a.o} off screen (${Math.round(pt.x)},${Math.round(pt.y)})`); continue; }
        const b0 = await p.evaluate(()=>JSON.stringify(__P().s));
        if(a.tap) await T.tapXY(pt.x, pt.y); else await T.swipe(pt.x, pt.y, pt.x + (a.dx || 0), pt.y + (a.dy2 || 0), 14);
        await p.waitForTimeout(250); const b1 = await p.evaluate(()=>JSON.stringify(__P().s)); const c1 = await p.evaluate(()=>__cam()[1]);
        if(b0===b1) issues.push(`p${pi+1} ${mode}: 3D ${a.tap ? 'tap' : 'drag'} ${a.o} had no effect`); if(!c1) issues.push(`p${pi+1} ${mode}: controls stuck disabled after ${a.o}`); }
      // rotate + zoom on empty area (top-left sky region of the stage)
      const sb = await T.stageBox(); const c0 = await cam(); await T.swipe(sb.x + sb.width*.12, sb.y + sb.height*.22, sb.x + sb.width*.45, sb.y + sb.height*.24); const c1 = await cam(); if(c0===c1) issues.push(`p${pi+1} ${mode}: rotate failed`);
      await T.pinch(sb.x + sb.width*.4, sb.y + sb.height*.3, 30, 100); const c2 = await cam(); if(c1===c2) issues.push(`p${pi+1} ${mode}: pinch zoom failed`);
      await p.evaluate(()=>{ const b = document.querySelector('[data-act="camReset"],[data-act="cam0"]'); });
      await T.shot(`rt-${tag}-p${pi+1}-${mode}.png`);
      if(mode==='full'){ const fb = await p.$('#fullBtn'); await T.tap(fb); await p.waitForTimeout(500); }
    }
  }
  log('\nISSUES', issues.length); issues.forEach(x=>log(' -', x)); log('errors', T.errs); await T.close();
})();
