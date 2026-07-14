import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

def read(f):
    path = os.path.join(BASE, 'templates', f)
    return open(path, 'r', encoding='utf-8', errors='replace').read()

def write(f, c):
    path = os.path.join(BASE, 'templates', f)
    open(path, 'w', encoding='utf-8', newline='').write(c)

def inject_before(content, marker, insertion):
    idx = content.find(marker)
    if idx == -1:
        print(f"  WARN: marker not found: {marker[:50]}")
        return content
    return content[:idx] + insertion + content[idx:]

def replace_first(content, old, new):
    idx = content.find(old)
    if idx == -1:
        print(f"  WARN: replace_first – target not found: {old[:60]}")
        return content
    return content[:idx] + new + content[idx+len(old):]

# ─── BACK BUTTON CSS snippet ──────────────────────────────────────────────────
BACK_BTN_CSS = """
<style>
/* DriveGO Settings-Style Back Button */
.dg-back-btn {
    position: fixed; top: 18px; left: 18px; z-index: 999;
    width: 44px; height: 44px; border-radius: 50%;
    background: linear-gradient(135deg, rgba(255,255,255,0.78), rgba(255,255,255,0.5));
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    border: 1.5px solid rgba(255,255,255,0.7);
    display: flex; align-items: center; justify-content: center;
    color: #475569; text-decoration: none;
    box-shadow: 0 4px 16px rgba(0,0,0,0.10), 0 0 0 1px rgba(255,255,255,0.4) inset;
    transition: all 0.28s cubic-bezier(0.4,0,0.2,1);
    cursor: pointer;
}
.dg-back-btn:hover {
    border-color: #0ea5e9; color: #0ea5e9;
    box-shadow: 0 0 20px rgba(14,165,233,0.38), 0 4px 16px rgba(0,0,0,0.12);
    transform: scale(1.08) translateX(-2px);
    background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(14,165,233,0.08));
}
[data-theme="dark"] .dg-back-btn {
    background: linear-gradient(135deg, rgba(15,23,42,0.88), rgba(30,41,59,0.75)) !important;
    border-color: rgba(71,85,105,0.5) !important;
    color: #94a3b8 !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.35), 0 0 0 1px rgba(255,255,255,0.04) inset !important;
}
[data-theme="dark"] .dg-back-btn:hover {
    border-color: #38bdf8 !important; color: #38bdf8 !important;
    box-shadow: 0 0 22px rgba(14,165,233,0.4), 0 4px 16px rgba(0,0,0,0.3) !important;
}
</style>
<a href="javascript:history.back()" class="dg-back-btn" title="Go Back">
    <span class="material-symbols-outlined" style="font-size:19px; line-height:1;">arrow_back_ios_new</span>
</a>
"""

# ─── 1. PAYMENT.HTML ─────────────────────────────────────────────────────────
print("payment.html...")
p = read('payment.html')
if 'dg-back-btn' not in p:
    # Inject CSS + button right after <body ...> opening tag
    body_match = re.search(r'<body[^>]*>', p)
    if body_match:
        end = body_match.end()
        p = p[:end] + '\n' + BACK_BTN_CSS + p[end:]
        write('payment.html', p)
        print("  back button added to payment.html")
    else:
        print("  WARN: no <body> found in payment.html")
else:
    print("  already has back btn")

# ─── 2. PROFILE.HTML ─────────────────────────────────────────────────────────
print("profile.html...")
pr = read('profile.html')
if 'dg-back-btn' not in pr:
    body_match = re.search(r'<body[^>]*>', pr)
    if body_match:
        end = body_match.end()
        pr = pr[:end] + '\n' + BACK_BTN_CSS + pr[end:]
        write('profile.html', pr)
        print("  back button added to profile.html")
    else:
        print("  WARN: no <body> found in profile.html")
else:
    print("  already has back btn")

