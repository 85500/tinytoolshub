class DimWeight extends HTMLElement{
  connectedCallback(){
    this.innerHTML = `<label>Length (in)<input id="L" type="number" step="any" /></label>
      <label>Width (in)<input id="W" type="number" step="any" /></label>
      <label>Height (in)<input id="H" type="number" step="any" /></label>
      <label>Divisor<select id="D"><option value="139">Air (139)</option><option value="166">Ground (166)</option></select></label>
      <button id="go">Compute</button><p id="out"></p>`;
    this.querySelector('#go').addEventListener('click',()=>{
      const L=+this.querySelector('#L').value||0, W=+this.querySelector('#W').value||0, H=+this.querySelector('#H').value||0;
      const D=+this.querySelector('#D').value||139;
      const dim = (L*W*H)/D;
      this.querySelector('#out').textContent = `Dimensional weight: ${dim.toFixed(2)} lb`;
    });
  }
}
customElements.define('dim-weight', DimWeight);
