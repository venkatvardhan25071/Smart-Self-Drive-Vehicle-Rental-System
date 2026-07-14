import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
def read(f): return open(os.path.join(BASE,'templates',f),'r',encoding='utf-8',errors='replace').read()
def write(f,c): open(os.path.join(BASE,'templates',f),'w',encoding='utf-8',newline='').write(c)

# ─── 1. ACTIVITY.HTML: Remove white background bar, keep only buttons ────────
print("activity.html filter bar fix...")
a = read('activity.html')

# Remove bg and border from the sticky outer div
a = a.replace(
    '<div class="border-b border-white/30 bg-white/30 sticky top-[88px] z-40 backdrop-blur-xl w-full">',
    '<div class="sticky top-[88px] z-40 w-full">'
)
# Remove backdrop and background from inner container too
a = a.replace(
    '<div class="container mx-auto px-4 py-3 flex gap-3 items-center overflow-x-auto whitespace-nowrap scrollbar-hide justify-between">',
    '<div class="container mx-auto px-4 py-4 flex gap-3 items-center overflow-x-auto whitespace-nowrap scrollbar-hide justify-between">'
)

write('activity.html', a)
print("  activity.html done")

# ─── 2. VEHICLES.HTML: Fix selectCategory JS and dropdown ───────────────────
print("vehicles.html category filter fix...")
v = read('vehicles.html')

# Fix 1: Pass `this` as parameter in onclick so we can reference the element
# Update all dd-item onclick calls to pass `this` as first argument
v = v.replace(
    "onclick=\"selectCategory('', 'All', 'car')\"",
    "onclick=\"selectCategory(this, '', 'All')\""
)

# Fix the loop items - they pass id, name, icon but need `this` first
# Use regex to fix all selectCategory calls that start with a quote (not `this`)
v = re.sub(
    r"onclick=\"selectCategory\('([^']+)', '([^']+)', getCategoryIcon\('([^']+)'\)\)\"",
    r"onclick=\"selectCategory(this, '\1', '\2')\"",
    v
)

# Fix 2: Rewrite the selectCategory JS function
old_js = """function selectCategory(id, name, icon) {
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
}"""

new_js = """function selectCategory(el, id, name) {
    // Set hidden form value
    document.getElementById('hidden-category-input').value = id;
    // Update trigger label
    document.getElementById('dd-label').textContent = name;
    // Update selected styling
    document.querySelectorAll('.glass-dd-item').forEach(function(item) {
        item.classList.remove('selected');
    });
    if (el) el.classList.add('selected');
    // Close dropdown
    document.getElementById('category-dd-wrapper').classList.remove('open');
    // Submit form to filter
    setTimeout(function() {
        document.getElementById('vehicle-filter-form').submit();
    }, 120);
}"""

if old_js in v:
    v = v.replace(old_js, new_js)
    print("  selectCategory JS fixed")
else:
    # Try to find and replace just the function
    v = re.sub(
        r'function selectCategory\(.*?\{.*?submit\(\);?\s*\}',
        new_js,
        v,
        flags=re.DOTALL
    )
    print("  selectCategory JS fixed (regex)")

# Fix 3: Also improve the DOMContentLoaded to fix icon labels correctly
old_dom = """// Fix: replace icon spans in each dd-item after load
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
});"""

new_dom = """document.addEventListener('DOMContentLoaded', function() {
    // Set label from selected item
    const sel = document.querySelector('.glass-dd-item.selected');
    if (sel) {
        const label = sel.textContent.trim();
        const ddLabel = document.getElementById('dd-label');
        if (ddLabel) ddLabel.textContent = label;
    }
    // Close on outside click
    document.addEventListener('click', function(e) {
        const w = document.getElementById('category-dd-wrapper');
        if (w && !w.contains(e.target)) w.classList.remove('open');
    });
});"""

if old_dom in v:
    v = v.replace(old_dom, new_dom)
    print("  DOMContentLoaded fixed")
else:
    v = re.sub(
        r'// Fix: replace icon spans.*?document\.addEventListener\(\'DOMContentLoaded\',.*?\}\);',
        new_dom,
        v,
        flags=re.DOTALL
    )
    print("  DOMContentLoaded fixed (regex)")

write('vehicles.html', v)
print("  vehicles.html done")
print("\nAll done!")
