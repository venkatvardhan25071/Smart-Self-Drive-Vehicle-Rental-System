import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
def read(f): return open(os.path.join(BASE,'templates',f),'r',encoding='utf-8',errors='replace').read()
def write(f,c): open(os.path.join(BASE,'templates',f),'w',encoding='utf-8',newline='').write(c)

# ─── 1. ACTIVITY.HTML ───────────────────────────────────────────────────────
print("activity.html...")
a = read('activity.html')

# NEW filter bar: receipts + bell BOTH on right, filters on left, NO wave spans
new_filter_bar = '''        <div class="border-b border-white/30 bg-white/30 sticky top-[88px] z-40 backdrop-blur-xl w-full">
            <div class="container mx-auto px-4 py-3 flex gap-3 items-center overflow-x-auto whitespace-nowrap scrollbar-hide justify-between">
                <!-- Filter Buttons LEFT -->
                <div class="flex gap-2 items-center">
                    <button data-filter="all" onclick="filterActivity('all', this)" class="activity-filter-btn is-active bg-sky-500 text-white px-5 py-2 rounded-full text-sm font-bold shadow-md">History</button>
                    <button data-filter="accepted" onclick="filterActivity('accepted', this)" class="activity-filter-btn bg-white/50 text-slate-600 px-5 py-2 rounded-full text-sm font-bold border border-white/50 shadow-inner">Accepted</button>
                    <button data-filter="pending" onclick="filterActivity('pending', this)" class="activity-filter-btn bg-white/50 text-slate-600 px-5 py-2 rounded-full text-sm font-bold border border-white/50 shadow-inner">Pending</button>
                    <button data-filter="rejected" onclick="filterActivity('rejected', this)" class="activity-filter-btn bg-white/50 text-slate-600 px-5 py-2 rounded-full text-sm font-bold border border-white/50 shadow-inner">Rejected</button>
                </div>
                <!-- RIGHT: Receipts Archive + Bell -->
                <div class="flex items-center gap-2 flex-shrink-0">
                    <!-- Downloaded Receipts -->
                    <button onclick="openReceiptsPanel()" id="receipts-archive-btn" title="Downloaded Receipts"
                        style="position:relative;width:42px;height:42px;border-radius:50%;background:rgba(255,255,255,0.68);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1.5px solid rgba(14,165,233,0.22);box-shadow:0 4px 14px rgba(14,165,233,0.14),inset 0 1px 0 rgba(255,255,255,0.9);display:flex;align-items:center;justify-content:center;cursor:pointer;transition:all 0.3s;flex-shrink:0;"
                        onmouseover="this.style.transform='scale(1.1)';this.style.borderColor='rgba(14,165,233,0.6)';this.style.boxShadow='0 0 18px rgba(14,165,233,0.35)'"
                        onmouseout="this.style.transform='';this.style.borderColor='rgba(14,165,233,0.22)';this.style.boxShadow='0 4px 14px rgba(14,165,233,0.14),inset 0 1px 0 rgba(255,255,255,0.9)'">
                        <span class="material-symbols-outlined" style="font-size:21px;color:#0ea5e9;line-height:1;">folder_open</span>
                        <span id="receipts-badge" style="display:none;position:absolute;top:-3px;right:-3px;width:17px;height:17px;background:linear-gradient(135deg,#0ea5e9,#3b82f6);border-radius:50%;color:white;font-size:9px;font-weight:800;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(14,165,233,0.5);border:2px solid white;">0</span>
                    </button>
                    <!-- Notification Bell (no wave) -->
                    <div class="relative z-50">
                        <button id="bell-btn" onclick="document.getElementById('admin-notification').classList.toggle('hidden')"
                            style="position:relative;width:42px;height:42px;border-radius:50%;background:rgba(255,255,255,0.68);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1.5px solid rgba(14,165,233,0.22);box-shadow:0 4px 14px rgba(14,165,233,0.14),inset 0 1px 0 rgba(255,255,255,0.9);display:flex;align-items:center;justify-content:center;cursor:pointer;transition:all 0.3s;flex-shrink:0;"
                            onmouseover="this.style.transform='scale(1.1)';this.style.borderColor='rgba(14,165,233,0.6)';this.style.boxShadow='0 0 18px rgba(14,165,233,0.35)'"
                            onmouseout="this.style.transform='';this.style.borderColor='rgba(14,165,233,0.22)';this.style.boxShadow='0 4px 14px rgba(14,165,233,0.14),inset 0 1px 0 rgba(255,255,255,0.9)'">
                            <span class="material-symbols-outlined" style="font-size:22px;color:#0ea5e9;line-height:1;">notifications</span>
                            {% if bookings and bookings.0.obj.status %}
                                {% if bookings.0.obj.status|lower == 'accepted' or bookings.0.obj.status|lower == 'approved' or bookings.0.obj.status|lower == 'rejected' %}
                                <span style="position:absolute;top:2px;right:2px;width:10px;height:10px;background:#ef4444;border-radius:50%;border:2px solid white;box-shadow:0 0 6px rgba(239,68,68,0.7);animation:notifDot 1.4s ease-in-out infinite;"></span>
                                {% endif %}
                            {% endif %}
                        </button>
                    </div>
                </div>
            </div>
        </div>'''

