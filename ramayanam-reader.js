(function(){
  'use strict';

  var SB_URL='https://rwyuywfjouzrfsbpudlc.supabase.co';
  var SB_KEY='sb_publishable_kdHyzS1SFfAhwEQMfjZR7A_-kHn9-lI';

  function base64Bytes(value){
    var clean=(value||'').replace(/\s+/g,'');
    var binary=atob(clean);
    var bytes=new Uint8Array(binary.length);
    for(var i=0;i<binary.length;i++) bytes[i]=binary.charCodeAt(i);
    return bytes;
  }

  async function decodePayload(payload,encoding){
    if(encoding!=='gzip+base64+json-v1') throw new Error('Unsupported manuscript encoding');
    if(!('DecompressionStream' in window)) throw new Error('This browser needs gzip decompression support. Please use a current Chrome, Edge, Firefox, or Safari browser.');
    var bytes=base64Bytes(payload);
    var stream=new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
    var json=await new Response(stream).text();
    return JSON.parse(json);
  }

  async function supabaseJson(path){
    var response=await fetch(SB_URL+'/rest/v1/'+path,{headers:{apikey:SB_KEY,'Accept':'application/json'},cache:'no-store'});
    if(!response.ok) throw new Error('Supabase source request failed ('+response.status+')');
    return response.json();
  }

  function renderPages(root,pages){
    root.innerHTML='';
    var bodyPages=pages.filter(function(page){return page.page_kind==='body';});
    if(!bodyPages.length) throw new Error('No manuscript body pages found');

    bodyPages.forEach(function(page){
      var section=document.createElement('section');
      section.className='source-page';

      var label=document.createElement('div');
      label.className='source-page-label';
      label.textContent='Source PDF page '+page.page_number;

      var pre=document.createElement('pre');
      pre.className='source-page-text';
      pre.textContent=page.display_text||page.raw_text||'';

      section.appendChild(label);
      section.appendChild(pre);
      root.appendChild(section);
    });
  }

  async function loadManuscript(){
    var root=document.getElementById('ramayanam-source-reader');
    if(!root) return;
    var slug=root.getAttribute('data-kanda');
    if(!slug) return;

    var meta=document.getElementById('source-meta');
    try{
      var payloadPath='ramayanam_kanda_payloads?select=kanda_slug,encoding,payload,page_count,source_sha256,updated_at&kanda_slug=eq.'+encodeURIComponent(slug)+'&limit=1';
      var sourcePath='ramayanam_sources?select=slug,title,source_filename,page_count,sha256,imported_at&slug=eq.'+encodeURIComponent(slug)+'&limit=1';
      var results=await Promise.all([supabaseJson(payloadPath),supabaseJson(sourcePath)]);
      var payloadRow=results[0][0];
      var sourceRow=results[1][0];
      if(!payloadRow||!sourceRow) throw new Error('Verified source content was not found');
      if(payloadRow.source_sha256!==sourceRow.sha256) throw new Error('Source checksum mismatch');

      var pages=await decodePayload(payloadRow.payload,payloadRow.encoding);
      if(!Array.isArray(pages)||pages.length!==sourceRow.page_count) throw new Error('Source page-count mismatch');
      renderPages(root,pages);

      if(meta){
        meta.textContent='Source: '+sourceRow.source_filename+' · '+sourceRow.page_count+' PDF pages · checksum '+sourceRow.sha256.slice(0,12)+'… verified';
        meta.classList.add('source-meta-ready');
      }
    }catch(error){
      console.error('Ramayanam source reader:',error);
      root.innerHTML='';
      var box=document.createElement('div');
      box.className='reader-error';
      box.textContent='The verified source manuscript could not be loaded. Please refresh this page or try a current browser.';
      root.appendChild(box);
      if(meta) meta.textContent='Verified source manuscript temporarily unavailable.';
    }
  }

  document.addEventListener('DOMContentLoaded',loadManuscript);
})();
