class BoardFeetCalc extends HTMLElement{
  connectedCallback(){
    this.innerHTML = `<label>Thickness (in)<input id="t" type="number" step="any" /></label>
      <label>Width (in)<input id="w" type="number" step="any" /></label>
      <label>Length (ft)<input id="l" type="number" step="any" /></label>
      <button id="go">Calculate</button>
      <p id="out"></p>`;
    this.querySelector('#go').addEventListener('click',()=>{
      const t=+this.querySelector('#t').value||0;
      const w=+this.querySelector('#w').value||0;
      const l=+this.querySelector('#l').value||0;
      const bf=(t*w*l)/12;
      this.querySelector('#out').textContent = `${bf.toFixed(2)} board feet`;
    });
  }
}
customElements.define('boardfeet-calc', BoardFeetCalc);
