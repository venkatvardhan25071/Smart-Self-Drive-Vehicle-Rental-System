path = r'templates/payment.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = (
    '        <div class="flex items-center gap-4">\n'
    '                    <a href="#" onclick="history.back()" class="text-slate-600 hover:text-sky-600 transition-colors">\n'
    '                        <span class="material-symbols-outlined">arrow_back_ios_new</span>\n'
    '                    </a>\n'
    '                    <h1 class="text-2xl font-bold text-slate-900">Payment &amp; Verification</h1>\n'
    '                </div>'
)

# Use regex to match flexibly
import re
pattern = re.compile(
    r'<div class="flex items-center gap-4">\s*'
    r'<a href="#" onclick="history\.back\(\)" class="text-slate-600 hover:text-sky-600 transition-colors">\s*'
    r'<span class="material-symbols-outlined">arrow_back_ios_new</span>\s*'
    r'</a>\s*'
    r'<h1 class="text-2xl font-bold text-slate-900">Payment &amp; Verification</h1>\s*'
    r'</div>',
    re.DOTALL
)

new = (
    '<div class="flex items-center gap-3 mb-2">\n'
    '                    <a href="javascript:history.back()" title="Go Back"\n'
    '                        style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,rgba(255,255,255,0.75),rgba(255,255,255,0.4));backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1.5px solid rgba(255,255,255,0.7);display:flex;align-items:center;justify-content:center;color:#475569;text-decoration:none;box-shadow:0 4px 14px rgba(0,0,0,0.1),inset 0 1px 0 rgba(255,255,255,0.8);transition:all 0.28s cubic-bezier(0.4,0,0.2,1);flex-shrink:0;"\n'
    "                        onmouseover=\"this.style.borderColor='#0ea5e9';this.style.color='#0ea5e9';this.style.boxShadow='0 0 18px rgba(14,165,233,0.4)';this.style.transform='scale(1.08) translateX(-2px)'\"\n"
    "                        onmouseout=\"this.style.borderColor='rgba(255,255,255,0.7)';this.style.color='#475569';this.style.boxShadow='0 4px 14px rgba(0,0,0,0.1)';this.style.transform=''\">\n"
    '                        <span class="material-symbols-outlined" style="font-size:18px;line-height:1;">arrow_back_ios_new</span>\n'
    '                    </a>\n'
    '                    <h1 class="text-2xl font-bold text-slate-900">Payment &amp; Verification</h1>\n'
    '                </div>'
)

result, count = pattern.subn(new, content, count=1)
if count:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(result)
    print('SUCCESS: payment header replaced')
else:
    print('REGEX not matched either')
