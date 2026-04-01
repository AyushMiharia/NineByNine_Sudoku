// ─── ENGINE ───────────────────────────────────────
function isValid(g,r,c,n){for(let i=0;i<9;i++){if(i!==c&&g[r][i]===n)return!1;if(i!==r&&g[i][c]===n)return!1}const br=Math.floor(r/3)*3,bc=Math.floor(c/3)*3;for(let rr=br;rr<br+3;rr++)for(let cc=bc;cc<bc+3;cc++)if((rr!==r||cc!==c)&&g[rr][cc]===n)return!1;return!0}
function getLegal(g,r,c){if(g[r][c]!==0)return[];const v=[];for(let n=1;n<=9;n++)if(isValid(g,r,c,n))v.push(n);return v}
function genSolved(){const g=Array.from({length:9},()=>Array(9).fill(0));function f(g){for(let r=0;r<9;r++)for(let c=0;c<9;c++){if(g[r][c]===0){const ns=[1,2,3,4,5,6,7,8,9].sort(()=>Math.random()-.5);for(const n of ns){if(isValid(g,r,c,n)){g[r][c]=n;if(f(g))return!0;g[r][c]=0}}return!1}}return!0}f(g);return g}
function makePuzzle(d){const cl={easy:45,medium:35,hard:28,expert:22}[d]||35;const sol=genSolved(),puz=sol.map(r=>[...r]),cells=[];for(let r=0;r<9;r++)for(let c=0;c<9;c++)cells.push([r,c]);cells.sort(()=>Math.random()-.5);let rem=81-cl;for(const[r,c]of cells){if(rem<=0)break;puz[r][c]=0;rem--}return{puzzle:puz,solution:sol}}

// ─── SOLVERS ──────────────────────────────────────
function solveBT(grid){const g=grid.map(r=>[...r]);let nd=0,bt=0,ck=0;function s(){for(let r=0;r<9;r++)for(let c=0;c<9;c++){if(g[r][c]===0){nd++;for(let n=1;n<=9;n++){ck++;if(isValid(g,r,c,n)){g[r][c]=n;if(s())return!0;g[r][c]=0;bt++}}return!1}}return!0}const t=performance.now(),ok=s();return{solved:ok,grid:g,metrics:{nodes:nd,backtracks:bt,checks:ck,time:performance.now()-t}}}

function solveMRV(grid){const g=grid.map(r=>[...r]);let nd=0,bt=0,ck=0;
function degree(r,c){let d=0;for(let i=0;i<9;i++){if(i!==c&&g[r][i]===0)d++;if(i!==r&&g[i][c]===0)d++}const br=Math.floor(r/3)*3,bc=Math.floor(c/3)*3;for(let rr=br;rr<br+3;rr++)for(let cc=bc;cc<bc+3;cc++)if((rr!==r||cc!==c)&&g[rr][cc]===0)d++;return d}
function lcv(r,c,vals){return vals.sort((a,b)=>{let ca=0,cb=0;for(const[nr,nc]of neighbors(r,c))if(g[nr][nc]===0){const lv=getLegal(g,nr,nc);if(lv.includes(a))ca++;if(lv.includes(b))cb++}return ca-cb})}
function neighbors(r,c){const s=[];for(let i=0;i<9;i++){if(i!==c)s.push([r,i]);if(i!==r)s.push([i,c])}const br=Math.floor(r/3)*3,bc=Math.floor(c/3)*3;for(let rr=br;rr<br+3;rr++)for(let cc=bc;cc<bc+3;cc++)if(rr!==r||cc!==c)s.push([rr,cc]);return s}
function mrv(){let best=null,mn=10,md=-1;for(let r=0;r<9;r++)for(let c=0;c<9;c++){if(g[r][c]===0){const lv=getLegal(g,r,c);ck++;const d=degree(r,c);if(lv.length<mn||(lv.length===mn&&d>md)){mn=lv.length;md=d;best={r,c,vals:lv};if(mn===0)return best}}}return best}
function s(){const cell=mrv();if(!cell)return!0;if(!cell.vals.length)return!1;nd++;const ordered=lcv(cell.r,cell.c,[...cell.vals]);for(const n of ordered){ck++;g[cell.r][cell.c]=n;if(s())return!0;g[cell.r][cell.c]=0;bt++}return!1}
const t=performance.now(),ok=s();return{solved:ok,grid:g,metrics:{nodes:nd,backtracks:bt,checks:ck,time:performance.now()-t}}}

