"""ม.5 ไฟฟ้าสถิต: fewer buttons, drag knobs, field/equipotential overlay, new parts 4 (induction) & 5 (capacitor).
usage: python3 es_patch.py <file>  (after hskit.py)"""
import sys, re
F = sys.argv[1]
s = open(F, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: sys.exit(f'COUNT {c}!={n}: {a[:120]}')
    s = s.replace(a, b)
def rep_between(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i)
    s = s[:i] + new + s[j:]

# ================= DATA =================
rep("key:'parkilab-m5-static-v1'", "key:'parkilab-m5-static-v2'")
rep("sub:'วัดแรงระหว่างทรงกลมมีประจุเพื่อตรวจสอบกฎของคูลอมบ์ วัดศักย์ไฟฟ้าระหว่างแผ่นโลหะคู่ขนานเพื่อหาสนามไฟฟ้า แล้วทำการทดลองหยดน้ำมันของมิลลิแกนเพื่อหาประจุไฟฟ้า'",
    "sub:'วัดแรงระหว่างทรงกลมมีประจุเพื่อตรวจสอบกฎของคูลอมบ์ วัดศักย์ไฟฟ้าระหว่างแผ่นโลหะคู่ขนานเพื่อหาสนามไฟฟ้า ทำการทดลองหยดน้ำมันของมิลลิแกน ทำให้อิเล็กโทรสโคปมีประจุโดยการเหนี่ยวนำ และวัดความจุของตัวเก็บประจุ'")
rep("hint:'ลากทรงกลม A เพื่อเปลี่ยนระยะ · ลากหัววัดระหว่างแผ่นโลหะ · ปรับความต่างศักย์จนหยดน้ำมันลอยนิ่ง'",
    "hint:'ลากทรงกลม A เพื่อเปลี่ยนระยะ · ลากหัววัดระหว่างแผ่นโลหะ · หมุนปุ่มสีส้มบนแหล่งจ่ายไฟ · ลากแท่งประจุเข้าใกล้อิเล็กโทรสโคป · ลากแผ่นตัวเก็บประจุ'")
rep("'หาประจุของหยดน้ำมันจาก qE = mg และสรุปว่าประจุไฟฟ้ามีค่าเป็นจำนวนเต็มเท่าของ e']}",
    "'หาประจุของหยดน้ำมันจาก qE = mg และสรุปว่าประจุไฟฟ้ามีค่าเป็นจำนวนเต็มเท่าของ e','อธิบายการทำให้ตัวนำมีประจุโดยการเหนี่ยวนำ และกฎอนุรักษ์ประจุ','หาความจุของตัวเก็บประจุจาก C = {Q|V} และอธิบายผลของระยะห่างแผ่น']}")
rep("'ตอนที่ 3 กดปุ่มบนจอปรับความต่างศักย์ ดูหยดน้ำมันผ่านกล้องในแผงข้างจนลอยนิ่ง']}",
    "'ตอนที่ 3 <b>หมุนปุ่มสีส้ม</b>บนแหล่งจ่ายไฟ (ลากขึ้น/ลง) หรือกดปุ่ม +/− ดูหยดน้ำมันผ่านกล้องจนลอยนิ่ง','ตอนที่ 4 <b>ลากแท่งประจุ</b>เข้าใกล้ปุ่มโลหะ แตะ <b>สายดิน</b>เพื่อต่อ/ถอด แล้วสังเกตแผ่นโลหะบาง','ตอนที่ 5 <b>ลากแผ่นขวา</b>เปลี่ยนระยะห่าง และหมุนปุ่มบนแหล่งจ่ายไฟ อ่านประจุจากคูลอมบ์มิเตอร์']}")

QUIZ_ADD = """  {q:'นำแท่งประจุลบเข้าใกล้ปุ่มโลหะของอิเล็กโทรสโคปที่เป็นกลาง (ไม่แตะ) แผ่นโลหะบางจะมีประจุชนิดใด', o:['ลบ','บวก','ไม่มีประจุ','บวกและลบเท่ากัน'], a:0, why:'อิเล็กตรอนในตัวนำถูกผลักลงไปที่แผ่นโลหะบาง แผ่นโลหะจึงมีประจุลบและกางออก'},
  {q:'การทำให้ตัวนำมีประจุโดยการเหนี่ยวนำ ต้องทำขั้นตอนใดก่อนนำวัตถุที่มีประจุออก', o:['ถอดสายดิน','ต่อสายดินเพิ่ม','แตะวัตถุกับตัวนำ','ถูตัวนำด้วยผ้า'], a:0, why:'ถ้านำวัตถุออกก่อนถอดสายดิน ประจุจะไหลกลับทางสายดินจนตัวนำเป็นกลาง'},
  {q:'ถูแท่งแก้วกับผ้าไหม แท่งแก้วมีประจุ +5 nC ผ้าไหมจะมีประจุเท่าใด', o:['−5 nC','+5 nC','0','−10 nC'], a:0, why:'กฎอนุรักษ์ประจุ ประจุรวมก่อนและหลังถูเป็นศูนย์ อิเล็กตรอนย้ายจากแก้วไปที่ผ้าไหม'},
  {q:'ตัวเก็บประจุแผ่นคู่ขนาน ถ้าเพิ่มระยะห่างระหว่างแผ่นเป็น 2 เท่า ความจุจะเป็นเท่าใดของเดิม', o:['1/2','2','1/4','เท่าเดิม'], a:0, why:'C = {ε₀A|d} ความจุแปรผกผันกับระยะห่างระหว่างแผ่น'},
  {q:'ตัวเก็บประจุความจุ 20 µF ต่อกับความต่างศักย์ 100 V สะสมพลังงานเท่าใด', o:['0.1 J','0.2 J','2 mJ','1 J'], a:0, why:'U = ½CV² = ½ × 20 × 10⁻⁶ × 100² = 0.1 J'},
];

const PARTS = ["""
rep("\n];\n\nconst PARTS = [", ",\n" + QUIZ_ADD)

PARTS_ADD = """,
  {k:'ตอนที่ 4', t:'การเหนี่ยวนำไฟฟ้าและอิเล็กโทรสโคป', d:'นำแท่งที่มีประจุเข้าใกล้อิเล็กโทรสโคป ต่อและถอดสายดิน ทำให้อิเล็กโทรสโคปมีประจุโดยไม่แตะ แล้วหาว่าเป็นประจุชนิดใด', time:'ประมาณ 15 นาที', bg:'#E9F7EF',
   pred:{q:"นำแท่งประจุลบเข้าใกล้ปุ่มโลหะ (ไม่แตะ) แผ่นโลหะบางด้านล่างจะเป็นอย่างไร", o:["กางออก", "หุบเหมือนเดิม", "หลุดออก"], a:0}, why:{"why": "การเหนี่ยวนำไฟฟ้าอธิบายฟ้าผ่า สายล่อฟ้า และการที่ลูกโป่งถูผมแล้วดูดกระดาษได้ อิเล็กโทรสโคปทำให้เห็นการย้ายที่ของประจุในตัวนำ", "find": "การกางและหุบของแผ่นโลหะบาง ขั้นตอนการทำให้มีประจุโดยการเหนี่ยวนำ และชนิดของประจุที่เหลือ", "how": "ประจุอิสระในตัวนำย้ายที่เมื่อมีวัตถุมีประจุมาใกล้ ประจุชนิดตรงข้ามถูกดูดไปใกล้วัตถุ ประจุชนิดเดียวกันถูกผลักไปไกล ถ้าต่อสายดิน ประจุจะไหลเข้าหรือออกทางสายดินได้ ประจุรวมคงตัวเสมอถ้าไม่มีทางให้ประจุเข้าออก", "steps": ["นำแท่งเข้าใกล้ปุ่มโลหะ (ไม่แตะ)", "ต่อสายดินขณะแท่งยังอยู่ใกล้", "ถอดสายดินก่อน แล้วจึงนำแท่งออก", "ทดสอบชนิดประจุด้วยแท่งเดิม"]}, refl:{"q": "ทำไมการเหนี่ยวนำจึงให้ประจุชนิดตรงข้ามกับแท่ง", "o": ["ขณะต่อสายดิน ประจุชนิดเดียวกับแท่งถูกผลักออกทางสายดิน เหลือประจุตรงข้ามที่ถูกดูดไว้", "แท่งส่งประจุตรงข้ามผ่านอากาศมาให้", "แผ่นโลหะสร้างประจุใหม่ขึ้นเอง"], "a": 0, "why": "ประจุสร้างใหม่ไม่ได้ สายดินเป็นทางให้อิเล็กตรอนไหลเข้าหรือออก เมื่อถอดสายดินแล้วนำแท่งออก ประจุที่ถูกดูดไว้จึงค้างอยู่และกระจายทั่วตัวนำ", "hint": "ตอนต่อสายดิน ประจุไหลไปทางไหน"},
   miss:[['near','นำแท่งเข้าใกล้ปุ่มโลหะ (ไม่แตะ)'],['ind','ทำให้มีประจุโดยการเหนี่ยวนำ'],['sign','บอกชนิดประจุที่เหลือ']]},
  {k:'ตอนที่ 5', t:'ตัวเก็บประจุและความจุไฟฟ้า', d:'ต่อตัวเก็บประจุแผ่นคู่ขนานกับแหล่งจ่ายไฟ วัดประจุที่ความต่างศักย์และระยะห่างแผ่นต่าง ๆ แล้วคำนวณความจุ', time:'ประมาณ 15 นาที', bg:'#EEF0FF',
   pred:{q:"ถ้าเพิ่มความต่างศักย์เป็น 2 เท่า ประจุบนแผ่นตัวเก็บประจุจะเป็นอย่างไร", o:["เพิ่มเป็น 2 เท่า", "เพิ่มเป็น 4 เท่า", "เท่าเดิม"], a:0}, why:{"why": "ตัวเก็บประจุอยู่ในโทรศัพท์ แฟลชกล้อง และเครื่องกระตุกหัวใจ ใช้สะสมประจุและพลังงานไว้ปล่อยออกมาอย่างรวดเร็ว", "find": "ประจุบนแผ่นที่ความต่างศักย์และระยะห่างต่าง ๆ ความจุ C และผลของระยะห่างแผ่น", "how": "ตัวเก็บประจุเก็บประจุ +Q และ −Q ไว้บนแผ่นทั้งสอง ประจุแปรผันตรงกับความต่างศักย์ Q = CV ความจุ C = {Q|V} ขึ้นกับพื้นที่แผ่นและระยะห่าง C = {ε₀A|d}", "steps": ["ตั้งระยะห่าง d ไว้ แล้วเปลี่ยน V วัดประจุ 3 ค่า", "คำนวณ C = {Q|V}", "เปลี่ยนระยะห่าง d ที่ V เดิม แล้ววัดประจุ", "กด ⚡ คายประจุผ่านหลอดไฟ ดูพลังงานที่สะสม"]}, refl:{"q": "ทำไมเพิ่มระยะห่างแผ่นแล้วประจุที่เก็บได้ลดลง (V เท่าเดิม)", "o": ["ความจุ C = ε₀A/d ลดลงเมื่อ d เพิ่ม จึงได้ Q = CV น้อยลง", "แหล่งจ่ายไฟจ่ายความต่างศักย์ลดลง", "ประจุรั่วออกทางอากาศเมื่อแผ่นห่างกัน"], "a": 0, "why": "ความจุขึ้นกับรูปร่างของตัวเก็บประจุ C = ε₀A/d ระยะห่างเพิ่ม ความจุลดลง ที่ความต่างศักย์เท่าเดิมจึงเก็บประจุได้น้อยลง", "hint": "C ขึ้นกับ A และ d อย่างไร"},
   miss:[['qv','วัดประจุที่ V 3 ค่า (d เท่าเดิม)'],['c','คำนวณความจุ C'],['dd','เปลี่ยนระยะห่างแผ่นแล้ววัดอีกครั้ง']]}
];
const PART_ART = ["""
rep("\n];\nconst PART_ART = [", PARTS_ADD)

ART_ADD = """,
  `<svg width="200" height="110" viewBox="0 0 200 110" aria-hidden="true"><rect x="110" y="40" width="70" height="60" rx="8" fill="#DCEBFB" stroke="#9AA3B5"/><path d="M145 40 V64" stroke="#8A93A8" stroke-width="3"/><circle cx="145" cy="22" r="10" fill="#C9CFDA" stroke="#8A93A8"/><path d="M145 64 L132 88 M145 64 L158 88" stroke="#E0A526" stroke-width="4"/><rect x="20" y="18" width="104" height="8" rx="4" fill="#2A2A33"/>${[34,48,62,76].map(x=>`<text x="${x}" y="15" font-size="12" fill="#2F6FED" text-anchor="middle">−</text>`).join('')}<text x="136" y="26" font-size="12" fill="#E5484D">+</text></svg>`,
  `<svg width="200" height="110" viewBox="0 0 200 110" aria-hidden="true"><rect x="78" y="14" width="8" height="70" fill="#E25555"/><rect x="114" y="14" width="8" height="70" fill="#5B8DEF"/>${[28,49,70].map(y=>`<path d="M88 ${y} H110" stroke="#F2994A" stroke-width="2"/><path d="M106 ${y-3} L111 ${y} L106 ${y+3}" fill="#F2994A"/>`).join('')}<path d="M82 84 V98 H40 M118 84 V98 H160" stroke="#2B3050" stroke-width="2" fill="none"/><rect x="40" y="90" width="20" height="16" fill="#2B3050"/><text x="66" y="40" font-size="14" fill="#E25555">+</text><text x="128" y="40" font-size="14" fill="#2F6FED">−</text></svg>`
];
"""
rep("</svg>`\n];\n\nconst SHEET = [", "</svg>`" + ART_ADD + "\nconst SHEET = [")

SHEET_ADD = """,
  {title:'ตอนที่ 4 การเหนี่ยวนำไฟฟ้าและอิเล็กโทรสโคป', cols:['ขั้นตอน','ผลที่สังเกต (แผ่นโลหะ · ประจุ)'], rows:[
    ['p4a','นำแท่งเข้าใกล้ปุ่มโลหะ (ไม่แตะ)','.....................................................'],
    ['p4b','ต่อสายดิน แล้วถอดสายดิน','.....................................................'],
    ['p4c','นำแท่งออก','.....................................................'],
    ['p4d','ประจุที่เหลือเทียบกับแท่ง',['ชนิดตรงข้าม','ชนิดเดียวกัน']]], concl:'p4s', cq:'อธิบายขั้นตอนการทำให้ตัวนำมีประจุโดยการเหนี่ยวนำ และเชื่อมโยงกับกฎอนุรักษ์ประจุ'},
  {title:'ตอนที่ 5 ตัวเก็บประจุและความจุไฟฟ้า', cols:['V (V) · d (mm)','Q (nC)'], rows:[
    ['p5a','V 3 ค่า (d เท่าเดิม)','.....................................................'],
    ['p5b','d 2 ค่า (V เท่าเดิม)','.....................................................'],
    ['p5c','ความจุ C (pF)','.....................................................'],
    ['p5d','ระยะห่างแผ่นเพิ่ม ความจุ',['ลดลง','เพิ่มขึ้น']]], concl:'p5s', cq:'เขียนกราฟ Q กับ V และอธิบายว่าความชันของกราฟคืออะไร'}
];
const GUIDE = ["""
rep("\n];\nconst GUIDE = [", SHEET_ADD)

GUIDE_ADD = """, {"near": ["[data-v=\\"rn\\"]", "ลากแท่งหรือกด เข้าใกล้ ให้แท่งอยู่ใกล้ปุ่มโลหะแต่ไม่แตะครับ", [], ""], "ind": ["[data-v=\\"gnd\\"]", "ทำตามลำดับ: แท่งใกล้ → ต่อสายดิน → ถอดสายดิน → นำแท่งออก ครับ", ["นำแท่งเข้าใกล้ปุ่มโลหะ (ไม่แตะ)", "แตะสายดินเพื่อต่อ", "ถอดสายดินขณะแท่งยังอยู่ใกล้", "นำแท่งออกไปไกล"], ""], "sign": ["[data-v^=\\"sg:\\"]", "นำแท่งเดิมเข้าใกล้อีกครั้ง ดูแผ่นโลหะหุบหรือกาง แล้วเลือกชนิดประจุครับ", [], "คำถามนี้จะขึ้นเมื่อเหนี่ยวนำสำเร็จ ทำข้อที่มี ▶ ทำต่อ ก่อนครับ"]}, {"qv": ["[data-v^=\\"cv:\\"]", "ตั้ง d เท่าเดิม แล้วเปลี่ยน V วัดประจุให้ครบ 3 ค่าครับ", [], ""], "c": ["#cv5", "คำนวณ C = Q/V ตอบเป็น pF ใส่ช่องคำตอบครับ", [], "ช่องคำนวณจะขึ้นเมื่อมีข้อมูลในตารางแล้ว ทำข้อที่มี ▶ ทำต่อ ก่อนครับ"], "dd": ["[data-v^=\\"cd:\\"]", "เปลี่ยนระยะห่างแผ่น d ที่ V เดิม แล้ววัดประจุครับ", [], ""]}];
const CMAP = """
rep("}];\nconst CMAP = ", "}" + GUIDE_ADD)

ENDQ_ADD = """,
 [{k:'cons', q:'ขณะนำแท่งเข้าใกล้ (ไม่แตะและไม่ต่อสายดิน) ประจุรวมของอิเล็กโทรสโคปเป็นอย่างไร', o:[['zero','เป็นศูนย์เท่าเดิม'],['opp','มีประจุตรงข้ามกับแท่ง'],['same','มีประจุชนิดเดียวกับแท่ง']], a:'zero',
   h:['นับประจุบนปุ่มโลหะและบนแผ่นโลหะรวมกัน','ไม่มีทางให้ประจุเข้าหรือออก'], r:[['move','ประจุแค่ย้ายที่ภายในตัวนำ ไม่มีประจุเข้าออก ประจุรวมจึงคงตัว (กฎอนุรักษ์ประจุ)'],['air','แท่งส่งประจุผ่านอากาศมาที่ปุ่มโลหะ'],['made','สนามไฟฟ้าของแท่งสร้างประจุใหม่ขึ้นในตัวนำ']], ra:'move',
   hr:['ประจุสร้างใหม่หรือทำลายไม่ได้','ปุ่มโลหะกับแผ่นโลหะมีประจุตรงข้ามกันเท่ากัน'], why:'การเหนี่ยวนำแค่แยกประจุในตัวนำ ปุ่มโลหะกับแผ่นโลหะมีประจุตรงข้ามกันเท่ากัน ประจุรวมยังเป็นศูนย์'},
  {k:'opp', q:'หลังเหนี่ยวนำเสร็จ ประจุที่เหลือบนอิเล็กโทรสโคปเทียบกับประจุบนแท่งเป็นอย่างไร', o:[['opp','ชนิดตรงข้ามกับแท่ง'],['same','ชนิดเดียวกับแท่ง'],['none','ไม่มีประจุเหลือ']], a:'opp',
   h:['นำแท่งเดิมเข้าใกล้อีกครั้ง แผ่นโลหะหุบหรือกาง','ลองทำซ้ำด้วยแท่งอีกชนิด'], r:[['ground','ขณะต่อสายดิน ประจุชนิดเดียวกับแท่งถูกผลักออกทางสายดิน เหลือประจุตรงข้ามที่ถูกดูดไว้'],['touch','แท่งส่งประจุมาให้ตอนอยู่ใกล้'],['leaf','แผ่นโลหะสร้างประจุตรงข้ามขึ้นเอง']], ra:'ground',
   hr:['ตอนต่อสายดิน ประจุไหลไปทางไหน','ต้องถอดสายดินก่อนนำแท่งออก'], why:'ประจุชนิดเดียวกับแท่งถูกผลักออกทางสายดิน (แท่งบวก: อิเล็กตรอนไหลขึ้นมาจากดิน) เมื่อถอดสายดินแล้วนำแท่งออก จึงเหลือประจุชนิดตรงข้ามกับแท่ง'}],
 [{k:'lin', q:'เมื่อระยะห่างแผ่นคงที่ เพิ่มความต่างศักย์เป็น 2 เท่า ประจุบนแผ่นเป็นอย่างไร', o:[['x2','เพิ่มเป็น 2 เท่า'],['x4','เพิ่มเป็น 4 เท่า'],['same','เท่าเดิม']], a:'x2',
   h:['เทียบแถวที่ d เท่ากันแต่ V ต่างกัน 2 เท่า','Q = CV'], r:[['cconst','ความจุ C = Q/V คงที่ ประจุจึงแปรผันตรงกับ V'],['cup','ความจุเพิ่มตาม V ประจุจึงเพิ่ม 4 เท่า'],['full','แผ่นเก็บประจุได้จำกัด ประจุจึงเท่าเดิม']], ra:'cconst',
   hr:['ลองหาร Q ด้วย V ทุกแถวที่ d เท่ากัน','C ขึ้นกับ A และ d ไม่ขึ้นกับ V'], why:'Q = CV และ C คงที่เมื่อ A และ d ไม่เปลี่ยน ประจุจึงแปรผันตรงกับความต่างศักย์'},
  {k:'dist', q:'เพิ่มระยะห่างระหว่างแผ่น (V คงที่) ความจุเป็นอย่างไร', o:[['dec','ลดลง'],['inc','เพิ่มขึ้น'],['same','เท่าเดิม']], a:'dec',
   h:['เทียบประจุที่ V เท่ากันแต่ d ต่างกัน','C = Q/V'], r:[['inv','C = ε₀A/d ความจุแปรผกผันกับระยะห่าง'],['more','แผ่นห่างกันมีที่ว่างเก็บประจุมากขึ้น'],['volt','ความต่างศักย์ลดลงเมื่อแผ่นห่างกัน']], ra:'inv',
   hr:['ประจุลดลงหรือเพิ่มขึ้นเมื่อ d มากขึ้น','ε₀ และ A คงที่'], why:'C = ε₀A/d ระยะห่างเพิ่ม ความจุลดลง ที่ V เท่าเดิมจึงเก็บประจุได้น้อยลง'}]
];
"""
i = s.index("const ENDQ = [")
j = s.index("\n];\n", i)
s = s[:j] + ENDQ_ADD + s[j+4:]

# ================= LAB CODE =================
rep("""  const CAMS = [
    {pos:V(0.2,1.7,2.7), tgt:V(0.2,.55,0)},
    {pos:V(0.4,1.7,3.3), tgt:V(-.1,.55,0)},
    {pos:V(0.5,1.5,3.0), tgt:V(0.2,.7,0)}
  ];""", """  const CAMS = [
    {pos:V(0.2,1.7,2.7), tgt:V(0.2,.55,0)},
    {pos:V(0.4,1.7,3.3), tgt:V(-.1,.55,0)},
    {pos:V(0.5,1.5,3.0), tgt:V(0.2,.7,0)},
    {pos:V(-0.2,1.45,2.6), tgt:V(-0.15,.7,0)},
    {pos:V(0.0,1.45,2.7), tgt:V(-0.05,.6,0)}
  ];""")

rep("""    V:0, drop:newDrop(1), y:.5, drops:{}, qOk:false});""",
    """    V:0, drop:newDrop(1), y:.5, drops:{}, qOk:false, fl:true,
    rod:'e', gap:.9, gnd:false, Q:0, how:null, st:[0,0,0,0], show:true, lockShow:false, sawNear:false, indOk:false, signOk:false,
    A:pick1([.02,.03,.04]), cV:100, cd:3, crecs:{}, cOk:false});""")
rep("if(P.i===0) buildP1(); else if(P.i===1) buildP2(); else buildP3(); labelsDOM(); }",
    "if(P.i===0) buildP1(); else if(P.i===1) buildP2(); else if(P.i===2) buildP3(); else if(P.i===3) buildP4(); else buildP5(); shadowAll(R.world); labelsDOM(); }")
rep("  function sync(){ if(P.i===0) updP1(); else if(P.i===1) updP2(); else updP3(); }",
    "  function sync(){ if(P.i===0) updP1(); else if(P.i===1) updP2(); else if(P.i===2) updP3(); else if(P.i===3) updP4(); else updP5(); }")

# shared helpers (after arrow())
HELP = r"""
  function arrow(col){ const a = new THREE.ArrowHelper(V(1,0,0), V(0,0,0), .3, col, .08, .06); R.world.add(a); return a; }
  const CHT = {};
  function chTex(sg){ if(CHT[sg]) return CHT[sg]; return CHT[sg] = canvasTex(64, 64, (x)=>{ x.fillStyle = sg > 0 ? '#E5484D' : '#2F6FED'; x.beginPath(); x.arc(32,32,28,0,7); x.fill(); x.strokeStyle = '#fff'; x.lineWidth = 7; x.lineCap = 'round'; x.beginPath(); x.moveTo(17,32); x.lineTo(47,32); if(sg > 0){ x.moveTo(32,17); x.lineTo(32,47); } x.stroke(); }); }
  function chSpr(sg, sz){ const m = new THREE.Sprite(new THREE.SpriteMaterial({map:chTex(sg || 1), depthTest:false, transparent:true})); m.scale.set(sz || .05, sz || .05, 1); m.renderOrder = 9; return m; }
  function textSpr(t, col){ const tx = canvasTex(256, 96, (x,w,h)=>{ x.fillStyle = 'rgba(255,255,255,.92)'; x.beginPath(); x.roundRect ? x.roundRect(4,4,w-8,h-8,30) : x.rect(4,4,w-8,h-8); x.fill(); x.fillStyle = col; x.font = '700 54px sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(t, w/2, h/2 + 3); }); const sp = new THREE.Sprite(new THREE.SpriteMaterial({map:tx, depthTest:false, transparent:true})); sp.scale.set(.2, .075, 1); sp.renderOrder = 8; return sp; }
  function tube(pts, c, r){ const m = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 28, r || .012, 6, false), mat(c, {roughness:.5})); R.world.add(m); return m; }
  function makePS(x, z, ry, knob){ const g = new THREE.Group(); g.add(at(box(.8,.42,.42, mat(0x2B3050,{roughness:.45})), 0,.21,0)); g.add(at(box(.82,.04,.44, mat(0x3A4166)), 0,.44,0));
    const d = lcd(.32,.12); d.position.set(-.16,.27,.211); g.add(d);
    const kn = new THREE.Group(); if(knob) kn.userData.id = 'knob'; const kc = cyl(.075,.085,.07, mat(0xF2994A,{roughness:.35}), 24); kc.rotation.x = Math.PI/2; kn.add(kc); kn.add(at(box(.014,.06,.012, mat(0xffffff)), 0,.035,.04)); if(knob) kn.add(at(hitBox(.32,.32,.3,0), 0,0,.05)); kn.position.set(.22,.25,.24); g.add(kn);
    [[-.3,0xE25555],[-.18,0x22263A]].forEach(([tx,c])=>{ const t = cyl(.026,.026,.05, mat(c), 12); t.rotation.x = Math.PI/2; t.position.set(tx,.1,.225); g.add(t); });
    g.position.set(x, TABLE_Y, z); g.rotation.y = ry || 0; g.userData.d = d; g.userData.kn = kn; R.world.add(g); return g; }
  const crackle = () => { for(let k=0;k<7;k++) setTimeout(()=>SFX.tick(), k*28 + Math.random()*20); SFX.pop(); };
"""
rep("\n  function arrow(col){ const a = new THREE.ArrowHelper(V(1,0,0), V(0,0,0), .3, col, .08, .06); R.world.add(a); return a; }\n", HELP)

# ---- part 2: overlay field lines + equipotentials; PS model
rep("""    const ps = new THREE.Group(); ps.add(box(.8,.4,.4, mat(0x2B3050))); P.vd = lcd(.36,.14); P.vd.position.set(-.1,.05,.201); ps.add(P.vd); ps.position.set(-1.35, TABLE_Y + .2, -.6); W.add(ps); lcdSet(P.vd, String(s.V0), 'V');
    P.labels.push({obj:ps, dy:.38, text:()=>'แหล่งจ่ายไฟ'});""",
"""    const ps = makePS(-1.35, -.6, 0, false); P.vd = ps.userData.d; ps.userData.kn.rotation.z = -s.V0/300*4.5; lcdSet(P.vd, String(s.V0), 'V');
    P.labels.push({obj:ps, dy:.58, text:()=>'แหล่งจ่ายไฟ'});""")
rep("""    for(const y of [PY - .25, PY, PY + .25]) for(const z of [-.35, 0, .35]){ const a = new THREE.ArrowHelper(V(1,0,0), V(-h + .04, y, z), 2*h - .08, 0xF2994A, .07, .05); a.line.material.transparent = true; a.line.material.opacity = .5; W.add(a); }""",
"""    P.flv = []; P.eqp = [];
    for(const y of [PY - .25, PY, PY + .25]) for(const z of [-.35, 0, .35]){ const a = new THREE.ArrowHelper(V(1,0,0), V(-h + .04, y, z), 2*h - .08, 0xF2994A, .07, .05); a.line.material.transparent = true; a.line.material.opacity = .75; W.add(a); P.flv.push(a); }
    for(let k=1;k<s.d;k++){ const g = new THREE.Group(), pg = new THREE.PlaneGeometry(1.0,.8);
      const pl = new THREE.Mesh(pg, new THREE.MeshBasicMaterial({color:0x4FC3F7, transparent:true, opacity:.13, side:THREE.DoubleSide, depthWrite:false})); pl.rotation.y = Math.PI/2; g.add(pl);
      const ed = new THREE.LineSegments(new THREE.EdgesGeometry(pg), new THREE.LineBasicMaterial({color:0x1E9BD7, transparent:true, opacity:.8})); ed.rotation.y = Math.PI/2; g.add(ed);
      const t = textSpr(Math.round(s.V0*k/s.d) + ' V', '#13739F'); t.position.set(0, .47, -.42); g.add(t);
      g.position.set(h - k/100*KD, PY, 0); W.add(g); P.eqp.push(g); }""")
rep("""  function updP2(){ const s = P.s; if(!P.pr) return; const h = hw(); s.px = Math.max(-h + .01, Math.min(h - .01, s.px)); P.pr.position.set(s.px, PY, s.pz); lcdSet(P.vmd, Vp().toFixed(1), 'V');""",
"""  const eqSolved = () => { try{ const q = EQ(1).find(x=>x.k==='eq'); return !!q && eqSt(1).a.eq===q.a; }catch(_){ return false; } };
  function updP2(){ const s = P.s; if(!P.pr) return; const h = hw(); s.px = Math.max(-h + .01, Math.min(h - .01, s.px)); P.pr.position.set(s.px, PY, s.pz); lcdSet(P.vmd, Vp().toFixed(1), 'V');
    const on = s.fl !== false, eo = on && eqSolved(); (P.flv || []).forEach(o=>o.visible = on); (P.eqp || []).forEach(o=>o.visible = eo);""")

# ---- part 3: PS with draggable knob
rep("""    const ps = new THREE.Group(); ps.add(box(.8,.4,.4, mat(0x2B3050))); P.vd = lcd(.36,.14); P.vd.position.set(-.1,.05,.201); ps.add(P.vd); ps.position.set(1.25, TABLE_Y + .2, -.5); ps.rotation.y = -.3; W.add(ps);
    P.labels.push({obj:ps, dy:.38, text:()=>'แหล่งจ่ายไฟ'});""",
"""    const ps = makePS(1.25, -.5, -.3, true); P.vd = ps.userData.d; P.kn = ps.userData.kn; P.kn.userData.hy = 0;
    P.labels.push({obj:ps, dy:.58, text:()=>'แหล่งจ่ายไฟ · หมุนปุ่มส้ม'});""")
rep("""  function updP3(){ const s = P.s; if(!P.drop) return; P.drop.position.set(0, YB + .05 + s.y*(YT - YB - .1), 0); lcdSet(P.vd, String(s.V), 'V'); """,
    """  function updP3(){ const s = P.s; if(!P.drop) return; P.drop.position.set(0, YB + .05 + s.y*(YT - YB - .1), 0); if(P.vdV !== s.V){ P.vdV = s.V; lcdSet(P.vd, String(s.V), 'V'); } if(P.kn) P.kn.rotation.z = -s.V/1000*4.5; """)

# ---- parts 4 & 5
P45 = r"""
  /* ===== part 4: electroscope & induction ===== */
  const KX = .35, KY = TABLE_Y + 1.0, LY = TABLE_Y + .5, RODL = .8, GX = KX + .85, GZ = .2;
  const RODS = {e:{n:'แท่งยางแข็ง', sg:-1, by:'ถูด้วยขนสัตว์'}, g:{n:'แท่งแก้ว', sg:1, by:'ถูด้วยผ้าไหม'}};
  const prox = () => Math.max(0, Math.min(1, 1 - P.s.gap/.5));
  function q4(){ const s = P.s, sr = RODS[s.rod].sg, I = 5*prox();
    if(s.gap===0) return s.gnd ? {qk:0, ql:0, Q:0} : {qk:sr*2, ql:sr*3, Q:s.Q};
    if(s.gnd) return {qk:-sr*Math.min(4, I), ql:0, Q:Math.round(-sr*Math.min(4, I))};
    return {qk:s.Q/2 - sr*I, ql:s.Q/2 + sr*I, Q:s.Q}; }
  function buildP4(){ const W = R.world, s = P.s, rd = RODS[s.rod];
    const es = new THREE.Group(); es.position.set(KX, TABLE_Y, 0); W.add(es); P.es = es;
    es.add(at(cyl(.36,.4,.06, mat(0x6B4A2E,{roughness:.6}), 32), 0,.03,0));
    es.add(at(cyl(.3,.3,.62, GLASS(.16), 40, true), 0,.37,0));
    es.add(at(cyl(.315,.315,.04, mat(0x333844,{roughness:.4}), 40), 0,.7,0));
    es.add(at(cyl(.06,.07,.09, mat(0x1E1E22,{roughness:.8}), 16), 0,.75,0));
    es.add(at(cyl(.012,.012, KY - LY, METAL(), 10), 0, (KY + LY)/2 - TABLE_Y, 0));
    es.add(at(box(.06,.015,.02, METAL()), 0, LY - TABLE_Y, 0));
    const kb = sph(.07, METAL(), 28); kb.position.y = KY - TABLE_Y; es.add(kb);
    const leafM = new THREE.MeshStandardMaterial({color:0xF2C14E, metalness:.85, roughness:.28, side:THREE.DoubleSide, envMap:ENVMAP, envMapIntensity:1.2});
    P.lv = [-1,1].map(sd=>{ const g = new THREE.Group(), pl = new THREE.Mesh(new THREE.PlaneGeometry(.05,.24), leafM); pl.position.y = -.12; g.add(pl); g.position.set(sd*.012, LY - TABLE_Y, .012); g.userData.sd = sd; es.add(g);
      g.userData.sp = [-.05,-.11,-.17].map(y=>{ const c = chSpr(1, .04); c.position.set(0, y, .02); g.add(c); return c; }); return g; });
    P.cl = P.lv.map(g=>g.userData.sp);
    P.ck = []; for(let k=0;k<8;k++){ const a = Math.PI*(.55 + k/7*.9), c = chSpr(1, .042); c.position.set(Math.cos(a)*.09, KY - TABLE_Y + Math.sin(a)*.09, .05); es.add(c); P.ck.push(c); }
    P.labels.push({obj:es, dy:-.02, text:()=>'อิเล็กโทรสโคป'});
    // charged rod on a sliding stand
    const rod = new THREE.Group(); rod.userData.id = 'rod'; rod.userData.hy = 0;
    const rm = s.rod==='e' ? mat(0x2A2A33,{roughness:.3}) : new THREE.MeshStandardMaterial({color:0xD6ECFA, transparent:true, opacity:.55, roughness:.05, envMap:ENVMAP, envMapIntensity:1.5});
    const rb = cyl(.024,.024, RODL, rm, 16); rb.rotation.z = Math.PI/2; rb.position.x = -RODL/2; rod.add(rb);
    rod.add(at(sph(.024, rm, 12), 0,0,0));
    const hd = cyl(.032,.032,.18, mat(0x8A5A2B,{roughness:.7}), 16); hd.rotation.z = Math.PI/2; hd.position.x = -RODL + .1; rod.add(hd);
    const sh = KY - TABLE_Y; rod.add(at(cyl(.014,.014, sh, mat(0x9AA3B5,{metalness:.6, roughness:.3}), 8), -RODL + .16, -sh/2, 0)); rod.add(at(cyl(.1,.12,.035, mat(0x2B3050), 20), -RODL + .16, -sh + .018, 0));
    rod.add(at(hitBox(RODL + .2, .35, .35, 0), -RODL/2, 0, 0));
    P.cr = [-.05,-.13,-.21,-.29].map(x=>{ const c = chSpr(rd.sg, .042); c.position.set(x, .045, .02); rod.add(c); return c; });
    W.add(rod); P.rod = rod;
    P.labels.push({obj:rod, dy:.16, text:()=>`${RODS[P.s.rod].n} (${RODS[P.s.rod].sg > 0 ? '+' : '−'})`});
    // ground plate
    const gp = new THREE.Group(); gp.userData.id = 'gnd'; gp.userData.hy = .05;
    gp.add(at(box(.34,.025,.34, mat(0x3E8E5A,{roughness:.5})), 0,.013,0));
    const gt = canvasTex(256, 256, (x,w,h)=>{ x.fillStyle = '#3E8E5A'; x.fillRect(0,0,w,h); x.strokeStyle = '#fff'; x.lineWidth = 14; x.lineCap = 'round'; x.beginPath(); x.moveTo(128,40); x.lineTo(128,120); x.moveTo(58,120); x.lineTo(198,120); x.moveTo(84,160); x.lineTo(172,160); x.moveTo(110,200); x.lineTo(146,200); x.stroke(); });
    const gtp = new THREE.Mesh(new THREE.PlaneGeometry(.3,.3), new THREE.MeshStandardMaterial({map:gt, roughness:.6})); gtp.rotation.x = -Math.PI/2; gtp.position.y = .027; gp.add(gtp);
    gp.add(hitBox(.5,.3,.5,.1)); gp.position.set(GX, TABLE_Y, GZ); W.add(gp); P.gp = gp;
    P.labels.push({obj:gp, dy:.12, text:()=>P.s.gnd ? 'สายดิน (ต่ออยู่)' : 'สายดิน (แตะเพื่อต่อ)'});
    P.gwOn = null; updP4();
  }
  function gndWire(){ const s = P.s; if(P.gwOn === s.gnd) return; P.gwOn = s.gnd; if(P.gw){ R.world.remove(P.gw); R.world.remove(P.gcl); }
    const A = V(GX, TABLE_Y + .03, GZ), pts = s.gnd ? [A, V(GX, TABLE_Y + .3, GZ), V(KX + .45, KY - .05, .1), V(KX + .07, KY, 0)] : [A, V(GX, TABLE_Y + .28, GZ), V(GX - .16, TABLE_Y + .4, GZ), V(GX - .3, TABLE_Y + .34, GZ)];
    P.gw = tube(pts, 0x2E9E5B, .01); const e = pts[pts.length - 1]; P.gcl = at(box(.05,.03,.03, mat(0xE25555,{roughness:.4})), e.x + (s.gnd ? .02 : 0), e.y, e.z); R.world.add(P.gcl); }
  function updP4(){ const s = P.s; if(!P.rod) return; P.rod.position.set(KX - .07 - s.gap, KY, 0);
    const c = q4(), sh = s.show;
    const put = (arr, n, sg) => arr.forEach((sp,k)=>{ sp.visible = sh && k < n; if(sp.visible && sg) sp.material.map = chTex(sg); });
    put(P.ck, Math.min(8, Math.round(Math.abs(c.qk))), Math.sign(c.qk));
    P.cl.forEach(arr=>put(arr, Math.min(3, Math.round(Math.abs(c.ql)/1.5)), Math.sign(c.ql)));
    P.cr.forEach(sp=>sp.visible = sh); gndWire(); }
  function resetInd(){ const s = P.s; s.st = [0,0,0,0]; s.how = null; s.show = true; s.lockShow = false; }
  function setGap(g){ const s = P.s, sr = RODS[s.rod].sg, was = s.gap, ql0 = q4().ql; s.gap = Math.max(0, Math.min(1, Math.round(g*100)/100)); const p = prox();
    if(s.gap===0){ if(was > 0){ crackle(); if(s.gnd){ s.Q = 0; P.say = 'แท่งแตะปุ่มโลหะขณะต่อสายดิน ประจุไหลลงดินหมดครับ'; } else { s.Q = sr*4; resetInd(); s.how = 'cond'; P.say = `แท่งแตะปุ่มโลหะ ประจุ${sr > 0 ? 'บวก' : 'ลบ'}ย้ายมาที่อิเล็กโทรสโคป นี่คือการทำให้มีประจุโดย "การสัมผัส" ไม่ใช่การเหนี่ยวนำ ลองต่อสายดินตอนแท่งอยู่ไกลเพื่อคายประจุ แล้วทำใหม่ครับ`; } } return; }
    if(s.gnd){ s.Q = Math.round(-sr*Math.min(4, 5*p));
      if(p >= .6){ if(!s.st[1]){ s.st = [1,1,0,0]; P.say = 'แท่งอยู่ใกล้ขณะต่อสายดิน ประจุชนิดเดียวกับแท่งถูกผลักลงดิน ต่อไปถอดสายดินก่อนครับ'; } }
      else if(p < .15 && s.st[1]){ resetInd(); P.say = 'นำแท่งออกก่อนถอดสายดิน ประจุจึงไหลกลับจนเป็นกลาง ลองใหม่: ถอดสายดินก่อน แล้วค่อยนำแท่งออกครับ'; }
      return; }
    if(p >= .6 && !s.Q){ s.sawNear = true; if(!s.st[0]) s.st = [1,0,0,0]; P.say = `แผ่นโลหะกางออก! ประจุ${sr > 0 ? 'ลบ' : 'บวก'}ถูกดูดขึ้นไปที่ปุ่มโลหะ ประจุ${sr > 0 ? 'บวก' : 'ลบ'}ถูกผลักลงไปที่แผ่นโลหะครับ`; }
    else if(p < .15 && !s.Q && was < .4){ P.say = 'นำแท่งออก ประจุกลับไปกระจายเหมือนเดิม แผ่นโลหะหุบลงครับ'; }
    if(s.st[2] && !s.st[3] && p < .15){ s.st[3] = 1; s.indOk = true;
      if(!S.miss[3].sign){ s.show = false; s.lockShow = true; P.say = 'สำเร็จ! อิเล็กโทรสโคปมีประจุค้างไว้ แผ่นโลหะกางอยู่ ผมซ่อนสัญลักษณ์ประจุไว้ ลองนำแท่งเข้าใกล้อีกครั้ง แล้วบอกว่าเป็นประจุชนิดใดครับ'; }
      else P.say = 'เหนี่ยวนำสำเร็จอีกครั้งครับ'; }
    else if(s.Q && s.gap < was && p >= .3){ const ql = q4().ql; P.say = Math.abs(ql) < Math.abs(ql0) ? 'นำแท่งเข้าใกล้ แผ่นโลหะหุบลง แสดงว่าประจุบนอิเล็กโทรสโคปเป็นชนิดตรงข้ามกับแท่งครับ' : 'นำแท่งเข้าใกล้ แผ่นโลหะกางมากขึ้น แสดงว่าประจุบนอิเล็กโทรสโคปเป็นชนิดเดียวกับแท่งครับ'; }
  }
  function setGnd(on){ const s = P.s, sr = RODS[s.rod].sg, p = prox(), q0 = s.Q; s.gnd = on; SFX.pop();
    if(on){ if(s.gap===0) s.Q = 0; else s.Q = Math.round(-sr*Math.min(4, 5*p));
      if(p >= .6){ s.st = [1,1,0,0]; P.say = 'ต่อสายดินแล้ว แผ่นโลหะหุบลง เพราะประจุที่ถูกผลักไหลออกทางสายดิน (ถ้าแท่งเป็นบวก อิเล็กตรอนไหลขึ้นมาจากดิน) ครับ'; }
      else { resetInd(); P.say = q0 ? 'ต่อสายดินตอนไม่มีแท่งอยู่ใกล้ = คายประจุ อิเล็กโทรสโคปกลับเป็นกลางครับ' : 'ต่อสายดินแล้วครับ'; } }
    else { if(s.st[1] && p >= .6 && s.Q){ s.st = [1,1,1,0]; s.how = 'ind'; P.say = 'ถอดสายดินแล้ว ประจุที่ถูกดูดไว้ออกไปไหนไม่ได้ ต่อไปนำแท่งออกไปไกล ๆ ครับ'; }
      else { if(!s.Q) resetInd(); P.say = 'ถอดสายดินแล้วครับ'; } }
  }
  function checkSign(sg){ const s = P.s, rs = RODS[s.rod].sg, q = Math.sign(q4().Q);
    if(!S.miss[3].ind){ P.warn = 'ทำการเหนี่ยวนำให้สำเร็จก่อนครับ'; return; }
    if(!q){ P.warn = 'ตอนนี้อิเล็กโทรสโคปเป็นกลางแล้ว (อาจต่อสายดินหรือแตะแท่ง) ทำการเหนี่ยวนำใหม่อีกครั้งครับ'; return; }
    if(sg===q){ s.signOk = true; s.show = true; s.lockShow = false; P.say = `ถูกต้องครับ ประจุเป็น${q > 0 ? 'บวก' : 'ลบ'} ${q===rs ? 'ชนิดเดียวกับแท่ง (ได้จากการสัมผัส)' : 'ตรงข้ามกับ' + RODS[s.rod].n} ดูสัญลักษณ์ประจุได้แล้ว`; return; }
    s.wrong += 1;
    P.warn = sg===rs && s.how!=='cond' ? hint(['ไม่ใช่ครับ ถ้าเป็นประจุชนิดเดียวกับแท่ง พอนำแท่งเข้าใกล้ แผ่นโลหะต้องกางมากขึ้น แต่มันหุบลง', 'ตอนต่อสายดิน ประจุชนิดเดียวกับแท่งถูกผลักออกไปทางสายดิน ที่เหลือจึงเป็นชนิดไหนครับ']) : hint(['ยังไม่ถูกครับ นำแท่งเข้าใกล้อีกครั้ง ดูว่าแผ่นโลหะหุบหรือกาง', 'แผ่นโลหะหุบเมื่อแท่งเข้าใกล้ = ประจุตรงข้ามกับแท่ง กางมากขึ้น = ชนิดเดียวกันครับ']);
  }

  /* ===== part 5: parallel-plate capacitor ===== */
  const E0 = 8.85e-12, GK = .06;
  const capC = () => E0*P.s.A/(P.s.cd*1e-3), capQ = () => capC()*P.s.cV*1e9;
  function buildP5(){ const W = R.world, s = P.s, w = Math.sqrt(s.A)*4.5, cy = TABLE_Y + w/2 + .14; P.w = w; P.cy = cy;
    const pm = new THREE.MeshStandardMaterial({color:0xC9CFDA, metalness:.9, roughness:.25, envMap:ENVMAP});
    const plate = (edge, id, sg) => { const g = new THREE.Group(); if(id){ g.userData.id = id; g.userData.hy = 0; } g.add(box(.03, w, w, pm)); g.add(box(.036,.03, w + .01, mat(edge), 0, w/2, 0));
      g.add(at(cyl(.02,.02,.14, mat(0xE8E2C8), 8), 0, -w/2 - .07, 0)); g.add(at(cyl(.1,.12,.035, mat(0x2B3050), 20), 0, -w/2 - .14 + .018, 0)); if(id) g.add(hitBox(.4, w + .2, w + .2, 0));
      const sp = []; for(let r=0;r<3;r++) for(let c=0;c<4;c++){ const m = chSpr(sg, .05); m.position.set(-sg*.03, (r - 1)*w*.3, (c - 1.5)*w*.24); g.add(m); sp.push(m); } g.userData.sp = sp; W.add(g); return g; };
    P.lp = plate(0xE25555, null, 1); P.mp = plate(0x5B8DEF, 'plate', -1); P.cp = P.lp.userData.sp; P.cn = P.mp.userData.sp;
    P.ar = []; for(const y of [-w/4, 0, w/4]) for(const z of [-w/4, 0, w/4]){ const a = new THREE.ArrowHelper(V(1,0,0), V(0, cy + y, z), .2, 0xF2994A, .04, .03); a.line.material.transparent = a.cone.material.transparent = true; W.add(a); a.userData.yz = [cy + y, z]; P.ar.push(a); }
    const ps = makePS(-1.3, -.45, .35, true); P.ps = ps; P.vd = ps.userData.d; P.kn = ps.userData.kn; P.kn.userData.hy = 0;
    P.labels.push({obj:ps, dy:.58, text:()=>'แหล่งจ่ายไฟ'});
    const qm = new THREE.Group(); qm.add(at(box(.46,.32,.14, mat(0xF2C94C,{roughness:.45})), 0,.16,0)); P.qd = lcd(.36,.13); P.qd.position.set(0,.18,.071); qm.add(P.qd); qm.position.set(1.1, TABLE_Y, .55); qm.rotation.y = -.35; W.add(qm);
    P.labels.push({obj:qm, dy:.44, text:()=>'คูลอมบ์มิเตอร์'});
    const bl = new THREE.Group(); bl.add(at(cyl(.05,.06,.08, METAL(), 16), 0,.04,0)); P.bm = new THREE.MeshStandardMaterial({color:0xFFF3C4, emissive:0xFFC23D, emissiveIntensity:0, transparent:true, opacity:.85, roughness:.1}); bl.add(at(sph(.085, P.bm, 20), 0,.15,0));
    P.glow = new THREE.Sprite(new THREE.SpriteMaterial({map:canvasTex(128,128,(x)=>{ const g = x.createRadialGradient(64,64,4,64,64,64); g.addColorStop(0,'rgba(255,230,140,1)'); g.addColorStop(1,'rgba(255,200,60,0)'); x.fillStyle = g; x.fillRect(0,0,128,128); }), transparent:true, depthWrite:false, blending:THREE.AdditiveBlending})); P.glow.scale.set(.7,.7,1); P.glow.position.y = .15; P.glow.visible = false; bl.add(P.glow);
    bl.position.set(-1.0, TABLE_Y, .7); W.add(bl); P.labels.push({obj:bl, dy:.3, text:()=>'หลอดไฟ'});
    P.labels.push({obj:P.mp, dy:w/2 + .1, text:()=>`d = ${P.s.cd} mm`});
    P.cdW = null; P.vdV = null; updP5(); }
  function cables5(){ (P.cab || []).forEach(m=>R.world.remove(m)); const gp = P.s.cd*GK, by = TABLE_Y + .03;
    const t1 = P.ps.localToWorld(V(-.3,.1,.25)), t2 = P.ps.localToWorld(V(-.18,.1,.25)), bl = V(-1.0, TABLE_Y + .05, .7);
    P.cab = [tube([t1, V(t1.x + .2, by, t1.z + .25), V(-gp/2 - .25, by, .25), V(-gp/2, by, 0)], 0xE25555), tube([t2, V(t2.x + .3, by, t2.z + .45), V(gp/2 + .25, by, .35), V(gp/2, by, 0)], 0x22263A), tube([bl, V(-.6, by, .6), V(-gp/2 - .1, by, .15)], 0x8A93A8, .008)]; }
  function updP5(){ const s = P.s; if(!P.mp) return; const gp = s.cd*GK, f = 1 - (P.dis || 0), Q = capQ()*f;
    P.lp.position.set(-gp/2, P.cy, 0); P.mp.position.set(gp/2, P.cy, 0);
    const n = Q > .05 ? Math.max(1, Math.min(12, Math.round(Math.sqrt(Q)*1.2))) : 0; P.cp.forEach((m,k)=>m.visible = k < n); P.cn.forEach((m,k)=>m.visible = k < n);
    const E = s.cV/s.cd, op = .3 + .7*Math.min(1, E/100); P.ar.forEach(a=>{ a.position.set(-gp/2 + .02, a.userData.yz[0], a.userData.yz[1]); a.setLength(Math.max(.02, gp - .04), Math.min(.05, gp*.35), Math.min(.035, gp*.28)); a.visible = s.cV > 0 && f > .3; a.line.material.opacity = a.cone.material.opacity = op; });
    if(P.vdV !== s.cV){ P.vdV = s.cV; lcdSet(P.vd, String(s.cV), 'V'); } lcdSet(P.qd, Q.toFixed(Q < 10 ? 2 : 1), 'nC'); P.kn.rotation.z = -s.cV/300*4.5;
    P.bm.emissiveIntensity = (P.dis || 0)*2.5; P.glow.visible = (P.dis || 0) > .02; P.glow.material.opacity = Math.min(1, (P.dis || 0)*Math.min(1.2, .4 + (P.disU || 0)/4));
    if(P.cdW !== s.cd){ P.cdW = s.cd; cables5(); } }
  function rec5(){ const s = P.s; if(!s.cV){ P.say = 'ตั้งความต่างศักย์ก่อนครับ (หมุนปุ่มสีส้ม หรือกด V +)'; return; }
    const Q = +capQ().toFixed(2), k = s.cV + '|' + s.cd, first = !s.crecs[k]; delete s.crecs[k]; s.crecs[k] = {V:s.cV, d:s.cd, Q}; const ks = Object.keys(s.crecs); if(ks.length > 10) delete s.crecs[ks[0]]; P.lastC = k;
    P.say = `V = ${s.cV} V, d = ${s.cd} mm → Q = ${Q} nC${first ? ' บันทึกแล้ว' : ''}ครับ`; }
  function discharge(){ const s = P.s; if(!s.cV){ P.warn = 'ยังไม่มีประจุ ตั้งความต่างศักย์ก่อนครับ'; return; } const U = .5*capC()*s.cV*s.cV*1e6; P.dis = 1; P.disU = U; crackle();
    P.say = `หลอดไฟสว่างวาบจากพลังงานที่สะสม U = ½CV² ≈ ${U.toFixed(2)} µJ แล้วแหล่งจ่ายไฟประจุใหม่ครับ`; }
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
  const byGroup = (key, val) => { const g = {}; Object.values(P.s.crecs).forEach(r=>{ if(r.V > 0) (g[r[key]] = g[r[key]] || new Set()).add(r[val]); }); return Math.max(0, ...Object.values(g).map(x=>x.size)); };

  function sync(){"""
rep("\n  function sync(){", P45)

# answers / missions
rep("const OKA = [{qv:'x2', inv:'q'}, {eq:'par', uni:'same'}, {e:'int'}];", "const OKA = [{qv:'x2', inv:'q'}, {eq:'par', uni:'same'}, {e:'int'}, {}, {}];")
rep("{e:'ยังไม่ถูกครับ ลองหารประจุแต่ละหยดด้วย 1.6 × 10⁻¹⁹ C'}];", "{e:'ยังไม่ถูกครับ ลองหารประจุแต่ละหยดด้วย 1.6 × 10⁻¹⁹ C'}, {}, {}];")
rep("""    "q": {id:"qq", f:() =>""", """    "c": {id:"cv5", f:() => { const so = cSol(); return so ? so.txt : null; }},
    "q": {id:"qq", f:() =>""")
rep("    else { const n = Object.keys(s.drops).length; if(n >= 1) set('bal'); if(s.qOk) set('q'); if(n >= 3) set('n3'); if(s.ans.e) set('e'); }",
    """    else if(P.i===2){ const n = Object.keys(s.drops).length; if(n >= 1) set('bal'); if(s.qOk) set('q'); if(n >= 3) set('n3'); if(s.ans.e) set('e'); }
    else if(P.i===3){ if(s.sawNear) set('near'); if(s.indOk) set('ind'); if(s.signOk) set('sign'); }
    else { if(byGroup('d','V') >= 3) set('qv'); if(s.cOk) set('c'); if(byGroup('V','d') >= 2) set('dd'); }""")

# mascot
rep("""    const n = Object.keys(s.drops).length;
    if(!m.bal) return ['think', s.V===0 ? 'กดปุ่มบนจอเพิ่มความต่างศักย์ ดูหยดน้ำมันในกล้องครับ' : 'ปรับความต่างศักย์จนหยดน้ำมันลอยนิ่งครับ'];""",
"""    if(P.i===3){ const p = prox();
      if(!m.near) return ['think', 'ลากแท่ง (หรือกด เข้าใกล้) ให้อยู่ใกล้ปุ่มโลหะด้านบน แต่อย่าให้แตะ แล้วดูแผ่นโลหะบางครับ'];
      if(!m.ind){ if(s.how==='cond' && s.Q) return ['think', 'ตอนนี้มีประจุจากการสัมผัส ต่อสายดินตอนแท่งอยู่ไกลเพื่อคายประจุ แล้วทำแบบเหนี่ยวนำครับ'];
        if(s.st[2]) return ['think', 'ขั้นที่ 4: นำแท่งออกไปไกล ๆ (ถอยออก) ครับ'];
        if(s.gnd) return ['think', p >= .6 ? 'ขั้นที่ 3: ถอดสายดินก่อน (แท่งยังอยู่ใกล้) ครับ' : 'นำแท่งเข้าใกล้ปุ่มโลหะ ขณะต่อสายดินอยู่ครับ'];
        return ['think', p >= .6 ? 'ขั้นที่ 2: แตะสายดินเพื่อต่อ ขณะแท่งยังอยู่ใกล้ครับ' : 'ขั้นที่ 1: นำแท่งเข้าใกล้ปุ่มโลหะ (ไม่แตะ) ครับ']; }
      if(!m.sign) return ['think', 'ประจุที่ค้างอยู่เป็นชนิดใด นำแท่งเข้าใกล้อีกครั้ง ถ้าแผ่นโลหะหุบลง = ตรงข้ามกับแท่ง แล้วตอบในแผงด้านข้างครับ'];
      return ['yay', 'การเหนี่ยวนำให้ประจุชนิดตรงข้ามกับวัตถุที่นำมาใกล้ และประจุรวมคงตัวถ้าไม่มีทางให้ประจุเข้าออกครับ']; }
    if(P.i===4){
      if(!m.qv) return ['think', `ตั้ง d ไว้เท่าเดิม หมุนปุ่มสีส้มบนแหล่งจ่ายไฟ (หรือกด V +/−) วัดประจุให้ครบ 3 ค่า V ครับ (ได้ ${byGroup('d','V')})`];
      if(!m.c) return ['think', 'คำนวณความจุ C = Q/V จากแถวล่าสุด ตอบเป็น pF ครับ'];
      if(!m.dd) return ['think', 'ลากแผ่นสีฟ้าหรือกด d +/− เปลี่ยนระยะห่างแผ่นที่ V เดิม แล้วดูประจุครับ'];
      return ['yay', 'ความจุขึ้นกับรูปร่าง C = ε₀A/d ไม่ขึ้นกับ V ครับ ลองกด ⚡ คายประจุผ่านหลอดไฟ ดูพลังงานที่สะสมได้']; }
    const n = Object.keys(s.drops).length;
    if(!m.bal) return ['think', s.V===0 ? 'หมุนปุ่มสีส้มบนแหล่งจ่ายไฟ (ลากขึ้น) หรือกด +10 เพิ่มความต่างศักย์ ดูหยดน้ำมันในกล้องครับ' : 'ปรับความต่างศักย์จนหยดน้ำมันลอยนิ่ง (ใช้ ±1 ปรับละเอียด) ครับ'];""")

# refreshUI per part
rep("""      dk = DB('q1', `q₁ ${s.q1.toFixed(2)} µC ▸`, 1) + DB('dr:-5','r −5') + DB('dr:-1','r −1') + PILL(`r = ${Math.round(s.r*100)} cm`) + DB('dr:1','r +1') + DB('dr:5','r +5');""",
    """      dk = DB('q1', `q₁ ${s.q1.toFixed(2)} µC ▸`, 1) + DB('dr:-5','r −5') + PILL(`r = ${Math.round(s.r*100)} cm`) + DB('dr:5','r +5');""")
rep("""      ctrls = FORM(`<b>แผ่นโลหะคู่ขนาน</b> E = {V|d}<br><span class="note">ตอนนี้ V = ${s.V0} V · d = ${s.d} cm</span>`)""",
    """      sig += eqSolved();
      ctrls = FORM(`<b>แผ่นโลหะคู่ขนาน</b> E = {V|d}<br><span class="note">ตอนนี้ V = ${s.V0} V · d = ${s.d} cm</span>`) + `<div class="row" style="gap:6px;margin-top:8px">${B('pv', `V ${s.V0} V ▸`, 1)}${B('pd', `d ${s.d} cm ▸`, 1)}</div>` + (eqSolved() ? '' : '<div class="note" style="margin-top:6px">🔒 เส้นศักย์เท่าจะแสดงในฉากหลังตอบคำถามท้ายตอนเรื่องเส้นศักย์เท่าถูก</div>')""")
rep("""      dk = DB('pv', `V ${s.V0} V ▸`, 1) + DB('pd', `d ${s.d} cm ▸`, 1) + DB('ps:-0.5','◀ 0.5 cm') + DB('ps:0.5','0.5 cm ▶') + DB('pz','↕ เลื่อนขนานแผ่น');""",
    """      dk = DB('ps:-0.5','◀ 0.5 cm') + PILL(`${sOf().toFixed(1)} cm`) + DB('ps:0.5','0.5 cm ▶') + DB('pz','↕ ขนานแผ่น') + DB('fl', s.fl !== false ? '🧲 เส้นแรง ✓' : '🧲 เส้นแรง', s.fl !== false);""")
rep("""    } else {
      const ks = Object.keys(s.drops);""", """    } else if(P.i===2){
      const ks = Object.keys(s.drops);""")
rep("""      dk = DB('dv:-50','−50') + DB('dv:-10','−10') + DB('dv:-1','−1') + PILL(s.V + ' V') + DB('dv:1','+1') + DB('dv:10','+10') + DB('dv:50','+50') + DB('nd','🆕 หยดใหม่', 1);
    }""", """      dk = DB('dv:-10','−10') + DB('dv:-1','−1') + PILL(s.V + ' V') + DB('dv:1','+1') + DB('dv:10','+10') + DB('nd','🆕 หยดใหม่', 1);
    } else if(P.i===3){
      const rd = RODS[s.rod], c = q4(), ang = Math.min(.75, .16*Math.abs(c.ql)), stp = ['นำแท่งเข้าใกล้ (ไม่แตะ)','ต่อสายดิน','ถอดสายดิน (แท่งยังใกล้)','นำแท่งออก'];
      sig = JSON.stringify(['p3', s.rod, !!m.ind, !!m.sign, s.lockShow]);
      ctrls = FORM('<b>การเหนี่ยวนำไฟฟ้า</b> ประจุอิสระในตัวนำย้ายที่เมื่อมีวัตถุมีประจุมาใกล้ · ประจุรวมคงตัวถ้าไม่มีทางให้ประจุเข้าออก (กฎอนุรักษ์ประจุ)')
        + `<div class="row" style="gap:6px;margin-top:8px;align-items:center">${B('rod', `${rd.n} (${rd.sg > 0 ? '+' : '−'}) ▸`, 1)}<span class="note">${rd.by}</span></div>`
        + (m.ind && !m.sign ? `<h2 style="margin-top:8px">ประจุที่ค้างบนอิเล็กโทรสโคปเป็นชนิดใด</h2><div class="note">ทดสอบ: นำแท่งเดิมเข้าใกล้อีกครั้ง ถ้าแผ่นโลหะหุบลง = ประจุตรงข้ามกับแท่ง</div><div class="row" style="gap:6px;margin-top:6px">${B('sg:1', '+ บวก', true)}${B('sg:-1', '− ลบ', true)}</div>` : '');
      res = `<h2>อิเล็กโทรสโคป · แผ่นโลหะ${ang > .1 ? 'กาง' : 'หุบ'}</h2>` + grid('auto 1fr', `<b>แท่ง</b><span>${rd.n} (${rd.sg > 0 ? '+' : '−'})</span><b>ระยะแท่ง–ปุ่ม</b><span>${s.gap===0 ? 'แตะ' : Math.round(s.gap*100) + ' cm'}</span><b>สายดิน</b><span>${s.gnd ? 'ต่ออยู่' : 'ไม่ต่อ'}</span><b>ประจุรวม</b><span>${s.show ? (c.Q > 0 ? '+' : c.Q < 0 ? '−' : '') + Math.abs(c.Q) + ' หน่วย' : '? (ทดสอบด้วยแท่ง)'}</span>`)
        + `<div style="margin-top:8px;font-size:14px;line-height:1.7">${stp.map((t,k)=>`<div${HL(s.st[k] && !s.st[k+1])}>${s.st[k] ? '✅' : '⬜'} ${k+1}. ${t}</div>`).join('')}</div>`;
      dk = DB('rf','⬅ ถอยออก') + DB('rn','เข้าใกล้ ➡') + DB('gnd', s.gnd ? '⏚ ถอดสายดิน' : '⏚ ต่อสายดิน', s.gnd) + (s.lockShow ? '' : DB('show', s.show ? '👁 ซ่อนประจุ' : '👁 แสดงประจุ', s.show));
    } else {
      const ks = Object.keys(s.crecs);
      sig = JSON.stringify(['p4', ks.length, s.cOk, !!m.c, s.A]);
      ctrls = FORM(`<b>ตัวเก็บประจุแผ่นคู่ขนาน</b> C = {Q|V} = {ε₀A|d}<br><span class="note">A = ${s.A} m² · ε₀ = 8.85 × 10⁻¹² F/m · 1 nC = 10⁻⁹ C · 1 pF = 10⁻¹² F</span>`)
        + (ks.length && !s.cOk && !m.c ? `<h2 style="margin-top:6px">ความจุจากแถวล่าสุด (pF)</h2>${IN('cv5','เช่น 130','c','ตรวจ')}` : '')
        + `<div style="margin-top:8px">${B('dis', '⚡ คายประจุผ่านหลอดไฟ', false)}</div>`;
      res = `<h2>คูลอมบ์มิเตอร์ · ${capQ().toFixed(2)} nC</h2>` + (ks.length ? grid('auto auto auto', `<b>V (V)</b><b>d (mm)</b><b>Q (nC)</b>${ks.map(k=>{ const r = s.crecs[k], h = HL(P.lastC===k); return `<span${h}>${r.V}</span><span${h}>${r.d}</span><span${h}>${r.Q.toFixed(2)}</span>`; }).join('')}`) : '<div class="note">ปรับ V หรือ d แล้วค่าจะบันทึกลงตารางอัตโนมัติ</div>');
      dk = DB('cv:-25','V −') + PILL(`${s.cV} V`) + DB('cv:25','V +') + DB('cd:-1','d −') + PILL(`d ${s.cd} mm`) + DB('cd:1','d +');
    }""")

# actions
rep("    else if(v.startsWith('ans:')){ const [,q,a] = v.split(':'); answer(q, a); }",
"""    else if(v==='fl') act(()=>{ s.fl = s.fl===false; });
    else if(v==='rod') act(()=>{ s.rod = s.rod==='e' ? 'g' : 'e'; rebuild(); P.say = `เปลี่ยนเป็น${RODS[s.rod].n} (${RODS[s.rod].by} มีประจุ${RODS[s.rod].sg > 0 ? 'บวก' : 'ลบ'}) ครับ`; });
    else if(v==='rn' || v==='rf') act(()=>{ const nx = v==='rn' ? [.9,.12,0].find(g=>g < s.gap - .005) : [0,.12,.9].find(g=>g > s.gap + .005); if(nx!==undefined) setGap(nx); });
    else if(v==='gnd') act(()=>setGnd(!s.gnd));
    else if(v==='show') act(()=>{ if(!s.lockShow) s.show = !s.show; });
    else if(v.startsWith('sg:')) act(()=>checkSign(+v.slice(3)));
    else if(v.startsWith('cv:')) act(()=>{ s.cV = Math.max(0, Math.min(300, s.cV + (+v.slice(3)))); rec5(); });
    else if(v.startsWith('cd:')) act(()=>{ s.cd = Math.max(1, Math.min(10, s.cd + (+v.slice(3)))); rec5(); });
    else if(v==='c') act(()=>checkC(val('cv5'))); else if(v.startsWith('c:')) act(()=>{ const so = cSol(); checkC(v.slice(2)==='auto' ? String(so ? so.t : '') : v.slice(2)); });
    else if(v==='dis') act(discharge);
    else if(v.startsWith('ans:')){ const [,q,a] = v.split(':'); answer(q, a); }""")

# pointer
NEWPTR = r"""  function bindPointer(){
    const el = R.renderer.domElement;
    const DRG = () => P.i===0 ? [P.A] : P.i===1 ? [P.pr] : P.i===2 ? [P.kn] : P.i===3 ? [P.rod, P.gp] : [P.mp, P.kn];
    el.addEventListener('pointerdown', e=>{
      if(!P || drag) return; pick(e);
      const h = R.raycaster.intersectObjects(R.world.children, true).find(x=>rootOf(x.object));
      let g = h ? rootOf(h.object) : null; const lim = Math.max(60, el.clientWidth*.1);
      if(!g){ let best = lim; DRG().forEach(o=>{ if(!o) return; const p = scr(o.getWorldPosition(V(0,0,0)).add(V(0, o.userData.hy!=null ? o.userData.hy : (P.i===0 ? SY - TABLE_Y : .3), 0))); const dd = Math.hypot(p.x - e.clientX, p.y - e.clientY); if(dd < best){ best = dd; g = o; } }); }
      if(!g) return;
      drag = {id:g.userData.id, x:e.clientX, y:e.clientY, pid:e.pointerId, moved:false, V0:P.i===2 ? P.s.V : P.s.cV};
      if(drag.id==='rod' || drag.id==='plate' || drag.id==='A' || drag.id==='probe') SFX.pick();
      e.stopImmediatePropagation(); e.preventDefault(); R.controls.enabled = false; try{ el.setPointerCapture(e.pointerId); }catch(_){}
    }, {capture:true});
    el.addEventListener('pointermove', e=>{ if(!drag || e.pointerId!==drag.pid) return; if(!drag.moved && Math.abs(e.clientX-drag.x) + Math.abs(e.clientY-drag.y) > 5) drag.moved = true; if(!drag.moved || drag.id==='gnd') return;
      pick(e); const pt = new THREE.Vector3(), s = P.s;
      if(drag.id==='A'){ if(!R.raycaster.ray.intersectPlane(new THREE.Plane(UP, -SY), pt)) return; const r0 = s.r; s.r = Math.max(.06, Math.min(.45, Math.round((XB - pt.x)/KS*100)/100)); if(s.r!==r0) SFX.tick(); updP1(); }
      else if(drag.id==='probe'){ if(!R.raycaster.ray.intersectPlane(new THREE.Plane(UP, -PY), pt)) return; const h = hw(); s.px = Math.max(-h + .01, Math.min(h - .01, Math.round((pt.x)/KD*1000)/1000*KD)); s.pz = Math.max(-.45, Math.min(.45, Math.round(pt.z*20)/20)); updP2(); }
      else if(drag.id==='rod'){ if(!R.raycaster.ray.intersectPlane(new THREE.Plane(UP, -KY), pt)) return; if(drag.off==null) drag.off = pt.x - P.rod.position.x; let gp = KX - .07 - (pt.x - drag.off); if(gp < .03) gp = 0; const g0 = s.gap; setGap(gp); if(Math.abs(s.gap - g0) > .04) SFX.tick(); P.dirty = true; updP4(); }
      else if(drag.id==='plate'){ if(!R.raycaster.ray.intersectPlane(new THREE.Plane(UP, -P.cy), pt)) return; const d = Math.max(1, Math.min(10, Math.round(2*pt.x/GK))); if(d!==s.cd){ s.cd = d; SFX.tick(); updP5(); P.dirty = true; } }
      else if(drag.id==='knob'){ const dv = drag.y - e.clientY + (e.clientX - drag.x)*.5;
        if(P.i===2){ const v = Math.max(0, Math.min(1000, Math.round(drag.V0 + dv*1.5))); if(v!==s.V){ s.V = v; SFX.tick(); updP3(); P.dirty = true; } }
        else { const v = Math.max(0, Math.min(300, Math.round((drag.V0 + dv*1.2)/5)*5)); if(v!==s.cV){ s.cV = v; SFX.tick(); updP5(); P.dirty = true; } } } });
    const end = e=>{ if(!drag || e.pointerId!==drag.pid) return; const d = drag; drag = null; R.controls.enabled = true;
      if(d.id==='gnd'){ if(!d.moved) act(()=>setGnd(!P.s.gnd)); return; }
      if(d.id==='A') act(()=>setR(P.s.r)); else if(d.id==='probe') act(()=>{ updP2(); rec2(); });
      else if(!d.moved) return;
      else if(d.id==='rod'){ SFX.drop(); act(()=>{}); }
      else if(d.id==='plate'){ SFX.drop(); act(rec5); }
      else if(d.id==='knob') act(()=>{ if(P.i===2) setV(P.s.V); else rec5(); }); };
    el.addEventListener('pointerup', end); el.addEventListener('pointercancel', end);
  }

"""
rep_between("  function bindPointer(){", "  /* ----- loop ----- */", NEWPTR)

# tick
rep("        updP3(); drawMic(); }", """        updP3(); drawMic(); }
      if(P.i===1 && P.eqp && P.eqp.length){ const eo = P.s.fl !== false && eqSolved(); if(P.eqp[0].visible !== eo){ P.eqp.forEach(o=>o.visible = eo); if(eo) toast('ปลดล็อกเส้นศักย์เท่าแล้ว'); } }
      if(P.i===3 && P.lv){ const ql = q4().ql, ang = Math.min(.75, .16*Math.abs(ql)); P.lv.forEach(g=>{ g.rotation.z += (g.userData.sd*ang - g.rotation.z)*Math.min(1, dt*6); }); }
      if(P.i===4 && P.dis > 0){ P.dis = Math.max(0, P.dis - dt*1.3); updP5(); }""")

# narrow-screen camera per part
rep("const el = R.renderer.domElement, a = el.clientWidth/Math.max(1, el.clientHeight); if(a < 1){ const k = Math.min(1.25, .8/a);",
    "const el = R.renderer.domElement, a = el.clientWidth/Math.max(1, el.clientHeight), c = CAMS[P.i]; if(a < (c.na || 1)){ const k = Math.min(c.nk || 1.25, (c.na ? c.na : .8)/a);")

open(F, 'w', encoding='utf-8').write(s)
print('es ok')
