# Changelogs

Below you'll find aggregated changelog entries from all discovered packages (newest first). Use the filter in the secondary sidebar (right side on wide screens) to narrow by package.

{% for entry in changelog_entries %}
<details class="changelog-entry" data-package="{{ entry.package }}">
  <summary>
    <span class="chg-meta">
      <span class="chg-pkg">{{ entry.package }}</span>
      <span class="chg-version">{{ entry.version }}</span>
      <span class="chg-date">{{ entry.date }}</span>
    </span>
  </summary>
  <div class="chg-body">
    <div class="chg-source">Source: <code>{{ entry.path }}</code></div>
    {{ entry.html | safe }}
  </div>
</details>
{% endfor %}

<!-- Static filter panel (no JS relocation) -->
<div class="changelog-filter-panel">
  <h4>Filter</h4>
  <div class="chg-dropdown" id="package-filter" data-value="">
    <button type="button" class="chg-dropdown__button" aria-haspopup="listbox" aria-expanded="false" aria-labelledby="package-filter-label package-filter-current">
      <span id="package-filter-label" class="chg-dropdown__label">Package</span>
      <span id="package-filter-current" class="chg-dropdown__current" data-all-label="All">All</span>
      <span class="chg-dropdown__arrow" aria-hidden="true"></span>
    </button>
    <ul class="chg-dropdown__list" role="listbox" tabindex="-1" aria-labelledby="package-filter-label">
      <li class="chg-dropdown__option is-active" role="option" data-value="" aria-selected="true">All</li>
      {% for pkg in changelog_packages %}
      <li class="chg-dropdown__option" role="option" data-value="{{ pkg }}" aria-selected="false">{{ pkg }}</li>
      {% endfor %}
    </ul>
  </div>
  <p class="hint">Showing newest first. Select a package to narrow the list.</p>
</div>


