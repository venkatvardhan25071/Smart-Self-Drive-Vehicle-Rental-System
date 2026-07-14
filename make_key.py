html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>DriveGO — Smart Lock System</title>
<script src="https://unpkg.com/mqtt@4.3.7/dist/mqtt.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--c:#00e5ff;--u:#ff6b35;--bg:#080c10;--panel:rgba(0,229,255,0.04);--border:rgba(0,229,255,0.18);--text:#c8dce8;--dim:#4a6272;}
html,body{height:100%;overflow:hidden;}
body{background:var(--bg);color:var(--text);font-family:'Space Grotesk',sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;}

/* ── Grid bg ── */
body::before{content:"";position:fixed;inset:0;background-image:linear-gradient(rgba(0,229,255,0.025) 1px,transparent 1px),linear-gradient(90deg,rgba(0,229,255,0.025) 1px,transparent 1px);background-size:36px 36px;pointer-events:none;z-index:0;}
/* ── Central glow ── */
body::after{content:"";position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);width:800px;height:800px;border-radius:50%;background:radial-gradient(circle,var(--glow,rgba(0,229,255,0.08)) 0%,transparent 68%);pointer-events:none;transition:background 1.2s;z-index:0;}

/* ── Scanline overlay ── */
.scanlines{position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.07) 2px,rgba(0,0,0,0.07) 4px);pointer-events:none;z-index:1;}

/* ── Floating particles ── */
.particle{position:fixed;width:2px;height:2px;background:rgba(0,229,255,0.6);border-radius:50%;animation:floatP var(--dur,8s) linear infinite;pointer-events:none;z-index:1;}
@keyframes floatP{0%{transform:translateY(100vh) translateX(0);opacity:0;}10%{opacity:1;}90%{opacity:1;}100%{transform:translateY(-10vh) translateX(var(--dx,20px));opacity:0;}}

.wrap{position:relative;z-index:10;width:min(540px,96vw);display:flex;flex-direction:column;align-items:center;gap:18px;padding:16px 0;}

