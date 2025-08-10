
class SpoolManager extends HTMLElement{
  connectedCallback(){
    this.innerHTML=`
      <div style="display:flex;gap:10px;flex-wrap:wrap">
        <label style="flex:1">Name<input id="name" placeholder="PLA Gray"/></label>
        <label style="width:140px">Weight (g)<input id="w" type="number"/></label>
        <label style="width:140px">Diameter<select id="d"><option>1.75</option><option>2.85</option></select></label>
        <label style="width:140px">Density<input id="rho" type="number" step="any" value="1.24"/></label>
      </div>
      <div class="toolbar">
        <button id="add">Add/Update Spool</button>
        <button id="use">Log Usage (g)</button><input id="useg" type="number" style="width:120px"/>
      </div>
      <div id="list"></div>`;
    this.key='ame-spools';
    this.querySelector('#add').onclick=()=>this.addOrUpdate();
    this.querySelector('#use').onclick=()=>this.consume();
    this.render();
  }
  data(){ try{ return JSON.parse(localStorage.getItem(this.key)||'[]'); }catch(e){ return []; } }
  save(arr){ localStorage.setItem(this.key, JSON.stringify(arr)); }
  addOrUpdate(){
    const name=this.querySelector('#name').value.trim(); if(!name) return;
    const w=+this.querySelector('#w').value||0, d=+this.querySelector('#d').value||1.75, rho=+this.querySelector('#rho').value||1.24;
    const arr=this.data();
    const idx=arr.findIndex(s=>s.name===name);
    const r = d/10/2; const area = Math.PI*r*r; const Lm=(w/rho)/(area)/100; // meters
    const obj={name,w,d,rho,est_m:parseFloat(Lm.toFixed(1))};
    if(idx>=0) arr[idx]=obj; else arr.push(obj);
    this.save(arr); this.render();
  }
  consume(){
    const g=+this.querySelector('#useg').value||0; if(g<=0) return;
    const arr=this.data(); if(arr.length===0) return;
    arr[0].w = Math.max(0, (arr[0].w||0) - g);
    const d=arr[0].d, rho=arr[0].rho; const r=d/10/2; const area=Math.PI*r*r; const Lm=(arr[0].w/rho)/area/100;
    arr[0].est_m=parseFloat(Lm.toFixed(1));
    this.save(arr); this.render();
  }
  render(){
    const list=this.querySelector('#list'), arr=this.data();
    if(arr.length===0){ list.innerHTML='<p class="lede">No spools yet. Add one above.</p>'; return; }
    list.innerHTML = arr.map(s=>`<div class="card small"><strong>${s.name}</strong><div>${s.w} g • Ø${s.d} • est ${s.est_m} m left</div></div>`).join('');
  }
}
customElements.define('spool-manager', SpoolManager);
