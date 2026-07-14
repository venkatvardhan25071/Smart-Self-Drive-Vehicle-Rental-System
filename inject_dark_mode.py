import os, re

TEMPLATE_DIR = r'c:\Users\venka\Desktop\vv\templates'

DARK_CSS = '''<script>
/* DriveGO Global Theme System */
(function(){
    var t = localStorage.getItem('drivego_theme') || 'light';
    var resolved = (t === 'system') ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light') : t;
    document.documentElement.setAttribute('data-theme', resolved);
})();
</script>
<style>
/* === DriveGO Global Dark Mode === */
[data-theme="dark"] body,
[data-theme="dark"] .bg-main-mesh {
    background-color: #0f172a !important;
    background-image: none !important;
    color: #e2e8f0 !important;
}
[data-theme="dark"] body::before {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
}
[data-theme="dark"] body::after { background: none !important; }
[data-theme="dark"] .glass-panel,
[data-theme="dark"] [class*="bg-white/4"],
[data-theme="dark"] [class*="bg-white/5"],
[data-theme="dark"] [class*="bg-white/6"],
[data-theme="dark"] [class*="bg-white/3"] {
    background: rgba(30,41,59,0.88) !important;
    border-color: rgba(71,85,105,0.45) !important;
}
[data-theme="dark"] h1,[data-theme="dark"] h2,[data-theme="dark"] h3 { color: #f1f5f9 !important; }
[data-theme="dark"] p,[data-theme="dark"] span:not([class*="text-sky"]):not([class*="text-emerald"]):not([class*="text-red"]):not([class*="text-amber"]):not([class*="text-yellow"]) { color: inherit; }
[data-theme="dark"] .text-slate-900 { color: #f1f5f9 !important; }
[data-theme="dark"] .text-slate-800 { color: #e2e8f0 !important; }
[data-theme="dark"] .text-slate-700 { color: #cbd5e1 !important; }
[data-theme="dark"] .text-slate-600 { color: #94a3b8 !important; }
[data-theme="dark"] .text-slate-500 { color: #64748b !important; }
[data-theme="dark"] [class*="border-white/"] { border-color: rgba(71,85,105,0.4) !important; }
[data-theme="dark"] input:not([type="submit"]):not([type="button"]),
[data-theme="dark"] .input-box,
[data-theme="dark"] select,
[data-theme="dark"] textarea {
    background: rgba(15,23,42,0.75) !important;
    color: #e2e8f0 !important;
    border-color: rgba(71,85,105,0.6) !important;
}
[data-theme="dark"] input::placeholder,
[data-theme="dark"] textarea::placeholder { color: #475569 !important; }
[data-theme="dark"] header { background: rgba(15,23,42,0.92) !important; border-color: rgba(71,85,105,0.3) !important; }
[data-theme="dark"] nav { background: rgba(15,23,42,0.9) !important; }
[data-theme="dark"] .glass-nav,
[data-theme="dark"] #nav-container { background: rgba(15,23,42,0.92) !important; border-color: rgba(71,85,105,0.3) !important; }
[data-theme="dark"] label { color: #cbd5e1 !important; }
[data-theme="dark"] .bg-white { background: #1e293b !important; }
[data-theme="dark"] .bg-sky-50 { background: rgba(14,165,233,0.1) !important; }
[data-theme="dark"] .bg-slate-100,
[data-theme="dark"] .bg-slate-200 { background: rgba(30,41,59,0.7) !important; }
[data-theme="dark"] :root {
    --bg: #0f172a;
    --glass: linear-gradient(135deg, rgba(30,41,59,0.88), rgba(15,23,42,0.75));
    --border: rgba(71,85,105,0.45);
    --border-highlight: rgba(100,116,139,0.6);
    --card-bg: rgba(30,41,59,0.8);
    --text-main: #f1f5f9;
    --text-muted: #94a3b8;
}
</style>'''

# Files that need dark mode injected
targets = [
    'vehicles.html', 'host.html', 'booking_summary.html', 'changepassword.html',
    'chat.html', 'confirm.html', 'help.html', 'key.html', 'location_tracking.html',
    'login.html', 'membership.html', 'Services.html', 'offers.html', 'payment.html',
    'report_issue.html', 'signup.html', 'support_call.html', 'support_email.html',
    'success.html', 'support.html'
]

injected = 0
for fname in targets:
    fpath = os.path.join(TEMPLATE_DIR, fname)
    if not os.path.exists(fpath):
        print(f'SKIP (not found): {fname}')
        continue
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if 'drivego_theme' in content:
        print(f'SKIP (already has theme): {fname}')
        continue
    if '</head>' not in content.lower():
        print(f'SKIP (no </head>): {fname}')
        continue
    # Inject before </head>
    content = re.sub(r'</head>', DARK_CSS + '\n</head>', content, count=1, flags=re.IGNORECASE)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'OK: {fname}')
    injected += 1

print(f'\nDone! Injected dark mode into {injected} files.')
