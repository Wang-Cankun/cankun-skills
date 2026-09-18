// Exercise the static feedback export handler without a server.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const html = fs.readFileSync(new URL('../skills/ck-skill-creator/eval-viewer/viewer.html', import.meta.url), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1]
  .replace('/*__EMBEDDED_DATA__*/', 'const EMBEDDED_DATA = {runs: [{id:"A"}, {id:"B"}]};')
  .replace('    init();\n    renderBenchmark();', '');
const nodes = new Map();
const node = id => {
  if (!nodes.has(id)) nodes.set(id, {value: '', textContent: '', classList: {add() {}, remove() {}}});
  return nodes.get(id);
};
let exported, download;
const context = vm.createContext({
  Blob,
  URL: {createObjectURL(blob) { exported = blob; return 'blob:review'; }, revokeObjectURL() {}},
  setTimeout(fn) { fn(); },
  document: {
    getElementById: node,
    addEventListener() {},
    body: {appendChild() {}},
    createElement(tag) {
      assert.equal(tag, 'a');
      return {click() { download = this.download; }, remove() {}};
    },
  },
  fetch() { throw new Error('Static viewer must not request a feedback API'); },
});
vm.runInContext(script, context);
node('feedback').value = 'Use the supplied report format';
vm.runInContext('visitedRuns.add("A"); showDoneDialog();', context);
assert.equal(download, 'feedback.json');
let payload = JSON.parse(await exported.text());
assert.equal(payload.status, 'in_progress');
assert.deepEqual(payload.reviews, [
  {run_id: 'A', feedback: 'Use the supplied report format', reviewed: true},
  {run_id: 'B', feedback: '', reviewed: false},
]);
vm.runInContext('visitedRuns.add("B"); showDoneDialog();', context);
payload = JSON.parse(await exported.text());
assert.equal(payload.status, 'complete');
assert.ok(!/<(?:script|link)\b[^>]+(?:src|href)=["']https?:/i.test(html), 'Viewer dependencies must be local');
console.log('Static feedback download, review state, and offline asset checks passed.');
