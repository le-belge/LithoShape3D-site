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
  function setCmp(v) { var c = 'inset(0 ' + (100 - v) + '% 0 0)'; topImg.style.clipPath = c; topImg.style.webkitClipPath = c; handle.style.left = v + '%'; }
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

  // easter egg : code Konami (ou 5 clics sur le logo) = mode lampe torche
  var torch = document.createElement('div'), tmsg = document.createElement('div'), lang = document.documentElement.lang === 'fr';
  torch.id = 'torch'; tmsg.id = 'torch-msg'; document.body.appendChild(torch); document.body.appendChild(tmsg);
  function say(t) { tmsg.textContent = t; tmsg.classList.add('on'); setTimeout(function () { tmsg.classList.remove('on'); }, 3200); }
  function moveTorch(x, y) { torch.style.setProperty('--x', x + 'px'); torch.style.setProperty('--y', y + 'px'); }
  window.addEventListener('mousemove', function (e) { moveTorch(e.clientX, e.clientY); }, { passive: true });
  window.addEventListener('touchmove', function (e) { var t = e.touches[0]; moveTorch(t.clientX, t.clientY); }, { passive: true });
  function toggleTorch() { var on = torch.classList.toggle('on'); moveTorch(innerWidth / 2, innerHeight / 2); say(on ? (lang ? 'Plus de courant ! Éclairez avec la souris. (Échap pour rallumer)' : 'Power cut! Light it up with your mouse. (Esc to restore)') : (lang ? 'Et la lumière fut.' : 'And there was light.')); }
  var code = 'ArrowUp,ArrowUp,ArrowDown,ArrowDown,ArrowLeft,ArrowRight,ArrowLeft,ArrowRight,b,a'.split(','), pos = 0;
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && torch.classList.contains('on')) { toggleTorch(); return; }
    pos = e.key.toLowerCase() === code[pos].toLowerCase() ? pos + 1 : (e.key === code[0] ? 1 : 0);
    if (pos === code.length) { pos = 0; toggleTorch(); }
  });
  var clicks = 0, clickT, brand = $('.brand');
  if (brand) brand.addEventListener('click', function () { clearTimeout(clickT); clicks++; clickT = setTimeout(function () { clicks = 0; }, 900); if (clicks >= 5) { clicks = 0; toggleTorch(); } });
  if (window.console) console.log(lang ? '💡 Psst… essayez le code Konami.' : '💡 Psst… try the Konami code.');
  var y = $('#y'); if (y) y.textContent = new Date().getFullYear();
})();