# Find and replace the entire filter bar block
old_start = '        <div class="border-b border-white/30 bg-white/30 sticky top-[88px] z-40 backdrop-blur-xl w-full">'
old_end = '        </div>'

# Find start position
start_idx = a.find(old_start)
if start_idx != -1:
    # Find the matching closing div (2 levels deep)
    search_from = start_idx + len(old_start)
    depth = 1
    pos = search_from
    while pos < len(a) and depth > 0:
        next_open = a.find('<div', pos)
        next_close = a.find('</div>', pos)
        if next_open != -1 and (next_open < next_close or next_close == -1):
            depth += 1
            pos = next_open + 4
        elif next_close != -1:
            depth -= 1
            if depth == 0:
                end_idx = next_close + len('</div>')
                break
            pos = next_close + 6
        else:
            break
    a = a[:start_idx] + new_filter_bar + a[end_idx:]
    print("  filter bar replaced")
else:
    print("  WARN: filter bar start not found")

# Also add dark mode styles for the new buttons
dark_btns = """
        /* Dark mode for right-side action buttons */
        [data-theme="dark"] #receipts-archive-btn,
        [data-theme="dark"] #bell-btn {
            background: rgba(15,23,42,0.82) !important;
            border-color: rgba(14,165,233,0.38) !important;
            box-shadow: 0 4px 14px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05) !important;
        }
        [data-theme="dark"] #receipts-archive-btn:hover,
        [data-theme="dark"] #bell-btn:hover {
            border-color: rgba(14,165,233,0.65) !important;
            box-shadow: 0 0 20px rgba(14,165,233,0.35) !important;
        }
"""
# Inject before last </style> before </head>
head_end = a.find('</head>')
last_style_before_head = a.rfind('</style>', 0, head_end)
if last_style_before_head != -1:
    a = a[:last_style_before_head] + dark_btns + a[last_style_before_head:]
    print("  dark mode button CSS injected")

write('activity.html', a)
print("  activity.html done")

# ─── 2. VEHICLES.HTML – Glassmorphic custom dropdown ────────────────────────
print("vehicles.html...")
v = read('vehicles.html')

