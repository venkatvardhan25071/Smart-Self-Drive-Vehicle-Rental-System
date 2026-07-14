import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
def read(f): return open(os.path.join(BASE, 'templates', f), 'r', encoding='utf-8').read()
def write(f, c): open(os.path.join(BASE, 'templates', f), 'w', encoding='utf-8').write(c)

# ── VEHICLES.HTML: Add back-btn-v CSS + enhance existing back arrow ─────────
v = read('vehicles.html')

back_v_css = """
    /* Settings-style back button */
    .back-btn-v {
        background: rgba(255,255,255,0.65);
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        border: 1.5px solid rgba(14,165,233,0.22);
        border-radius: 50%; width: 44px; height: 44px;
        display: flex; align-items: center; justify-content: center;
        color: #475569; text-decoration: none; transition: all 0.3s;
        box-shadow: 0 4px 14px rgba(0,0,0,0.09); flex-shrink: 0;
    }
    .back-btn-v:hover {
        border-color: #0ea5e9; color: #0ea5e9;
        box-shadow: 0 0 18px rgba(14,165,233,0.4);
        transform: scale(1.07);
    }
    [data-theme="dark"] .back-btn-v {
        background: rgba(15,23,42,0.78) !important;
        border-color: rgba(14,165,233,0.35) !important;
        color: #94a3b8 !important;
    }
    [data-theme="dark"] .back-btn-v:hover {
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
        box-shadow: 0 0 18px rgba(14,165,233,0.4) !important;
    }
"""

# Insert before </style> in the first style block (after glass-nav CSS)
v = v.replace('</style>\n</head>', back_v_css + '\n</style>\n</head>', 1)

# Replace the existing text-slate-600 back arrow with the styled one
old_arrow = '''<a href="{% url 'index' %}" class="text-slate-600 hover:text-primary-start transition-colors">
                    <span class="material-symbols-outlined">arrow_back_ios_new</span>
                </a>'''
new_arrow = '''<a href="{% url 'index' %}" class="back-btn-v" title="Back to Home">
                    <span class="material-symbols-outlined" style="font-size:20px;">arrow_back_ios_new</span>
                </a>'''
if old_arrow in v:
    v = v.replace(old_arrow, new_arrow)
    print("  vehicles: back arrow replaced")
else:
    # Try to find it with different whitespace
    v = re.sub(
        r'<a href="\{% url \'index\' %\}" class="text-slate-600 hover:text-primary-start transition-colors">\s*<span class="material-symbols-outlined">arrow_back_ios_new</span>\s*</a>',
        new_arrow,
        v
    )
    print("  vehicles: back arrow replaced (regex)")

write('vehicles.html', v)
print("  vehicles.html done")

# ── ACTIVITY.HTML: Add receipts archive button + panel ──────────────────────
a = read('activity.html')

# Find the filter bar and inject receipts button to the left
receipts_btn = '''<button onclick="openReceiptsPanel()" class="receipts-btn w-10 h-10 rounded-full flex items-center justify-center" style="position:relative;background:rgba(255,255,255,0.65);backdrop-filter:blur(12px);border:1.5px solid rgba(14,165,233,0.22);box-shadow:0 4px 14px rgba(14,165,233,0.14),inset 0 1px 0 rgba(255,255,255,0.9);flex-shrink:0;cursor:pointer;transition:all 0.3s;" title="Downloaded Receipts" onmouseover="this.style.transform='scale(1.08)';this.style.borderColor='rgba(14,165,233,0.6)'" onmouseout="this.style.transform='';this.style.borderColor='rgba(14,165,233,0.22)'">
                        <span class="material-symbols-outlined" style="font-size:22px;color:#0ea5e9;line-height:1;">folder_open</span>
                        <span id="receipts-badge" style="display:none;position:absolute;top:-4px;right:-4px;width:16px;height:16px;background:#0ea5e9;border-radius:50%;color:white;font-size:9px;font-weight:700;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(14,165,233,0.5);">0</span>
                    </button>'''

# Find filter buttons container and prepend receipts button
old_filter_open = '''<!-- Left Side: Receipts Archive + Filter Buttons -->
                <div class="flex gap-3 items-center flex-wrap">'''