function solveFC(grid){const g=grid.map(r=>[...r]);let nd=0,bt=0,ck=0,arcs=0;
function initD(){const d={};for(let r=0;r<9;r++)for(let c=0;c<9;c++)d[`${r},${c}`]=g[r][c]===0?new Set(getLegal(g,r,c)):new Set([g[r][c]]);return d}
function cloneD(d){const n={};for(const k in d)n[k]=new Set(d[k]);return n}
function getMRV(d){let best=null,mn=10;for(let r=0;r<9;r++)for(let c=0;c<9;c++){if(g[r][c]===0){const s=d[`${r},${c}`].size;if(s<mn){mn=s;best={r,c};if(mn<=1)return best}}}return best}
function nbrs(r,c){const s=new Set();for(let i=0;i<9;i++){if(i!==c)s.add(`${r},${i}`);if(i!==r)s.add(`${i},${c}`)}const br=Math.floor(r/3)*3,bc=Math.floor(c/3)*3;for(let rr=br;rr<br+3;rr++)for(let cc=bc;cc<bc+3;cc++)if(rr!==r||cc!==c)s.add(`${rr},${cc}`);return s}
function fc(d,r,c,v){for(const k of nbrs(r,c)){const[nr,nc]=k.split(",").map(Number);if(g[nr][nc]===0){ck++;d[k].delete(v);if(d[k].size===0)return!1}}return!0}
function ac3(d,r,c){const q=[];for(const k of nbrs(r,c)){const[nr,nc]=k.split(",").map(Number);if(g[nr][nc]===0)for(const k2 of nbrs(nr,nc)){const[nnr,nnc]=k2.split(",").map(Number);if(g[nnr][nnc]===0&&!(nnr===r&&nnc===c))q.push([`${nr},${nc}`,`${nnr},${nnc}`])}}
while(q.length){const[k1,k2]=q.shift();arcs++;const d1=d[k1],d2=d[k2];let rev=false;for(const v of [...d1]){ck++;if(d2.size===1&&d2.has(v)){d1.delete(v);rev=true}}if(rev){if(d1.size===0)return false;const[r1,c1]=k1.split(",").map(Number);for(const nk of nbrs(r1,c1)){const[nr,nc]=nk.split(",").map(Number);if(g[nr][nc]===0&&nk!==k2)q.push([nk,k1])}}}return true}
function s(d){const cell=getMRV(d);if(!cell)return!0;const vals=[...d[`${cell.r},${cell.c}`]];if(!vals.length)return!1;nd++;for(const n of vals){ck++;const saved=cloneD(d);g[cell.r][cell.c]=n;d[`${cell.r},${cell.c}`]=new Set([n]);if(fc(d,cell.r,cell.c,n)&&ac3(d,cell.r,cell.c)&&s(d))return!0;g[cell.r][cell.c]=0;Object.assign(d,saved);bt++}return!1}
const t=performance.now(),ok=s(initD());return{solved:ok,grid:g,metrics:{nodes:nd,backtracks:bt,checks:ck,time:performance.now()-t,arcs}}}

