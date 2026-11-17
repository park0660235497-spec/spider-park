// real-interaction test helpers (Android Chrome emulation: Pixel 7)
const { chromium, devices } = require('playwright');
const L='/tmp/claude-0/-home-claude/47ceed5a-d5ff-5a5d-a420-b3a8b09a223d/scratchpad/libs/node_modules/';
const MAP={'three.min.js':L+'three/build/three.min.js','OrbitControls.js':L+'three/examples/js/controls/OrbitControls.js','html2canvas.min.js':L+'html2canvas/dist/html2canvas.min.js','jspdf.umd.min.js':L+'jspdf/dist/jspdf.umd.min.js'};
async function open(file, key, np, mode, nq){
  const b=await chromium.launch({args:['--use-gl=swiftshader','--ignore-gpu-blocklist','--autoplay-policy=no-user-gesture-required']});
  const c=await b.newContext(mode==='m'?{...devices['Pixel 7'], deviceScaleFactor:1}:{viewport:{width:1280,height:860}});
  await c.route(/cdnjs|jsdelivr|googleapis|gstatic/, r=>{ const u=r.request().url(); const k=Object.keys(MAP).find(k=>u.endsWith(k)); return k? r.fulfill({path:MAP[k],contentType:'application/javascript'}) : r.abort(); });
  const p=await c.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.addInitScript(([key,np,nq])=>{ if(!localStorage.getItem(key)) localStorage.setItem(key, JSON.stringify({pre:{a:Array(nq).fill(0),done:true,score:5},guideRead:true,labDone:Array(np).fill(false),pred:Array(np).fill(null),nick:'ต้น',miss:Object.fromEntries([...Array(np).keys()].map(i=>[i,{}])),sheet:{},sheetDone:false,post:{a:Array(nq).fill(null),done:false,score:null}})); },[key,np,nq||20]);
  await p.goto('http://localhost:8765/lab/'+file,{waitUntil:'load'}); await p.waitForTimeout(900);
  const cdp = mode==='m' ? await c.newCDPSession(p) : null;
  const T = {b,p,errs,cdp,mode};
  T.tap = async (sel)=>{ const el = typeof sel==='string' ? await p.$(sel) : sel; if(!el) throw new Error('no el '+sel); await el.scrollIntoViewIfNeeded(); const bb = await el.boundingBox(); const x=bb.x+bb.width/2, y=bb.y+bb.height/2;
    if(mode==='m'){ await p.touchscreen.tap(x,y); } else await p.mouse.click(x,y); await p.waitForTimeout(350); };
  T.tapXY = async (x,y)=>{ if(mode==='m') await p.touchscreen.tap(x,y); else await p.mouse.click(x,y); await p.waitForTimeout(350); };
  T.swipe = async (x0,y0,x1,y1,steps=12)=>{ if(mode!=='m'){ await p.mouse.move(x0,y0); await p.mouse.down(); for(let k=1;k<=steps;k++) await p.mouse.move(x0+(x1-x0)*k/steps, y0+(y1-y0)*k/steps); await p.mouse.up(); await p.waitForTimeout(300); return; }
    const tp = (type,x,y)=>cdp.send('Input.dispatchTouchEvent',{type, touchPoints: type==='touchEnd'?[]:[{x,y,id:1}]});
    await tp('touchStart',x0,y0); for(let k=1;k<=steps;k++){ await tp('touchMove',x0+(x1-x0)*k/steps,y0+(y1-y0)*k/steps); await p.waitForTimeout(16); } await tp('touchEnd'); await p.waitForTimeout(300); };
  T.pinch = async (cx,cy,d0,d1,steps=10)=>{ const tp=(type,d)=>cdp.send('Input.dispatchTouchEvent',{type,touchPoints:type==='touchEnd'?[]:[{x:cx-d,y:cy,id:1},{x:cx+d,y:cy,id:2}]}); await tp('touchStart',d0); for(let k=1;k<=steps;k++){ await tp('touchMove',d0+(d1-d0)*k/steps); await p.waitForTimeout(16);} await tp('touchEnd'); await p.waitForTimeout(300); };
  T.canvasHash = async ()=>{ const el = await p.$('#stage canvas'); const buf = await el.screenshot(); return require('crypto').createHash('md5').update(buf).digest('hex'); };
  T.stageBox = async ()=>(await p.$('#stage canvas')).boundingBox();
  T.fire = async (act,v)=>{ await p.evaluate(([act,v])=>{ const b=document.createElement('button'); b.dataset.act=act; if(v!==undefined) b.dataset.v=v; document.getElementById('main').appendChild(b); b.click(); b.remove(); },[act,v]); await p.waitForTimeout(250); };
  T.shot = async n=>{ await p.waitForTimeout(250); await p.screenshot({path:n}); };
  T.S = ()=>p.evaluate(K=>JSON.parse(localStorage.getItem(K)),key);
  T.msg = ()=>p.$eval('#bubbleMsg',e=>e.textContent).catch(()=>'');
  // enter a part through the real UI
  T.part = async i=>{ await T.fire('part',String(i)); await p.waitForTimeout(900); const w = await p.$('#whyModal:not([hidden]) .btn'); if(w){ const bs = await p.$$('#whyModal:not([hidden]) button'); await T.tap(bs[bs.length-1]); }
    const ch = await p.$('[data-act="pred"]'); if(ch) await T.tap(ch); await p.evaluate(()=>{ document.getElementById('stage').scrollIntoView({block:'start'}); }); await p.waitForTimeout(400); };
  T.dockBtn = async v => { const el = await p.$(`#dock [data-v="${v}"]`); if(!el) throw new Error('no dock btn '+v); await T.tap(el); };
  T.close = ()=>b.close();
  return T;
}
module.exports = {open};
