class UnitConverter extends HTMLElement{
  connectedCallback(){
    this.innerHTML = `<label>Value<input id="v" type="number" step="any" /></label>
      <label>From<select id="from"><option>feet</option><option>meters</option><option>inches</option><option>centimeters</option></select></label>
      <label>To<select id="to"><option>meters</option><option>feet</option><option>inches</option><option>centimeters</option></select></label>
      <button id="go">Convert</button>
      <p id="out"></p>`;
    this.querySelector('#go').addEventListener('click',()=>this.convert());
  }
  convert(){
    const v=parseFloat(this.querySelector('#v').value||0);
    const f=this.querySelector('#from').value;
    const t=this.querySelector('#to').value;
    const m = {'feet':0.3048,'meters':1,'inches':0.0254,'centimeters':0.01};
    const res = (v*m[f])/m[t];
    this.querySelector('#out').textContent = isFinite(res)? `${res.toFixed(4)} ${t}` : '';
  }
}
customElements.define('unit-converter', UnitConverter);
