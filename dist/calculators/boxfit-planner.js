
class BoxFitPlanner extends HTMLElement{
  connectedCallback(){
    this.innerHTML = `
      <label>Item L×W×H (in)<div style="display:flex;gap:8px">
        <input id="L" type="number" step="any" placeholder="10"/>
        <input id="W" type="number" step="any" placeholder="6"/>
        <input id="H" type="number" step="any" placeholder="4"/>
      </div></label>
      <label>Mode<select id="mode"><option value="139">Air (divisor 139)</option><option value="166">Ground (divisor 166)</option></select></label>
      <label>Candidate boxes (one per line, LxWxH) <textarea id="boxes" rows="5" placeholder="12x9x6\n10x8x4\n14x10x6"></textarea></label>
      <button id="go">Find best fit</button>
      <div id="out"></div>`;
    this.querySelector('#go').onclick=()=>this.run();
  }
  run(){
    const L=+this.querySelector('#L').value||0, W=+this.querySelector('#W').value||0, H=+this.querySelector('#H').value||0;
    const D=+this.querySelector('#mode').value||139;
    const boxes=this.querySelector('#boxes').value.split(/\n+/).map(s=>s.trim()).filter(Boolean).map(s=>s.split(/[xX*]/).map(Number)).filter(a=>a.length===3);
    if(!L||!W||!H||boxes.length===0){ this.querySelector('#out').textContent="Enter item and boxes."; return; }
    const dims=[L,W,H];
    function fits(box){
      const [a,b,c]=box.sort((x,y)=>x-y);
      const perms=[[dims[0],dims[1],dims[2]],[dims[0],dims[2],dims[1]],[dims[1],dims[0],dims[2]],[dims[1],dims[2],dims[0]],[dims[2],dims[0],dims[1]],[dims[2],dims[1],dims[0]]];
      for(const p of perms){
        const [x,y,z]=p.sort((m,n)=>m-n);
        if(x<=a && y<=b && z<=c) return p; // orientation that fits
      }
      return null;
    }
    const results=[];
    boxes.forEach(b=>{
      const o=fits(b);
      const vol=b[0]*b[1]*b[2];
      const dim=(b[0]*b[1]*b[2])/D;
      results.push({b, ok:!!o, orient:o, dim, vol});
    });
    results.sort((r1,r2)=> (r1.ok===r2.ok ? r1.dim-r2.dim : (r1.ok?-1:1)));
    const out=this.querySelector('#out');
    out.innerHTML = `<h3>Results</h3>` + results.map(r=>{
      const label=`${r.b[0]}×${r.b[1]}×${r.b[2]}`;
      if(!r.ok) return `<div class="card small"><strong>${label}</strong><div>Does not fit</div></div>`;
      const o=r.orient; const waste = (r.b[0]-o[0])*(r.b[1]-o[1])*(r.b[2]-o[2]);
      return `<div class="card small"><strong>${label}</strong>
        <div>Orientation: ${o.join('×')}</div>
        <div>Dim weight: ${r.dim.toFixed(2)} lb</div>
        <div>Empty volume (approx): ${Math.max(0,waste).toFixed(2)} in³</div>
      </div>`;
    }).join('');
  }
}
customElements.define('boxfit-planner', BoxFitPlanner);