function solveMinCon(grid){const g=grid.map(r=>[...r]);let nd=0,bt=0,ck=0,iters=0,restarts=0;
const fixed=new Set();for(let r=0;r<9;r++)for(let c=0;c<9;c++)if(g[r][c]!==0)fixed.add(`${r},${c}`);
function initBoxes(){for(let br=0;br<9;br+=3)for(let bc=0;bc<9;bc+=3){const used=new Set(),empty=[];for(let r=br;r<br+3;r++)for(let c=bc;c<bc+3;c++)if(fixed.has(`${r},${c}`))used.add(g[r][c]);else empty.push([r,c]);const av=[...Array.from({length:9},(_,i)=>i+1).filter(n=>!used.has(n))].sort(()=>Math.random()-.5);empty.forEach(([r,c],i)=>g[r][c]=av[i])}}
function conf(r,c){const v=g[r][c];if(!v)return 0;ck++;let ct=0;for(let i=0;i<9;i++){if(i!==c&&g[r][i]===v)ct++;if(i!==r&&g[i][c]===v)ct++}return ct}
function total(){let t=0;for(let r=0;r<9;r++)for(let c=0;c<9;c++)t+=conf(r,c);return t/2}
function repair(){let stale=0,best=total();for(let it=0;it<200000;it++){iters++;if(best===0)return!0;const br=3*[0,1,2][Math.random()*3|0],bc=3*[0,1,2][Math.random()*3|0];const sw=[];for(let r=br;r<br+3;r++)for(let c=bc;c<bc+3;c++)if(!fixed.has(`${r},${c}`))sw.push([r,c]);if(sw.length<2)continue;const i=Math.random()*sw.length|0;let j;do{j=Math.random()*sw.length|0}while(j===i);const[r1,c1]=sw[i],[r2,c2]=sw[j];if(g[r1][c1]===g[r2][c2])continue;nd++;const old=conf(r1,c1)+conf(r2,c2);const v1=g[r1][c1],v2=g[r2][c2];g[r1][c1]=v2;g[r2][c2]=v1;const nw=conf(r1,c1)+conf(r2,c2);const d=nw-old;if(d<0){best+=d;stale=0}else if(d===0&&Math.random()<.3){stale++}else{g[r1][c1]=v1;g[r2][c2]=v2;stale++}if(stale>5000)break}return total()===0}
const t=performance.now();for(let rs=0;rs<20;rs++){restarts=rs+1;for(let r=0;r<9;r++)for(let c=0;c<9;c++)if(!fixed.has(`${r},${c}`))g[r][c]=0;initBoxes();if(repair())return{solved:true,grid:g,metrics:{nodes:nd,backtracks:bt,checks:ck,time:performance.now()-t,iters,restarts}};bt++}
return{solved:false,grid:g,metrics:{nodes:nd,backtracks:bt,checks:ck,time:performance.now()-t,iters,restarts}}}

// ─── ALGO INFO ────────────────────────────────────
const ALGOS={
backtracking:{name:"Plain Backtracking",icon:"↩️",tag:"Brute-force baseline",desc:"Tries values 1-9 at each cell in row-major order. Backtracks on constraint violation. Simple but explores many unnecessary branches — serves as the performance baseline for comparison.",solver:solveBT},
mrv:{name:"Backtracking + MRV + LCV",icon:"🎯",tag:"Smart variable & value selection",desc:"Always picks the most constrained cell (fewest legal values). Uses degree heuristic to break ties and Least Constraining Value ordering to try values that leave the most options for neighbors.",solver:solveMRV},
fc:{name:"MRV + Forward Checking + AC-3",icon:"⚡",tag:"Constraint propagation",desc:"After each assignment, prunes that value from all neighbors' domains. AC-3 arc consistency further propagates constraints — if any neighbor has only one option left, that cascades through the board. Domain wipeout triggers immediate backtracking.",solver:solveFC},
mincon:{name:"Min-Conflicts (Local Search)",icon:"🔄",tag:"Iterative repair with box swaps",desc:"Completely different paradigm — no search tree. Fills each 3×3 box with a valid permutation, then swaps cells within boxes to reduce row/column conflicts. Uses sideways moves to escape plateaus and restarts when stuck.",solver:solveMinCon}};

// ─── STATE ────────────────────────────────────────
let puzzle=null,solution=null,grid=null,selected=null,hintCell=null;
let errors=new Set(),difficulty=null,hintsUsed=0;
let timerInt=null,t0=null,elapsed=0,aiOn=false,done=false;

// ─── NAV ──────────────────────────────────────────
function show(id){document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));document.getElementById(id).classList.add('active')}
function goHome(){clearInterval(timerInt);show('home-screen')}
function goPlay(){show('play-screen')}

