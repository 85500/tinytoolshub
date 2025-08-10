class GearInches extends HTMLElement{
  connectedCallback(){
    this.innerHTML = `<label>Front teeth<input id="f" type="number"/></label>
      <label>Rear teeth<input id="r" type="number"/></label>
      <label>Wheel diameter (in)<input id="d" type="number" value="27"/></label>
      <button id="go">Calculate</button><p id="out"></p>`;
    this.querySelector('#go').addEventListener('click',()=>{
      const f=+this.querySelector('#f').value||0;
      const r=+this.querySelector('#r').value||1;
      const d=+this.querySelector('#d').value||27;
      const gi = d*(f/r);
      this.querySelector('#out').textContent = `${gi.toFixed(1)} gear inches`;
    });
  }
}
customElements.define('gear-inches', GearInches);
