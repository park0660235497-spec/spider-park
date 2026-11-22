/**
 * ParK_iLab result receiver (Google Apps Script, bound to a Google Sheet)
 * - One row per student per lab part (uid). A newer send for the same uid updates that row.
 * - Each lab part gets its own tab, named after it (e.g. "ไฟฟ้าสถิต ตอนที่ 1").
 * - Written answers get a "_คะแนน" column with a 0/1/2 drop-down for the teacher. The teacher's grades are never overwritten.
 * - A "สรุป …" tab per part is rebuilt after every send: averages per class, item difficulty, who has not finished.
 */
function doPost(e) {
  try { return out_(save_(JSON.parse(e.postData.contents))); }
  catch (err) { return out_({ok: false, err: String(err)}); }
}

/* the lab can also send through a new browser window: ?d=<web-safe base64 of the JSON> */
function doGet(e) {
  if (!e || !e.parameter || !e.parameter.d) return ContentService.createTextOutput('ParK_iLab receiver is running');
  var res;
  try {
    var json = Utilities.newBlob(Utilities.base64DecodeWebSafe(e.parameter.d)).getDataAsString('UTF-8');
    res = save_(JSON.parse(json));
  } catch (err) { res = {ok: false, err: String(err)}; }
  var msg = res.ok ? '<h2 style="color:#1F8A63">ส่งผลเรียบร้อย ✓</h2><p>ปิดหน้าต่างนี้ แล้วกลับไปที่แล็บได้เลย</p>'
                   : '<h2 style="color:#C0392B">ส่งผลไม่สำเร็จ</h2><p>' + res.err + '</p>';
  return HtmlService.createHtmlOutput('<div style="font-family:sans-serif;text-align:center;padding:40px">' + msg + '</div>').setTitle('ParK_iLab ส่งผล');
}

function save_(d) {
  var lock = LockService.getScriptLock();
  lock.waitLock(25000);
  try {
    if (!d || !d.uid) return {ok: false, err: 'no uid'};
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var tab = clean_(d.lab || 'ParK_iLab');
    var sh = ss.getSheetByName(tab) || ss.insertSheet(tab);
    var open = d._open || [], models = d._models || {}, items = d._items || [];
    var keys = Object.keys(d).filter(function (k) { return k.charAt(0) !== '_'; });

    var lastCol = sh.getLastColumn();
    var head = lastCol ? sh.getRange(1, 1, 1, lastCol).getValues()[0] : [];
    var added = false;
    keys.forEach(function (k) {
      if (head.indexOf(k) < 0) {
        head.push(k); added = true;
        if (open.indexOf(k) >= 0) head.push(k + '_คะแนน');
      }
    });
    if (added) {
      sh.getRange(1, 1, 1, head.length).setValues([head]).setFontWeight('bold').setBackground('#EAF1FD');
      sh.setFrozenRows(1);
      var rule = SpreadsheetApp.newDataValidation().requireValueInList(['0', '1', '2'], true).setAllowInvalid(false).build();
      head.forEach(function (h, i) {
        if (/_คะแนน$/.test(h)) sh.getRange(2, i + 1, 999, 1).setDataValidation(rule).setBackground('#FFF8E6');
      });
    }

    var uidCol = head.indexOf('uid') + 1, r = 0, n = sh.getLastRow();
    if (n > 1) {
      var ids = sh.getRange(2, uidCol, n - 1, 1).getValues();
      for (var i = 0; i < ids.length; i++) { if (String(ids[i][0]) === String(d.uid)) { r = i + 2; break; } }
    }
    var row = r ? sh.getRange(r, 1, 1, head.length).getValues()[0] : head.map(function () { return ''; });
    head.forEach(function (h, i) {
      if (keys.indexOf(h) < 0) return;            // keep teacher columns (grades, notes)
      var v = d[h];
      if (typeof v === 'string' && /^[=+\-@]/.test(v)) v = "'" + v;   // never run text as a formula
      row[i] = v;
    });
    if (r) sh.getRange(r, 1, 1, head.length).setValues([row]);
    else sh.getRange(sh.getLastRow() + 1, 1, 1, head.length).setValues([row]);

    summary_(ss, tab, sh, models, items);
    return {ok: true};
  } finally {
    lock.releaseLock();
  }
}