// ─── START ────────────────────────────────────────
function startGame(diff){
    const d=makePuzzle(diff);puzzle=d.puzzle;solution=d.solution;grid=puzzle.map(r=>[...r]);
    difficulty=diff;selected=null;hintCell=null;errors=new Set();hintsUsed=0;done=false;aiOn=false;elapsed=0;
    document.getElementById('badge').textContent=diff.toUpperCase();
    document.getElementById('hints-used').textContent='Hints: 0';
    document.getElementById('win-banner').classList.add('hidden');
    document.getElementById('panel-ai').classList.add('hidden');
    document.getElementById('panel-info').classList.remove('hidden');
    document.getElementById('ai-toggle').classList.remove('on');
    buildNumpad();render();startTimer();show('play-screen');
}

function buildNumpad(){const np=document.getElementById('numpad');np.innerHTML='';for(let n=1;n<=9;n++){const b=document.createElement('button');b.className='num-btn';b.textContent=n;b.onclick=()=>inputNum(n);np.appendChild(b)}}
function startTimer(){clearInterval(timerInt);t0=Date.now();timerInt=setInterval(()=>{elapsed=Math.floor((Date.now()-t0)/1000);const m=String(Math.floor(elapsed/60)).padStart(2,'0'),s=String(elapsed%60).padStart(2,'0');document.getElementById('timer').textContent=`${m}:${s}`},1000)}

// ─── RENDER ───────────────────────────────────────
function render(){
    const b=document.getElementById('board');b.innerHTML='';
    for(let r=0;r<9;r++)for(let c=0;c<9;c++){
        const el=document.createElement('div');el.className='cell';
        const v=grid[r][c],orig=puzzle[r][c]!==0;
        if(orig)el.classList.add('original');else if(v)el.classList.add('user-val');
        if((c+1)%3===0&&c<8)el.classList.add('br');if((r+1)%3===0&&r<8)el.classList.add('bb');
        if(selected){if(selected.r===r&&selected.c===c)el.classList.add('selected');
        else if(selected.r===r||selected.c===c||Math.floor(selected.r/3)===Math.floor(r/3)&&Math.floor(selected.c/3)===Math.floor(c/3))el.classList.add('highlight');
        if(v&&grid[selected.r]?.[selected.c]===v&&!(selected.r===r&&selected.c===c))el.classList.add('same-val')}
        if(errors.has(`${r},${c}`))el.classList.add('error');
        if(hintCell&&hintCell.r===r&&hintCell.c===c)el.classList.add('hint-glow');
        el.textContent=v||'';el.onclick=()=>clickCell(r,c);b.appendChild(el)}
    // Update numpad done state
    document.querySelectorAll('.num-btn').forEach((btn,i)=>{const n=i+1;let ct=0;for(let r=0;r<9;r++)for(let c=0;c<9;c++)if(grid[r][c]===n)ct++;btn.classList.toggle('done',ct>=9)});
    // Stats
    let emp=0;for(let r=0;r<9;r++)for(let c=0;c<9;c++)if(!grid[r][c])emp++;
    document.getElementById('st-empty').textContent=emp;
    document.getElementById('st-errors').textContent=errors.size||'None';
}

// ─── INPUT ────────────────────────────────────────
function clickCell(r,c){if(puzzle[r][c])return;selected={r,c};hintCell=null;render()}
function inputNum(n){if(!selected||puzzle[selected.r][selected.c])return;grid[selected.r][selected.c]=n;chkErr();render();chkWin()}
function eraseCell(){if(!selected||puzzle[selected.r][selected.c])return;grid[selected.r][selected.c]=0;chkErr();render()}
function chkErr(){errors=new Set();for(let r=0;r<9;r++)for(let c=0;c<9;c++)if(grid[r][c]&&!isValid(grid,r,c,grid[r][c]))errors.add(`${r},${c}`)}
function chkWin(){if(done)return;let full=true;for(let r=0;r<9;r++)for(let c=0;c<9;c++)if(!grid[r][c])full=false;if(full&&!errors.size){done=true;clearInterval(timerInt);document.getElementById('win-banner').classList.remove('hidden')}}