# Custom glassmorphic dropdown CSS
dropdown_css = """
        /* ==== Glassmorphic Category Dropdown ==== */
        .glass-dropdown-wrapper { position: relative; display: inline-block; }
        .glass-dropdown-trigger {
            display: flex; align-items: center; gap: 10px;
            background: rgba(255,255,255,0.72);
            backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
            border: 1.5px solid rgba(14,165,233,0.3);
            border-radius: 9999px; padding: 10px 20px;
            font-size: 14px; font-weight: 700; color: #0f172a;
            cursor: pointer; transition: all 0.3s;
            box-shadow: 0 4px 16px rgba(14,165,233,0.16), inset 0 1px 0 rgba(255,255,255,0.9);
            min-width: 140px; user-select: none;
        }
        .glass-dropdown-trigger:hover {
            border-color: rgba(14,165,233,0.6);
            box-shadow: 0 0 20px rgba(14,165,233,0.3), inset 0 1px 0 rgba(255,255,255,0.9);
            transform: translateY(-1px);
        }
        .glass-dropdown-trigger .dd-arrow {
            margin-left: auto; transition: transform 0.3s;
            font-size: 18px; color: #0ea5e9;
        }
        .glass-dropdown-wrapper.open .dd-arrow { transform: rotate(180deg); }
        .glass-dropdown-menu {
            position: absolute; top: calc(100% + 8px); left: 0; z-index: 500;
            background: rgba(255,255,255,0.88);
            backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
            border: 1.5px solid rgba(14,165,233,0.22);
            border-radius: 20px; overflow: hidden;
            box-shadow: 0 16px 48px rgba(14,165,233,0.18), 0 4px 12px rgba(0,0,0,0.08), inset 0 1px 0 rgba(255,255,255,0.9);
            min-width: 180px;
            opacity: 0; transform: translateY(-8px) scale(0.97);
            pointer-events: none;
            transition: opacity 0.22s ease, transform 0.22s cubic-bezier(0.4,0,0.2,1);
        }
        .glass-dropdown-wrapper.open .glass-dropdown-menu {
            opacity: 1; transform: translateY(0) scale(1); pointer-events: all;
        }
        .glass-dd-item {
            display: flex; align-items: center; gap: 10px;
            padding: 11px 18px; font-size: 14px; font-weight: 600;
            color: #334155; cursor: pointer; transition: all 0.18s;
            border-bottom: 1px solid rgba(14,165,233,0.07);
        }
        .glass-dd-item:last-child { border-bottom: none; }
        .glass-dd-item:hover {
            background: rgba(14,165,233,0.1);
            color: #0ea5e9;
            padding-left: 22px;
        }
        .glass-dd-item.selected {
            background: rgba(14,165,233,0.12);
            color: #0ea5e9; font-weight: 700;
        }
        .glass-dd-item .dd-icon {
            width: 28px; height: 28px; border-radius: 8px; flex-shrink: 0;
            background: linear-gradient(135deg, rgba(14,165,233,0.15), rgba(59,130,246,0.1));
            border: 1px solid rgba(14,165,233,0.2);
            display: flex; align-items: center; justify-content: center;
            font-size: 15px;
        }
        /* Dark mode */
        [data-theme="dark"] .glass-dropdown-trigger {
            background: rgba(15,23,42,0.82) !important;
            border-color: rgba(14,165,233,0.35) !important;
            color: #e2e8f0 !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05) !important;
        }
        [data-theme="dark"] .glass-dropdown-trigger:hover {
            border-color: rgba(14,165,233,0.6) !important;
            box-shadow: 0 0 20px rgba(14,165,233,0.3) !important;
        }
        [data-theme="dark"] .glass-dropdown-menu {
            background: rgba(10,15,28,0.96) !important;
            border-color: rgba(14,165,233,0.3) !important;
            box-shadow: 0 16px 48px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.04) !important;
        }
        [data-theme="dark"] .glass-dd-item {
            color: #94a3b8 !important;
            border-color: rgba(14,165,233,0.08) !important;
        }
        [data-theme="dark"] .glass-dd-item:hover, [data-theme="dark"] .glass-dd-item.selected {
            background: rgba(14,165,233,0.14) !important;
            color: #38bdf8 !important;
        }
"""

# Find the closing </style> just before </head> and inject CSS
head_end_v = v.find('</head>')
last_style_v = v.rfind('</style>', 0, head_end_v)
v = v[:last_style_v] + dropdown_css + v[last_style_v:]

# Category icons mapping
ICONS = {
    'all': ('directions_car', 'All'),
    'cars': ('directions_car', 'Cars'),
    'car': ('directions_car', 'Car'),
    'scoty': ('two_wheeler', 'Scoty'),
    'scooter': ('two_wheeler', 'Scooter'),
    'bike': ('pedal_bike', 'Bike'),
    '4 seater': ('airport_shuttle', '4 Seater'),
    '5 seater': ('airport_shuttle', '5 Seater'),
    '6 seater': ('directions_bus', '6 Seater'),
    '7 seater': ('directions_bus', '7 Seater'),
    '8 seater': ('directions_bus', '8 Seater'),
    '3 seater': ('airline_seat_recline_normal', '3 Seater'),
    'luxury': ('star', 'Luxury'),
    'suv': ('directions_car', 'SUV'),
    'van': ('airport_shuttle', 'Van'),
}

# Replace the old <form> + <select> with a glassmorphic custom dropdown
old_form = '''            <form method="get" action="{% url 'vehicles' %}" class="flex items-center gap-2">
                <select name="category" class="bg-white/80 border-2 border-sky-400 text-slate-800 rounded-full py-2.5 px-6 text-sm shadow-[0_4px_15px_rgba(14,165,233,0.2)] focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-300 font-bold backdrop-blur-md transition-all cursor-pointer">
                    <option value="">All</option>
                    {% for category in categories %}
                        <option value="{{ category.id }}" {% if selected_category_id == category.id %}selected{% endif %}>
                            {{ category.name }}
                        </option>
                    {% endfor %}
                </select>
                <button type="submit" class="bg-gradient-to-r from-primary-start to-primary-end text-white font-bold py-2.5 px-6 rounded-full hover:shadow-lg hover:shadow-sky-500/30 transition-all">
                    Filter
                </button>
            </form>'''

