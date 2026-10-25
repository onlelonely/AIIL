/* AIIL shared page script for collaborators.html and publications.html.
   A page defines window.I18N = { zh: {...}, en: {...} } before loading this file,
   and may define window.onLangChange(lang) to re-render content built in JS. */
(() => {
  function setLang(lang) {
    if (!I18N[lang]) return;
    document.documentElement.lang = lang === 'zh' ? 'zh-Hant' : 'en';
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const val = I18N[lang][el.getAttribute('data-i18n')];
      if (val != null) el.innerHTML = val;
    });
    document.querySelectorAll('.lang-switch button').forEach(b => {
      b.classList.toggle('active', b.dataset.lang === lang);
    });
    try { localStorage.setItem('aiil_lang', lang); } catch(e){}
    if (typeof window.onLangChange === 'function') window.onLangChange(lang);
  }

  function refreshPenStrokes() {
    const cs = getComputedStyle(document.body);
    const primary = cs.getPropertyValue('--cinnabar').trim() || '#8d6a94';
    const secondary = cs.getPropertyValue('--ink-secondary').trim() || primary;
    const width = parseFloat(cs.getPropertyValue('--ink-width')) || 1.4;

    const wave = encodeURIComponent(
      `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 240 14' preserveAspectRatio='none'>
         <path d='M2 9 C 24 3, 50 11, 78 6 S 132 3, 160 9 S 210 4, 238 8'
               fill='none' stroke='${primary}' stroke-width='${width*1.1}' stroke-linecap='round'/>
         <path d='M2 11 C 30 7, 56 13, 82 10 S 136 8, 164 12 S 214 9, 238 11'
               fill='none' stroke='${secondary}' stroke-width='${width*0.55}' stroke-linecap='round' opacity='0.55'/>
       </svg>`
    );
    const underline = encodeURIComponent(
      `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 6' preserveAspectRatio='none'>
         <path d='M1 3 C 30 1, 60 5, 100 3 S 170 1, 199 3' fill='none'
               stroke='${primary}' stroke-width='${width}' stroke-linecap='round'/>
       </svg>`
    );
    const underlineH = encodeURIComponent(
      `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 300 10' preserveAspectRatio='none'>
         <path d='M2 6 C 40 2, 90 9, 150 5 S 250 2, 298 6' fill='none'
               stroke='${primary}' stroke-width='${width*1.3}' stroke-linecap='round'/>
         <path d='M6 8 C 60 5, 110 10, 170 7 S 260 5, 292 8' fill='none'
               stroke='${secondary}' stroke-width='${width*0.6}' stroke-linecap='round' opacity='0.5'/>
       </svg>`
    );

    document.body.style.setProperty('--pen-wave', `url("data:image/svg+xml;utf8,${wave}")`);
    document.body.style.setProperty('--pen-underline', `url("data:image/svg+xml;utf8,${underline}")`);
    document.body.style.setProperty('--pen-underline-h', `url("data:image/svg+xml;utf8,${underlineH}")`);
  }

  window.setLang = setLang;
  document.querySelectorAll('.lang-switch button').forEach(b => {
    b.addEventListener('click', () => setLang(b.dataset.lang));
  });

  let lang = null;
  try { const s = localStorage.getItem('aiil_lang'); if (s === 'zh' || s === 'en') lang = s; } catch(e){}
  if (!lang) lang = (navigator.language || '').toLowerCase().startsWith('zh') ? 'zh' : 'en';
  refreshPenStrokes();
  setLang(lang);
})();
