"""ม.5 ไฟฟ้าสถิต round 2: arrows, cables, precipitator (part 3), rod button in stage, capacitor area, no bulb, pointer robustness."""
import sys
F = sys.argv[1]; s = open(F, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit(f'COUNT {c}!={n}: {a[:160]}')
    s = s.replace(a, b)
def between(a, b, new, keep_b=True):
    global s
    i = s.index(a); j = s.index(b, i + len(a))
    s = s[:i] + new + (s[j:] if keep_b else s[j + len(b):])
def line_starting(prefix):
    i = s.index(prefix); j = s.index('\n', i); return s[i:j]

# ================= DATA =================
rep("key:'parkilab-m5-static-v2'", "key:'parkilab-m5-static-v3'")
rep("ทำการทดลองหยดน้ำมันของมิลลิแกน ทำให้อิเล็กโทรสโคป", "ศึกษาเครื่องกรองฝุ่นไฟฟ้าสถิต ทำให้อิเล็กโทรสโคป")
rep("และความต่างศักย์ที่ทำให้หยดน้ำมันลอยนิ่ง'", "ฝุ่นที่ถูกดักเมื่อเปลี่ยนความต่างศักย์และความเร็วลม การกางของแผ่นโลหะบาง และประจุบนตัวเก็บประจุ'")
rep("'หาประจุของหยดน้ำมันจาก qE = mg และสรุปว่าประจุไฟฟ้ามีค่าเป็นจำนวนเต็มเท่าของ e'", "'อธิบายหลักการทำงานของเครื่องกรองฝุ่นไฟฟ้าสถิต และคำนวณสนามไฟฟ้าเฉลี่ย E = {V|d}'")
rep("'หาความจุของตัวเก็บประจุจาก C = {Q|V} และอธิบายผลของระยะห่างแผ่น'", "'หาความจุของตัวเก็บประจุจาก C = {Q|V} และอธิบายผลของระยะห่างและพื้นที่แผ่น'")
rep("'ตอนที่ 3 <b>หมุนปุ่มสีส้ม</b>บนแหล่งจ่ายไฟ (ลากขึ้น/ลง) หรือกดปุ่ม +/− ดูหยดน้ำมันผ่านกล้องจนลอยนิ่ง'", "'ตอนที่ 3 <b>หมุนปุ่มสีส้ม</b>บนแหล่งจ่ายไฟแรงสูง (ลากขึ้น/ลง) และ<b>แตะพัดลม</b>เปลี่ยนความเร็วลม ดูฝุ่นที่ถูกดัก'")
rep("'ตอนที่ 5 <b>ลากแผ่นขวา</b>เปลี่ยนระยะห่าง และหมุนปุ่มบนแหล่งจ่ายไฟ อ่านประจุจากคูลอมบ์มิเตอร์'", "'ตอนที่ 5 <b>ลากแผ่นสีฟ้า</b>เปลี่ยนระยะห่าง <b>แตะแผ่นสีแดง</b>เปลี่ยนขนาดแผ่น และหมุนปุ่มบนแหล่งจ่ายไฟ อ่านประจุจากคูลอมบ์มิเตอร์'")

rep(line_starting("  {q:'ในการทดลองของมิลลิแกน หยดน้ำมันลอยนิ่งเมื่อใด'"),
    "  {q:'เครื่องกรองฝุ่นไฟฟ้าสถิตดักฝุ่นได้เพราะอะไร', o:['ฝุ่นได้รับประจุแล้วถูกแรงไฟฟ้าดึงไปติดแผ่นโลหะ','ฝุ่นถูกแม่เหล็กในแผ่นดูด','ฝุ่นถูกความร้อนจากลวดเผา','ฝุ่นตกลงเพราะน้ำหนักของตัวเอง'], a:0, why:'ลวดแรงสูงให้ประจุแก่ฝุ่น สนามไฟฟ้าทำให้เกิดแรง F = qE ดึงฝุ่นไปติดแผ่นโลหะที่ต่อดิน'},")
rep(line_starting("  {q:'หยดน้ำมันมวล m ลอยนิ่งระหว่างแผ่นห่าง d"),
    "  {q:'ลวดกับแผ่นโลหะห่างกัน 0.10 m ความต่างศักย์ 20 kV สนามไฟฟ้าเฉลี่ยเท่าใด', o:['2 × 10⁵ V/m','2 × 10³ V/m','200 V/m','2 × 10⁶ V/m'], a:0, why:'E = {V|d} = {20 000|0.10} = 2 × 10⁵ V/m'},")
rep(line_starting("  {q:'ผลการทดลองของมิลลิแกนสรุปได้ว่าอย่างไร'"),
    "  {q:'ข้อใดใช้หลักไฟฟ้าสถิตแบบเดียวกับเครื่องกรองฝุ่นไฟฟ้าสถิต', o:['การพ่นสีรถยนต์ด้วยไฟฟ้าสถิต','เตารีดไฟฟ้า','หม้อหุงข้าวไฟฟ้า','พัดลมตั้งโต๊ะ'], a:0, why:'ละอองสีได้รับประจุแล้วถูกดูดไปติดชิ้นงานที่ต่อดิน เหมือนฝุ่นถูกดูดไปติดแผ่นโลหะ'},")

i = s.index("  {k:'ตอนที่ 3', t:'การทดลองหยดน้ำมันของมิลลิแกน'"); j = s.index("  {k:'ตอนที่ 4'", i)
s = s[:i] + """  {k:'ตอนที่ 3', t:'เครื่องกรองฝุ่นไฟฟ้าสถิต', d:'เปิดไฟแรงสูงให้ลวดตรงกลางท่อ ดูฝุ่นได้รับประจุแล้วถูกดูดไปติดแผ่นโลหะ ปรับความต่างศักย์และความเร็วลม แล้ววัดร้อยละของฝุ่นที่ดักได้', time:'ประมาณ 15 นาที', bg:'#FDF3E6',
   pred:{q:"ถ้าเพิ่มความต่างศักย์ระหว่างลวดกับแผ่นโลหะ ฝุ่นที่ออกจากปลายท่อจะเป็นอย่างไร", o:["น้อยลง", "มากขึ้น", "เท่าเดิม"], a:0}, why:{"why": "โรงไฟฟ้าและโรงงานใช้เครื่องกรองฝุ่นไฟฟ้าสถิตดักฝุ่นในควันก่อนปล่อยออกสู่อากาศ เป็นการนำความรู้ไฟฟ้าสถิตไปใช้ลดฝุ่น PM2.5", "find": "ร้อยละของฝุ่นที่ดักได้เมื่อเปลี่ยนความต่างศักย์และความเร็วลม และสนามไฟฟ้าเฉลี่ยระหว่างลวดกับแผ่น", "how": "ลวดตรงกลางต่อกับไฟแรงสูงขั้วลบ ทำให้ฝุ่นที่ผ่านใกล้ลวดได้รับประจุลบ สนามไฟฟ้าระหว่างลวดกับแผ่นโลหะที่ต่อดินทำให้เกิดแรง F = qE ดึงฝุ่นไปติดแผ่น สนามเฉลี่ย E = {V|d}", "steps": ["หมุนปุ่มบนแหล่งจ่ายไฟแรงสูงเพิ่ม kV ดูฝุ่น", "อ่านฝุ่นขาเข้าและขาออก หาร้อยละที่ดักได้", "แตะพัดลมเปลี่ยนความเร็วลมที่ kV เดิม", "คำนวณ E = {V|d}"]}, refl:{"q": "ทำไมลมพัดเร็วขึ้นแล้วดักฝุ่นได้น้อยลง", "o": ["ฝุ่นอยู่ในสนามไฟฟ้าเป็นเวลาสั้นลง จึงเคลื่อนไปถึงแผ่นไม่ทัน", "ลมแรงทำให้สนามไฟฟ้าลดลง", "ลมพัดประจุออกจากลวดหมด"], "a": 0, "why": "แรงไฟฟ้าทำให้ฝุ่นเคลื่อนเข้าหาแผ่นด้วยอัตราเร็วค่าหนึ่ง ถ้าลมพาฝุ่นผ่านท่อเร็วขึ้น เวลาที่อยู่ในท่อลดลง ฝุ่นบางส่วนจึงหลุดออกไปก่อนถึงแผ่น", "hint": "ฝุ่นต้องใช้เวลาเคลื่อนไปถึงแผ่น"},
   miss:[['eff','ดักฝุ่นได้อย่างน้อย 90%'],['spd','เทียบความเร็วลม 2 ระดับ (kV เท่าเดิม)'],['E3','คำนวณสนามไฟฟ้าเฉลี่ย E']]},
""" + s[j:]

rep("['dd','เปลี่ยนระยะห่างแผ่นแล้ววัดอีกครั้ง']]}", "['dd','เปลี่ยนระยะห่างแผ่นแล้ววัดอีกครั้ง'],['aa','เปลี่ยนขนาดแผ่นแล้ววัดอีกครั้ง']]}")
rep('"steps": ["ตั้งระยะห่าง d ไว้ แล้วเปลี่ยน V วัดประจุ 3 ค่า", "คำนวณ C = {Q|V}", "เปลี่ยนระยะห่าง d ที่ V เดิม แล้ววัดประจุ", "กด ⚡ คายประจุผ่านหลอดไฟ ดูพลังงานที่สะสม"]',
    '"steps": ["ตั้งระยะห่าง d ไว้ แล้วเปลี่ยน V วัดประจุ 3 ค่า", "คำนวณ C = {Q|V}", "เปลี่ยนระยะห่าง d ที่ V เดิม แล้ววัดประจุ", "แตะแผ่นสีแดงเปลี่ยนขนาดแผ่น A แล้ววัดประจุ"]')
rep('"find": "ประจุบนแผ่นที่ความต่างศักย์และระยะห่างต่าง ๆ ความจุ C และผลของระยะห่างแผ่น"', '"find": "ประจุบนแผ่นที่ความต่างศักย์ ระยะห่าง และขนาดแผ่นต่าง ๆ ความจุ C และผลของระยะห่างและขนาดแผ่น"')

# PART_ART[2]
i = s.index('const PART_ART = ['); arts = s[i:s.index('\n];', i)]; old = arts.split('`,\n')[2]
s = s.replace(old, """  `<svg width="200" height="110" viewBox="0 0 200 110" aria-hidden="true"><rect x="20" y="24" width="160" height="62" rx="6" fill="#EEF4FB" stroke="#9AA3B5"/><rect x="34" y="30" width="132" height="6" fill="#8A93A8"/><rect x="34" y="74" width="132" height="6" fill="#8A93A8"/><path d="M28 55 H172" stroke="#2F6FED" stroke-width="2.5"/>${[48,70,92,114,136].map((x,k)=>`<circle cx="${x}" cy="${k%2 ? 64 : 46}" r="3.5" fill="#7A5A3A"/><path d="M${x} ${k%2 ? 67 : 43} V${k%2 ? 72 : 38}" stroke="#2F6FED" stroke-width="1.5"/>`).join('')}<text x="8" y="60" font-size="13" fill="#7A5A3A">ฝุ่น</text><text x="176" y="20" font-size="12" fill="#2F6FED">−</text></svg>""")

i = s.index("{title:'ตอนที่ 3 การทดลองหยดน้ำมันของมิลลิแกน'"); j = s.index("{title:'ตอนที่ 4", i)
s = s[:i] + """{title:'ตอนที่ 3 เครื่องกรองฝุ่นไฟฟ้าสถิต', cols:['kV · ความเร็วลม','ฝุ่นขาเข้า · ขาออก · ร้อยละที่ดักได้'], rows:[
    ['p3a','kV ที่ดักได้อย่างน้อย 90%','.....................................................'],
    ['p3b','ความเร็วลม 2 ระดับ (kV เท่าเดิม)','.....................................................'],
    ['p3c','สนามไฟฟ้าเฉลี่ย E (V/m)','.....................................................'],
    ['p3d','ลมพัดเร็วขึ้น ฝุ่นที่ดักได้',['ลดลง','เพิ่มขึ้น']]], concl:'p3s', cq:'อธิบายหลักการทำงานของเครื่องกรองฝุ่นไฟฟ้าสถิต และยกตัวอย่างการนำไฟฟ้าสถิตไปใช้ประโยชน์อีก 1 ตัวอย่าง'},
  """ + s[j:]
rep("    ['p5c','ความจุ C (pF)','.....................................................'],", "    ['p5c','ความจุ C (pF)','.....................................................'],\n    ['p5e','A 2 ค่า (V และ d เท่าเดิม)','.....................................................'],")

g0 = s.index('const GUIDE = ['); gi = s.index('{"bal"', g0); gj = s.index('}, {"near"', gi)
s = s[:gi] + """{"eff": ["[data-v^=\\"hv:\\"]", "หมุนปุ่มสีส้มบนแหล่งจ่ายไฟแรงสูง หรือกด kV +/− จนดักฝุ่นได้อย่างน้อย 90% ครับ", [], ""], "spd": ["[data-v=\\"sp\\"]", "แตะพัดลมหรือกดปุ่มลม เปลี่ยนความเร็วลมที่ kV เดิมครับ", [], ""], "E3": ["#ev3", "คำนวณ E = V/d (d = 0.10 m) ตอบเป็น V/m ครับ", [], "ช่องคำนวณจะขึ้นเมื่อมีข้อมูลในตารางแล้ว ทำข้อที่มี ▶ ทำต่อ ก่อนครับ"]""" + s[gj:]
rep('"dd": ["[data-v^=\\"cd:\\"]", "เปลี่ยนระยะห่างแผ่น d ที่ V เดิม แล้ววัดประจุครับ", [], ""]}',
    '"dd": ["[data-v^=\\"cd:\\"]", "เปลี่ยนระยะห่างแผ่น d ที่ V เดิม แล้ววัดประจุครับ", [], ""], "aa": ["[data-v=\\"ca\\"]", "แตะแผ่นสีแดงหรือกดปุ่มขนาดแผ่น เปลี่ยน A ที่ V และ d เดิม แล้ววัดประจุครับ", [], ""]}')

e0 = s.index('const ENDQ = ['); ei = s.index(" [{k:'e', q:'ประจุของหยดน้ำมัน", e0); ej = s.index(" [{k:'cons'", ei)
s = s[:ei] + """ [{k:'how', q:'ฝุ่นไปติดที่แผ่นโลหะได้อย่างไร', o:[['charge','ฝุ่นได้รับประจุจากลวด แล้วถูกแรงไฟฟ้าดึงไปที่แผ่น'],['wind','ลมพัดฝุ่นไปชนแผ่นเอง'],['mag','แผ่นโลหะเป็นแม่เหล็กดูดฝุ่น']], a:'charge',
   h:['ดูสีของฝุ่นเมื่อผ่านใกล้ลวด','ปิดไฟแรงสูงแล้วฝุ่นยังติดแผ่นไหม'], r:[['field','สนามไฟฟ้าระหว่างลวดกับแผ่นทำให้เกิดแรง F = qE กับฝุ่นที่มีประจุ'],['grav','น้ำหนักของฝุ่นทำให้ฝุ่นตกลงบนแผ่น'],['heat','ความร้อนจากลวดเผาฝุ่นให้ติดแผ่น']], ra:'field',
   hr:['ฝุ่นที่ไม่มีประจุจะมีแรงไฟฟ้าไหม','F = qE'], why:'ฝุ่นได้รับประจุลบจากลวดแรงสูง สนามไฟฟ้าระหว่างลวดกับแผ่นที่ต่อดินทำให้เกิดแรง F = qE ดึงฝุ่นไปติดแผ่น'},
  {k:'spd', q:'ที่ความต่างศักย์เท่าเดิม ถ้าลมพัดเร็วขึ้น ร้อยละของฝุ่นที่ดักได้เป็นอย่างไร', o:[['less','ลดลง'],['more','เพิ่มขึ้น'],['same','เท่าเดิม']], a:'less',
   h:['เทียบแถวที่ kV เท่ากันแต่ความเร็วลมต่างกัน','ดูฝุ่นที่หลุดออกปลายท่อ'], r:[['time','ฝุ่นอยู่ในสนามไฟฟ้าเป็นเวลาสั้นลง จึงเคลื่อนไปถึงแผ่นไม่ทัน'],['force','ลมแรงทำให้สนามไฟฟ้าลดลง'],['charge','ลมพัดประจุออกจากลวดหมด']], ra:'time',
   hr:['ฝุ่นต้องใช้เวลาเคลื่อนไปถึงแผ่น','สนามไฟฟ้าขึ้นกับ V และ d ไม่ขึ้นกับลม'], why:'ลมเร็วขึ้น ฝุ่นผ่านท่อเร็วขึ้น เวลาที่ถูกแรงไฟฟ้าดึงลดลง ฝุ่นบางส่วนจึงหลุดออกไปก่อนถึงแผ่น'}],
""" + s[ej:]
rep("""   hr:['ประจุลดลงหรือเพิ่มขึ้นเมื่อ d มากขึ้น','ε₀ และ A คงที่'], why:'C = ε₀A/d ระยะห่างเพิ่ม ความจุลดลง ที่ V เท่าเดิมจึงเก็บประจุได้น้อยลง'}]""",
"""   hr:['ประจุลดลงหรือเพิ่มขึ้นเมื่อ d มากขึ้น','ε₀ และ A คงที่'], why:'C = ε₀A/d ระยะห่างเพิ่ม ความจุลดลง ที่ V เท่าเดิมจึงเก็บประจุได้น้อยลง'},
  {k:'area', q:'ใช้แผ่นโลหะขนาดใหญ่ขึ้น (V และ d เท่าเดิม) ประจุที่เก็บได้เป็นอย่างไร', o:[['more','มากขึ้น'],['less','น้อยลง'],['same','เท่าเดิม']], a:'more',
   h:['เทียบแถวที่ V และ d เท่ากันแต่ A ต่างกัน','C = ε₀A/d'], r:[['prop','C = ε₀A/d ความจุแปรผันตรงกับพื้นที่แผ่น จึงเก็บประจุได้มากขึ้น'],['volt','แผ่นใหญ่ทำให้ความต่างศักย์เพิ่มขึ้น'],['dist','แผ่นใหญ่ทำให้แผ่นอยู่ห่างกันมากขึ้น']], ra:'prop',
   hr:['A อยู่ด้านบนของเศษส่วน','A เพิ่ม 2 เท่า C เพิ่มกี่เท่า'], why:'C = ε₀A/d พื้นที่แผ่นเพิ่ม ความจุเพิ่มตาม ที่ V เท่าเดิมจึงเก็บประจุ Q = CV ได้มากขึ้น'}]""")

# ================= LAB CODE =================
# robust pointer end + cable helper
rep("  const crackle = () =>", """  function cable(a, b, c, sag, r){ const pts = []; for(let k=0;k<=16;k++){ const t = k/16, p = a.clone().lerp(b, t); p.y -= (sag==null ? .25 : sag)*4*t*(1 - t); p.y = Math.max(TABLE_Y + .012, p.y); pts.push(p); } return tube(pts, c, r || .011); }
  const crackle = () =>""")

# part 1 arrows centred on the spheres, always visible
rep("P.fa = [arrow(0xE25555), arrow(0x5B8DEF)];", "P.fa = [arrow(0xE25555), arrow(0x5B8DEF)]; P.fa.forEach(a=>{ [a.line, a.cone].forEach(o=>{ o.material.depthTest = false; o.renderOrder = 7; }); });")
rep("P.fa[0].position.set(xa - .09, SY, 0); P.fa[0].setDirection(V(-1,0,0)); P.fa[0].setLength(L, .07, .05); P.fa[1].position.set(XB, SY + .12, 0); P.fa[1].setDirection(V(1,0,0)); P.fa[1].setLength(L, .07, .05);",
    "P.fa[0].position.set(xa, SY, 0); P.fa[0].setDirection(V(-1,0,0)); P.fa[0].setLength(L + .08, .07, .05); P.fa[1].position.set(XB, SY, 0); P.fa[1].setDirection(V(1,0,0)); P.fa[1].setLength(L + .08, .07, .05);")

# part 2 cables
rep("""    [[-h, 0xE25555, -.25], [h, 0x5B8DEF, .25]].forEach(([x, c, ox])=>{ W.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([V(x, PY + .4, -.45), V(x - .3, PY + .5, -.6), V(-1.35 + ox, TABLE_Y + .42, -.6)]), new THREE.LineBasicMaterial({color:c}))); });""",
    """    [[-h, 0xE25555, -.3], [h, 0x5B8DEF, -.18]].forEach(([x, c, ox])=>cable(V(x, PY - .38, -.42), V(-1.35 + ox, TABLE_Y + .1, -.6 + .25), c, .3));""")
rep("    P.lead = new THREE.Line(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({color:0xE25555})); W.add(P.lead);", "    P.lead = null;")
rep("    P.lead.geometry.setFromPoints([V(s.px, PY + .65, s.pz), V((s.px + 1.1)/2, PY + .5, (s.pz + .6)/2), V(.78, TABLE_Y + .45, .7)]); }",
    "    const lk = s.px.toFixed(3) + '|' + s.pz; if(P.leadK !== lk){ P.leadK = lk; if(P.lead) R.world.remove(P.lead); P.lead = cable(V(s.px, PY + .65, s.pz), V(.78, TABLE_Y + .2, .7), 0xE25555, .55, .008); } }")

# ---- part 3: electrostatic precipitator (replaces Millikan)
P3 = r"""  /* ===== part 3: electrostatic precipitator ===== */
  const VC = 8, VMAX = 40, DW = .10, SPD = [1,2,3], PCY = TABLE_Y + .62, PL = 1.6, PZ = .2, NP3 = 170;
  const eta3 = (kv, u) => kv <= VC ? 0 : 1 - Math.exp(-2*((kv - VC)/10)**2/u);
  function buildP3(){ const W = R.world, s = P.s;
    // duct (glass) on stands
    W.add(at(box(2.2, .5, .5, GLASS(.13)), 0, PCY, 0));
    [-1.1, 1.1].forEach(x=>{ const fr = new THREE.Mesh(new THREE.TorusGeometry(.33,.018,6,4), mat(0x9AA3B5,{metalness:.6, roughness:.3})); fr.rotation.set(0, Math.PI/2, Math.PI/4); fr.scale.set(1,1,1); fr.position.set(x, PCY, 0); W.add(fr); });
    [-.85, .85].forEach(x=>{ W.add(at(box(.06, PCY - .25 - TABLE_Y, .06, mat(0x9AA3B5,{metalness:.6, roughness:.3})), x, TABLE_Y + (PCY - .25 - TABLE_Y)/2, -.18)); W.add(at(box(.06, PCY - .25 - TABLE_Y, .06, mat(0x9AA3B5,{metalness:.6, roughness:.3})), x, TABLE_Y + (PCY - .25 - TABLE_Y)/2, .18)); });
    // collecting plates (grounded) + discharge wire (−)
    P.pm3 = new THREE.MeshStandardMaterial({color:0xC9CFDA, metalness:.75, roughness:.35, envMap:ENVMAP, side:THREE.DoubleSide});
    [-PZ - .012, PZ + .012].forEach(z=>W.add(at(box(PL, .42, .012, P.pm3), 0, PCY, z)));
    P.wm = new THREE.MeshStandardMaterial({color:0xD8DEEA, metalness:.8, roughness:.25, emissive:0x5AA0FF, emissiveIntensity:0, envMap:ENVMAP});
    const wr = cyl(.007,.007, PL + .3, P.wm, 8); wr.rotation.z = Math.PI/2; wr.position.set(0, PCY, 0); W.add(wr); P.wire = wr;
    P.cor = new THREE.Mesh(new THREE.CylinderGeometry(.05,.05, PL, 16, 1, true), new THREE.MeshBasicMaterial({color:0x7FB8FF, transparent:true, opacity:0, depthWrite:false, blending:THREE.AdditiveBlending})); P.cor.rotation.z = Math.PI/2; P.cor.position.set(0, PCY, 0); W.add(P.cor);
    P.labels.push({obj:wr, dy:.3, text:()=>'ลวดไฟแรงสูง (−) · แผ่นเก็บฝุ่นต่อดิน'});
    // fan at the inlet (tap to change wind speed)
    const fan = new THREE.Group(); fan.userData.id = 'fan'; fan.userData.hy = 0; const ring = new THREE.Mesh(new THREE.TorusGeometry(.24,.02,8,32), mat(0x2B3050)); ring.rotation.y = Math.PI/2; fan.add(ring);
    P.blade = new THREE.Group(); for(let k=0;k<4;k++){ const b = box(.012,.2,.07, mat(0xF2994A,{roughness:.4})); b.position.y = .11; const p = new THREE.Group(); p.add(b); p.rotation.x = k*Math.PI/2; b.rotation.y = .5; P.blade.add(p); } P.blade.add(sph(.035, mat(0x2B3050), 12)); fan.add(P.blade);
    fan.add(at(box(.06, PCY - TABLE_Y, .06, mat(0x2B3050)), 0, -(PCY - TABLE_Y)/2, 0)); fan.add(at(box(.3,.03,.3, mat(0x2B3050)), 0, -(PCY - TABLE_Y) + .015, 0));
    fan.add(hitBox(.4,.7,.7,0)); fan.position.set(-1.38, PCY, 0); W.add(fan); P.fan = fan;
    P.labels.push({obj:fan, dy:.36, text:()=>`พัดลม ระดับ ${P.s.u}`});
    // dust sensors (in / out)
    const sens = (x, lbl) => { const g = new THREE.Group(); g.add(at(box(.22,.16,.1, mat(0xF2C94C,{roughness:.45})), 0,0,0)); const d = lcd(.18,.07); d.position.set(0,.01,.051); g.add(d); g.position.set(x, PCY + .38, .2); W.add(g); W.add(at(cyl(.008,.008,.14, METAL(), 6), x, PCY + .25, .2)); g.userData.d = d; return g; };
    P.sIn = sens(-.95); P.sOut = sens(.95);
    // high-voltage supply
    const ps = makePS(.1, -.95, 0, true); P.vd = ps.userData.d; P.kn = ps.userData.kn; P.kn.userData.hy = 0;
    P.labels.push({obj:ps, dy:.58, text:()=>'แหล่งจ่ายไฟแรงสูง'});
    cable(ps.localToWorld(V(-.18,.1,.25)), V(-.95, PCY, 0), 0x22263A, .2, .01);
    cable(ps.localToWorld(V(-.3,.1,.25)), V(.6, TABLE_Y + .02, -.3), 0x2E9E5B, .05, .01); W.add(at(box(.2,.02,.2, mat(0x3E8E5A)), .6, TABLE_Y + .01, -.3));
    cable(V(.6, TABLE_Y + .02, -.3), V(.5, PCY - .2, -PZ - .02), 0x2E9E5B, .05, .008);
    // dust particles
    const pos = new Float32Array(NP3*3), col = new Float32Array(NP3*3), gm = new THREE.BufferGeometry(); gm.setAttribute('position', new THREE.BufferAttribute(pos, 3)); gm.setAttribute('color', new THREE.BufferAttribute(col, 3));
    const dtx = canvasTex(32, 32, (x)=>{ const g = x.createRadialGradient(16,16,1,16,16,15); g.addColorStop(0,'rgba(255,255,255,1)'); g.addColorStop(1,'rgba(255,255,255,0)'); x.fillStyle = g; x.fillRect(0,0,32,32); });
    P.dust = new THREE.Points(gm, new THREE.PointsMaterial({size:.045, vertexColors:true, map:dtx, transparent:true, depthWrite:false})); W.add(P.dust);
    P.pp = Array.from({length:NP3}, (_,k)=>spawn3({}, -1.3 + k/NP3*2.6));
    P.stuck = 0; P.vdV = null; updP3();
  }
  function spawn3(p, x){ p.x = x==null ? -1.3 - Math.random()*.15 : x; p.y = PCY + (Math.random()*2 - 1)*.18; p.z = (Math.random()*2 - 1)*(PZ - .03); p.cap = Math.random(); p.q = 0; p.st = 0; p.vz = 0; return p; }
  function tick3(dt){ const s = P.s, u = s.u, vx = u*.32, on = s.kv > VC, e = eta3(s.kv, u), pos = P.dust.geometry.attributes.position.array, col = P.dust.geometry.attributes.color.array;
    P.pp.forEach((p,k)=>{
      if(p.st > 0){ p.st -= dt; if(p.st <= 0) spawn3(p); }
      else { p.x += vx*dt*(.85 + (k%7)*.04); const inF = p.x > -PL/2 && p.x < PL/2;
        if(inF && on && !p.q){ p.q = 1; const need = PZ - .006 - Math.abs(p.z), tl = (PL/2 - p.x)/vx; p.vz = (p.z >= 0 ? 1 : -1)*(p.cap < e ? need/(tl*.85) : need/(tl*3.2)); }
        if(!on && p.q){ p.q = 0; p.vz = 0; }
        if(p.q){ p.z += p.vz*dt; if(Math.abs(p.z) >= PZ - .006){ p.z = Math.sign(p.z)*(PZ - .006); p.st = 2.5 + Math.random()*2; P.stuck = Math.min(1, P.stuck + .0012); } }
        if(p.x > 1.35) spawn3(p); }
      pos[k*3] = p.x; pos[k*3+1] = p.y; pos[k*3+2] = p.z;
      const c = p.st > 0 ? [.35,.28,.2] : p.q ? [.36,.55,.95] : [.55,.42,.3]; col[k*3] = c[0]; col[k*3+1] = c[1]; col[k*3+2] = c[2]; });
    P.dust.geometry.attributes.position.needsUpdate = true; P.dust.geometry.attributes.color.needsUpdate = true;
    if(P.blade) P.blade.rotation.x += dt*u*6;
    const gl = on ? .25 + .75*(s.kv - VC)/(VMAX - VC) : 0; P.wm.emissiveIntensity = gl*1.4; P.cor.material.opacity = gl*.22*(.85 + .15*Math.sin(P.tt*40));
    const k = 1 - P.stuck*.5; P.pm3.color.setRGB(.79*k, .81*k, .85*k);
    SFX.amb(on ? {buzz:.25 + .75*(s.kv - VC)/(VMAX - VC)} : {}); }
  function updP3(){ const s = P.s; if(!P.sIn) return; if(P.vdV !== s.kv){ P.vdV = s.kv; lcdSet(P.vd, String(s.kv), 'kV'); } if(P.kn) P.kn.rotation.z = -s.kv/VMAX*4.5;
    const e = eta3(s.kv, s.u), co = Math.round(s.cin*(1 - e)); const k = s.cin + '|' + co; if(P.sk !== k){ P.sk = k; lcdSet(P.sIn.userData.d, String(s.cin), 'µg'); lcdSet(P.sOut.userData.d, String(co), 'µg'); } }
  function rec3(){ const s = P.s, e = eta3(s.kv, s.u), co = Math.round(s.cin*(1 - e)), eta = Math.round((s.cin - co)/s.cin*1000)/10, k = s.kv + '|' + s.u, first = !s.prec[k];
    delete s.prec[k]; s.prec[k] = {kv:s.kv, u:s.u, cin:s.cin, co, eta}; const ks = Object.keys(s.prec); if(ks.length > 10) delete s.prec[ks[0]]; P.last3 = k;
    P.say = s.kv <= VC ? (s.kv ? `${s.kv} kV ยังต่ำเกินไป ลวดยังไม่ปล่อยประจุให้ฝุ่น ฝุ่นจึงไม่ถูกดักครับ` : 'ยังไม่เปิดไฟแรงสูง ฝุ่นผ่านท่อออกไปหมดครับ') : `${s.kv} kV ลมระดับ ${s.u} ดักฝุ่นได้ ${eta}%${first ? ' บันทึกแล้ว' : ''}ครับ`; }
  function setKV(v){ const s = P.s; s.kv = Math.max(0, Math.min(VMAX, Math.round(v))); updP3(); rec3(); }
  function e3Sol(){ const s = P.s, r = s.prec[P.last3] || Object.values(s.prec).filter(x=>x.kv > 0).pop(); if(!r || !r.kv) return null; const t = r.kv*1000/DW; return {r, t, txt:`ถูกต้องครับ E = V/d = (${r.kv} × 10³ V) ÷ 0.10 m = ${(t/1e5).toFixed(1)} × 10⁵ V/m`}; }
  function checkE3(v){ const s = P.s, so = e3Sol(), x = num(v); if(!so){ P.warn = 'เปิดไฟแรงสูงแล้วบันทึกค่าก่อนครับ'; return; } if(x===null){ P.warn = 'พิมพ์สนามไฟฟ้าเป็นตัวเลข หน่วย V/m (เช่น 2e5)'; return; }
    const {r, t} = so; if(rel(x, t, .03)){ s.eOk = true; P.say = so.txt; return; }
    s.wrong += 1;
    if(rel(x, t/1000, .03)) P.warn = hint(['แปลง kV เป็น V ก่อนครับ 1 kV = 1000 V', 'ความต่างศักย์เป็น kV ต้องคูณ 1000 ก่อนหารด้วย d ครับ']);
    else if(rel(x, t/100, .03) || rel(x, r.kv*1000/10, .03)) P.warn = 'd = 10 cm = 0.10 m ครับ แปลงเป็นเมตรก่อน';
    else if(rel(x, r.kv*1000*DW, .03) || rel(x, r.kv*DW, .03)) P.warn = 'E = V ÷ d ไม่ใช่ V × d ครับ';
    else P.warn = hint([`ใช้แถวล่าสุด: V = ${r.kv} kV = ${r.kv*1000} V และ d = 0.10 m แล้ว E = V/d ครับ`, 'สนามไฟฟ้าเฉลี่ย = ความต่างศักย์ ÷ ระยะห่างลวดถึงแผ่น หน่วย V/m ครับ']);
    if(P.warn && escN(P.s, 'checkE3') >= 3){ P.warn = '📘 ลองมาหลายครั้งแล้ว ดูวิธีทำครับ: ' + so.txt.replace(/^ถูกต้อง(ครับ)?[ ]*/,'') + ' → พิมพ์ค่านี้แล้วกดตรวจอีกครั้ง'; } }
  const g3 = (key, val) => { const g = {}; Object.values(P.s.prec).forEach(r=>{ if(r.kv > VC) (g[r[key]] = g[r[key]] || new Set()).add(r[val]); }); return Math.max(0, ...Object.values(g).map(x=>x.size)); };

"""
between("  /* ===== part 3: Millikan ===== */", "  /* ===== part 4: electroscope & induction ===== */", P3)
rep("V:0, drop:newDrop(1), y:.5, drops:{}, qOk:false, fl:true,", "V:0, drop:newDrop(1), y:.5, drops:{}, qOk:false, fl:true, kv:0, u:2, cin:pick1([420,480,540,600]), prec:{}, eOk:false,")

# part 5: area variable, no bulb
P5 = r"""  /* ===== part 5: parallel-plate capacitor ===== */
  const E0 = 8.85e-12, GK = .09, AS = [.02,.03,.04];
  const capC = () => E0*P.s.A/(P.s.cd*1e-3), capQ = () => capC()*P.s.cV*1e9;
  function buildP5(){ const W = R.world, s = P.s, w = Math.sqrt(s.A)*3.2, cy = TABLE_Y + Math.sqrt(.04)*1.6 + .14; P.w = w; P.cy = cy;
    const pm = new THREE.MeshStandardMaterial({color:0xC9CFDA, metalness:.9, roughness:.25, envMap:ENVMAP});
    const plate = (edge, id, sg) => { const g = new THREE.Group(); g.userData.id = id; g.userData.hy = 0; g.add(box(.03, w, w, pm)); g.add(box(.036,.03, w + .01, mat(edge), 0, w/2, 0));
      const ph = cy - TABLE_Y - w/2; g.add(at(cyl(.02,.02, ph, mat(0xE8E2C8), 8), 0, -w/2 - ph/2, 0)); g.add(at(cyl(.1,.12,.035, mat(0x2B3050), 20), 0, -(cy - TABLE_Y) + .018, 0)); g.add(hitBox(.4, w + .2, w + .2, 0));
      const sp = []; for(let r=0;r<3;r++) for(let c=0;c<4;c++){ const m = chSpr(sg, .045); m.position.set(-sg*.03, (r - 1)*w*.3, (c - 1.5)*w*.24); g.add(m); sp.push(m); } sp.sort((a,b)=>a.position.length() - b.position.length()); g.userData.sp = sp; W.add(g); return g; };
    P.lp = plate(0xE25555, 'pA', 1); P.mp = plate(0x5B8DEF, 'plate', -1); P.cp = P.lp.userData.sp; P.cn = P.mp.userData.sp;
    P.ar = []; for(const y of [-w/4, 0, w/4]) for(const z of [-w/4, 0, w/4]){ const a = new THREE.ArrowHelper(V(1,0,0), V(0, cy + y, z), .2, 0xF2994A, .04, .03); a.line.material.transparent = a.cone.material.transparent = true; W.add(a); a.userData.yz = [cy + y, z]; P.ar.push(a); }
    const ps = makePS(-1.0, -.4, .3, true); P.ps = ps; P.vd = ps.userData.d; P.kn = ps.userData.kn; P.kn.userData.hy = 0;
    P.labels.push({obj:ps, dy:.58, text:()=>'แหล่งจ่ายไฟ'});
    const qm = new THREE.Group(); qm.add(at(box(.46,.32,.14, mat(0xF2C94C,{roughness:.45})), 0,.16,0)); P.qd = lcd(.36,.13); P.qd.position.set(0,.18,.071); qm.add(P.qd); qm.position.set(.7, TABLE_Y, -.45); qm.rotation.y = .2; W.add(qm); P.qm = qm;
    P.labels.push({obj:qm, dy:.44, text:()=>'คูลอมบ์มิเตอร์'});
    P.labels.push({obj:P.mp, dy:w/2 + .1, text:()=>`d = ${P.s.cd} mm`});
    P.labels.push({obj:P.lp, dy:w/2 + .1, text:()=>`A = ${P.s.A} m²`});
    P.cdW = null; P.vdV = null; updP5(); }
  function cables5(){ (P.cab || []).forEach(m=>R.world.remove(m)); const gp = P.s.cd*GK, by = TABLE_Y + .03;
    const t1 = P.ps.localToWorld(V(-.3,.1,.25)), t2 = P.ps.localToWorld(V(-.18,.1,.25));
    P.cab = [cable(t1, V(-gp/2, by, 0), 0xE25555, .1), cable(t2, V(gp/2, by, .05), 0x22263A, .1), cable(V(gp/2, by, -.04), P.qm.localToWorld(V(0,.06,-.07)), 0xF2C94C, .1, .008)]; }
  function updP5(){ const s = P.s; if(!P.mp) return; const gp = s.cd*GK, Q = capQ();
    P.lp.position.set(-gp/2, P.cy, 0); P.mp.position.set(gp/2, P.cy, 0);
    const n = Q > .05 ? Math.max(1, Math.min(12, Math.round(Math.sqrt(Q)*1.2))) : 0; P.cp.forEach((m,k)=>m.visible = k < n); P.cn.forEach((m,k)=>m.visible = k < n);
    const E = s.cV/s.cd, op = .3 + .7*Math.min(1, E/100); P.ar.forEach(a=>{ a.position.set(-gp/2 + .02, a.userData.yz[0], a.userData.yz[1]); a.setLength(Math.max(.02, gp - .04), Math.min(.05, gp*.35), Math.min(.035, gp*.28)); a.visible = s.cV > 0; a.line.material.opacity = a.cone.material.opacity = op; });
    if(P.vdV !== s.cV){ P.vdV = s.cV; lcdSet(P.vd, String(s.cV), 'V'); } const qs = Q.toFixed(Q < 10 ? 2 : 1); if(P.qdV !== qs){ P.qdV = qs; lcdSet(P.qd, qs, 'nC'); } P.kn.rotation.z = -s.cV/300*4.5;
    if(P.cdW !== s.cd){ P.cdW = s.cd; cables5(); } }
  function rec5(){ const s = P.s; if(!s.cV){ P.say = 'ตั้งความต่างศักย์ก่อนครับ (หมุนปุ่มสีส้ม หรือกด V +)'; return; }
    const Q = +capQ().toFixed(2), k = s.cV + '|' + s.cd + '|' + s.A, first = !s.crecs[k]; delete s.crecs[k]; s.crecs[k] = {V:s.cV, d:s.cd, A:s.A, Q}; const ks = Object.keys(s.crecs); if(ks.length > 12) delete s.crecs[ks[0]]; P.lastC = k;
    P.say = `V = ${s.cV} V, d = ${s.cd} mm, A = ${s.A} m² → Q = ${Q} nC${first ? ' บันทึกแล้ว' : ''}ครับ`; }
  function setA(){ const s = P.s; s.A = AS[(AS.indexOf(s.A) + 1) % AS.length]; rebuild(); rec5(); SFX.pick(); }
  function cSol(){ const s = P.s, r = s.crecs[P.lastC] || Object.values(s.crecs).filter(x=>x.V > 0).pop(); if(!r) return null; const t = r.Q/r.V*1000;
    return {r, t, txt:`ถูกต้องครับ C = Q/V = (${r.Q} × 10⁻⁹) ÷ ${r.V} ≈ ${(t*1e-12).toExponential(2).replace('e-', ' × 10^-')} F = ${t.toFixed(1)} pF`}; }
  function checkC(v){ const s = P.s, x = num(v), so = cSol(); if(!so){ P.warn = 'วัดประจุก่อนครับ'; return; } if(x===null){ P.warn = 'พิมพ์ความจุเป็นตัวเลข หน่วย pF'; return; }
    const {r, t} = so;
    if(rel(x, t, .03) || rel(x, t*1e-12, .03)){ s.cOk = true; P.say = so.txt; return; }
    s.wrong += 1;
    if(rel(x, t/1000, .03)) P.warn = hint(['นั่นคือหน่วย nF ครับ 1 nF = 1000 pF', 'Q เป็น nC หาร V ได้ nF ต้องคูณ 1000 ให้เป็น pF ครับ']);
    else if(rel(x, r.V/r.Q, .03) || rel(x, 1e6/t, .03)) P.warn = 'C = Q/V ครับ เอาประจุเป็นตัวตั้ง หารด้วยความต่างศักย์ ไม่ใช่ V/Q';
    else if(rel(x, r.Q*r.V, .03)) P.warn = 'ความจุ = Q ÷ V ไม่ใช่ Q × V ครับ';
    else if(rel(x, t*1e3, .03) || rel(x, t*1e-3*1e-9, .03)) P.warn = 'ระวังหน่วยครับ 1 nC = 10⁻⁹ C และ 1 pF = 10⁻¹² F';
    else P.warn = hint([`ใช้แถวล่าสุด: Q = ${r.Q} nC, V = ${r.V} V แล้ว C = Q/V ครับ`, 'แปลง Q เป็นคูลอมบ์ (× 10⁻⁹) หารด้วย V จะได้ F แล้วแปลงเป็น pF (÷ 10⁻¹²) ครับ']);
    if(P.warn && escN(P.s, 'checkC') >= 3){ const _w = so.txt.replace(/^ถูกต้อง(แล้ว)?(ครับ)?[ !:,]*/,''); P.warn = '📘 ลองมาหลายครั้งแล้ว ดูวิธีทำครับ: ' + _w + ' → พิมพ์ค่านี้แล้วกดตรวจอีกครั้ง'; }
  }
  const byG5 = (fix, val) => { const g = {}; Object.values(P.s.crecs).forEach(r=>{ if(r.V > 0){ const k = fix.map(f=>r[f]).join('|'); (g[k] = g[k] || new Set()).add(r[val]); } }); return Math.max(0, ...Object.values(g).map(x=>x.size)); };

  function sync(){"""
between("  /* ===== part 5: parallel-plate capacitor ===== */", "  function sync(){", P5, keep_b=False)

# missions / OKA / SOLS
rep("const OKA = [{qv:'x2', inv:'q'}, {eq:'par', uni:'same'}, {e:'int'}, {}, {}];", "const OKA = [{qv:'x2', inv:'q'}, {eq:'par', uni:'same'}, {}, {}, {}];")
rep("{e:'ยังไม่ถูกครับ ลองหารประจุแต่ละหยดด้วย 1.6 × 10⁻¹⁹ C'}, {}, {}];", "{}, {}, {}];")
i = s.index('    "q": {id:"qq", f:() =>'); j = s.index('\n    "', i + 10) if s.find('\n    "', i + 10) != -1 and s.find('\n    "', i + 10) < s.index('\n  };', i) else s.index('\n  };', i)
s = s[:i] + '    "e3": {id:"ev3", f:() => { const so = e3Sol(); return so ? so.txt : null; }},' + s[j:]
rep("    else if(P.i===2){ const n = Object.keys(s.drops).length; if(n >= 1) set('bal'); if(s.qOk) set('q'); if(n >= 3) set('n3'); if(s.ans.e) set('e'); }",
    "    else if(P.i===2){ if(Object.values(s.prec).some(r=>r.eta >= 90)) set('eff'); if(g3('kv','u') >= 2) set('spd'); if(s.eOk) set('E3'); }")
rep("    else { if(byGroup('d','V') >= 3) set('qv'); if(s.cOk) set('c'); if(byGroup('V','d') >= 2) set('dd'); }",
    "    else { if(byG5(['d','A'],'V') >= 3) set('qv'); if(s.cOk) set('c'); if(byG5(['V','A'],'d') >= 2) set('dd'); if(byG5(['V','d'],'A') >= 2) set('aa'); }")

# mascot
i = s.index("    const n = Object.keys(s.drops).length;\n    if(!m.bal)"); j = s.index("\n  }", i)
s = s[:i] + """    const best = Math.max(0, ...Object.values(s.prec).map(r=>r.eta));
    if(!m.eff) return ['think', s.kv <= VC ? 'หมุนปุ่มสีส้มบนแหล่งจ่ายไฟแรงสูง (ลากขึ้น) หรือกด kV + เปิดไฟแรงสูงให้ลวด แล้วดูฝุ่นครับ' : `ตอนนี้ดักได้ ${eta3(s.kv, s.u) ? (eta3(s.kv, s.u)*100).toFixed(1) : 0}% เพิ่ม kV ให้ดักได้อย่างน้อย 90% ครับ`];
    if(!m.spd) return ['think', 'แตะพัดลมหรือกดปุ่มลม เปลี่ยนความเร็วลมที่ kV เดิม แล้วเทียบร้อยละที่ดักได้ครับ'];
    if(!m.E3) return ['think', 'คำนวณสนามไฟฟ้าเฉลี่ยระหว่างลวดกับแผ่น E = V/d (d = 0.10 m) จากแถวล่าสุดครับ'];
    return ['yay', `สนามไฟฟ้าดึงฝุ่นที่มีประจุไปติดแผ่น ยิ่ง V สูง สนามยิ่งแรง ดักฝุ่นได้มากขึ้นครับ (ดีที่สุด ${best}%)`];""" + s[j:]
rep("      if(!m.dd) return ['think', 'ลากแผ่นสีฟ้าหรือกด d +/− เปลี่ยนระยะห่างแผ่นที่ V เดิม แล้วดูประจุครับ'];\n      return ['yay', 'ความจุขึ้นกับรูปร่าง C = ε₀A/d ไม่ขึ้นกับ V ครับ ลองกด ⚡ คายประจุผ่านหลอดไฟ ดูพลังงานที่สะสมได้']; }",
    "      if(!m.dd) return ['think', 'ลากแผ่นสีฟ้าหรือกด d +/− เปลี่ยนระยะห่างแผ่นที่ V เดิม แล้วดูประจุครับ'];\n      if(!m.aa) return ['think', 'แตะแผ่นสีแดงหรือกดปุ่มขนาดแผ่น เปลี่ยนพื้นที่ A ที่ V และ d เดิม แล้วดูประจุครับ'];\n      return ['yay', 'ความจุขึ้นกับรูปร่าง C = ε₀A/d แผ่นใหญ่ขึ้นหรือใกล้กันขึ้น เก็บประจุได้มากขึ้น และไม่ขึ้นกับ V ครับ']; }")
rep("`ตั้ง d ไว้เท่าเดิม หมุนปุ่มสีส้มบนแหล่งจ่ายไฟ (หรือกด V +/−) วัดประจุให้ครบ 3 ค่า V ครับ (ได้ ${byGroup('d','V')})`", "`ตั้ง d และ A ไว้เท่าเดิม หมุนปุ่มสีส้มบนแหล่งจ่ายไฟ (หรือกด V +/−) วัดประจุให้ครบ 3 ค่า V ครับ (ได้ ${byG5(['d','A'],'V')})`")

# refreshUI part 3
i = s.index("    } else if(P.i===2){\n      const ks = Object.keys(s.drops);"); j = s.index("    } else if(P.i===3){", i)
s = s[:i] + """    } else if(P.i===2){
      const ks = Object.keys(s.prec), e = eta3(s.kv, s.u);
      sig = JSON.stringify(['p2', ks.length, s.eOk, !!m.E3]);
      ctrls = FORM('<b>เครื่องกรองฝุ่นไฟฟ้าสถิต</b> ฝุ่นได้รับประจุจากลวด แล้วถูกแรง F = qE ดึงไปติดแผ่น<br>สนามไฟฟ้าเฉลี่ย E = {V|d} · d (ลวดถึงแผ่น) = 0.10 m<br><span class="note">ร้อยละที่ดักได้ = {ฝุ่นขาเข้า − ฝุ่นขาออก|ฝุ่นขาเข้า} × 100</span>')
        + (ks.some(k=>s.prec[k].kv > 0) && !s.eOk && !m.E3 ? `<h2 style="margin-top:6px">สนามไฟฟ้าเฉลี่ยจากแถวล่าสุด (V/m)</h2>${IN('ev3','เช่น 2e5','e3','ตรวจ')}` : '');
      res = `<h2>ฝุ่นขาออก · ดักได้ ${(e*100).toFixed(1)}%</h2>` + (ks.length ? grid('auto auto auto auto', `<b>kV</b><b>ลม</b><b>ขาออก (µg)</b><b>ดักได้ (%)</b>${ks.map(k=>{ const r = s.prec[k], h = HL(P.last3===k); return `<span${h}>${r.kv}</span><span${h}>${r.u}</span><span${h}>${r.co}</span><span${h}>${r.eta}</span>`; }).join('')}`) + `<div class="note">ฝุ่นขาเข้า ${s.cin} µg/m³</div>` : '<div class="note">หมุนปุ่มบนแหล่งจ่ายไฟแรงสูง ค่าจะบันทึกลงตารางอัตโนมัติ</div>');
      dk = DB('hv:-5','kV −5') + DB('hv:-1','−1') + PILL(`${s.kv} kV`) + DB('hv:1','+1') + DB('hv:5','kV +5') + DB('sp', `💨 ลม ${s.u} ▸`, 1);
""" + s[j:]

# refreshUI part 4: rod button into the stage dock
rep("""        + `<div class="row" style="gap:6px;margin-top:8px;align-items:center">${B('rod', `${rd.n} (${rd.sg > 0 ? '+' : '−'}) ▸`, 1)}<span class="note">${rd.by}</span></div>`""",
    """        + `<div class="note" style="margin-top:6px">${rd.n} ${rd.by} มีประจุ${rd.sg > 0 ? 'บวก' : 'ลบ'} · เปลี่ยนแท่งได้ที่ปุ่มในจอ หรือแตะแท่งที่วางบนโต๊ะ</div>`""")
rep("      dk = DB('rf','⬅ ถอยออก') + DB('rn','เข้าใกล้ ➡')", "      dk = DB('rod', `${rd.n === 'แท่งแก้ว' ? 'แก้ว (+)' : 'ยาง (−)'} ▸`, 1) + DB('rf','⬅ ถอยออก') + DB('rn','เข้าใกล้ ➡')")

# refreshUI part 5
i = s.index("    } else {\n      const ks = Object.keys(s.crecs);"); j = s.index("    dock(dk);", i)
s = s[:i] + """    } else {
      const ks = Object.keys(s.crecs);
      sig = JSON.stringify(['p4', ks.length, s.cOk, !!m.c]);
      ctrls = FORM(`<b>ตัวเก็บประจุแผ่นคู่ขนาน</b> C = {Q|V} = {ε₀A|d}<br><span class="note">ε₀ = 8.85 × 10⁻¹² F/m · 1 nC = 10⁻⁹ C · 1 pF = 10⁻¹² F</span>`)
        + (ks.length && !s.cOk && !m.c ? `<h2 style="margin-top:6px">ความจุจากแถวล่าสุด (pF)</h2>${IN('cv5','เช่น 130','c','ตรวจ')}` : '');
      res = `<h2>คูลอมบ์มิเตอร์ · ${capQ().toFixed(2)} nC</h2>` + (ks.length ? grid('auto auto auto auto', `<b>V (V)</b><b>d (mm)</b><b>A (m²)</b><b>Q (nC)</b>${ks.map(k=>{ const r = s.crecs[k], h = HL(P.lastC===k); return `<span${h}>${r.V}</span><span${h}>${r.d}</span><span${h}>${r.A || s.A}</span><span${h}>${r.Q.toFixed(2)}</span>`; }).join('')}`) : '<div class="note">ปรับ V, d หรือ A แล้วค่าจะบันทึกลงตารางอัตโนมัติ</div>');
      dk = DB('cv:-25','V −') + DB('cv:25','V +') + DB('cd:-1','d −') + DB('cd:1','d +') + DB('ca', `A ${s.A} m² ▸`, 1);
    }
""" + s[j:]

# actions
i = s.index("    else if(v.startsWith('dv:')) act(()=>setV(s.V + (+v.slice(3))));"); j = s.index("    else if(v==='fl')", i)
s = s[:i] + """    else if(v.startsWith('hv:')) act(()=>setKV(s.kv + (+v.slice(3))));
    else if(v.startsWith('kv:')) act(()=>setKV(+v.slice(3)));
    else if(v==='sp') act(()=>{ s.u = SPD[(SPD.indexOf(s.u) + 1) % SPD.length]; updP3(); rec3(); });
    else if(v==='e3') act(()=>checkE3(val('ev3'))); else if(v.startsWith('e3:')) act(()=>{ const so = e3Sol(); checkE3(v.slice(3)==='auto' ? String(so ? so.t : '') : v.slice(3)); });
""" + s[j:]
rep("    else if(v==='dis') act(discharge);\n", "    else if(v==='ca') act(setA);\n")

# pointer: knob in part 3 = kV, fan / plate A taps, window-level end, stale-drag reset
rep("const DRG = () => P.i===0 ? [P.A] : P.i===1 ? [P.pr] : P.i===2 ? [P.kn] : P.i===3 ? [P.rod, P.gp] : [P.mp, P.kn];",
    "const DRG = () => P.i===0 ? [P.A] : P.i===1 ? [P.pr] : P.i===2 ? [P.kn, P.fan] : P.i===3 ? [P.rod, P.gp, P.rod2] : [P.mp, P.kn, P.lp];")
rep("      if(!P || drag) return; pick(e);\n      const h = R.raycaster.intersectObjects(R.world.children, true).find(x=>rootOf(x.object));\n      let g = h ? rootOf(h.object) : null; const lim = Math.max(60, el.clientWidth*.1);",
    "      if(drag && performance.now() - (drag.ts || 0) > 1500){ drag = null; R.controls.enabled = true; }\n      if(!P || drag) return; pick(e);\n      const h = R.raycaster.intersectObjects(R.world.children, true).find(x=>rootOf(x.object));\n      let g = h ? rootOf(h.object) : null; const lim = Math.max(60, el.clientWidth*.1);")
rep("drag = {id:g.userData.id, x:e.clientX, y:e.clientY, pid:e.pointerId, moved:false, V0:P.i===2 ? P.s.V : P.s.cV};",
    "drag = {id:g.userData.id, x:e.clientX, y:e.clientY, pid:e.pointerId, moved:false, V0:P.i===2 ? P.s.kv : P.s.cV, ts:performance.now()};")
rep("el.addEventListener('pointermove', e=>{ if(!drag || e.pointerId!==drag.pid) return; if(!drag.moved",
    "el.addEventListener('pointermove', e=>{ if(!drag || e.pointerId!==drag.pid) return; drag.ts = performance.now(); if(!drag.moved")
rep("if(!drag.moved || drag.id==='gnd') return;", "if(!drag.moved || drag.id==='gnd' || drag.id==='fan' || drag.id==='pA' || drag.id==='rod2') return;")
rep("        if(P.i===2){ const v = Math.max(0, Math.min(1000, Math.round(drag.V0 + dv*1.5))); if(v!==s.V){ s.V = v; SFX.tick(); updP3(); P.dirty = true; } }",
    "        if(P.i===2){ const v = Math.max(0, Math.min(VMAX, Math.round(drag.V0 + dv*.12))); if(v!==s.kv){ s.kv = v; SFX.tick(); updP3(); P.dirty = true; } }")
rep("      if(d.id==='gnd'){ if(!d.moved) act(()=>setGnd(!P.s.gnd)); return; }",
    "      if(d.id==='gnd'){ if(!d.moved) act(()=>setGnd(!P.s.gnd)); return; }\n      if(d.id==='fan'){ if(!d.moved) action('sp'); return; }\n      if(d.id==='pA'){ if(!d.moved) action('ca'); return; }\n      if(d.id==='rod2'){ if(!d.moved) action('rod'); return; }")
rep("      else if(d.id==='knob') act(()=>{ if(P.i===2) setV(P.s.V); else rec5(); }); };\n    el.addEventListener('pointerup', end); el.addEventListener('pointercancel', end);",
    "      else if(d.id==='knob') act(()=>{ if(P.i===2) rec3(); else rec5(); }); };\n    el.addEventListener('pointerup', end); el.addEventListener('pointercancel', end); window.addEventListener('pointerup', end); window.addEventListener('pointercancel', end);")

# tick
i = s.index("      if(P.i===2 && P.drop){"); j = s.index("      if(P.i===1 && P.eqp", i)
s = s[:i] + "      if(P.i===2 && P.dust) tick3(dt); else SFX.amb({});\n" + s[j:]
rep("      if(P.i===4 && P.dis > 0){ P.dis = Math.max(0, P.dis - dt*1.3); updP5(); }\n", "")

# part 4: spare rod lying on the table (tap to swap)
rep("    W.add(rod); P.rod = rod;", """    W.add(rod); P.rod = rod;
    const o = s.rod==='e' ? 'g' : 'e', r2 = new THREE.Group(); r2.userData.id = 'rod2'; r2.userData.hy = .03;
    const m2 = o==='e' ? mat(0x2A2A33,{roughness:.3}) : new THREE.MeshStandardMaterial({color:0xD6ECFA, transparent:true, opacity:.55, roughness:.05, envMap:ENVMAP, envMapIntensity:1.5});
    const b2 = cyl(.022,.022,.7, m2, 14); b2.rotation.z = Math.PI/2; r2.add(b2); const h2 = cyl(.03,.03,.16, mat(0x8A5A2B,{roughness:.7}), 14); h2.rotation.z = Math.PI/2; h2.position.x = -.3; r2.add(h2); r2.add(hitBox(.8,.25,.3,0));
    r2.position.set(-.55, TABLE_Y + .025, .62); r2.rotation.y = .15; W.add(r2); P.rod2 = r2;
    P.labels.push({obj:r2, dy:.12, text:()=>`${RODS[P.s.rod==='e' ? 'g' : 'e'].n} (แตะเพื่อสลับ)`});""")

# CAMS part 3 view
rep("{pos:V(0.5,1.5,3.0), tgt:V(0.2,.7,0), nx:.1}", "{pos:V(0.9,1.55,2.9), tgt:V(-0.1,.62,0), nx:.05}")
open(F, 'w', encoding='utf-8').write(s); print('es_fix ok')
