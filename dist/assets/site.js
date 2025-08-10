
(function(){
  const qs=(s,el=document)=>el.querySelector(s), qsa=(s,el=document)=>[...el.querySelectorAll(s)];
  function hydrateSearch(){
    const input=qs('#global-search'); if(!input) return;
    const items=[...qsa('[data-search-item]')].map(el=>({el, key: (el.dataset.title+' '+(el.dataset.cat||'')).toLowerCase()}));
    const filter=()=>{
      const q=input.value.trim().toLowerCase();
      items.forEach(({el,key})=>{ el.parentElement.style.display = !q || key.includes(q) ? '' : 'none'; });
    };
    input.addEventListener('input', filter);
    document.addEventListener('keydown', e=>{ if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){ e.preventDefault(); input.focus(); }});
  }
  document.addEventListener('DOMContentLoaded', hydrateSearch);
})();
