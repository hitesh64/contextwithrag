'use strict';
// Kept apart from app.js so that it can be tested without a browser (frontend/tests/latest.test.js).

/**
 * Wrap an async job so that it never runs twice at once and only the newest request is carried out:
 * requests made while a run is in progress wait for it, and all but the last of them are dropped.
 * The job must report its own errors; a rejection only ends that run.
 */
function latestOnly(job) {
  let newest = 0;
  let running = Promise.resolve();
  return async (...args) => {
    const mine = ++newest;
    await running;
    if (mine !== newest) return;
    running = (async () => job(...args))().catch(() => {});
    await running;
  };
}

if (typeof module !== 'undefined') module.exports = { latestOnly };
