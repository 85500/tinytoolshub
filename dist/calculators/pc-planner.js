
class PCPlanner extends HTMLElement{
  connectedCallback(){
    this.innerHTML=`
      <label>CPU TDP (W)<input id="cpu" type="number" placeholder="125"/></label>
      <label>GPU TDP (W)<input id="gpu" type="number" placeholder="300"/></label>
      <label>Drives/fans/etc (W)<input id="other" type="number" placeholder="40"/></label>
      <label>PSU target headroom<select id="head"><option value="1.2">20%</option><option value="1.3">30%</option><option value="1.5">50%</option></select></label>
      <label>Case fans (count)<input id="fans" type="number" placeholder="3"/></label>
      <label>Per-fan CFM<input id="cfm" type="number" placeholder="50"/></label>
      <label>Filter penalty (%)<input id="pen" type="number" value="15"/></label>
      <button id="go">Estimate</button>
      <div id="out"></div>`;
    this.querySelector('#go').onclick=()=>this.run();
  }
  run(){
    const cpu=+cpu.value||0, gpu=+gpu.value||0, other=+other.value||0;
    const head=+head.value||1.3, fans=+fans.value||0, cfm=+cfm.value||0, pen=(+pen.value||0)/100;
    const load=cpu+gpu+other, psu=Math.ceil(load*head/10)*10;
    const airflow = fans*cfm*(1-pen);
    let verdict = airflow<120 ? "Low airflow" : airflow<200 ? "OK for mid builds" : "Good airflow";
    out.innerHTML=`<div class="card small">
      <div><strong>Recommended PSU:</strong> ${psu} W</div>
      <div>Estimated intake airflow: ${airflow.toFixed(0)} CFM — ${verdict}</div>
      <div>Peak load est: ${load} W, headroom: ${(head*100-100).toFixed(0)}%</div>
    </div>`;
  }
}
customElements.define('pc-planner', PCPlanner);
