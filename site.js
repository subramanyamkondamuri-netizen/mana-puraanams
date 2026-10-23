(function(){
  var ANALYTICS_URL='https://rwyuywfjouzrfsbpudlc.supabase.co/rest/v1/analytics_hits';
  var ANALYTICS_KEY='sb_publishable_kdHyzS1SFfAhwEQMfjZR7A_-kHn9-lI';
  function translateUrl(lang){
    var clean=window.location.href.split('#')[0];
    return 'https://translate.google.com/translate?sl=en&tl='+encodeURIComponent(lang)+'&u='+encodeURIComponent(clean);
  }
  function installStyles(){
    if(document.getElementById('site-ui-styles')) return;
    var s=document.createElement('style');s.id='site-ui-styles';s.textContent=`.topbar{gap:18px}.topbar nav{display:flex;align-items:center;gap:18px;flex-wrap:wrap;justify-content:flex-end}.language-control{display:flex;align-items:center;gap:7px;margin-left:2px;padding-left:12px;border-left:1px solid #dcc79b}.language-control label{font-size:.76rem;color:#765f4d;font-weight:700;letter-spacing:.05em}.language-control select{font-family:Georgia,'Times New Roman',serif;border:1px solid #d7bd83;background:#fffaf0;color:#781f18;border-radius:999px;padding:7px 28px 7px 10px;cursor:pointer}.author-profile{max-width:900px;margin:0 auto 72px;padding:0 20px}.author-card,.enquiry-form,.thanks-card{background:#fff;border:1px solid #ead9b8;border-radius:22px;box-shadow:0 16px 38px rgba(58,31,14,.15)}.author-card{padding:clamp(26px,5vw,48px)}.author-card h2{color:#781f18;margin:0 0 8px;font-size:clamp(2rem,5vw,3.4rem)}.author-degree{color:#c08e2f;font-weight:700;letter-spacing:.08em;margin-bottom:28px}.contact-row{display:grid;grid-template-columns:120px 1fr;gap:14px;padding:15px 0;border-top:1px solid #f0e4ca}.contact-row strong{color:#34170f}.contact-row a{color:#781f18;word-break:break-word}.author-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}.btn-primary,.btn-secondary{display:inline-block;padding:12px 18px;border-radius:999px;font-weight:700}.btn-primary{background:#781f18;color:#fff}.btn-secondary{border:1px solid #c99a34;color:#781f18;background:#fffaf0}.form-shell{max-width:900px;margin:0 auto 72px;padding:0 20px}.enquiry-form{padding:clamp(24px,5vw,42px)}.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.field{display:flex;flex-direction:column;gap:7px}.field.full{grid-column:1/-1}.field label{font-weight:700;color:#34170f}.field input,.field textarea,.field select{width:100%;font:inherit;border:1px solid #dac49a;border-radius:12px;padding:12px 13px;background:#fffdf8;color:#2e2119}.field textarea{min-height:170px;resize:vertical}.form-note{color:#765f4d;line-height:1.6;font-size:.92rem}.submit-btn{border:0;background:#781f18;color:#fff;font:inherit;font-weight:700;border-radius:999px;padding:13px 22px;cursor:pointer}.thanks-card{max-width:760px;margin:50px auto 90px;padding:42px 28px;text-align:center}.ramayanam-thumb-wrap{height:auto!important;aspect-ratio:16/9;position:relative;overflow:hidden;background:#2d0d07}.ramayanam-thumb{display:block;width:100%;height:100%;object-fit:cover}.ramayanam-thumb-wrap .badge{position:absolute;top:12px;right:12px;z-index:2}.ramayanam-cover-card{max-width:720px;margin:0 auto 30px;background:#fff;border:1px solid #ead9b8;border-radius:22px;overflow:hidden;box-shadow:0 16px 38px rgba(58,31,14,.15)}.ramayanam-cover{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;background:#2d0d07}.ramayanam-cover-caption{display:flex;justify-content:space-between;gap:14px;align-items:center;padding:13px 17px;background:#fffaf0;color:#765f4d}.ramayanam-cover-caption strong{color:#781f18;font-size:1.08rem}.analytics-note{margin-top:10px;font-size:.72rem;color:#8b7563;line-height:1.45}@media(max-width:900px){.topbar{align-items:flex-start}.topbar nav{gap:11px;font-size:.86rem}.language-control{border-left:0;padding-left:0}.form-grid{grid-template-columns:1fr}.field.full{grid-column:auto}}@media(max-width:720px){.topbar{flex-direction:column;align-items:stretch}.topbar nav{display:flex!important;justify-content:flex-start}.language-control{width:100%;margin-top:4px}.contact-row{grid-template-columns:1fr;gap:5px}.ramayanam-cover-caption{flex-direction:column;align-items:flex-start}}`;
    document.head.appendChild(s);
  }
  function thumbFile(lang){return 'assets/ramayanam-thumb-'+(lang==='te'?'te':lang==='hi'?'hi':'en')+'.b64';}
  function detectedLanguage(){
    var lang=localStorage.getItem('siteLanguage')||'en';
    try{var q=new URLSearchParams(window.location.search);var ql=q.get('tl')||q.get('_x_tr_tl');if(ql==='te'||ql==='hi'||ql==='en')lang=ql;}catch(e){}
    var hl=(document.documentElement.lang||'').toLowerCase();if(hl.indexOf('te')===0)lang='te';else if(hl.indexOf('hi')===0)lang='hi';
    return lang;
  }
  function loadRamayanamThumb(lang){
    var imgs=document.querySelectorAll('[data-ramayanam-thumb]'); if(!imgs.length) return;
    fetch(thumbFile(lang)).then(function(r){if(!r.ok) throw new Error('thumb');return r.text();}).then(function(b64){var uri='data:image/jpeg;base64,'+b64.replace(/\s+/g,'');imgs.forEach(function(img){img.src=uri;});}).catch(function(){});
  }
  function installNav(){
    var nav=document.querySelector('.topbar nav');if(!nav)return;nav.innerHTML='';
    [['index.html','Home'],['index.html#library','Library'],['ramayanam.html','Ramayanam'],['upanishads.html','Upanishads'],['author.html','Author'],['enquiry.html','Enquiry']].forEach(function(p){var a=document.createElement('a');a.href=p[0];a.textContent=p[1];nav.appendChild(a);});
    var wrap=document.createElement('span');wrap.className='language-control';var label=document.createElement('label');label.htmlFor='site-language';label.textContent='Language';var sel=document.createElement('select');sel.id='site-language';sel.setAttribute('aria-label','Select language');[['en','English'],['te','తెలుగు'],['hi','हिन्दी']].forEach(function(x){var o=document.createElement('option');o.value=x[0];o.textContent=x[1];sel.appendChild(o);});
    var saved=detectedLanguage();sel.value=saved;sel.addEventListener('change',function(){var lang=sel.value;localStorage.setItem('siteLanguage',lang);loadRamayanamThumb(lang);if(lang==='en'){window.location.href=window.location.href.split('#')[0];}else{setTimeout(function(){window.location.href=translateUrl(lang);},120);}});wrap.appendChild(label);wrap.appendChild(sel);nav.appendChild(wrap);
  }
  function installAnalyticsNotice(){
    var footer=document.querySelector('footer');if(!footer||footer.querySelector('.analytics-note'))return;
    var note=document.createElement('div');note.className='analytics-note';note.textContent='This site records page visits, IP address and basic browser/device metadata for traffic analytics.';footer.appendChild(note);
  }
  function visitorId(){
    try{
      var id=localStorage.getItem('mp_visitor_id');
      if(!id){id=(window.crypto&&crypto.randomUUID)?crypto.randomUUID():'v-'+Date.now()+'-'+Math.random().toString(36).slice(2);localStorage.setItem('mp_visitor_id',id);}
      return id;
    }catch(e){return 'v-'+Date.now()+'-'+Math.random().toString(36).slice(2);}
  }
  function trackVisit(){
    if(location.protocol!=='http:'&&location.protocol!=='https:')return;
    if(/\/analytics\.html$/i.test(location.pathname))return;
    var tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||'';}catch(e){}
    var platform=(navigator.userAgentData&&navigator.userAgentData.platform)||navigator.platform||'';
    var payload={
      page_path:(location.pathname||'/')+(location.search||''),
      page_title:document.title||'',
      referrer:document.referrer||'',
      visitor_id:visitorId(),
      browser_language:navigator.language||document.documentElement.lang||'',
      timezone:tz,
      screen_width:(window.screen&&screen.width)||null,
      screen_height:(window.screen&&screen.height)||null,
      platform:platform
    };
    fetch(ANALYTICS_URL,{method:'POST',headers:{apikey:ANALYTICS_KEY,'Content-Type':'application/json','Prefer':'return=minimal'},body:JSON.stringify(payload),keepalive:true,mode:'cors'}).catch(function(){});
  }
  document.addEventListener('DOMContentLoaded',function(){installStyles();installNav();loadRamayanamThumb(detectedLanguage());installAnalyticsNotice();trackVisit();});
})();