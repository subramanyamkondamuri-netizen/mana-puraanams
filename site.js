(function(){
  function translateUrl(lang){
    var clean = window.location.href.split('#')[0];
    return 'https://translate.google.com/translate?sl=en&tl=' + encodeURIComponent(lang) + '&u=' + encodeURIComponent(clean);
  }
  function installStyles(){
    if(document.getElementById('site-ui-styles')) return;
    var style=document.createElement('style');
    style.id='site-ui-styles';
    style.textContent=`.topbar{gap:18px}.topbar nav{display:flex;align-items:center;gap:18px;flex-wrap:wrap;justify-content:flex-end}.language-control{display:flex;align-items:center;gap:7px;margin-left:2px;padding-left:12px;border-left:1px solid #dcc79b}.language-control label{font-size:.76rem;color:#765f4d;font-weight:700;letter-spacing:.05em}.language-control select{font-family:Georgia,'Times New Roman',serif;border:1px solid #d7bd83;background:#fffaf0;color:#781f18;border-radius:999px;padding:7px 28px 7px 10px;cursor:pointer}.author-profile{max-width:900px;margin:0 auto 72px;padding:0 20px}.author-card{background:#fff;border:1px solid #ead9b8;border-radius:22px;box-shadow:0 16px 38px rgba(58,31,14,.15);padding:clamp(26px,5vw,48px)}.author-card h2{color:#781f18;margin:0 0 8px;font-size:clamp(2rem,5vw,3.4rem)}.author-degree{color:#c08e2f;font-weight:700;letter-spacing:.08em;margin-bottom:28px}.contact-row{display:grid;grid-template-columns:120px 1fr;gap:14px;padding:15px 0;border-top:1px solid #f0e4ca}.contact-row strong{color:#34170f}.contact-row a{color:#781f18;word-break:break-word}.author-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}.btn-primary,.btn-secondary{display:inline-block;padding:12px 18px;border-radius:999px;font-weight:700}.btn-primary{background:#781f18;color:#fff}.btn-secondary{border:1px solid #c99a34;color:#781f18;background:#fffaf0}.form-shell{max-width:900px;margin:0 auto 72px;padding:0 20px}.enquiry-form{background:#fff;border:1px solid #ead9b8;border-radius:22px;box-shadow:0 16px 38px rgba(58,31,14,.15);padding:clamp(24px,5vw,42px)}.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.field{display:flex;flex-direction:column;gap:7px}.field.full{grid-column:1/-1}.field label{font-weight:700;color:#34170f}.field input,.field textarea,.field select{width:100%;font:inherit;border:1px solid #dac49a;border-radius:12px;padding:12px 13px;background:#fffdf8;color:#2e2119}.field textarea{min-height:170px;resize:vertical}.form-note{color:#765f4d;line-height:1.6;font-size:.92rem}.submit-btn{border:0;background:#781f18;color:#fff;font:inherit;font-weight:700;border-radius:999px;padding:13px 22px;cursor:pointer}.submit-btn:hover{filter:brightness(.95)}.thanks-card{max-width:760px;margin:50px auto 90px;background:#fff;border:1px solid #ead9b8;border-radius:22px;padding:42px 28px;text-align:center;box-shadow:0 16px 38px rgba(58,31,14,.15)}@media(max-width:900px){.topbar{align-items:flex-start}.topbar nav{gap:11px;font-size:.86rem}.language-control{border-left:0;padding-left:0}.form-grid{grid-template-columns:1fr}.field.full{grid-column:auto}}@media(max-width:720px){.topbar{flex-direction:column;align-items:stretch}.topbar nav{display:flex!important;justify-content:flex-start}.language-control{width:100%;margin-top:4px}.contact-row{grid-template-columns:1fr;gap:5px}}`;
    document.head.appendChild(style);
  }
  function installNav(){
    var nav=document.querySelector('.topbar nav'); if(!nav) return; nav.innerHTML='';
    [['index.html','Home'],['index.html#library','Puraanams'],['ramayanam.html','Ramayanam'],['author.html','Author'],['enquiry.html','Enquiry']].forEach(function(pair){var a=document.createElement('a');a.href=pair[0];a.textContent=pair[1];nav.appendChild(a);});
    var wrap=document.createElement('span');wrap.className='language-control';
    var label=document.createElement('label');label.htmlFor='site-language';label.textContent='Language';
    var sel=document.createElement('select');sel.id='site-language';sel.setAttribute('aria-label','Select language');
    [['en','English'],['te','తెలుగు'],['hi','हिन्दी']].forEach(function(x){var o=document.createElement('option');o.value=x[0];o.textContent=x[1];sel.appendChild(o);});
    sel.value='en';sel.addEventListener('change',function(){if(sel.value==='en'){window.location.href=window.location.href.split('#')[0];}else{window.location.href=translateUrl(sel.value);}});
    wrap.appendChild(label);wrap.appendChild(sel);nav.appendChild(wrap);
  }
  document.addEventListener('DOMContentLoaded',function(){installStyles();installNav();});
})();