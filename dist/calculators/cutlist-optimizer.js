
class CutListOptimizer extends HTMLElement{
  connectedCallback(){
    this.innerHTML = `
      <label>Stock length (in)<input id="stock" type="number" step="any"/></label>
      <label>Kerf (saw blade width, in)<input id="kerf" type="number" step="any" value="0.125"/></label>
      <label>Required cuts (in, one per line)<textarea id="cuts" rows="6" placeholder="48\n36\n24\n24"></textarea></label>
      <button id="go">Optimize</button>
      <p id="summary"></p>
      <div id="plan"></div>`;

    this.querySelector('#go').onclick = ()=> this.optimize();
  }
  parse(){
    const stock = +this.querySelector('#stock').value||0;
    const kerf = +this.querySelector('#kerf').value||0;
    const cuts = this.querySelector('#cuts').value.split(/\s+/).map(Number).filter(x=>x>0);
    return {stock, kerf, cuts};
  }
  optimize(){
    const {stock, kerf, cuts} = this.parse();
    if(!stock || cuts.length===0){ this.querySelector('#summary').textContent="Enter stock and cuts."; return; }
    const parts = cuts.slice().sort((a,b)=>b-a); // descending
    const boards = [];
    for(const p of parts){
      let best=-1, minWaste=1e9;
      for(let i=0;i<boards.length;i++){
        const b=boards[i];
        const used = b.reduce((s,x)=>s+x,0);
        const slots = b.length>0 ? b.length : 0;
        const remaining = stock - used - (Math.max(0, b.length)*kerf);
        const waste = remaining - p - (kerf);
        if(p + kerf <= remaining && Math.abs(waste) < minWaste){
          minWaste = Math.abs(waste); best=i;
        }
      }
      if(best<0) boards.push([p]);
      else boards[best].push(p);
    }
    // compute stats
    let stockCount = boards.length;
    let totalUsed=0, totalKerf=0;
    boards.forEach(b=>{
      const used=b.reduce((s,x)=>s+x,0);
      const kerfAmt = Math.max(0,(b.length-1))*kerf;
      totalUsed += used; totalKerf += kerfAmt;
    });
    const totalLength = stock*stockCount;
    const waste = totalLength - totalUsed - totalKerf;
    this.querySelector('#summary').textContent = `Boards: ${stockCount} | Waste: ${waste.toFixed(2)} in (kerf ${totalKerf.toFixed(2)} in)`;

    const plan = this.querySelector('#plan');
    plan.innerHTML = boards.map((b,i)=>{
      const segs=b.map(x=>`<div style="background:#1e293b;border:1px solid #334155;border-radius:6px;padding:4px 6px;margin-right:6px">${x}"</div>`).join('');
      return `<div style="display:flex;align-items:center;margin:8px 0"><strong style="width:90px">Board ${i+1}</strong><div style="display:flex">${segs}</div></div>`;
    }).join('');
  }
}
customElements.define('cutlist-optimizer', CutListOptimizer);
