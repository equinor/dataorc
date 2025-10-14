// Changelog filter script (custom dropdown variant) - static panel version
function ensurePanelInSidebar(panel) {
  if (!panel) return;
  // Already inside a secondary sidebar inner container
  if (panel.closest('.md-sidebar--secondary')) return;
  let secondary = document.querySelector('.md-sidebar--secondary');
  if (!secondary) {
    const layout = document.querySelector('.md-container');
    if (!layout) return; // bail if layout not ready yet
    secondary = document.createElement('div');
    secondary.className = 'md-sidebar md-sidebar--secondary';
    layout.appendChild(secondary);
  }
  const inner = secondary.querySelector('.md-sidebar__inner') || (() => {
    const div = document.createElement('div');
    div.className = 'md-sidebar__inner';
    secondary.appendChild(div);
    return div;
  })();
  inner.prepend(panel);
}

function initChangelogFilter() {
  const panel = document.querySelector('.changelog-filter-panel');
  ensurePanelInSidebar(panel);
  const dropdown = panel && panel.querySelector('.chg-dropdown');
  if (!dropdown) return;
  const button = dropdown.querySelector('.chg-dropdown__button');
  const list = dropdown.querySelector('.chg-dropdown__list');
  const options = Array.from(dropdown.querySelectorAll('.chg-dropdown__option'));
  const currentSpan = dropdown.querySelector('.chg-dropdown__current');
  const entries = Array.from(document.querySelectorAll('.changelog-entry'));

  let open = false;
  let activeIndex = options.findIndex(o => o.classList.contains('is-active'));

  function setOpen(state) {
    open = state;
    button.setAttribute('aria-expanded', String(open));
    dropdown.classList.toggle('is-open', open);
    if (open) {
      list.focus();
    }
  }

  function applyFilter(value) {
    let visibleCount = 0;
    entries.forEach(entry => {
      const pkg = entry.getAttribute('data-package');
      const show = !value || pkg === value;
      entry.style.display = show ? '' : 'none';
      if (show) visibleCount++;
    });
    const hint = panel ? panel.querySelector('.hint') : null;
    if (hint) {
      hint.textContent = `Showing ${visibleCount} of ${entries.length} entries (newest first).`;
    }
  }

  function selectIndex(index) {
    if (index < 0 || index >= options.length) return;
    options.forEach((o, i) => {
      const selected = i === index;
      o.classList.toggle('is-active', selected);
      o.setAttribute('aria-selected', String(selected));
      if (selected) {
        activeIndex = i;
        const val = o.getAttribute('data-value') || '';
        dropdown.dataset.value = val;
        currentSpan.textContent = val || currentSpan.getAttribute('data-all-label') || 'All';
        applyFilter(val);
      }
    });
  }

  // Initial filter application
  selectIndex(activeIndex === -1 ? 0 : activeIndex);

  button.addEventListener('click', () => setOpen(!open));
  button.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      setOpen(true);
      const delta = e.key === 'ArrowDown' ? 1 : -1;
      let next = (activeIndex + delta + options.length) % options.length;
      selectIndex(next);
    } else if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      setOpen(!open);
    }
  });

  list.addEventListener('click', e => {
    const li = e.target.closest('.chg-dropdown__option');
    if (!li) return;
    const idx = options.indexOf(li);
    if (idx !== -1) {
      selectIndex(idx);
      setOpen(false);
      button.focus();
    }
  });

  list.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      e.preventDefault();
      setOpen(false);
      button.focus();
      return;
    }
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      const delta = e.key === 'ArrowDown' ? 1 : -1;
      let next = (activeIndex + delta + options.length) % options.length;
      selectIndex(next);
      return;
    }
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      setOpen(false);
      button.focus();
    }
  });

  document.addEventListener('click', e => {
    if (!dropdown.contains(e.target) && open) {
      setOpen(false);
    }
  });
}

// Support MkDocs Material instant navigation & normal loads
if (window.document$ && typeof window.document$.subscribe === 'function') {
  window.document$.subscribe(initChangelogFilter);
}
document.addEventListener('DOMContentLoaded', initChangelogFilter);
