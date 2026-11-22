/**
 * ParK_iLab result receiver (Google Apps Script, bound to a Google Sheet)
 * Each lab sends one JSON row per student attempt (uid). A newer send for the same uid updates that row.
 * Each lab gets its own tab, named after the lab.
 */
function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var d = JSON.parse(e.postData.contents);
    if (!d || !d.uid) return out_({ok: false, err: 'no uid'});
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var tab = String(d.lab || 'ParK_iLab').replace(/[\[\]\*\?\/\\:]/g, ' ').slice(0, 90);
    var sh = ss.getSheetByName(tab) || ss.insertSheet(tab);
    var lastCol = sh.getLastColumn();
    var head = lastCol ? sh.getRange(1, 1, 1, lastCol).getValues()[0] : [];
    var keys = Object.keys(d), added = false;
    keys.forEach(function (k) { if (head.indexOf(k) < 0) { head.push(k); added = true; } });
    if (added) {
      sh.getRange(1, 1, 1, head.length).setValues([head]).setFontWeight('bold');
      sh.setFrozenRows(1);
    }
    var row = head.map(function (h) {
      var v = d.hasOwnProperty(h) ? d[h] : '';
      if (typeof v === 'string' && /^[=+\-@]/.test(v)) v = "'" + v;   // never run text as a formula
      return v;
    });
    var uidCol = head.indexOf('uid') + 1, r = 0, n = sh.getLastRow();
    if (n > 1) {
      var ids = sh.getRange(2, uidCol, n - 1, 1).getValues();
      for (var i = 0; i < ids.length; i++) { if (String(ids[i][0]) === String(d.uid)) { r = i + 2; break; } }
    }
    if (r) sh.getRange(r, 1, 1, row.length).setValues([row]);
    else sh.appendRow(row);
    return out_({ok: true, row: r || sh.getLastRow()});
  } catch (err) {
    return out_({ok: false, err: String(err)});
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  return ContentService.createTextOutput('ParK_iLab receiver is running');
}

function out_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
