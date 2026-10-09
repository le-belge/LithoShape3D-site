// Interactions : scene du hero (eteint/allume), curseur, onglets, apparitions au defilement, menu mobile.
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); }, $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  // en-tete : trait sous la barre apres un peu de defilement
  var top = $('header.top'); function onScroll() { top.classList.toggle('scrolled', window.scrollY > 8); var m = $('.mbar'); if (m) m.classList.toggle('show', window.scrollY > 520); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // hero : l'objet s'allume tout seul, ou au clic
  var stage = $('.stage'), btns = $$('.switch button'), timer = null, userSet = false;
  function setLit(on) { stage.classList.toggle('on', on); btns.forEach(function (b) { b.setAttribute('aria-pressed', String((b.dataset.state === 'on') === on)); }); }
  btns.forEach(function (b) { b.addEventListener('click', function () { userSet = true; clearInterval(timer); setLit(b.dataset.state === 'on'); }); });
  if (stage) { setLit(false); setTimeout(function () { setLit(true); }, reduce ? 0 : 900); if (!reduce) timer = setInterval(function () { if (!userSet) setLit(!stage.classList.contains('on')); }, 3800); }

  // curseur eteinte / allumee
  var range = $('#cmp'), topImg = $('#cmp-top'), handle = $('#cmp-handle');
  function setCmp(v) { topImg.style.clipPath = 'inset(0 ' + (100 - v) + '% 0 0)'; handle.style.left = v + '%'; }
  if (range) { range.addEventListener('input', function () { setCmp(range.value); }); setCmp(range.value); }

  // onglets des creations
  var tabs = $$('[role=tab]'), panels = $$('.panel');
  function pick(t) { tabs.forEach(function (x) { x.setAttribute('aria-selected', String(x === t)); x.tabIndex = x === t ? 0 : -1; }); panels.forEach(function (p) { p.classList.toggle('on', p.id === t.getAttribute('aria-controls')); }); }
  tabs.forEach(function (t, i) { t.addEventListener('click', function () { pick(t); }); t.addEventListener('keydown', function (e) { var n = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (n) { var x = tabs[(i + n + tabs.length) % tabs.length]; x.focus(); pick(x); } }); });

  // apparitions
  var rv = $$('.rv');
  if ('IntersectionObserver' in window && !reduce) { var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { threshold: .12 }); rv.forEach(function (n) { io.observe(n); }); }
  else rv.forEach(function (n) { n.classList.add('in'); });

  // menu mobile
  var burger = $('.burger'), nav = $('nav.main');
  if (burger) burger.addEventListener('click', function () { var o = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', String(o)); });
  $$('nav.main a').forEach(function (a) { a.addEventListener('click', function () { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }); });
  var y = $('#y'); if (y) y.textContent = new Date().getFullYear();
})();
