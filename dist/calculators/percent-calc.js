class PercentCalc extends HTMLElement{
  connectedCallback(){
    this.innerHTML = `<label>Base value<input id="base" type="number" step="any"/></label>
      <label>Percent (%)<input id="pct" type="number" step="any"/></label>
      <div style="display:flex;gap:8px;margin-top:8px">
        <button id="of">X% of Y</button>
        <button id="add">Add %</button>
        <button id="sub">Subtract %</button>
      </div>
      <p id="out"></p>`;
    const base=()=>+this.querySelector('#base').value||0;
    const pct =()=>+this.querySelector('#pct').value||0;
    this.querySelector('#of').onclick=()=>this.#out((base()*pct()/100).toFixed(4));
    this.querySelector('#add').onclick=()=>this.#out((base()*(1+pct()/100)).toFixed(4));
    this.querySelector('#sub').onclick=()=>this.#out((base()*(1-pct()/100)).toFixed(4));
  }
  #out(v){ this.querySelector('#out').textContent = v; }
}
customElements.define('percent-calc', PercentCalc);
