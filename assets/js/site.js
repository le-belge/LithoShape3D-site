// Curseur « éteinte / allumée », menu mobile, année du pied de page.
(function () {
  var range = document.getElementById('cmp'), top = document.getElementById('cmp-top'), handle = document.getElementById('cmp-handle');
  function set(v) { top.style.clipPath = 'inset(0 ' + (100 - v) + '% 0 0)'; handle.style.left = v + '%'; }
  if (range) { range.addEventListener('input', function () { set(range.value); }); set(range.value); }
  var burger = document.querySelector('.burger'), nav = document.querySelector('nav.main');
  if (burger) burger.addEventListener('click', function () { var o = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', o); });
  document.querySelectorAll('nav.main a').forEach(function (a) { a.addEventListener('click', function () { nav.classList.remove('open'); }); });
  var y = document.getElementById('y'); if (y) y.textContent = new Date().getFullYear();
})();
