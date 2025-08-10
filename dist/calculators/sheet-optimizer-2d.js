
class SheetOptimizer2D extends HTMLElement{
  connectedCallback(){
    this.innerHTML = `
      <label>Sheet size (W × H, in)<div style="display:flex;gap:8px">
        <input id="sw" type="number" step="any" placeholder="48"/><input id="sh" type="number" step="any" placeholder="96"/>
      </div></label>
      <label>Kerf (in)<input id="kerf" type="number" step="any" value="0.125"/></label>
      <label>Parts (WxH x Qty, one per line)<textarea id="parts" rows="6" placeholder="12x24 x 2\n18x30 x 1\n10x10 x 4"></textarea></label>
      <button id="go">Optimize</button>
      <p id="summary"></p>
      <canvas id="cnv" width="800" height="600" style="width:100%;background:#0b1322;border-radius:12px;border:1px solid #243146"></canvas>`;
    this.querySelector('#go').onclick = ()=> this.optimize();
  }
  parse(){
    const sw=+this.querySelector('#sw').value||0, sh=+this.querySelector('#sh').value||0, kerf=+this.querySelector('#kerf').value||0;
    const lines=this.querySelector('#parts').value.split(/\n+/).map(s=>s.trim()).filter(Boolean);
    const parts=[];
    for(const ln of lines){
      const m=ln.match(/([\d\.]+)\s*x\s*([\d\.]+)\s*x\s*(\d+)/i);
      if(m){ const w=+m[1], h=+m[2], q=+m[3]; for(let i=0;i<q;i++) parts.push({w,h}); }
    }
    return {sw,sh,kerf,parts};
  }
  optimize(){
    const {sw,sh,kerf,parts}=this.parse();
    if(!sw||!sh||parts.length===0){ this.querySelector('#summary').textContent="Enter sheet and parts."; return; }
    const items=parts.slice().map((p,i)=>({id:i,w:p.w,h:p.h,area:p.w*p.h})).sort((a,b)=>b.area-a.area);
    const sheets=[], placements=[];
    function placeOnSheet(sheet, it){
      for(let r=0;r<sheet.free.length;r++){
        const fr=sheet.free[r];
        if((it.w+kerf<=fr.w && it.h+kerf<=fr.h) || (it.h+kerf<=fr.w && it.w+kerf<=fr.h)){
          let w=it.w, h=it.h;
          if(!(w+kerf<=fr.w && h+kerf<=fr.h)){ w=it.h; h=it.w; }
          const x=fr.x, y=fr.y;
          placements.push({sheet:sheet.id, x, y, w, h});
          const right = {x:x+w+kerf, y:y, w:fr.w - (w+kerf), h:h};
          const bottom = {x:x, y:y+h+kerf, w:fr.w, h:fr.h - (h+kerf)};
          const leftovers=[right,bottom].filter(r=>r.w>0.01 && r.h>0.01);
          sheet.free.splice(r,1, ...leftovers);
          return true;
        }
      }
      return false;
    }
    let sid=0;
    items.forEach(it=>{
      let done=false;
      for(const s of sheets){ if(placeOnSheet(s,it)){ done=true; break; } }
      if(!done){
        const s={id:sid++, w:sw, h:sh, free:[{x:0,y:0,w:sw,h:sh}]};
        placeOnSheet(s,it);
        sheets.push(s);
      }
    });
    const cnv=this.querySelector('#cnv'), ctx=cnv.getContext('2d');
    const cols= Math.ceil(Math.sqrt(sheets.length));
    const rows= Math.ceil(sheets.length/cols);
    const pad=16, gw=(cnv.width - pad*(cols+1))/cols, gh=(cnv.height - pad*(rows+1))/rows;
    ctx.clearRect(0,0,cnv.width,cnv.height);
    sheets.forEach((s,idx)=>{
      const r=Math.floor(idx/cols), c=idx%cols;
      const scale = Math.min(gw/s.w, gh/s.h);
      const ox = pad + c*(gw+pad);
      const oy = pad + r*(gh+pad);
      ctx.strokeStyle='#334155'; ctx.strokeRect(ox,oy,s.w*scale,s.h*scale);
      ctx.fillStyle='#1e3a8a'; ctx.strokeStyle='#60a5fa';
      placements.filter(p=>p.sheet===s.id).forEach(p=>{
        ctx.fillRect(ox+p.x*scale, oy+p.y*scale, p.w*scale, p.h*scale);
        ctx.strokeRect(ox+p.x*scale, oy+p.y*scale, p.w*scale, p.h*scale);
      });
      ctx.fillStyle='#9fb3c8'; ctx.fillText(`Sheet ${s.id+1}`, ox, oy-4);
    });
    const usedArea = placements.reduce((sum,p)=>sum+p.w*p.h,0);
    const sheetsArea = sheets.length * sw * sh;
    const waste = sheetsArea - usedArea;
    this.querySelector('#summary').textContent = `Sheets: ${sheets.length} | Used area: ${usedArea.toFixed(0)} in² | Waste (approx): ${Math.max(0,waste).toFixed(0)} in²`;
  }
}
customElements.define('sheet-optimizer-2d', SheetOptimizer2D);
