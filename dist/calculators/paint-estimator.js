class PaintEstimator extends HTMLElement{
  connectedCallback(){
    this.innerHTML = `<label>Wall area (sq ft)<input id="a" type="number" step="any" /></label>
      <label>Coats<select id="c"><option>1</option><option>2</option><option>3</option></select></label>
      <label>Covers (sq ft/gal)<input id="cov" type="number" value="350"/></label>
      <button id="go">Estimate</button>
      <p id="out"></p>`;
    this.querySelector('#go').addEventListener('click',()=>{
      const a=+this.querySelector('#a').value||0;
      const c=+this.querySelector('#c').value||1;
      const cov=+this.querySelector('#cov').value||350;
      const gallons = (a*c)/cov;
      const cans = Math.ceil(gallons);
      this.querySelector('#out').textContent = `~${gallons.toFixed(2)} gallons (${cans} can${cans>1?'s':''})`;
    });
  }
}
customElements.define('paint-estimator', PaintEstimator);