/* ── Brand ── */
.brand{text-align:center;}
.brand-sub{font-size:10px;color:var(--dim);text-transform:uppercase;letter-spacing:0.5em;font-family:'Share Tech Mono',monospace;}
.brand-h1{font-size:36px;font-weight:700;color:#fff;letter-spacing:0.2em;text-transform:uppercase;line-height:1.1;}
.brand-h1 span{color:var(--c);text-shadow:0 0 20px rgba(0,229,255,0.8);}

/* ── Glass card ── */
.glass{background:rgba(13,21,32,0.82);border:1px solid var(--border);border-radius:6px;backdrop-filter:blur(20px);}

/* ── JOIN SCREEN ── */
#joinScreen{width:100%;display:flex;flex-direction:column;gap:14px;}
.room-bar{width:100%;padding:14px 18px;display:flex;align-items:center;gap:12px;font-family:'Share Tech Mono',monospace;font-size:12px;color:var(--dim);}
.room-bar label{white-space:nowrap;text-transform:uppercase;letter-spacing:0.1em;}
.room-bar input{flex:1;background:transparent;border:none;border-bottom:1px solid var(--border);color:var(--c);font-family:'Share Tech Mono',monospace;font-size:14px;letter-spacing:0.2em;padding:4px;outline:none;text-transform:uppercase;}
.room-bar input::placeholder{color:var(--dim);}
.hint{font-family:'Share Tech Mono',monospace;font-size:10px;color:var(--dim);text-align:center;cursor:pointer;text-decoration:underline;text-underline-offset:3px;opacity:0.7;transition:0.2s;}
.hint:hover{opacity:1;color:var(--c);}
.join-btn{width:100%;height:56px;background:rgba(0,229,255,0.06);border:1px solid var(--c);border-radius:4px;cursor:pointer;font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:700;letter-spacing:0.3em;text-transform:uppercase;color:var(--c);transition:all 0.3s;position:relative;overflow:hidden;box-shadow:0 0 20px rgba(0,229,255,0.15);}
.join-btn:hover{background:rgba(0,229,255,0.12);box-shadow:0 0 35px rgba(0,229,255,0.35);}

/* ── MAIN HUD ── */
#mainHud{width:100%;display:none;flex-direction:column;gap:16px;align-items:center;}
.ch-badge{font-family:'Share Tech Mono',monospace;font-size:11px;color:var(--dim);text-align:center;letter-spacing:0.15em;}
.ch-badge span{color:var(--c);font-size:13px;font-weight:bold;}
.ch-badge a{color:var(--dim);text-decoration:underline;cursor:pointer;margin-left:12px;font-size:10px;}
.ch-badge a:hover{color:var(--u);}

/* ── Status panel ── */
.status-panel{width:100%;padding:16px 22px;display:flex;align-items:center;justify-content:space-between;gap:16px;}
.s-ind{display:flex;align-items:center;gap:12px;}
.s-dot{width:10px;height:10px;border-radius:50%;background:var(--c);box-shadow:0 0 10px var(--c),0 0 20px var(--c);flex-shrink:0;transition:background 0.6s,box-shadow 0.6s;}
.s-dot.unlocked{background:var(--u);box-shadow:0 0 10px var(--u),0 0 20px var(--u);}
.s-dot.connecting{background:var(--dim);box-shadow:none;animation:pdot 1s infinite;}
@keyframes pdot{0%,100%{opacity:1}50%{opacity:0.3}}
.s-text{font-family:'Share Tech Mono',monospace;font-size:12px;color:var(--dim);}
.s-text strong{display:block;font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:700;letter-spacing:0.15em;color:#fff;text-transform:uppercase;}
.cbadge{font-family:'Share Tech Mono',monospace;font-size:10px;padding:4px 10px;border-radius:2px;border:1px solid var(--dim);color:var(--dim);letter-spacing:0.1em;transition:all 0.4s;}
.cbadge.live{color:#4cff9f;border-color:#4cff9f;box-shadow:0 0 10px rgba(76,255,159,0.3);}

/* ── CAR VISUALIZATION ── */
.car-vis{position:relative;width:100%;height:240px;display:flex;align-items:center;justify-content:center;overflow:hidden;}

/* Scan bracket corners */
.corner{position:absolute;width:18px;height:18px;z-index:5;}
.corner::before,.corner::after{content:"";position:absolute;background:var(--c);transition:background 0.6s;box-shadow:0 0 6px var(--c);}
.corner::before{width:100%;height:1.5px;top:0;left:0;}
.corner::after{width:1.5px;height:100%;top:0;left:0;}
.corner.tr{top:6px;right:6px;transform:rotate(90deg);}
.corner.bl{bottom:6px;left:6px;transform:rotate(270deg);}
.corner.br{bottom:6px;right:6px;transform:rotate(180deg);}
.corner.tl{top:6px;left:6px;}
.corner.unlocked::before,.corner.unlocked::after{background:var(--u);box-shadow:0 0 6px var(--u);}

/* ── HOLOGRAPHIC CAR STAGE ── */
.car-stage{position:relative;width:340px;height:200px;display:flex;align-items:center;justify-content:center;}

/* Anti-gravity float animation */
.car-float{animation:carFloat 4s ease-in-out infinite;}
@keyframes carFloat{
  0%,100%{transform:translateY(0px) rotate(0deg);}
  25%{transform:translateY(-8px) rotate(0.4deg);}
  75%{transform:translateY(-4px) rotate(-0.3deg);}
}

/* Car image wrapper */
.car-img-wrap{position:relative;width:300px;height:160px;display:flex;align-items:center;justify-content:center;}
.car-img-wrap img{width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 0 30px rgba(0,229,255,0.5)) drop-shadow(0 10px 40px rgba(0,229,255,0.3)) contrast(1.1) brightness(1.05);transition:filter 1s;border-radius:4px;}

/* Energy scan sweep */
.scan-sweep{position:absolute;top:0;left:-100%;width:60%;height:100%;background:linear-gradient(90deg,transparent,rgba(0,229,255,0.12),transparent);animation:scanSweep 3s ease-in-out infinite;pointer-events:none;z-index:2;}
@keyframes scanSweep{0%{left:-60%;}100%{left:110%;}}

/* Wheel energy rings */
.wheel-ring{position:absolute;width:50px;height:50px;border-radius:50%;border:1px solid rgba(0,229,255,0.5);animation:wheelRing 1.5s ease-out infinite;pointer-events:none;}
.wheel-ring.wr-left{bottom:18px;left:28px;}
.wheel-ring.wr-right{bottom:18px;right:28px;}
.wheel-ring:nth-child(2){animation-delay:0.75s;}
@keyframes wheelRing{0%{transform:scale(0.8);opacity:0.8;}100%{transform:scale(2);opacity:0;}}

/* Glass floor reflection */
.reflection{position:absolute;bottom:-20px;left:10%;width:80%;height:30px;background:linear-gradient(to bottom,rgba(0,229,255,0.08),transparent);border-radius:50%;filter:blur(6px);}

/* ── HOLOGRAPHIC HUD OVERLAYS ── */
.holo-overlay{position:absolute;top:6px;left:6px;font-family:'Share Tech Mono',monospace;font-size:9px;color:var(--c);line-height:1.9;z-index:6;text-shadow:0 0 8px rgba(0,229,255,0.8);}
.holo-overlay div{opacity:0;animation:holoFadeIn 0.4s ease forwards;}
.holo-overlay div:nth-child(1){animation-delay:0.3s;}
.holo-overlay div:nth-child(2){animation-delay:0.6s;}
.holo-overlay div:nth-child(3){animation-delay:0.9s;}
@keyframes holoFadeIn{from{opacity:0;transform:translateX(-4px);}to{opacity:1;transform:translateX(0);}}

/* Lock state ring pulse */
.lock-ring{position:absolute;width:200px;height:200px;border-radius:50%;border:1px solid var(--c);opacity:0;animation:ringout 1.5s ease-out forwards;pointer-events:none;}
@keyframes ringout{0%{opacity:0.6;transform:scale(0.5);}100%{opacity:0;transform:scale(1.8);}}

/* Waiting overlay */
#waitOver{display:none;position:absolute;inset:0;background:rgba(8,12,16,0.9);border-radius:6px;align-items:center;justify-content:center;flex-direction:column;gap:12px;font-family:'Share Tech Mono',monospace;font-size:12px;color:var(--dim);z-index:20;}
#waitOver.show{display:flex;}
.spinner{width:30px;height:30px;border:2px solid rgba(0,229,255,0.15);border-top-color:var(--c);border-radius:50%;animation:spin 0.8s linear infinite;}
@keyframes spin{to{transform:rotate(360deg)}}

/* ── LOCK BUTTON ── */
.lock-btn{position:relative;width:100%;height:72px;background:rgba(0,229,255,0.06);border:1px solid var(--c);border-radius:4px;cursor:pointer;font-family:'Space Grotesk',sans-serif;font-size:21px;font-weight:700;letter-spacing:0.3em;text-transform:uppercase;color:var(--c);transition:all 0.3s;overflow:hidden;display:flex;align-items:center;justify-content:center;gap:14px;box-shadow:0 0 20px rgba(0,229,255,0.1),inset 0 0 30px rgba(0,229,255,0.03);}
.lock-btn::before{content:"";position:absolute;inset:0;background:var(--c);opacity:0;transition:opacity 0.3s;}
.lock-btn:hover::before{opacity:0.06;}
.lock-btn:hover{box-shadow:0 0 40px rgba(0,229,255,0.35);}
.lock-btn:disabled{opacity:0.3;cursor:not-allowed;}
.lock-btn .bi,.lock-btn .bl{position:relative;z-index:1;}
.lock-btn .bi{font-size:26px;}
.lock-btn.us{border-color:var(--u);color:var(--u);box-shadow:0 0 20px rgba(255,107,53,0.15);}
.lock-btn.us::before{background:var(--u);}
.lock-btn.us:hover{box-shadow:0 0 40px rgba(255,107,53,0.35);}
.lock-sub{font-family:'Share Tech Mono',monospace;font-size:9px;color:var(--dim);text-align:center;letter-spacing:0.3em;text-transform:uppercase;}

/* ── LOG PANEL ── */
.log-panel{width:100%;padding:12px 16px;max-height:110px;overflow-y:auto;font-family:'Share Tech Mono',monospace;font-size:11px;}
.log-panel::-webkit-scrollbar{width:3px;}
.log-panel::-webkit-scrollbar-thumb{background:var(--dim);}
.ll{display:flex;gap:12px;line-height:1.8;color:var(--dim);}
.ll .ts{color:#1a3040;min-width:62px;}
.ll.ev{color:var(--c);}
.ll.ev.unl{color:var(--u);}
.ll.inf{color:#4cff9f;}
.ll.wrn{color:#ffb300;}

/* ── BACK BUTTON ── */
.back-btn{position:fixed;top:18px;left:18px;z-index:100;background:rgba(13,21,32,0.88);border:1px solid var(--border);border-radius:4px;padding:8px 16px;color:var(--c);font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:0.15em;text-decoration:none;transition:all 0.3s;backdrop-filter:blur(12px);}
.back-btn:hover{border-color:var(--c);box-shadow:0 0 14px rgba(0,229,255,0.3);}
</style>
</head>
<body>
<div class="scanlines"></div>
<a class="back-btn" href="/activity/">&larr; BACK</a>

<div class="wrap">
  <div class="brand">
    <div class="brand-sub">Smart Vehicle Access System</div>
    <h1 class="brand-h1">Drive<span>Go</span></h1>
  </div>

  <!-- JOIN SCREEN -->
  <div id="joinScreen">
    <div class="glass room-bar">
      <label>VEHICLE ID</label>
      <input type="text" id="roomInput" maxlength="20" placeholder="e.g. DEMO123"/>
    </div>
    <div class="hint" onclick="generateId()">&#8635; Generate a random Vehicle ID</div>
    <button class="join-btn" onclick="joinRoom()">&#9654; JOIN CHANNEL</button>
  </div>

  <!-- MAIN HUD -->
  <div id="mainHud">
    <div class="ch-badge">CHANNEL: <span id="chLabel">&#8212;</span><a onclick="leaveRoom()">leave</a></div>

    <div class="glass status-panel">
      <div class="s-ind">
        <div class="s-dot connecting" id="sDot"></div>
        <div class="s-text"><strong id="sLabel">&#8212;</strong><span id="sSub">connecting...</span></div>
      </div>
      <div class="cbadge" id="cBadge">OFFLINE</div>
    </div>

    <!-- CAR VISUALIZATION -->
    <div class="car-vis glass" id="carVis">
      <div class="corner tl"></div><div class="corner tr"></div>
      <div class="corner bl"></div><div class="corner br"></div>

      <!-- Holographic overlays -->
      <div class="holo-overlay">
        <div>SCAN_ID: VR-9902-X</div>
        <div>CHASSIS_STABILITY: 100%</div>
        <div>PRESSURE_PSI: 32/32/32/32</div>
      </div>

      <div id="waitOver" class="show">
        <div class="spinner"></div>
        <span>reading lock state...</span>
      </div>

      <div class="car-stage">
        <div class="car-float">
          <div class="car-img-wrap">
            <img id="carImg" src="/static/hypercar.png" alt="Hypercar"/>
            <div class="scan-sweep"></div>
          </div>
        </div>
        <!-- Wheel rings -->
        <div class="wheel-ring wr-left"></div>
        <div class="wheel-ring wr-right"></div>
        <!-- Floor reflection -->
        <div class="reflection"></div>
      </div>
    </div>

    <button class="lock-btn" id="lockBtn" disabled onclick="toggleLock()">
      <span class="bi" id="bIcon">&#128275;</span>
      <span class="bl" id="bLabel">Unlock</span>
    </button>
    <div class="lock-sub">AUTHENTICATION REQUIRED &bull; BIOMETRIC SENSOR READY</div>

    <div class="glass log-panel" id="logPanel"></div>
  </div>
</div>

<script>
// ── Floating particles ──
(function(){
  for(let i=0;i<18;i++){
    const p=document.createElement('div');
    p.className='particle';
    p.style.cssText='left:'+Math.random()*100+'vw;--dur:'+(6+Math.random()*10)+'s;--dx:'+(Math.random()*60-30)+'px;animation-delay:'+(Math.random()*8)+'s';
    document.body.appendChild(p);
  }
})();

let client=null,topic=null,locked=true,got=false,conn=false,bi=0;
const PRE='drivego/lock/v3/';
const BKS=['wss://broker.emqx.io:8084/mqtt','ws://broker.emqx.io:8083/mqtt','wss://test.mosquitto.org:8081/mqtt','ws://broker.hivemq.com:8000/mqtt'];

function generateId(){document.getElementById('roomInput').value=Math.random().toString(36).slice(2,8).toUpperCase();}

function leaveRoom(){
  if(client){try{client.end(true);}catch(e){}}
  client=null;got=false;conn=false;bi=0;
  document.getElementById('mainHud').style.display='none';
  document.getElementById('joinScreen').style.display='flex';
  document.getElementById('roomInput').value='';
  document.getElementById('logPanel').innerHTML='';
}

function joinRoom(){
  const raw=document.getElementById('roomInput').value.trim().toUpperCase();
  if(!raw){alert('Enter a Vehicle ID');return;}
  topic=PRE+raw;got=false;conn=false;bi=0;
  document.getElementById('joinScreen').style.display='none';
  document.getElementById('mainHud').style.display='flex';
  document.getElementById('chLabel').textContent=raw;
  document.getElementById('waitOver').classList.add('show');
  document.getElementById('lockBtn').disabled=true;
  tryConn();
}

function tryConn(){
  if(bi>=BKS.length){log('wrn','All brokers failed.');setConn('off');return;}
  const url=BKS[bi],host=url.replace(/wss?:\/\//,'').split(':')[0];
  log('inf','Trying '+host+'...');setConn('ing');
  if(client){try{client.end(true);}catch(e){}}
  client=mqtt.connect(url,{clientId:'dg_'+Math.random().toString(36).slice(2,10),clean:true,connectTimeout:6000,reconnectPeriod:0});
  const t=setTimeout(()=>{if(!conn){log('wrn','Timeout: '+host);try{client.end(true);}catch(e){}bi++;tryConn();}},7000);
  client.on('connect',()=>{
    clearTimeout(t);conn=true;setConn('on');log('inf','Connected via '+host);
    client.subscribe(topic,{qos:1},err=>{
      if(err){log('wrn','Sub err');return;}
      setTimeout(()=>{if(!got){log('wrn','No state — defaulting LOCKED');apply(true,'default');}},2000);
    });
  });
  client.on('message',(tp,pl)=>{const m=pl.toString();if(m==='LOCKED')apply(true,got?'remote':'retained');if(m==='UNLOCKED')apply(false,got?'remote':'retained');});
  client.on('error',err=>{clearTimeout(t);log('wrn','Error: '+err.message);try{client.end(true);}catch(e){}bi++;setTimeout(tryConn,500);});
  client.on('close',()=>{if(conn){conn=false;setConn('off');document.getElementById('lockBtn').disabled=true;log('wrn','Disconnected');}});
}

function toggleLock(){if(!client||!conn)return;client.publish(topic,locked?'UNLOCKED':'LOCKED',{qos:1,retain:true});}

function apply(lk,src){
  if(!got){got=true;document.getElementById('waitOver').classList.remove('show');document.getElementById('lockBtn').disabled=false;}
  locked=lk;updateUI(lk);spawnRing();
  const lb={remote:'← remote',retained:'← restored',default:'(default)'}[src]||src;
  log('ev',(lk?'LOCKED':'UNLOCKED')+' '+lb,lk);
}

function updateUI(lk){
  const c=lk?'#00e5ff':'#ff6b35',c2=lk?'rgba(0,229,255,0.32)':'rgba(255,107,53,0.28)';
  document.body.style.setProperty('--glow',c2);
  const img=document.getElementById('carImg');
  img.style.filter=lk
    ?'drop-shadow(0 0 30px rgba(0,229,255,0.55)) drop-shadow(0 10px 40px rgba(0,229,255,0.3)) contrast(1.1)'
    :'drop-shadow(0 0 30px rgba(255,107,53,0.55)) drop-shadow(0 10px 40px rgba(255,107,53,0.25)) contrast(1.1) saturate(1.2)';
  document.getElementById('sDot').className='s-dot'+(lk?'':' unlocked');
  document.querySelectorAll('.corner').forEach(el=>{
    const p=['tl','tr','bl','br'].find(x=>el.classList.contains(x))||'';
    el.className='corner '+p+(lk?'':' unlocked');
  });
  document.getElementById('sLabel').textContent=lk?'LOCKED':'UNLOCKED';
  document.getElementById('sSub').textContent=lk?'vehicle secured & encrypted':'vehicle accessible';
  document.getElementById('bIcon').textContent=lk?'🔓':'🔒';
  document.getElementById('bLabel').textContent=lk?'Unlock Vehicle':'Lock Vehicle';
  const btn=document.getElementById('lockBtn');
  btn.className='lock-btn'+(lk?'':' us');
  btn.style.borderColor=c;btn.style.color=c;
  document.querySelectorAll('.wheel-ring').forEach(r=>r.style.borderColor=c);
}

function spawnRing(){
  const v=document.getElementById('carVis'),r=document.createElement('div');
  r.className='lock-ring';r.style.borderColor=locked?'#00e5ff':'#ff6b35';
  v.appendChild(r);setTimeout(()=>r.remove(),1600);
}

function setConn(s){
  const d=document.getElementById('sDot'),b=document.getElementById('cBadge');
  if(s==='on'){d.className='s-dot';b.className='cbadge live';b.textContent='LIVE';}
  else if(s==='ing'){d.className='s-dot connecting';b.className='cbadge';b.textContent='CONNECTING';}
  else{d.className='s-dot connecting';b.className='cbadge';b.textContent='OFFLINE';}
}

function log(t,m,lk){
  const p=document.getElementById('logPanel'),l=document.createElement('div');
  l.className='ll '+t+(t==='ev'&&lk===false?' unl':'');
  l.innerHTML='<span class="ts">'+new Date().toTimeString().slice(0,8)+'</span><span>'+m+'</span>';
  p.appendChild(l);p.scrollTop=p.scrollHeight;
  while(p.children.length>30)p.removeChild(p.firstChild);
}

document.getElementById('roomInput').addEventListener('keydown',e=>{if(e.key==='Enter')joinRoom();});
</script>
</body>
</html>"""

with open('templates/key.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('key.html written OK')