function summary_(ss, tab, sh, models, items) {
  var data = sh.getDataRange().getValues();
  if (data.length < 2) return;
  var H = data[0], rows = data.slice(1), c = function (k) { return H.indexOf(k); };
  var name = clean_('สรุป ' + tab);
  var su = ss.getSheetByName(name) || ss.insertSheet(name);
  su.clear();
  var out = [], num = function (v) { return v === '' || v === null ? null : Number(v); };
  var avg = function (a) { a = a.filter(function (x) { return x !== null && !isNaN(x); }); return a.length ? Math.round(a.reduce(function (s, x) { return s + x; }, 0) / a.length * 100) / 100 : ''; };

  out.push(['สรุปผล ' + tab, '', '', '', '', '', '']);
  out.push(['อัปเดตล่าสุด', new Date().toLocaleString('th-TH'), '', '', '', '', '']);
  out.push(['', '', '', '', '', '', '']);
  out.push(['ห้อง', 'จำนวนคน', 'ทำหลังเรียนแล้ว', 'เฉลี่ยก่อนเรียน', 'เฉลี่ยหลังเรียน', 'เฉลี่ย gain', 'คะแนนเต็ม']);
  var rooms = {};
  rows.forEach(function (x) { var k = x[c('grade')] + '/' + x[c('room')]; (rooms[k] = rooms[k] || []).push(x); });
  Object.keys(rooms).sort().concat(['รวม']).forEach(function (k) {
    var L = k === 'รวม' ? rows : rooms[k];
    var done = L.filter(function (x) { return x[c('post_score')] !== ''; });
    out.push([k, L.length, done.length, avg(L.map(function (x) { return num(x[c('pre_score')]); })), avg(done.map(function (x) { return num(x[c('post_score')]); })),
      avg(done.map(function (x) { return num(x[c('gain')]); })), L[0] ? L[0][c('max_score')] : '']);
  });

  out.push(['', '', '', '', '', '', '']);
  out.push(['ข้อ', 'ตอบถูกก่อนเรียน (%)', 'ตอบถูกหลังเรียน (%)', 'มั่นใจหลังเรียน (%)', 'มั่นใจแต่ผิด หลังเรียน (คน)', 'โจทย์', '']);
  for (var j = 1; j <= 10; j++) {
    var pk = c('pre_' + j), qk = c('post_' + j); if (pk < 0 || qk < 0) continue;
    var isOpen = H.indexOf('post_' + j + '_คะแนน') >= 0;
    var pct = function (col) { var v = rows.map(function (x) { return x[col]; }).filter(function (x) { return x !== ''; }); return v.length ? Math.round(v.filter(function (x) { return Number(x) === 1; }).length / v.length * 100) : ''; };
    var cf = c('post_' + j + '_มั่นใจ'), wrongSure = 0;
    if (!isOpen) rows.forEach(function (x) { if (x[qk] !== '' && Number(x[qk]) === 0 && Number(x[cf]) === 1) wrongSure++; });
    out.push([j + (isOpen ? ' (ข้อเขียน)' : ''), isOpen ? 'ครูตรวจ' : pct(pk), isOpen ? 'ครูตรวจ' : pct(qk), cf >= 0 ? pct(cf) : '', isOpen ? '' : wrongSure, items[j - 1] || '', '']);
  }

  var mk = Object.keys(models || {});
  if (mk.length) {
    out.push(['', '', '', '', '', '', '']);
    out.push(['แนวคำตอบข้อเขียน (ใช้ตรวจ 0/1/2)', '', '', '', '', '', '']);
    mk.forEach(function (k) { out.push([k, models[k], '', '', '', '', '']); });
  }

  out.push(['', '', '', '', '', '', '']);
  out.push(['ยังทำไม่ครบ', 'ห้อง', 'เลขที่', 'ถึงขั้น', '', '', '']);
  rows.filter(function (x) { return x[c('post_score')] === ''; })
    .sort(function (a, b) { return String(a[c('room')]).localeCompare(String(b[c('room')])) || Number(a[c('no')]) - Number(b[c('no')]); })
    .forEach(function (x) { out.push([x[c('name')], x[c('grade')] + '/' + x[c('room')], x[c('no')], x[c('stage')], '', '', '']); });

  su.getRange(1, 1, out.length, 7).setValues(out);
  su.getRange(1, 1).setFontWeight('bold').setFontSize(14);
  su.setColumnWidth(1, 220); su.setColumnWidth(6, 420);
}

function clean_(t) { return String(t).replace(/[\[\]\*\?\/\\:]/g, ' ').slice(0, 90); }

function out_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
