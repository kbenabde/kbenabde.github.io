/* Site interactions for the publication list, the home-page counters and the contact e-mail. */
(function () {
  'use strict';

  /* ---------- publications: search, type filters, year chart ---------- */
  function initPublications() {
    var search = document.getElementById('pub-search');
    var filters = document.getElementById('pub-filters');
    if (!search || !filters) return;
    var count = document.getElementById('pub-count');
    var empty = document.getElementById('pub-empty');
    var items = Array.prototype.slice.call(document.querySelectorAll('.kb-pubgroup .kb-pub'));
    var groups = Array.prototype.slice.call(document.querySelectorAll('.kb-pubgroup'));
    var cols = Array.prototype.slice.call(document.querySelectorAll('.kb-chart__col'));
    var state = { q: '', filter: 'all', year: '' };

    function apply() {
      var terms = state.q.toLowerCase().split(/\s+/).filter(Boolean);
      var shown = 0;
      items.forEach(function (li) {
        var ok = true;
        if (state.filter === 'award') ok = li.getAttribute('data-award') === '1';
        else if (state.filter !== 'all') ok = li.getAttribute('data-type') === state.filter;
        if (ok && state.year) ok = li.getAttribute('data-year') === state.year;
        if (ok && terms.length) {
          var hay = li.getAttribute('data-search') || '';
          ok = terms.every(function (t) { return hay.indexOf(t) !== -1; });
        }
        li.hidden = !ok;
        if (ok) shown++;
      });
      groups.forEach(function (g) {
        Array.prototype.forEach.call(g.querySelectorAll('.kb-yearmark'), function (m) {
          var n = m.nextElementSibling, any = false;
          while (n && !n.classList.contains('kb-yearmark')) {
            if (!n.hidden) { any = true; break; }
            n = n.nextElementSibling;
          }
          m.hidden = !any;
        });
        g.hidden = !g.querySelector('.kb-pub:not([hidden])');
      });
      cols.forEach(function (c) { c.classList.toggle('is-active', c.getAttribute('data-year') === state.year); });
      if (count) count.textContent = 'Showing ' + shown + ' of ' + items.length + (state.year ? ' · ' + state.year : '');
      if (empty) empty.hidden = shown !== 0;
    }

    function setFilter(name) {
      var b = filters.querySelector('[data-filter="' + name + '"]');
      if (!b) return false;
      state.filter = name;
      Array.prototype.forEach.call(filters.querySelectorAll('.kb-filter'), function (x) {
        x.classList.toggle('is-active', x === b);
        x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
      });
      apply();
      return true;
    }

    search.addEventListener('input', function () { state.q = search.value; apply(); });
    filters.addEventListener('click', function (e) {
      var b = e.target.closest('.kb-filter');
      if (b) setFilter(b.getAttribute('data-filter'));
    });
    cols.forEach(function (c) {
      c.addEventListener('click', function () {
        var y = c.getAttribute('data-year');
        state.year = state.year === y ? '' : y;
        apply();
      });
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-jump]'), function (a) {
      a.addEventListener('click', function () { setFilter(a.getAttribute('data-jump')); });
    });
    var hash = (location.hash || '').slice(1);
    if (!(hash && setFilter(hash))) apply();
  }

  /* ---------- home page: count-up numbers ---------- */
  function initCounters() {
    var nums = document.querySelectorAll('[data-count]');
    if (!nums.length || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    Array.prototype.forEach.call(nums, function (el) {
      var target = parseInt(el.getAttribute('data-count'), 10);
      if (!target) return;
      var start = null, dur = 900;
      el.textContent = '0';
      function step(ts) {
        if (start === null) start = ts;
        var t = Math.min((ts - start) / dur, 1);
        el.textContent = String(Math.round(target * (1 - Math.pow(1 - t, 3))));
        if (t < 1) window.requestAnimationFrame(step);
      }
      window.requestAnimationFrame(step);
    });
  }

  /* ---------- contact: assemble the e-mail address in the browser ---------- */
  function initEmail() {
    Array.prototype.forEach.call(document.querySelectorAll('[data-email-user]'), function (el) {
      var addr = el.getAttribute('data-email-user') + '@' + el.getAttribute('data-email-domain');
      el.setAttribute('href', 'mailto:' + addr);
      var label = el.querySelector('[data-email-label]');
      if (label) label.textContent = addr;
    });
  }

  function init() { initPublications(); initCounters(); initEmail(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
