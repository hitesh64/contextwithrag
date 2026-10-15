'use strict';
// Run with: node --test frontend/tests/latest.test.js   (also run by backend/tests/test_frontend_routing.py)
const assert = require('node:assert');
const { test } = require('node:test');
const { latestOnly } = require('../js/latest.js');

/** A page whose data arrives after `ms`; what is on screen is the last thing written to `screen`. */
function slowPages(screen, delays) {
  let address = '';
  const draw = latestOnly(async () => {
    const name = address;
    await new Promise(resolve => setTimeout(resolve, delays[name]));
    screen.push(name);
  });
  return name => { address = name; return draw(); };
}

const moment = () => new Promise(resolve => setTimeout(resolve, 2));

test('a slow page that was left is not drawn over the page the user went to', async () => {
  const screen = [];
  const go = slowPages(screen, { assets: 60, conflicts: 5 });
  const first = go('assets');
  await moment();   // the request for assets is now on its way
  await Promise.all([first, go('conflicts')]);
  assert.deepStrictEqual(screen, ['assets', 'conflicts']);
});

test('pages passed through on the way are not drawn at all', async () => {
  const screen = [];
  const go = slowPages(screen, { assets: 30, documents: 5, breakdowns: 5, conflicts: 5 });
  const first = go('assets');
  await moment();
  await Promise.all([first, ...['documents', 'breakdowns', 'conflicts'].map(go)]);
  assert.deepStrictEqual(screen, ['assets', 'conflicts']);
});

test('addresses changed before anything started draw only the last one', async () => {
  const screen = [];
  const go = slowPages(screen, { assets: 30, conflicts: 5 });
  await Promise.all([go('assets'), go('conflicts')]);
  assert.deepStrictEqual(screen, ['conflicts']);
});

test('two runs never overlap', async () => {
  let active = 0;
  let most = 0;
  const draw = latestOnly(async () => {
    most = Math.max(most, ++active);
    await new Promise(resolve => setTimeout(resolve, 5));
    active--;
  });
  await Promise.all([draw(), draw(), draw()]);
  assert.strictEqual(most, 1);
});

test('a run that fails does not block the next one', async () => {
  const screen = [];
  let fail = true;
  const draw = latestOnly(async () => {
    if (fail) throw new Error('page failed');
    screen.push('drawn');
  });
  await draw();
  fail = false;
  await draw();
  assert.deepStrictEqual(screen, ['drawn']);
});
