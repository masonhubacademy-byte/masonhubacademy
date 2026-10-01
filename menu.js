/* =========================================================
   MasonHubAcademy · Menu Sanduíche Compartilhado
   Fonte única de verdade. Não duplicar em páginas.
   Uso:
     <div id="mha-menu-root"></div>
     <link rel="stylesheet" href="/menu.css">
     <script src="/menu.js" defer></script>
   ========================================================= */
(function () {
  'use strict';

  var LINKS = [
    { href: '/',                            label: 'Início · Guardião' },
    { href: '/o-que-e-maconaria.html',      label: 'O que é Maçonaria' },
    { href: '/historia-da-maconaria.html',  label: 'História' },
    { href: '/ritos-e-tradicoes.html',      label: 'Ritos e Tradições' },
    { href: '/mitos-e-verdades.html',       label: 'Mitos e Verdades' },
    { href: '/onde-a-maconaria-acontece.html', label: 'Onde Acontece' },
    { href: '/parceiros.html',              label: 'Rede de Irmãos' },
    { href: '/consultoria.html',            label: 'Consultoria' },
    { href: '/politica-de-privacidade.html',label: 'Política de Privacidade' },
    { href: '/termos-de-uso.html',          label: 'Termos de Uso' }
  ];

  function normalizePath(p) {
    var s = String(p || '').split('?')[0].split('#')[0];
    if (!s) s = '/';
    if (s.length > 1 && s.charAt(s.length - 1) === '/') s = s.slice(0, -1);
    if (s === '' || s === '/index.html') return '/';
    return s;
  }

  function isActive(href, currentPath) {
    var h = normalizePath(href);
    var c = normalizePath(currentPath);
    if (h === '/') return c === '/';
    return c === h;
  }

  function buildMenuHTML(currentPath) {
    var items = LINKS.map(function (l) {
      var cls = isActive(l.href, currentPath) ? ' class="is-active"' : '';
      return '<a href="' + l.href + '"' + cls + '>' + l.label + '</a>';
    }).join('');

    return '' +
      '<button id="mha-menu-btn" class="mha-menu-btn" type="button" ' +
        'aria-label="Abrir menu" aria-expanded="false" aria-controls="mha-menu-panel">' +
        '<span></span><span></span><span></span>' +
      '</button>' +
      '<div id="mha-menu-overlay" class="mha-menu-overlay" aria-hidden="true"></div>' +
      '<aside id="mha-menu-panel" class="mha-menu-panel" role="navigation" ' +
        'aria-label="Menu principal">' +
        '<div class="mha-menu-head">' +
          '<h2>MasonHubAcademy</h2>' +
          '<p>Conhecimento antes da Porta</p>' +
        '</div>' +
        '<nav class="mha-menu-nav">' + items + '</nav>' +
        '<div class="mha-menu-foot">' +
          'MasonHubAcademy® · Atendimento preliminar' +
        '</div>' +
      '</aside>';
  }

  function initMenu() {
    var root = document.getElementById('mha-menu-root');
    if (!root) return;
    if (document.getElementById('mha-menu-btn')) return;

    root.innerHTML = buildMenuHTML(location.pathname);

    var btn = document.getElementById('mha-menu-btn');
    var panel = document.getElementById('mha-menu-panel');
    var overlay = document.getElementById('mha-menu-overlay');
    if (!btn || !panel || !overlay) return;

    function open() {
      panel.classList.add('is-open');
      overlay.classList.add('is-open');
      btn.classList.add('is-open');
      btn.setAttribute('aria-expanded', 'true');
      btn.setAttribute('aria-label', 'Fechar menu');
      document.documentElement.style.overflow = 'hidden';
    }
    function close() {
      panel.classList.remove('is-open');
      overlay.classList.remove('is-open');
      btn.classList.remove('is-open');
      btn.setAttribute('aria-expanded', 'false');
      btn.setAttribute('aria-label', 'Abrir menu');
      document.documentElement.style.overflow = '';
    }
    function toggle() {
      if (panel.classList.contains('is-open')) close(); else open();
    }

    btn.addEventListener('click', toggle);
    overlay.addEventListener('click', close);
    panel.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', close);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel.classList.contains('is-open')) close();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMenu);
  } else {
    initMenu();
  }
})();
