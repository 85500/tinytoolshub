class FilamentEstimator extends HTMLElement{
  connectedCallback(){
    this.innerHTML = `<label>Spool net weight (g)<input id="w" type="number" step="any"/></label>
      <label>Diameter<select id="d"><option value="1.75">1.75 mm</option><option value="2.85">2.85 mm</option></select></label>
      <label>Density (g/cm³)<input id="rho" type="number" step="any" value="1.24"/></label>
      <button id="go">Estimate length</button><p id="out"></p>`;
    this.querySelector('#go').onclick=()=>{
      const w=+this.querySelector('#w').value||0;
      const d=+this.querySelector('#d').value||1.75;
      const rho=+this.querySelector('#rho').value||1.24;
      const r = d/10/2; // radius in cm
      const area = Math.PI*r*r; // cm^2
      const vol = w/rho; // cm^3
      const Lcm = vol/area; // cm
      const Lm = Lcm/100; // m
      this.querySelector('#out').textContent = `~${Lm.toFixed(1)} meters`;
    };
  }
}
customElements.define('filament-estimator', FilamentEstimator);