# ─── 3. VEHICLES.HTML back btn CSS ────────────────────────────────────────────
print("vehicles.html...")
v = read('vehicles.html')
if 'back-btn-v' not in v:
    # Find first </style> and inject before it
    first_style_end = v.find('</style>')
    if first_style_end != -1:
        btn_css = """
        /* Settings-style back button */
        .back-btn-v {
            background: rgba(255,255,255,0.68);
            backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
            border: 1.5px solid rgba(14,165,233,0.22); border-radius: 50%;
            width: 44px; height: 44px; display: flex; align-items: center;
            justify-content: center; color: #475569; text-decoration: none;
            transition: all 0.3s; box-shadow: 0 4px 14px rgba(0,0,0,0.09);
            flex-shrink: 0;
        }
        .back-btn-v:hover {
            border-color: #0ea5e9; color: #0ea5e9;
            box-shadow: 0 0 18px rgba(14,165,233,0.4); transform: scale(1.07);
        }
        [data-theme="dark"] .back-btn-v {
            background: rgba(15,23,42,0.8) !important;
            border-color: rgba(14,165,233,0.35) !important; color: #94a3b8 !important;
        }
        [data-theme="dark"] .back-btn-v:hover {
            border-color: #38bdf8 !important; color: #38bdf8 !important;
        }
"""
        v = v[:first_style_end] + btn_css + v[first_style_end:]
        print("  CSS injected")
    # Replace existing back arrow link
    v = re.sub(
        r'<a href="\{% url \'index\' %\}"[^>]*class="text-slate-600[^"]*"[^>]*>\s*<span class="material-symbols-outlined">arrow_back_ios_new</span>\s*</a>',
        '<a href="{% url \'index\' %}" class="back-btn-v" title="Back to Home"><span class="material-symbols-outlined" style="font-size:20px;">arrow_back_ios_new</span></a>',
        v
    )
    write('vehicles.html', v)
    print("  vehicles.html done")
else:
    print("  already has back-btn-v")

# ─── 4. ACTIVITY.HTML – fix receipts panel CSS ───────────────────────────────
print("activity.html receipts panel CSS...")
a = read('activity.html')

# The panel uses classList.add('open') – make sure the CSS rule exists
receipts_panel_css_exists = '#receipts-panel {' in a or '#receipts-panel{' in a
if not receipts_panel_css_exists:
    panel_css = """
        /* Receipts Panel */
        #receipts-panel {
            position: fixed; inset: 0; z-index: 200;
            display: none; align-items: center; justify-content: center;
            background: rgba(15,23,42,0.55); backdrop-filter: blur(14px);
        }
        #receipts-panel.open { display: flex; }
        .receipts-card {
            background: rgba(255,255,255,0.88); backdrop-filter: blur(28px);
            -webkit-backdrop-filter: blur(28px);
            border: 1.5px solid rgba(14,165,233,0.22); border-radius: 28px;
            padding: 28px; width: 92%; max-width: 480px; max-height: 80vh;
            display: flex; flex-direction: column;
            box-shadow: 0 20px 60px rgba(14,165,233,0.18), 0 0 0 1px rgba(255,255,255,0.5) inset;
            animation: slideUpIn 0.35s cubic-bezier(0.4,0,0.2,1);
        }
        [data-theme="dark"] .receipts-card {
            background: rgba(10,15,28,0.97) !important;
            border-color: rgba(14,165,233,0.3) !important;
            box-shadow: 0 20px 60px rgba(14,165,233,0.12) !important;
        }
        @keyframes slideUpIn {
            from { transform: translateY(40px); opacity: 0; }
            to   { transform: translateY(0);    opacity: 1; }
        }
        .receipt-item {
            background: rgba(14,165,233,0.07); border: 1px solid rgba(14,165,233,0.18);
            border-radius: 14px; padding: 14px 16px;
            display: flex; align-items: center; gap: 14px; margin-bottom: 10px;
            transition: all 0.25s;
        }
        .receipt-item:hover { background: rgba(14,165,233,0.13); border-color: rgba(14,165,233,0.38); transform: translateX(4px); }
"""
    # Inject into the last </style> before </head>
    head_style_end = a.rfind('</style>', 0, a.find('</head>'))
    if head_style_end != -1:
        a = a[:head_style_end] + panel_css + a[head_style_end:]
        print("  receipts panel CSS injected")
else:
    print("  receipts panel CSS already present")

write('activity.html', a)
print("  activity.html done")

# ─── 5. INDEX.HTML – verify chat FAB and logout-btn ──────────────────────────
print("index.html verify...")
idx = read('index.html')
has_chat = 'chat-fab' in idx
has_logout = 'logout-btn' in idx
print(f"  chat-fab: {has_chat}, logout-btn: {has_logout}")
if has_chat and has_logout:
    print("  index.html OK")

# ─── 6. SERVICES.HTML – verify 3 balanced style tags ────────────────────────
print("services.html verify...")
s = read('services.html')
opens = s.count('<style')
closes = s.count('</style>')
print(f"  <style> opens={opens}, closes={closes} => {'OK' if opens==closes else 'MISMATCH!'}")

print("\nAll done!")
