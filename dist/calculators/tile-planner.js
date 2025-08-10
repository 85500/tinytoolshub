
class TilePlanner extends HTMLElement{
  connectedCallback(){
    this.innerHTML=`
      <label>Room size (ft)<div style="display:flex;gap:8px">
        <input id="Rf" type="number" step="any" placeholder="12"/><input id="Rw" type="number" step="any" placeholder="10"/>
      </div></label>
      <label>Tile size (in)<div style="display:flex;gap:8px">
        <input id="Tf" type="number" step="any" placeholder="12"/><input id="Tw" type="number" step="any" placeholder="24"/>
      </div></label>
      <label>Grout width (in)<input id="G" type="number" step="any" value="0.125"/></label>
      <label>Waste %<input id="W" type="number" step="any" value="10"/></label>
      <label>Stagger<select id="S"><option value="0">None</option><option value="50">50% (brick)</option><option value="33">33%</option></select></label>
      <button id="go">Plan</button>
      <div id="out"></div>`;
    this.querySelector('#go').onclick=()=>this.run();
  }
  run(){
    const Rf=+Rf.value||0, Rw=+Rw.value||0;
    const Tf=+Tf.value||0, Tw=+Tw.value||0;
    const G=+G.value||0, Wp=+W.value||0, S=+S.value||0;
    if(!Rf||!Rw||!Tf||!Tw){ out.textContent="Enter room and tile sizes."; return; }
    const roomF = Rf*12, roomW = Rw*12; // inches
    const effF = Tf+G, effW = Tw+G;
    const fullRows = Math.floor((roomF+G)/effF);
    const fullCols = Math.floor((roomW+G)/effW);
    const partialF = ((roomF+G) % effF);
    const partialW = ((roomW+G) % effW);
    let tiles = fullRows*fullCols;
    // simple stagger effect: potential extra cuts at edges (approximation)
    const extra = S>0 ? Math.ceil(fullRows*0.5) : 0;
    tiles += extra;
    const waste = Math.ceil(tiles*(Wp/100));
    const total = tiles + waste;
    const covSqft = (Tf*Tw/144);
    const neededBoxes = Math.ceil((total*covSqft)/10); // if box covers ~10 sqft (common), just a hint
    out.innerHTML=`<div class="card small">
      <div><strong>Total tiles (incl. waste):</strong> ${total}</div>
      <div>Full rows × cols: ${fullRows} × ${fullCols}</div>
      <div>Edge cuts (approx): F:${partialF.toFixed(1)} in, W:${partialW.toFixed(1)} in</div>
      <div>Suggested boxes (10 sqft/box est): ${neededBoxes}</div>
    </div>`;
  }
}
customElements.define('tile-planner', TilePlanner);
