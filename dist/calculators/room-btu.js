class RoomBTU extends HTMLElement{
  connectedCallback(){
    this.innerHTML = `<label>Room area (sq ft)<input id="a" type="number"/></label>
      <label>Sun exposure<select id="sun"><option value="0">Normal</option><option value="10">Sunny</option><option value="-10">Shaded</option></select></label>
      <button id="go">Estimate</button><p id="out"></p>`;
    this.querySelector('#go').addEventListener('click',()=>{
      const a=+this.querySelector('#a').value||0;
      let btu=a*20;
      const sun=+this.querySelector('#sun').value;
      btu += btu*(sun/100);
      this.querySelector('#out').textContent = `Recommended ~${Math.round(btu)} BTU/h`;
    });
  }
}
customElements.define('room-btu', RoomBTU);