// ─── HINT ─────────────────────────────────────────
function doHint(){
    if(!solution||done)return;
    let best=null,mn=10;for(let r=0;r<9;r++)for(let c=0;c<9;c++)if(!grid[r][c]){const lv=getLegal(grid,r,c);if(lv.length>0&&lv.length<mn){mn=lv.length;best={r,c,v:solution[r][c]};if(mn===1)break}}
    if(!best)return;hintCell=best;selected={r:best.r,c:best.c};hintsUsed++;document.getElementById('hints-used').textContent=`Hints: ${hintsUsed}`;render();
    setTimeout(()=>{grid[best.r][best.c]=best.v;hintCell=null;chkErr();render();
    const cells=document.querySelectorAll('#board .cell'),idx=best.r*9+best.c;if(cells[idx])cells[idx].classList.add('hint-pop');chkWin()},700)}

// ─── AI ───────────────────────────────────────────
function toggleAI(){aiOn=!aiOn;document.getElementById('panel-ai').classList.toggle('hidden',!aiOn);document.getElementById('panel-info').classList.toggle('hidden',aiOn);document.getElementById('ai-toggle').classList.toggle('on',aiOn)}

function aiSolve(key){
    const info=ALGOS[key];if(!info)return;clearInterval(timerInt);
    const res=info.solver(puzzle);
    document.getElementById('res-icon').textContent=info.icon;
    document.getElementById('res-name').textContent=info.name;
    document.getElementById('res-tag').textContent=info.tag;
    document.getElementById('res-desc').textContent=info.desc;
    // Metrics
    const m=res.metrics,mg=document.getElementById('res-metrics');mg.innerHTML='';
    const mets=[{l:'Status',v:res.solved?'Solved ✓':'Failed ✗',c:res.solved?'#22c55e':'#ef4444'},{l:'Time',v:m.time.toFixed(1)+'ms',c:'#fbbf24'},{l:'Nodes',v:m.nodes.toLocaleString(),c:'#60a5fa'},{l:'Backtracks',v:m.backtracks.toLocaleString(),c:'#fb923c'},{l:'Checks',v:m.checks.toLocaleString(),c:'#a78bfa'}];
    if(m.arcs!==undefined)mets.push({l:'Arc Revisions',v:m.arcs.toLocaleString(),c:'#06b6d4'});
    if(m.iters!==undefined)mets.push({l:'Iterations',v:m.iters.toLocaleString(),c:'#06b6d4'});
    if(m.restarts!==undefined)mets.push({l:'Restarts',v:m.restarts.toLocaleString(),c:'#f97316'});
    for(const mt of mets){const d=document.createElement('div');d.className='met-card';d.innerHTML=`<div class="met-label">${mt.l}</div><div class="met-val" style="color:${mt.c}">${mt.v}</div>`;mg.appendChild(d)}
    // Board
    const rb=document.getElementById('res-board');rb.innerHTML='';
    for(let r=0;r<9;r++)for(let c=0;c<9;c++){const el=document.createElement('div');el.className='cell';const v=res.grid[r][c];if(puzzle[r][c])el.classList.add('original');else el.classList.add('solved-cell');if((c+1)%3===0&&c<8)el.classList.add('br');if((r+1)%3===0&&r<8)el.classList.add('bb');el.textContent=v||'';rb.appendChild(el)}
    show('result-screen')}

// ─── KEYBOARD ─────────────────────────────────────
document.addEventListener('keydown',e=>{if(!selected||!document.getElementById('play-screen').classList.contains('active'))return;
const n=parseInt(e.key);if(n>=1&&n<=9)inputNum(n);if(e.key==='Backspace'||e.key==='Delete')eraseCell();
if(e.key==='ArrowUp'&&selected.r>0){selected.r--;render()}if(e.key==='ArrowDown'&&selected.r<8){selected.r++;render()}
if(e.key==='ArrowLeft'&&selected.c>0){selected.c--;render()}if(e.key==='ArrowRight'&&selected.c<8){selected.c++;render()}});
