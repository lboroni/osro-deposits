import json
data = json.load(open('/sessions/ecstatic-gifted-mccarthy/mnt/outputs/data.json'))
DATA_JS = json.dumps(data, ensure_ascii=False)

html = r'''<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OSRO Midrate — Deposits Tracker</title>
<style>
:root{--bg:#11131a;--panel:#1b1f2a;--panel2:#222838;--bd:#2e3650;--tx:#e7eaf3;--mut:#8b93a7;--acc:#5b8cff;--acc2:#7c5bff;--ok:#3fcf8e;--warn:#ffb454;--bad:#ff6b6b}
*{box-sizing:border-box}
body{margin:0;font:14px/1.45 -apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--tx)}
header{padding:14px 18px;background:linear-gradient(90deg,#1b1f2a,#222838);border-bottom:1px solid var(--bd);display:flex;align-items:center;gap:14px;flex-wrap:wrap;position:sticky;top:0;z-index:30}
header h1{font-size:17px;margin:0;font-weight:700}
header .sub{color:var(--mut);font-size:12px}
.spacer{flex:1}
button{font:inherit;cursor:pointer;border:1px solid var(--bd);background:var(--panel2);color:var(--tx);padding:6px 12px;border-radius:8px}
button:hover{border-color:var(--acc)}
button.primary{background:var(--acc);border-color:var(--acc);color:#fff}
button.danger{color:var(--bad);border-color:transparent;background:transparent;padding:2px 6px}
button.danger:hover{background:rgba(255,107,107,.12)}
.wrap{display:flex;gap:16px;padding:16px;align-items:flex-start}
.main{flex:1;min-width:0}
.side{width:360px;flex:none;position:sticky;top:64px;max-height:calc(100vh - 80px);overflow:auto}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.tab{padding:8px 14px;border-radius:9px;background:var(--panel);border:1px solid var(--bd);color:var(--mut)}
.tab.active{background:var(--acc);color:#fff;border-color:var(--acc)}
.tab .n{opacity:.7;font-size:12px;margin-left:6px}
.controls{display:flex;gap:8px;align-items:center;margin-bottom:10px;flex-wrap:wrap}
input[type=text],input[type=number]{font:inherit;background:var(--panel);border:1px solid var(--bd);color:var(--tx);padding:7px 10px;border-radius:8px}
input[type=text]{min-width:160px}
.controls .cnt{color:var(--mut);font-size:12px;margin-left:auto}
label.chkfilter{display:flex;align-items:center;gap:6px;color:var(--mut);font-size:13px}
.addbar{background:var(--panel);border:1px dashed var(--bd);border-radius:10px;padding:10px;margin-bottom:12px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.addbar .tag{color:var(--mut);font-size:12px;font-weight:600}
table{width:100%;border-collapse:collapse;background:var(--panel);border-radius:10px;overflow:hidden}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--bd);font-size:13px;vertical-align:middle}
th{color:var(--mut);font-weight:600;position:sticky;top:56px;background:var(--panel2);z-index:5}
tr:hover td{background:rgba(91,140,255,.06)}
td.c{width:34px;text-align:center}
input[type=checkbox]{width:17px;height:17px;accent-color:var(--ok);cursor:pointer}
.eff{color:var(--warn)}
.muted{color:var(--mut);font-size:12px}
.unchecked td:not(.c){opacity:.45}
.panel{background:var(--panel);border:1px solid var(--bd);border-radius:12px;padding:14px;margin-bottom:14px}
.panel h2{margin:0 0 4px;font-size:14px;display:flex;align-items:center;gap:8px}
.panel h2 .pill{font-size:11px;color:var(--mut);font-weight:500}
.scope{display:flex;gap:4px;margin:8px 0 12px;flex-wrap:wrap}
.scope button{padding:4px 9px;font-size:12px;border-radius:7px}
.scope button.on{background:var(--acc2);border-color:var(--acc2);color:#fff}
.tot{display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px dashed var(--bd);font-size:13px}
.tot:last-child{border:0}
.tot .v{font-weight:700;color:var(--ok)}
.tot .v.pct{color:var(--acc)}
.tot .v.neg{color:var(--bad)}
.grp{margin-top:6px}
.grp .h{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--mut);margin:10px 0 4px;border-top:1px solid var(--bd);padding-top:8px}
.empty{color:var(--mut);font-size:12px;padding:6px 0}
mark{background:rgba(255,180,84,.3);color:inherit;border-radius:3px}
.foot{color:var(--mut);font-size:11px;padding:0 18px 18px}
</style>
</head>
<body>
<header>
  <h1>OSRO Midrate · Deposits</h1>
  <span class="sub" id="globalsub"></span>
  <span class="spacer"></span>
  <button onclick="exportJSON()">⤓ Exportar JSON</button>
  <button onclick="resetAll()" class="danger" style="border:1px solid var(--bd)">Restaurar original</button>
</header>
<div class="wrap">
  <div class="main">
    <div class="tabs" id="tabs"></div>
    <div class="controls">
      <input type="text" id="search" placeholder="Buscar nome ou efeito…" oninput="render()">
      <label class="chkfilter"><input type="checkbox" id="onlychecked" onchange="render()"> só depositados</label>
      <span class="cnt" id="tabcount"></span>
    </div>
    <div class="addbar" id="addbar"></div>
    <div id="tablewrap"></div>
  </div>
  <div class="side">
    <div class="panel">
      <h2>Totais <span class="pill" id="scopelbl"></span></h2>
      <div class="scope" id="scope"></div>
      <div id="totals"></div>
    </div>
  </div>
</div>
<div class="foot">Os dados são salvos automaticamente no seu navegador (localStorage). Marque/desmarque, adicione ou remova itens livremente. Os totais somam apenas itens <b>depositados</b> (marcados).</div>

<script>
const DEFAULT_DATA = __DATA__;
const TAB_ORDER = ["Card Deposits","Card Unlocks","Equipment","Costume"];
const TAB_FIELDS = {
  "Card Deposits":[{k:"req",label:"# Req",type:"number",w:70}],
  "Card Unlocks":[],
  "Equipment":[{k:"id",label:"ID",type:"text",w:90},{k:"origin",label:"Origin",type:"text",w:140}],
  "Costume":[{k:"id",label:"ID",type:"text",w:90},{k:"origin",label:"Origin",type:"text",w:140}]
};
const LS="osro_deposits_v1";
let DB = load();
let activeTab = TAB_ORDER[0];
let scope = "ALL"; // ALL or a tab name

function load(){ try{const s=localStorage.getItem(LS); if(s) return JSON.parse(s);}catch(e){} return JSON.parse(JSON.stringify(DEFAULT_DATA)); }
function save(){ localStorage.setItem(LS, JSON.stringify(DB)); }
function resetAll(){ if(confirm("Restaurar todos os dados originais da planilha? Suas alterações serão perdidas.")){ DB=JSON.parse(JSON.stringify(DEFAULT_DATA)); save(); render(); renderTotals(); } }
function exportJSON(){ const b=new Blob([JSON.stringify(DB,null,2)],{type:"application/json"}); const a=document.createElement("a"); a.href=URL.createObjectURL(b); a.download="osro_deposits.json"; a.click(); }

/* ---------- EFFECT PARSER ---------- */
const STAT_RE = /^(MAX HP|ATK\/MATK|ATK & MATK|HP\/SP|HP & SP|PERFECT DODGE|STR|AGI|VIT|INT|DEX|LUK|ATK|MATK|HP|SP|HIT|FLEE|CRITICAL|CRIT|PD|ASPD|MS|DEF|MDEF)\s*\+?\s*([+-]?\d+)\s*(%?)$/i;
const STAT_NAMES = ["STR","AGI","VIT","INT","DEX","LUK","ATK","MATK","HP","SP","HIT","FLEE","CRITICAL","CRIT","PD","PERFECT DODGE","ASPD","MS","DEF","MDEF"];
const STAT_ORDER = ["STR","AGI","VIT","INT","DEX","LUK","ATK","MATK","HIT","FLEE","CRIT","PD","DEF","MDEF","HP","SP","MAX HP"];
function canon(n){ n=n.toUpperCase(); if(n==="CRITICAL")return"CRIT"; if(n==="PERFECT DODGE")return"PD"; return n; }
function expand(name,num,pct){ // returns array of [stat,num,pct]
  name=name.toUpperCase();
  if(name==="ATK/MATK"||name==="ATK & MATK") return [["ATK",num,pct],["MATK",num,pct]];
  if(name==="HP/SP"||name==="HP & SP") return [["HP",num,pct],["SP",num,pct]];
  if(name==="MAX HP") return [["MAX HP",num,true]];
  return [[canon(name),num,pct]];
}
function parseSegment(seg){ const m=seg.trim().match(STAT_RE); if(!m)return null; return expand(m[1],parseInt(m[2],10),m[3]==="%"); }
// returns {stats:[[name,num,pct]...], mods:[{label,value,pct}...]}
function parseEffect(raw){
  const out={stats:[],mods:[]};
  if(!raw) return out;
  let s=raw.replace(/\s+/g," ").trim();
  if(s==="??"||s==="") return out;
  // 1) whole string as one stat segment (covers "ATK & MATK +2", "MAX HP +3%")
  let whole=parseSegment(s);
  if(whole){ out.stats.push(...whole); return out; }
  // 2) split on comma and ' & '
  let parts=s.split(/\s*,\s*|\s+&\s+/).map(x=>x.trim()).filter(Boolean);
  let parsed=parts.map(parseSegment);
  if(parsed.every(p=>p!==null)){ parsed.forEach(p=>out.stats.push(...p)); return out; }
  // 3) shared-trailing-value pattern e.g. "STR, INT, DEX, LUK +2"
  const last=parts[parts.length-1].match(STAT_RE);
  if(last && parts.slice(0,-1).every(p=>STAT_NAMES.includes(p.toUpperCase()))){
    const num=parseInt(last[2],10), pct=last[3]==="%";
    parts.slice(0,-1).forEach(p=>out.stats.push(...expand(p,num,pct)));
    out.stats.push(...expand(last[1],num,pct));
    return out;
  }
  // 4) modifier: a real value must carry an explicit +/- sign (avoids "LV1","LV3")
  const nm=s.match(/([+\-])\s*(\d+)\s*(%?)/);
  if(nm){
    const val=parseInt(nm[1]+nm[2],10);
    const pct=nm[3]==="%";
    let label=s.replace(nm[0]," ");
    label=label.replace(/\s*,\s*/g,", ").replace(/\s+/g," ").trim();
    label=label.replace(/^[,\s+\-]+|[,\s+\-]+$/g,"").trim();
    out.mods.push({label:label||s,value:val,pct});
  } else {
    out.mods.push({label:s,value:null,pct:false});
  }
  return out;
}

/* ---------- TOTALS ---------- */
function computeTotals(){
  const stats={}; const mods={};
  const tabs = scope==="ALL"? TAB_ORDER : [scope];
  for(const t of tabs){
    for(const it of (DB[t]||[])){
      if(!it.depo) continue;
      const p=parseEffect(it.effect);
      for(const [name,num,pct] of p.stats){
        const key=name+"|"+(pct?"%":"");
        stats[key]=(stats[key]||0)+num;
      }
      for(const m of p.mods){
        const key=m.label+"|"+(m.pct?"%":"");
        if(!mods[key]) mods[key]={label:m.label,pct:m.pct,value:0,count:0,hasNum:false};
        mods[key].count++;
        if(m.value!==null){ mods[key].value+=m.value; mods[key].hasNum=true; }
      }
    }
  }
  return {stats,mods};
}
function fmt(v,pct){ return (v>=0?"+":"")+v+(pct?"%":""); }
function renderTotals(){
  const {stats,mods}=computeTotals();
  let h="";
  // stats section
  const statKeys=Object.keys(stats).sort((a,b)=>{
    const [na,ua]=a.split("|"),[nb,ub]=b.split("|");
    const ia=STAT_ORDER.indexOf(na), ib=STAT_ORDER.indexOf(nb);
    if(ia!==ib) return (ia<0?99:ia)-(ib<0?99:ib);
    return ua.localeCompare(ub);
  });
  h+='<div class="grp"><div class="h">Atributos</div>';
  if(!statKeys.length) h+='<div class="empty">nenhum atributo</div>';
  for(const k of statKeys){
    const [name,unit]=k.split("|"); const v=stats[k]; const pct=unit==="%";
    h+=`<div class="tot"><span>${name}${pct?" (%)":""}</span><span class="v ${pct?"pct":""} ${v<0?"neg":""}">${fmt(v,pct)}</span></div>`;
  }
  h+='</div>';
  // modifiers
  const modKeys=Object.keys(mods).sort((a,b)=>mods[b].count-mods[a].count||a.localeCompare(b));
  h+='<div class="grp"><div class="h">Modificadores / Especiais</div>';
  if(!modKeys.length) h+='<div class="empty">nenhum</div>';
  for(const k of modKeys){
    const m=mods[k];
    const val= m.hasNum? fmt(m.value,m.pct) : `×${m.count}`;
    h+=`<div class="tot"><span>${esc(m.label)}${m.pct?" (%)":""}</span><span class="v ${m.pct?"pct":""} ${m.value<0?"neg":""}">${val}</span></div>`;
  }
  h+='</div>';
  document.getElementById("totals").innerHTML=h;
  document.getElementById("scopelbl").textContent = scope==="ALL"?"todas as abas":scope;
}

/* ---------- RENDER ---------- */
function esc(s){ return String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c])); }
function hl(s,q){ s=esc(s); if(!q)return s; try{return s.replace(new RegExp("("+q.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")+")","ig"),"<mark>$1</mark>");}catch(e){return s;} }

function renderTabs(){
  document.getElementById("tabs").innerHTML = TAB_ORDER.map(t=>{
    const arr=DB[t]||[]; const c=arr.filter(x=>x.depo).length;
    return `<div class="tab ${t===activeTab?"active":""}" onclick="setTab('${t}')">${t}<span class="n">${c}/${arr.length}</span></div>`;
  }).join("");
}
function setTab(t){ activeTab=t; document.getElementById("search").value=""; render(); }

function renderAddbar(){
  const fields=TAB_FIELDS[activeTab];
  let h=`<span class="tag">+ Novo em ${activeTab}:</span>`;
  h+=`<input type="text" id="add_name" placeholder="Nome" style="min-width:180px">`;
  h+=`<input type="text" id="add_effect" placeholder="Efeito (ex: ATK/MATK +2)" style="min-width:200px">`;
  for(const f of fields) h+=`<input type="${f.type}" id="add_${f.k}" placeholder="${f.label}" style="width:${f.w}px;min-width:${f.w}px">`;
  h+=`<button class="primary" onclick="addItem()">Adicionar</button>`;
  document.getElementById("addbar").innerHTML=h;
}
function addItem(){
  const name=document.getElementById("add_name").value.trim();
  const effect=document.getElementById("add_effect").value.trim();
  if(!name){ alert("Informe o nome."); return; }
  const it={depo:true,name,effect};
  for(const f of TAB_FIELDS[activeTab]){ const v=document.getElementById("add_"+f.k).value.trim(); it[f.k]= f.type==="number"&&v!==""? parseInt(v,10): v; }
  DB[activeTab].unshift(it); save(); render(); renderTotals();
}

function render(){
  renderTabs(); renderAddbar();
  const q=document.getElementById("search").value.trim().toLowerCase();
  const only=document.getElementById("onlychecked").checked;
  const fields=TAB_FIELDS[activeTab];
  const arr=DB[activeTab]||[];
  let rows=arr.map((it,i)=>({it,i}));
  if(only) rows=rows.filter(r=>r.it.depo);
  if(q) rows=rows.filter(r=>(r.it.name+" "+r.it.effect).toLowerCase().includes(q));
  let h=`<table><thead><tr><th class="c">✓</th><th>Nome</th><th>Efeito</th>`;
  for(const f of fields) h+=`<th>${f.label}</th>`;
  h+=`<th class="c"></th></tr></thead><tbody>`;
  if(!rows.length) h+=`<tr><td colspan="${3+fields.length+1}" class="empty" style="padding:14px">Nenhum item.</td></tr>`;
  for(const {it,i} of rows){
    h+=`<tr class="${it.depo?"":"unchecked"}">`;
    h+=`<td class="c"><input type="checkbox" ${it.depo?"checked":""} onchange="toggle(${i})"></td>`;
    h+=`<td>${hl(it.name,q)}</td>`;
    h+=`<td class="eff">${hl(it.effect,q)}</td>`;
    for(const f of fields) h+=`<td class="muted">${esc(it[f.k])}</td>`;
    h+=`<td class="c"><button class="danger" title="Remover" onclick="del(${i})">✕</button></td>`;
    h+=`</tr>`;
  }
  h+=`</tbody></table>`;
  document.getElementById("tablewrap").innerHTML=h;
  const c=arr.filter(x=>x.depo).length;
  document.getElementById("tabcount").textContent=`${c} depositados · ${rows.length} exibidos · ${arr.length} total`;
  let g=0,gt=0; for(const t of TAB_ORDER){g+=(DB[t]||[]).filter(x=>x.depo).length; gt+=(DB[t]||[]).length;}
  document.getElementById("globalsub").textContent=`${g} depositados de ${gt} itens`;
}
function toggle(i){ DB[activeTab][i].depo=!DB[activeTab][i].depo; save(); render(); renderTotals(); }
function del(i){ if(confirm("Remover \""+DB[activeTab][i].name+"\"?")){ DB[activeTab].splice(i,1); save(); render(); renderTotals(); } }

function renderScope(){
  let h=`<button class="${scope==='ALL'?'on':''}" onclick="setScope('ALL')">Todas</button>`;
  h+=TAB_ORDER.map(t=>`<button class="${scope===t?'on':''}" onclick="setScope('${t}')">${t}</button>`).join("");
  document.getElementById("scope").innerHTML=h;
}
function setScope(s){ scope=s; renderScope(); renderTotals(); }

renderScope(); render(); renderTotals();
</script>
</body>
</html>'''

html = html.replace("__DATA__", DATA_JS)
open('/sessions/ecstatic-gifted-mccarthy/mnt/outputs/OSRO_Deposits_Tracker.html','w').write(html)
print("written", len(html), "bytes")
