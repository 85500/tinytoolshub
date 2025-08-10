
class QuoteBuilder extends HTMLElement{
  connectedCallback(){
    this.innerHTML=`
      <label>Items (name, qty, unit cost) — one per line
        <textarea id="lines" rows="7" placeholder="Plywood 3/4, 2, 52.00
Screws 1-1/4, 1, 6.50
Labor (hours), 3, 45.00"></textarea>
      </label>
      <div style="display:flex;gap:10px;flex-wrap:wrap">
        <label style="flex:1">Tax % <input id="tax" type="number" step="any" value="8.75"/></label>
        <label style="flex:1">Markup % <input id="margin" type="number" step="any" value="20"/></label>
        <label style="flex:1">Discount % <input id="disc" type="number" step="any" value="0"/></label>
      </div>
      <div class="toolbar" style="margin:8px 0">
        <button id="calc">Calculate</button>
        <button id="csv">Export CSV</button>
      </div>
      <div id="out"></div>`;
    this.querySelector('#calc').onclick=()=>this.calc();
    this.querySelector('#csv').onclick=()=>this.csv();
  }
  parse(){
    const lines=this.querySelector('#lines').value.split(/\n+/).map(s=>s.trim()).filter(Boolean);
    const items=[]; for(const ln of lines){
      const m=ln.match(/^([^,]+),\s*([\d\.]+),\s*([\d\.]+)/); if(!m) continue;
      items.push({name:m[1], qty:+m[2], unit:+m[3]});
    }
    const tax=+this.querySelector('#tax').value||0, margin=+this.querySelector('#margin').value||0, disc=+this.querySelector('#disc').value||0;
    return {items, tax, margin, disc};
  }
  calc(){
    const {items,tax,margin,disc}=this.parse();
    let sub=0; items.forEach(i=> sub += i.qty*i.unit);
    const discount = sub*(disc/100);
    const afterDisc = sub - discount;
    const taxed = afterDisc*(1+tax/100);
    const total = taxed*(1+margin/100);
    this.querySelector('#out').innerHTML = `<div class="card small">
      <div>Subtotal: $${sub.toFixed(2)}</div>
      <div>Discount: −$${discount.toFixed(2)}</div>
      <div>After discount: $${afterDisc.toFixed(2)}</div>
      <div>+ Tax (${tax}%): $${(taxed-afterDisc).toFixed(2)}</div>
      <div>+ Markup (${margin}%): $${(total-taxed).toFixed(2)}</div>
      <div><strong>Total quote: $${total.toFixed(2)}</strong></div>
    </div>`;
  }
  csv(){
    const {items,tax,margin,disc}=this.parse();
    let rows=[["Item","Qty","Unit","Line Total"],...items.map(i=>[i.name,i.qty,i.unit,(i.qty*i.unit).toFixed(2)])];
    let sub=0; items.forEach(i=> sub += i.qty*i.unit);
    const discount = sub*(disc/100);
    const afterDisc = sub - discount;
    const taxed = afterDisc*(1+tax/100);
    const total = taxed*(1+margin/100);
    rows.push(["Subtotal","","",sub.toFixed(2)]);
    rows.push(["Discount %",disc,"",(-discount).toFixed(2)]);
    rows.push(["Tax %",tax,"", (taxed-afterDisc).toFixed(2)]);
    rows.push(["Markup %",margin,"", (total-taxed).toFixed(2)]);
    rows.push(["Total","","", total.toFixed(2)]);
    const csv = rows.map(r=>r.join(",")).join("\n");
    const blob = new Blob([csv], {type:"text/csv"});
    const a=document.createElement('a');
    a.href=URL.createObjectURL(blob);
    a.download="quote.csv";
    a.click();
  }
}
customElements.define('quote-builder', QuoteBuilder);