if old_filter_open in a:
    # Already partially done - just check if receipts btn is there
    if 'folder_open' not in a:
        a = a.replace(
            old_filter_open,
            old_filter_open + '\n                    ' + receipts_btn
        )
        print("  activity: receipts btn injected into existing container")
else:
    # Find original container
    old_filter = '''<!-- Filter Buttons (LEFT) -->
                <div class="flex gap-3 items-center">'''
    if old_filter in a:
        a = a.replace(old_filter, '''<!-- Left Side: Receipts Archive + Filter Buttons -->
                <div class="flex gap-3 items-center flex-wrap">
                    ''' + receipts_btn)
        print("  activity: receipts btn injected")
    else:
        print("  WARNING: could not find filter container - trying broad search")
        # Try broad: find first History filter button
        a = a.replace(
            '''<button data-filter="all" onclick="filterActivity('all', this)" class="activity-filter-btn is-active bg-sky-500 text-white px-5 py-2 rounded-full text-sm font-bold shadow-md">History</button>''',
            receipts_btn + '\n                    <button data-filter="all" onclick="filterActivity(\'all\', this)" class="activity-filter-btn is-active bg-sky-500 text-white px-5 py-2 rounded-full text-sm font-bold shadow-md">History</button>'
        )
        print("  activity: receipts btn injected before History")

# Add popup dark mode CSS if not already there
if '.pending-alert-card' not in a:
    popup_css = """
        /* Popup dark mode */
        .pending-alert-card { background: rgba(255,253,240,0.95); }
        .rejected-alert-card { background: rgba(255,250,250,0.95); }
        [data-theme="dark"] .pending-alert-card {
            background: linear-gradient(135deg, rgba(15,23,42,0.98), rgba(20,30,50,0.98)) !important;
            border-color: rgba(234,179,8,0.4) !important;
            box-shadow: 0 0 60px rgba(234,179,8,0.12), 0 20px 50px rgba(0,0,0,0.7) !important;
        }
        [data-theme="dark"] .rejected-alert-card {
            background: linear-gradient(135deg, rgba(15,23,42,0.98), rgba(25,10,15,0.98)) !important;
            border-color: rgba(239,68,68,0.4) !important;
            box-shadow: 0 0 60px rgba(239,68,68,0.12), 0 20px 50px rgba(0,0,0,0.7) !important;
        }
        [data-theme="dark"] .popup-title { color: #f1f5f9 !important; }
        [data-theme="dark"] .popup-body { color: #94a3b8 !important; }
"""
    a = a.replace('        @keyframes notifDot {', popup_css + '\n        @keyframes notifDot {')
    print("  activity: popup CSS added")

# Fix pending card class
a = a.replace(
    'class="bg-white/85 backdrop-blur-2xl border border-yellow-200/50 rounded-[2.5rem] p-8 max-w-sm w-full text-center animate-yellow-glow transform scale-95 transition-transform duration-500 relative overflow-hidden" id="pending-alert-box"',
    'class="pending-alert-card backdrop-blur-2xl border border-yellow-200/50 rounded-[2.5rem] p-8 max-w-sm w-full text-center animate-yellow-glow transform scale-95 transition-transform duration-500 relative overflow-hidden" id="pending-alert-box"'
)
a = a.replace(
    'class="bg-white/85 backdrop-blur-2xl border border-red-200/50 rounded-[2.5rem] p-8 max-w-sm w-full text-center animate-red-glow transform scale-95 transition-transform duration-500 relative overflow-hidden" id="rejected-alert-box"',
    'class="rejected-alert-card backdrop-blur-2xl border border-red-200/50 rounded-[2.5rem] p-8 max-w-sm w-full text-center animate-red-glow transform scale-95 transition-transform duration-500 relative overflow-hidden" id="rejected-alert-box"'
)
a = a.replace(
    'class="text-2xl font-black text-slate-800 mb-3 tracking-tight relative z-10">Booking Pending',
    'class="text-2xl font-black popup-title mb-3 tracking-tight relative z-10">Booking Pending'
)
a = a.replace(
    'class="text-2xl font-black text-slate-800 mb-3 tracking-tight relative z-10">Your Order is Rejected',
    'class="text-2xl font-black popup-title mb-3 tracking-tight relative z-10">Your Order is Rejected'
)
a = a.replace(
    '<p class="text-slate-600 text-sm mb-8 leading-relaxed font-medium relative z-10">Details are not available because the booking is currently',
    '<p class="popup-body text-sm mb-8 leading-relaxed font-medium relative z-10">Details are not available because the booking is currently'
)
a = a.replace(
    '<p class="text-slate-600 text-sm mb-8 leading-relaxed font-medium relative z-10">Details are not available because the booking has been',
    '<p class="popup-body text-sm mb-8 leading-relaxed font-medium relative z-10">Details are not available because the booking has been'
)
print("  activity: popup classes patched")

