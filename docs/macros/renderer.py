"""HTML rendering helpers for parsed changelog sections."""

from __future__ import annotations

import html
import re
from typing import List

from .constants import CATEGORY_RE, COMMIT_MARKDOWN_LINK_RE, MARKDOWN_LINK_RE

_BULLET_RE = re.compile(r"^\s*[-*+]\s+(.*)$")
_PARENS_COMMIT_RE = re.compile(r"\((<a[^>]+class=\"chg-commit\"[^>]*>[^<]+</a>)\)")
_GENERIC_CATEGORY_RE = re.compile(r"^###\s+(.+?)\s*$")


def render_lines_to_html(lines: List[str]) -> str:
    html_out: List[str] = []
    in_list = False
    for raw in lines:
        line = raw.rstrip()
        if not line:
            if in_list:
                html_out.append("</ul>")
                in_list = False
            continue
        cat = CATEGORY_RE.match(line)
        if not cat:
            generic = _GENERIC_CATEGORY_RE.match(line)
            if generic:
                cat = generic
        if cat and cat.groups():
            if in_list:
                html_out.append("</ul>")
                in_list = False
            raw_label = cat.group(1)
            canonical = raw_label.title()
            slug = canonical.lower().replace(" ", "-")
            html_out.append(
                f'<h4 class="chg-cat"><span class="badge badge-{slug}">{html.escape(canonical)}</span></h4>'
            )
            continue
        bullet_match = _BULLET_RE.match(line)
        if bullet_match:
            if not in_list:
                html_out.append('<ul class="chg-list">')
                in_list = True
            item_text = bullet_match.group(1)

            def repl_commit_md(m):
                full_url = m.group(2)
                sha = m.group(3)
                return f'<a href="{html.escape(full_url)}" class="chg-commit" title="Commit {sha}">{sha[:7]}</a>'

            item_text = COMMIT_MARKDOWN_LINK_RE.sub(repl_commit_md, item_text)

            def repl_link(m):
                txt, url = m.groups()
                return f'<a href="{html.escape(url)}" class="chg-link">{html.escape(txt)}</a>'

            item_text = MARKDOWN_LINK_RE.sub(repl_link, item_text)
            html_out.append(f"<li>{item_text}</li>")
            continue
        safe = html.escape(line)
        safe = COMMIT_MARKDOWN_LINK_RE.sub(
            lambda m: f'<a href="{html.escape(m.group(2))}" class="chg-commit" title="Commit {m.group(3)}">{m.group(3)[:7]}</a>',
            safe,
        )
        safe = MARKDOWN_LINK_RE.sub(
            lambda m: f'<a href="{html.escape(m.group(2))}" class="chg-link">{html.escape(m.group(1))}</a>',
            safe,
        )
        html_out.append(f"<p>{safe}</p>")
    if in_list:
        html_out.append("</ul>")
    rendered = "\n".join(html_out)
    rendered = _PARENS_COMMIT_RE.sub(r"\1", rendered)
    return rendered


__all__ = ["render_lines_to_html"]
