#!/usr/bin/env python3
"""
Smart GitHub Profile Auto-Updater for @sahil0017.
Fetches live repository telemetry & recent commit activity from the GitHub API,
generates an animated SVG dashboard (assets/telemetry.svg), and refreshes the
LIVE_ACTIVITY section in README.md.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

USERNAME = os.environ.get("GITHUB_USERNAME", "sahil0017")
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
ROOT = Path(__file__).resolve().parent.parent

LANG_COLORS = {
    "Go": "#00ADD8",
    "TypeScript": "#3178C6",
    "Python": "#3572A5",
    "Java": "#ED8B00",
    "Swift": "#F05138",
    "C": "#64748B",
    "JavaScript": "#F1E05A",
    "Dart": "#00B4AB",
    "Shell": "#34D399",
    "HTML": "#E34C26",
    "CSS": "#818CF8",
    "Dockerfile": "#38BDF8",
}


def gh_get(url: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "sahil0017-profile-updater",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def truncate(text: str, limit: int = 72) -> str:
    clean = " ".join(text.strip().splitlines()[:1])
    if len(clean) <= limit:
        return clean
    return clean[: limit - 1].rstrip() + "…"


def build_telemetry_svg(
    repo_count: int,
    total_stars: int,
    lang_percentages: list[tuple[str, float]],
    latest_repo: str,
    latest_date: str,
    synced_utc: str,
) -> str:
    bar_rows = []
    y_start = 66
    row_gap = 34
    max_bar_width = 390

    for idx, (lang, pct) in enumerate(lang_percentages[:5]):
        y = y_start + idx * row_gap
        color = LANG_COLORS.get(lang, "#38BDF8")
        bar_w = max(8.0, round((pct / 100.0) * max_bar_width, 1))
        delay = round(0.15 * idx, 2)
        bar_rows.append(
            f"""    <g transform="translate(620, {y})">
      <circle cx="5" cy="7" r="4.5" fill="{color}"/>
      <text x="18" y="11" fill="#E2E8F0" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="13" font-weight="600">{html.escape(lang)}</text>
      <text x="530" y="11" text-anchor="end" fill="#94A3B8" font-family="ui-monospace, SFMono-Regular, monospace" font-size="12">{pct:.1f}%</text>
      <rect x="125" y="2" width="{max_bar_width}" height="10" rx="5" fill="#1E293B"/>
      <rect x="125" y="2" width="{bar_w}" height="10" rx="5" fill="{color}">
        <animate attributeName="width" from="0" to="{bar_w}" dur="1.1s" begin="{delay}s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1"/>
      </rect>
    </g>"""
        )

    bars_markup = "\n".join(bar_rows)

    return f"""<svg width="1200" height="260" viewBox="0 0 1200 260" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="tBg" x1="0" y1="0" x2="1200" y2="260" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#080D18"/>
      <stop offset="100%" stop-color="#0E1729"/>
    </linearGradient>
  </defs>

  <style>
    .sync-pulse {{
      animation: sPulse 2.4s ease-out infinite;
      transform-origin: center;
      transform-box: fill-box;
    }}
    @keyframes sPulse {{
      0% {{ transform: scale(1); opacity: 0.9; }}
      100% {{ transform: scale(2.3); opacity: 0; }}
    }}
  </style>

  <rect width="1200" height="260" rx="14" fill="url(#tBg)" stroke="#1E293B" stroke-width="1.5"/>

  <!-- Left Panel: Live Metrics -->
  <g transform="translate(36, 28)">
    <circle cx="8" cy="8" r="4" fill="#34D399" class="sync-pulse"/>
    <circle cx="8" cy="8" r="3.5" fill="#34D399"/>
    <text x="22" y="12" fill="#94A3B8" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11.5" font-weight="600" letter-spacing="0.9">LIVE GITHUB TELEMETRY · AUTO-SYNCED</text>

    <!-- Metric Cards 2x2 -->
    <g transform="translate(0, 32)">
      <rect width="252" height="72" rx="10" fill="#0F172A" stroke="#1E293B" stroke-width="1"/>
      <text x="16" y="26" fill="#64748B" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11">PUBLIC SYSTEMS</text>
      <text x="16" y="55" fill="#F8FAFC" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="26" font-weight="700">{repo_count}</text>
      <text x="64" y="54" fill="#38BDF8" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11">curated repos</text>
    </g>

    <g transform="translate(268, 32)">
      <rect width="252" height="72" rx="10" fill="#0F172A" stroke="#1E293B" stroke-width="1"/>
      <text x="16" y="26" fill="#64748B" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11">TOTAL STARS</text>
      <text x="16" y="55" fill="#F8FAFC" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="26" font-weight="700">{total_stars}</text>
      <text x="64" y="54" fill="#FBBF24" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11">across portfolio</text>
    </g>

    <g transform="translate(0, 118)">
      <rect width="252" height="72" rx="10" fill="#0F172A" stroke="#1E293B" stroke-width="1"/>
      <text x="16" y="26" fill="#64748B" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11">LATEST ACTIVE SYSTEM</text>
      <text x="16" y="54" fill="#34D399" font-family="ui-monospace, SFMono-Regular, monospace" font-size="17" font-weight="700">{html.escape(truncate(latest_repo, 20))}</text>
    </g>

    <g transform="translate(268, 118)">
      <rect width="252" height="72" rx="10" fill="#0F172A" stroke="#1E293B" stroke-width="1"/>
      <text x="16" y="26" fill="#64748B" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11">LAST PUSH (UTC)</text>
      <text x="16" y="54" fill="#E2E8F0" font-family="ui-monospace, SFMono-Regular, monospace" font-size="16" font-weight="600">{html.escape(latest_date)}</text>
    </g>
  </g>

  <!-- Vertical Divider -->
  <line x1="588" y1="28" x2="588" y2="226" stroke="#1E293B" stroke-width="1.2"/>

  <!-- Right Panel: Animated Language Distribution -->
  <text x="620" y="40" fill="#94A3B8" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11.5" font-weight="600" letter-spacing="0.9">CODEBASE LANGUAGE DISTRIBUTION (LIVE)</text>
{bars_markup}

  <!-- Footer -->
  <text x="1164" y="246" text-anchor="end" fill="#475569" font-family="ui-monospace, SFMono-Regular, monospace" font-size="10.5">Synced via GitHub Actions · {html.escape(synced_utc)}</text>