# Add receipts panel HTML + JS before </body>
if 'receipts-panel' not in a:
    receipts_html = """
    <!-- Receipts Archive Panel -->
    <div id="receipts-panel" onclick="if(event.target===this)closeReceiptsPanel()" style="display:none;position:fixed;inset:0;z-index:200;align-items:center;justify-content:center;background:rgba(15,23,42,0.6);backdrop-filter:blur(14px);">
        <div style="background:rgba(255,255,255,0.88);backdrop-filter:blur(28px);border:1.5px solid rgba(14,165,233,0.22);border-radius:28px;padding:28px;width:92%;max-width:480px;max-height:80vh;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(14,165,233,0.18);animation:slideUpIn 0.35s cubic-bezier(0.4,0,0.2,1);" class="receipts-card-inner">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;flex-shrink:0;">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div style="width:42px;height:42px;border-radius:14px;background:linear-gradient(135deg,#0ea5e9,#3b82f6);display:flex;align-items:center;justify-content:center;box-shadow:0 6px 16px rgba(14,165,233,0.4);">
                        <span class="material-symbols-outlined" style="color:white;font-size:22px;line-height:1;">receipt_long</span>
                    </div>
                    <div>
                        <div class="receipts-title" style="font-weight:800;font-size:17px;color:#0f172a;">Downloaded Receipts</div>
                        <div style="font-size:11px;color:#0ea5e9;font-weight:700;margin-top:2px;">Booking Summary Archive</div>
                    </div>
                </div>
                <button onclick="closeReceiptsPanel()" style="width:32px;height:32px;border-radius:50%;background:rgba(0,0,0,0.06);border:none;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:all 0.2s;" onmouseover="this.style.background='rgba(239,68,68,0.12)'" onmouseout="this.style.background='rgba(0,0,0,0.06)'">
                    <span class="material-symbols-outlined" style="font-size:18px;color:#475569;line-height:1;">close</span>
                </button>
            </div>
            <div id="receipts-list" style="overflow-y:auto;flex-grow:1;scrollbar-width:thin;scrollbar-color:rgba(14,165,233,0.3) transparent;"></div>
        </div>
    </div>
    <style>
        @keyframes slideUpIn { from{transform:translateY(40px);opacity:0} to{transform:translateY(0);opacity:1} }
        [data-theme="dark"] .receipts-card-inner { background:rgba(10,15,28,0.97)!important; border-color:rgba(14,165,233,0.3)!important; box-shadow:0 20px 60px rgba(14,165,233,0.12)!important; }
        [data-theme="dark"] .receipts-title { color:#f1f5f9!important; }
    </style>
    <script>
    const RECEIPTS_KEY = 'drivego_receipts';
    function saveReceipt(data) {
        let list = JSON.parse(localStorage.getItem(RECEIPTS_KEY)||'[]');
        list.unshift({...data,savedAt:new Date().toISOString()});
        if(list.length>50) list=list.slice(0,50);
        localStorage.setItem(RECEIPTS_KEY,JSON.stringify(list));
        updateReceiptsBadge();
    }
    function updateReceiptsBadge() {
        const list=JSON.parse(localStorage.getItem(RECEIPTS_KEY)||'[]');
        const b=document.getElementById('receipts-badge');
        if(b){ if(list.length>0){b.textContent=list.length>99?'99+':list.length;b.style.display='flex';}else{b.style.display='none';} }
    }
    function openReceiptsPanel() {
        const panel=document.getElementById('receipts-panel');
        const list=document.getElementById('receipts-list');
        const receipts=JSON.parse(localStorage.getItem(RECEIPTS_KEY)||'[]');
        const dark=document.documentElement.getAttribute('data-theme')==='dark';
        const textColor=dark?'#e2e8f0':'#0f172a';
        const subColor=dark?'#64748b':'#64748b';
        if(receipts.length===0){
            list.innerHTML=`<div style="text-align:center;padding:48px 0;"><span class="material-symbols-outlined" style="font-size:60px;color:rgba(14,165,233,0.25);display:block;margin-bottom:12px;">folder_open</span><p style="color:${subColor};font-weight:600;font-size:14px;margin:0;">No downloaded receipts yet.</p><p style="color:${subColor};font-size:12px;margin-top:6px;opacity:0.7;">Download booking summaries to store them here.</p></div>`;
        } else {
            list.innerHTML=receipts.map((r,i)=>`
                <div style="background:rgba(14,165,233,0.07);border:1px solid rgba(14,165,233,0.18);border-radius:14px;padding:14px 16px;display:flex;align-items:center;gap:14px;margin-bottom:10px;transition:all 0.25s;" onmouseover="this.style.background='rgba(14,165,233,0.13)';this.style.transform='translateX(4px)'" onmouseout="this.style.background='rgba(14,165,233,0.07)';this.style.transform=''">
                    <div style="width:40px;height:40px;border-radius:12px;background:linear-gradient(135deg,rgba(14,165,233,0.18),rgba(59,130,246,0.12));border:1px solid rgba(14,165,233,0.25);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                        <span class="material-symbols-outlined" style="color:#0ea5e9;font-size:20px;line-height:1;">description</span>
                    </div>
                    <div style="flex:1;min-width:0;">
                        <div style="font-weight:700;font-size:14px;color:${textColor};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${r.vehicleName||'Booking Receipt'}</div>
                        <div style="font-size:11px;color:${subColor};margin-top:2px;">${r.date||''} &nbsp;•&nbsp; <span style="color:#0ea5e9;font-weight:700;">&#x20B9;${r.amount||'0'}</span></div>
                    </div>
                    <button onclick="downloadStoredReceipt(${i})" style="flex-shrink:0;background:linear-gradient(135deg,#0ea5e9,#3b82f6);color:white;border:none;border-radius:10px;padding:8px 12px;font-size:12px;font-weight:700;cursor:pointer;box-shadow:0 4px 12px rgba(14,165,233,0.35);transition:all 0.2s;" onmouseover="this.style.transform='scale(1.06)'" onmouseout="this.style.transform=''">
                        <span class="material-symbols-outlined" style="font-size:16px;line-height:1;vertical-align:middle;">download</span>
                    </button>
                </div>`).join('');
        }
        panel.style.display='flex';
    }
    function closeReceiptsPanel() { document.getElementById('receipts-panel').style.display='none'; }
    function downloadStoredReceipt(i) {
        const r=JSON.parse(localStorage.getItem(RECEIPTS_KEY)||'[]')[i];
        if(!r) return;
        const blob=new Blob([r.html||`<h2>${r.vehicleName}</h2><p>Amount: &#x20B9;${r.amount}</p>`],{type:'text/html'});
        const url=URL.createObjectURL(blob);
        const a=document.createElement('a');
        a.href=url;a.download=`DriveGO_Receipt_${(r.vehicleName||'Booking').replace(/\\s+/g,'_')}.html`;
        document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(url);
    }
    document.addEventListener('DOMContentLoaded',updateReceiptsBadge);
    </script>
"""
    a = a.replace('</body>', receipts_html + '\n</body>', 1)
    print("  activity: receipts panel added")
else:
    print("  activity: receipts panel already present")

write('activity.html', a)
print("  activity.html done")

# ── INDEX.HTML: Add id=logout-btn if missing ────────────────────────────────
idx = read('index.html')
if 'id="logout-btn"' not in idx:
    idx = idx.replace(
        "href=\"{% url 'logout' %}\" class=\"",
        "href=\"{% url 'logout' %}\" id=\"logout-btn\" class=\"",
        1
    )
    write('index.html', idx)
    print("  index.html logout-btn id added")
else:
    print("  index.html logout-btn already present")

print("\nAll fixes complete!")
