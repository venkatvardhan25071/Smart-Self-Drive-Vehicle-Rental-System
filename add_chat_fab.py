import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

chat_fab = """
<!-- Chat FAB (Bottom Right) -->
<style>
.chat-fab{position:fixed;bottom:28px;right:24px;z-index:999;width:60px;height:60px;border-radius:50%;background:rgba(255,255,255,0.65);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1.5px solid rgba(14,165,233,0.3);box-shadow:0 8px 28px rgba(14,165,233,0.28),inset 0 1px 0 rgba(255,255,255,0.9);display:flex;align-items:center;justify-content:center;cursor:pointer;text-decoration:none;transition:all 0.3s cubic-bezier(0.4,0,0.2,1);}
.chat-fab:hover{transform:translateY(-4px) scale(1.1);box-shadow:0 16px 40px rgba(14,165,233,0.45),inset 0 1px 0 rgba(255,255,255,0.9);background:rgba(14,165,233,0.12);border-color:rgba(14,165,233,0.6);}
.cfr{position:absolute;width:60px;height:60px;border-radius:50%;border:2px solid rgba(14,165,233,0.4);animation:chatRipple 2s ease-out infinite;top:50%;left:50%;transform:translate(-50%,-50%) scale(0.8);opacity:0;pointer-events:none;}
.cfr:nth-child(2){animation-delay:0.65s;}.cfr:nth-child(3){animation-delay:1.3s;}
@keyframes chatRipple{0%{transform:translate(-50%,-50%) scale(0.8);opacity:0.8;}100%{transform:translate(-50%,-50%) scale(2.6);opacity:0;}}
[data-theme="dark"] .chat-fab{background:rgba(10,15,28,0.82)!important;border-color:rgba(14,165,233,0.45)!important;box-shadow:0 8px 28px rgba(14,165,233,0.22),inset 0 1px 0 rgba(255,255,255,0.06)!important;}
[data-theme="dark"] .chat-fab:hover{background:rgba(14,165,233,0.15)!important;box-shadow:0 16px 40px rgba(14,165,233,0.4)!important;}
#logout-btn{transition:all 0.3s!important;}
#logout-btn:hover{background:rgba(239,68,68,0.12)!important;color:#ef4444!important;box-shadow:0 0 18px rgba(239,68,68,0.22),inset 0 0 12px rgba(239,68,68,0.08)!important;}
[data-theme="dark"] #logout-btn:hover{background:rgba(239,68,68,0.18)!important;color:#f87171!important;box-shadow:0 0 24px rgba(239,68,68,0.35)!important;}
</style>
<a href="{% url 'chat' %}" class="chat-fab" title="Chat with DriveGO Support">
    <span class="cfr"></span><span class="cfr"></span><span class="cfr"></span>
    <span class="material-symbols-outlined" style="font-size:28px;color:#0ea5e9;position:relative;z-index:1;line-height:1;">chat</span>
</a>
"""

content = content.replace('</body>', chat_fab + '</body>', 1)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Chat FAB added successfully!')
