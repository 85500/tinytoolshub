
class BatchConverter extends HTMLElement{
  connectedCallback(){
    this.innerHTML=`
      <label>Input (one per line, value unit)<textarea id="inp" rows="7" placeholder="12 ft\n4.5 m\n3 in\n10 cm"></textarea></label>
      <label>Target unit<select id="to"><option>meters</option><option>feet</option><option>inches</option><option>centimeters</option></select></label>
      <button id="go">Convert</button>
      <label>Output<textarea id="out" rows="7" readonly></textarea></label>`;
    this.querySelector('#go').onclick=()=>this.run();
  }
  run(){
    const m = {'feet':0.3048,'foot':0.3048,'ft':0.3048,'meters':1,'meter':1,'m':1,'inches':0.0254,'inch':0.0254,'in':0.0254,'centimeters':0.01,'centimeter':0.01,'cm':0.01};
    const lines=this.querySelector('#inp').value.split(/\n/);
    const to=this.querySelector('#to').value;
    const out=[];
    for(const line of lines){
      const s=line.trim(); if(!s) { out.push(''); continue; }
      const match=s.match(/^([\d\.\-]+)\s*([a-zA-Z]+)$/);
      if(!match){ out.push('ERR'); continue; }
      const val=parseFloat(match[1]); const u=match[2].toLowerCase();
      if(!(u in m)){ out.push('ERR'); continue; }
      const res = (val*m[u])/m[to];
      out.push(`${res.toFixed(4)} ${to}`);
    }
    this.querySelector('#out').value=out.join('\n');
  }
}
customElements.define('batch-converter', BatchConverter);