</svg>
"""


def build_live_activity_md(recent_items: list[dict], synced_utc: str) -> str:
    lines = [
        "| System | Stack | Latest Commit | Updated |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for item in recent_items:
        repo_link = f"**[{item['name']}]({item['url']})**"
        lang = f"`{item['lang']}`" if item["lang"] else "`Multi`"
        commit_msg = item["commit"].replace("|", "\\|")
        date_str = f"`{item['date']}`"
        lines.append(f"| {repo_link} | {lang} | {commit_msg} | {date_str} |")
    lines.append("")
    lines.append(
        f"<sub>Auto-updated every 6 hours via GitHub Actions · Last sync: `{synced_utc}`</sub>"
    )
    return "\n".join(lines)


def main() -> int:
    repos = gh_get(
        f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner&sort=pushed"
    )
    portfolio = [
        r
        for r in repos
        if not r.get("fork")
        and not r.get("private")
        and r.get("name", "").lower() != USERNAME.lower()
    ]

    total_stars = sum(int(r.get("stargazers_count", 0)) for r in portfolio)
    repo_count = len(portfolio)

    # Aggregate real language bytes across portfolio repos
    lang_totals: dict[str, int] = {}
    for r in portfolio:
        try:
            langs = gh_get(r["languages_url"])
            for k, v in langs.items():
                lang_totals[k] = lang_totals.get(k, 0) + int(v)
        except urllib.error.URLError:
            primary = r.get("language")
            if primary:
                lang_totals[primary] = lang_totals.get(primary, 0) + 1

    total_bytes = sum(lang_totals.values()) or 1
    lang_percentages = sorted(
        [(k, (v / total_bytes) * 100.0) for k, v in lang_totals.items()],
        key=lambda x: x[1],
        reverse=True,
    )

    # Fetch latest commit for top 5 most recently pushed repos
    recent_items: list[dict] = []
    for r in portfolio[:5]:
        name = r["name"]
        commit_msg = r.get("description") or "Recent update"
        try:
            commits = gh_get(
                f"https://api.github.com/repos/{USERNAME}/{name}/commits?per_page=1"
            )
            if commits and isinstance(commits, list):
                commit_msg = truncate(commits[0]["commit"]["message"], 64)
        except urllib.error.URLError:
            pass
        pushed = (r.get("pushed_at") or "")[:10]
        recent_items.append(
            {
                "name": name,
                "url": r["html_url"],
                "lang": r.get("language") or "Multi",
                "commit": commit_msg,
                "date": pushed,
            }
        )

    now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    latest_repo = portfolio[0]["name"] if portfolio else "Systera"
    latest_date = (portfolio[0].get("pushed_at") or now_utc)[:10] if portfolio else now_utc[:10]

    # Write animated telemetry SVG
    svg_path = ROOT / "assets" / "telemetry.svg"
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text(
        build_telemetry_svg(
            repo_count=repo_count,
            total_stars=total_stars,
            lang_percentages=lang_percentages,
            latest_repo=latest_repo,
            latest_date=latest_date,
            synced_utc=now_utc,
        ),
        encoding="utf-8",
    )

    # Update LIVE_ACTIVITY block in README.md
    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    block = build_live_activity_md(recent_items, now_utc)
    pattern = re.compile(
        r"<!-- LIVE_ACTIVITY:START -->.*?<!-- LIVE_ACTIVITY:END -->",
        re.DOTALL,
    )
    replacement = f"<!-- LIVE_ACTIVITY:START -->\n{block}\n<!-- LIVE_ACTIVITY:END -->"
    if not pattern.search(readme):
        raise RuntimeError("Missing LIVE_ACTIVITY markers in README.md")
    readme_path.write_text(pattern.sub(replacement, readme), encoding="utf-8")
    print(f"Telemetry SVG & LIVE_ACTIVITY updated ({repo_count} repos, {total_stars} stars).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
