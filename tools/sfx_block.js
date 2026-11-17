/* ---------- sound effects + speech (Web Audio, no files) ---------- */
const SPK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/></svg>';
const SND_ON = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/></svg>';
const SND_OFF = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9z"/><path d="M16 9l5 6M21 9l-5 6"/></svg>';
const SFX = (function(){
  let ac = null, master = null, noise = null, ch = {}, last = {}, muted = false;
  try { muted = localStorage.getItem('parkilab-sfx-mute') === '1'; } catch(_){}
  const VOL = .32;
  function unlock(){
    if(ac){ if(ac.state === 'suspended') ac.resume(); return; }
    try {
      ac = new (window.AudioContext || window.webkitAudioContext)();
      master = ac.createGain(); master.gain.value = muted ? 0 : VOL; master.connect(ac.destination);
      const len = ac.sampleRate*2, buf = ac.createBuffer(1, len, ac.sampleRate), d = buf.getChannelData(0);
      for(let i=0;i<len;i++) d[i] = Math.random()*2 - 1; noise = buf;
      const mk = (type, freq, q, lfo) => { const src = ac.createBufferSource(); src.buffer = noise; src.loop = true;
        const f = ac.createBiquadFilter(); f.type = type; f.frequency.value = freq; f.Q.value = q;
        const g = ac.createGain(); g.gain.value = 0; src.connect(f); f.connect(g); g.connect(master); src.start();
        if(lfo){ const o = ac.createOscillator(), og = ac.createGain(); o.frequency.value = lfo; og.gain.value = freq*.35; o.connect(og); og.connect(f.frequency); o.start(); }
        return g; };
      const buzz = () => { const o = ac.createOscillator(); o.type = 'sawtooth'; o.frequency.value = 210; const v = ac.createOscillator(), vg = ac.createGain(); v.frequency.value = 9; vg.gain.value = 14; v.connect(vg); vg.connect(o.frequency); v.start();
        const f = ac.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = 900; const g = ac.createGain(); g.gain.value = 0; o.connect(f); f.connect(g); g.connect(master); o.start(); return g; };
      ch = { rain: mk('bandpass', 2600, .6), boil: mk('lowpass', 520, 1.2, 3.1), wind: mk('bandpass', 420, 1.4, .18), hiss: mk('highpass', 5200, .7), sizzle: mk('highpass', 2800, 1.5, 7), buzz: buzz() };
    } catch(_){ ac = null; }
  }
  addEventListener('pointerdown', unlock, {capture:true, passive:true});
  addEventListener('keydown', unlock, {capture:true});
  function tone(f0, f1, dur, type='sine', vol=.5, delay=0){
    if(!ac || muted) return; const t = ac.currentTime + delay, o = ac.createOscillator(), g = ac.createGain();
    o.type = type; o.frequency.setValueAtTime(f0, t); if(f1) o.frequency.exponentialRampToValueAtTime(f1, t + dur);
    g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(vol, t + .012); g.gain.exponentialRampToValueAtTime(.001, t + dur);
    o.connect(g); g.connect(master); o.start(t); o.stop(t + dur + .02);
  }
  const AMB = {rain:.5, boil:.9, wind:.55, hiss:.12, sizzle:.18, buzz:.07};
  return {
    unlock,
    get muted(){ return muted; },
    toggle(){ muted = !muted; try { localStorage.setItem('parkilab-sfx-mute', muted ? '1' : '0'); } catch(_){} if(master) master.gain.setTargetAtTime(muted ? 0 : VOL, ac.currentTime, .05); if(!muted){ unlock(); tone(660, 990, .12, 'sine', .4); } return muted; },
    click(){ tone(820, 620, .05, 'triangle', .25); },
    pick(){ tone(380, 620, .09, 'sine', .35); },
    drop(){ tone(240, 140, .12, 'sine', .45); },
    ok(){ tone(660, 0, .12, 'sine', .4); tone(990, 0, .18, 'sine', .35, .09); },
    bad(){ tone(220, 170, .22, 'square', .12); },
    done(){ [523, 659, 784, 1046].forEach((f,k)=>tone(f, 0, .22, 'triangle', .35, k*.09)); },
    pop(){ tone(900 + Math.random()*700, 1500, .04, 'sine', .12); },
    tick(){ tone(2400 + Math.random()*800, 0, .03, 'square', .06); },
    speak(w){ try{ const u = new SpeechSynthesisUtterance(w); u.lang = 'en-US'; u.rate = .8; const vs = speechSynthesis.getVoices().filter(x=>/^en/i.test(x.lang)); if(vs.length) u.voice = vs.find(x=>/en-US/i.test(x.lang)) || vs[0]; speechSynthesis.cancel(); speechSynthesis.speak(u); } catch(_){ toast('อุปกรณ์นี้อ่านออกเสียงไม่ได้'); } },
    amb(lv){ if(!ac) return; Object.keys(ch).forEach(k=>{ const v = Math.max(0, Math.min(1, (lv && lv[k]) || 0))*AMB[k]; if(Math.abs((last[k]||0) - v) > .01){ last[k] = v; ch[k].gain.setTargetAtTime(v, ac.currentTime, .25); } }); }
  };
})();
