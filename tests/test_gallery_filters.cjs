'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
// Optional explicit gallery directory also permits testing a staged export.
const dir = path.resolve(process.argv[2] || path.join(__dirname, '../gallery'));
const api = require(path.join(dir, 'gallery.js'));
const data = JSON.parse(fs.readFileSync(path.join(dir, 'figures.json'), 'utf8'));
const items = api.prepareItems(data);
const empty = {query:'', paper:'', object:'', category:'', type:''};
let checks = 0;
function check(ok) { assert.ok(ok); checks++; }
check(items.length > 0);
check(items.every(i => api.matchesFilters(i, empty)));
for (const item of items) {
  check(api.matchesFilters(item, {...empty, paper:item.paper_id}));
  check(api.matchesFilters(item, {...empty, category:item.category, type:item.figure_type, object:item.object_group}));
  check(!api.matchesFilters(item, {...empty, paper:'__nonexistent__'}));
  check(api.resolveFigureReference(items, item.paper_id, 'F'+item.figure_number)?.id === item.id);
  check(api.matchesFilters(item, {...empty, query:'  '+item.paper_title.toUpperCase()+'  '}));
}
for (const group of api.uniqueValues(items, 'object_group')) {
  check(items.filter(i => api.matchesFilters(i, {...empty, object:group})).length === items.filter(i => i.object_group === group).length);
}
for (const guide of data.reading_guides || []) {
  for (const ex of guide.source_examples) check(Boolean(api.resolveFigureReference(items, guide.paper_id, ex.figure_id)));
}
for (const bad of ['F0','F01','f1','F-1','F1x','']) check(api.resolveFigureReference(items, items[0].paper_id, bad) === undefined);
check(!items.some(i => api.matchesFilters(i, {...empty, query:'___no_figure_should_match_this___'})));
console.log(JSON.stringify({checks, figures:items.length, scope:'data/filter/reference model only; no browser or DOM interaction test'}));