new_form = '''            <!-- Hidden form for submission -->
            <form method="get" action="{% url 'vehicles' %}" id="vehicle-filter-form" style="display:none;">
                <input type="hidden" name="category" id="hidden-category-input" value="{{ selected_category_id|default:'' }}">
            </form>
            <!-- Glassmorphic Category Dropdown -->
            <div class="glass-dropdown-wrapper" id="category-dd-wrapper">
                <div class="glass-dropdown-trigger" onclick="toggleCategoryDD()" id="dd-trigger">
                    <span class="material-symbols-outlined" id="dd-icon" style="font-size:18px;color:#0ea5e9;line-height:1;">directions_car</span>
                    <span id="dd-label">All</span>
                    <span class="material-symbols-outlined dd-arrow">expand_more</span>
                </div>
                <div class="glass-dropdown-menu" id="category-dd-menu">
                    <!-- All option -->
                    <div class="glass-dd-item {% if not selected_category_id %}selected{% endif %}" onclick="selectCategory('', 'All', 'directions_car')">
                        <div class="dd-icon"><span class="material-symbols-outlined" style="font-size:15px;color:#0ea5e9;">directions_car</span></div>
                        All
                    </div>
                    {% for category in categories %}
                    <div class="glass-dd-item {% if selected_category_id == category.id %}selected{% endif %}"
                         onclick="selectCategory('{{ category.id }}', '{{ category.name }}', getCategoryIcon('{{ category.name|lower }}'))">
                        <div class="dd-icon">
                            <span class="material-symbols-outlined" style="font-size:15px;color:#0ea5e9;">{{ category.name|lower|slice:":3" }}</span>
                        </div>
                        {{ category.name }}
                    </div>
                    {% endfor %}
                </div>
            </div>'''

if old_form in v:
    v = v.replace(old_form, new_form)
    print("  select replaced with glassmorphic dropdown")
else:
    # Try finding just the form tag area
    form_idx = v.find('<form method="get" action="{% url \'vehicles\' %}"')
    if form_idx != -1:
        form_end = v.find('</form>', form_idx) + len('</form>')
        v = v[:form_idx] + new_form + v[form_end:]
        print("  select replaced (fallback)")
    else:
        print("  WARN: form not found")

# Add dropdown JS before </body>
dropdown_js = """
<script>
/* Glassmorphic Category Dropdown */
const CATEGORY_ICONS = {
    'all': 'directions_car',
    'cars': 'directions_car', 'car': 'directions_car',
    'scoty': 'two_wheeler', 'scooter': 'two_wheeler',
    'bike': 'pedal_bike',
    '4 seater': 'airport_shuttle', '5 seater': 'airport_shuttle',
    '6 seater': 'directions_bus', '7 seater': 'directions_bus',
    '8 seater': 'directions_bus', '3 seater': 'airline_seat_recline_normal',
    'luxury': 'star', 'suv': 'directions_car', 'van': 'airport_shuttle',
};

function getCategoryIcon(name) {
    return CATEGORY_ICONS[name] || CATEGORY_ICONS[name.split(' ')[0]] || 'directions_car';
}

function toggleCategoryDD() {
    const w = document.getElementById('category-dd-wrapper');
    w.classList.toggle('open');
}

function selectCategory(id, name, icon) {
    // Update hidden input and submit
    document.getElementById('hidden-category-input').value = id;
    // Update trigger label
    document.getElementById('dd-label').textContent = name;
    document.getElementById('dd-icon').textContent = icon || 'directions_car';
    // Update selected class
    document.querySelectorAll('.glass-dd-item').forEach(el => el.classList.remove('selected'));
    event.currentTarget.classList.add('selected');
    // Close & submit
    document.getElementById('category-dd-wrapper').classList.remove('open');
    document.getElementById('vehicle-filter-form').submit();
}

// Fix: replace icon spans in each dd-item after load
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.glass-dd-item').forEach(function(item) {
        const label = item.textContent.trim().toLowerCase();
        const icon = getCategoryIcon(label);
        const iconEl = item.querySelector('.material-symbols-outlined');
        if (iconEl) iconEl.textContent = icon;
    });
    // Set current label from selected
    const sel = document.querySelector('.glass-dd-item.selected');
    if (sel) {
        const label = sel.textContent.trim();
        const icon = getCategoryIcon(label.toLowerCase());
        document.getElementById('dd-label').textContent = label;
        document.getElementById('dd-icon').textContent = icon;
    }
    // Close on outside click
    document.addEventListener('click', function(e) {
        const w = document.getElementById('category-dd-wrapper');
        if (w && !w.contains(e.target)) w.classList.remove('open');
    });
});
</script>
"""

v = v.replace('</body>', dropdown_js + '\n</body>', 1)
print("  dropdown JS added")

write('vehicles.html', v)
print("  vehicles.html done")
print("\nAll done!")
