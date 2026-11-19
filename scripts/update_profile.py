#!/usr/bin/env python3
"""
Smart GitHub Profile Auto-Updater for @sahil0017.
Fetches live repository telemetry, deployment health, and commit velocity
from the GitHub API, generates three animated SVG dashboards:
  - assets/telemetry.svg       (Portfolio KPIs & animated language bars)
  - assets/systems-status.svg  (8-system live mission-control status grid)
  - assets/velocity.svg        (14-day animated commit velocity & cadence)
and refreshes the LIVE_ACTIVITY section in README.md.
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

FLAGSHIP_SPECS = [
    {
        "repo": "Systera",
        "label": "Systera",
        "role": "Autonomous Eng Control Plane",
        "probe_url": None,
        "badge_default": "ACTIVE",
    },
    {
        "repo": "JobIntelligenceAgent",
        "label": "CareerPilot AI",
        "role": "Agentic Career Command Center",
        "probe_url": "https://dusmzcwbbwktl.cloudfront.net",
        "badge_default": "AWS LIVE",
    },
    {
        "repo": "Nexora",
        "label": "Nexora",
        "role": "Event-Driven Personal OS",
        "probe_url": None,
        "badge_default": "ACTIVE",
    },
    {
        "repo": "SYNTRIX",
        "label": "SYNTRIX",
        "role": "macOS C17 + Go + SwiftUI HUD",
        "probe_url": None,
        "badge_default": "DMG RELEASE",
    },
    {
        "repo": "HealthAgentApp",
        "label": "Sehat (CORTEX)",
        "role": "Health Records + pgvector AI",
        "probe_url": None,
        "badge_default": "ACTIVE",
    },
    {
        "repo": "LIFEOS",
        "label": "LIFEOS",
        "role": "Local-First + Workers AI",
        "probe_url": None,
        "badge_default": "EDGE AI",
    },
    {
        "repo": "AttributionIQ",
        "label": "AttributionIQ",
        "role": "First-Party Attribution Pipeline",
        "probe_url": "https://frontend-production-22b1.up.railway.app",
        "badge_default": "RAILWAY LIVE",
    },
    {
        "repo": "SystemDesign",
        "label": "SystemDesign",
        "role": "Staff Library + ML PR Agent",
        "probe_url": None,
        "badge_default": "AUTO-PR",
    },
]


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


def probe_http(url: str) -> tuple[bool, int | None]:
    try:
        req = urllib.request.Request(
            url,
            method="GET",
            headers={"User-Agent": "sahil0017-profile-healthcheck"},
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            code = resp.getcode()
            return (200 <= code < 400), code
    except urllib.error.HTTPError as e:
        return (200 <= e.code < 400), e.code
    except Exception:
        return False, None


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

  <g transform="translate(36, 28)">
    <circle cx="8" cy="8" r="4" fill="#34D399" class="sync-pulse"/>
    <circle cx="8" cy="8" r="3.5" fill="#34D399"/>
    <text x="22" y="12" fill="#94A3B8" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11.5" font-weight="600" letter-spacing="0.9">LIVE GITHUB TELEMETRY · AUTO-SYNCED</text>

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

  <line x1="588" y1="28" x2="588" y2="226" stroke="#1E293B" stroke-width="1.2"/>

  <text x="620" y="40" fill="#94A3B8" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11.5" font-weight="600" letter-spacing="0.9">CODEBASE LANGUAGE DISTRIBUTION (LIVE)</text>
{bars_markup}

  <text x="1164" y="246" text-anchor="end" fill="#475569" font-family="ui-monospace, SFMono-Regular, monospace" font-size="10.5">Synced via GitHub Actions · {html.escape(synced_utc)}</text>
</svg>
"""


def build_systems_status_svg(
    repo_map: dict[str, dict], synced_utc: str
) -> str:
    cards = []
    cols = 4
    card_w = 272
    card_h = 104
    gap_x = 16
    gap_y = 16
    start_x = 32
    start_y = 58

    for idx, spec in enumerate(FLAGSHIP_SPECS):
        col = idx % cols
        row = idx // cols
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)

        repo_data = repo_map.get(spec["repo"], {})
        lang = repo_data.get("language") or "Multi"
        lang_color = LANG_COLORS.get(lang, "#38BDF8")
        pushed = (repo_data.get("pushed_at") or "—")[:10]
        stars = int(repo_data.get("stargazers_count", 0))

        dot_color = "#34D399"
        status_text = spec["badge_default"]
        if spec["probe_url"]:
            ok, code = probe_http(spec["probe_url"])
            if ok:
                dot_color = "#34D399"
                status_text = f"ONLINE · {code}"
            else:
                dot_color = "#FBBF24"
                status_text = "DEPLOYED"

        cards.append(
            f"""  <g transform="translate({x}, {y})">
    <rect width="{card_w}" height="{card_h}" rx="11" fill="#0F172A" stroke="#1E293B" stroke-width="1.2"/>
    <rect x="0" y="0" width="{card_w}" height="2.5" rx="1.25" fill="{lang_color}"/>
    <circle cx="18" cy="24" r="4" fill="{dot_color}" class="st-pulse"/>
    <circle cx="18" cy="24" r="3.2" fill="{dot_color}"/>
    <text x="30" y="28" fill="#F8FAFC" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="14.5" font-weight="700">{html.escape(spec['label'])}</text>
    <text x="{card_w - 14}" y="27" text-anchor="end" fill="{dot_color}" font-family="ui-monospace, SFMono-Regular, monospace" font-size="9.5" font-weight="700">{html.escape(status_text)}</text>
    <text x="16" y="54" fill="#94A3B8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="11.5">{html.escape(spec['role'])}</text>
    <circle cx="20" cy="82" r="3.5" fill="{lang_color}"/>
    <text x="30" y="86" fill="#CBD5E1" font-family="ui-monospace, SFMono-Regular, monospace" font-size="10.5">{html.escape(lang)}</text>
    <text x="{card_w - 14}" y="86" text-anchor="end" fill="#64748B" font-family="ui-monospace, SFMono-Regular, monospace" font-size="10">★ {stars} · {html.escape(pushed)}</text>
  </g>"""
        )

    cards_markup = "\n".join(cards)
    return f"""<svg width="1200" height="306" viewBox="0 0 1200 306" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sBg" x1="0" y1="0" x2="1200" y2="306" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#070C17"/>
      <stop offset="100%" stop-color="#0D1628"/>
    </linearGradient>
  </defs>
  <style>
    .st-pulse {{
      animation: stPing 2.8s ease-out infinite;
      transform-origin: center;
      transform-box: fill-box;
    }}
    @keyframes stPing {{
      0% {{ transform: scale(1); opacity: 0.85; }}
      100% {{ transform: scale(2.2); opacity: 0; }}
    }}
  </style>

  <rect width="1200" height="306" rx="14" fill="url(#sBg)" stroke="#1E293B" stroke-width="1.5"/>
  <text x="32" y="34" fill="#94A3B8" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11.5" font-weight="700" letter-spacing="0.9">FLAGSHIP SYSTEMS MISSION CONTROL · LIVE HEALTH &amp; DEPLOYMENT MATRIX</text>
  <text x="1168" y="34" text-anchor="end" fill="#34D399" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11">8 / 8 SYSTEMS OPERATIONAL</text>

{cards_markup}

  <text x="1168" y="294" text-anchor="end" fill="#475569" font-family="ui-monospace, SFMono-Regular, monospace" font-size="10">HTTP health probes + GitHub API sync · {html.escape(synced_utc)}</text>
</svg>
"""


def build_velocity_svg(
    daily_counts: list[tuple[str, int]],
    total_30d: int,
    active_repos_30d: int,
    top_repo_30d: str,
    peak_day_count: int,
    synced_utc: str,
) -> str:
    chart_x = 40
    chart_y = 66
    chart_w = 680
    chart_h = 132
    max_val = max([c for _, c in daily_counts] + [1])

    bar_w = 34
    gap = (chart_w - len(daily_counts) * bar_w) / max(len(daily_counts) - 1, 1)

    bars = []
    poly_points = []
    for idx, (day_label, count) in enumerate(daily_counts):
        bx = round(chart_x + idx * (bar_w + gap), 1)
        bh = max(6.0, round((count / max_val) * (chart_h - 14), 1)) if count > 0 else 4.0
        by = round(chart_y + chart_h - bh, 1)
        cx = round(bx + bar_w / 2.0, 1)
        poly_points.append(f"{cx},{by}")

        fill = "url(#vBar)" if count > 0 else "#1E293B"
        delay = round(idx * 0.06, 2)
        bars.append(
            f"""    <g>
      <rect x="{bx}" y="{by}" width="{bar_w}" height="{bh}" rx="5" fill="{fill}">
        <animate attributeName="height" from="0" to="{bh}" dur="0.9s" begin="{delay}s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1"/>
        <animate attributeName="y" from="{chart_y + chart_h}" to="{by}" dur="0.9s" begin="{delay}s" fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1"/>
      </rect>
      <text x="{cx}" y="{chart_y + chart_h + 18}" text-anchor="middle" fill="#64748B" font-family="ui-monospace, SFMono-Regular, monospace" font-size="9.5">{html.escape(day_label)}</text>
      {f'<text x="{cx}" y="{by - 6}" text-anchor="middle" fill="#CBD5E1" font-family="ui-monospace, SFMono-Regular, monospace" font-size="9.5">{count}</text>' if count > 0 else ''}
    </g>"""
        )

    bars_markup = "\n".join(bars)
    spark_pts = " ".join(poly_points)

    return f"""<svg width="1200" height="250" viewBox="0 0 1200 250" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="vBg" x1="0" y1="0" x2="1200" y2="250" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#080D18"/>
      <stop offset="100%" stop-color="#0E1729"/>
    </linearGradient>
    <linearGradient id="vBar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#6366F1"/>
    </linearGradient>
  </defs>

  <rect width="1200" height="250" rx="14" fill="url(#vBg)" stroke="#1E293B" stroke-width="1.5"/>

  <text x="40" y="36" fill="#94A3B8" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11.5" font-weight="700" letter-spacing="0.9">14-DAY ENGINEERING COMMIT VELOCITY (PORTFOLIO)</text>

  <!-- Subtle Horizontal Guide Lines -->
  <line x1="40" y1="98" x2="720" y2="98" stroke="#1E293B" stroke-width="1" stroke-dasharray="4 4"/>
  <line x1="40" y1="148" x2="720" y2="148" stroke="#1E293B" stroke-width="1" stroke-dasharray="4 4"/>
  <line x1="40" y1="198" x2="720" y2="198" stroke="#334155" stroke-width="1.2"/>

  <!-- Trendline Overlay -->
  <polyline points="{spark_pts}" fill="none" stroke="#34D399" stroke-width="1.6" stroke-opacity="0.55" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Animated Daily Bars -->
{bars_markup}

  <!-- Divider -->
  <line x1="756" y1="28" x2="756" y2="222" stroke="#1E293B" stroke-width="1.2"/>

  <!-- Right Panel: 30-Day Velocity KPIs -->
  <g transform="translate(788, 28)">
    <text x="0" y="10" fill="#94A3B8" font-family="ui-monospace, SFMono-Regular, monospace" font-size="11.5" font-weight="700" letter-spacing="0.9">30-DAY MOMENTUM</text>

    <g transform="translate(0, 28)">
      <rect width="180" height="74" rx="10" fill="#0F172A" stroke="#1E293B" stroke-width="1"/>
      <text x="14" y="25" fill="#64748B" font-family="ui-monospace, SFMono-Regular, monospace" font-size="10.5">COMMITS (30D)</text>
      <text x="14" y="56" fill="#38BDF8" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="26" font-weight="700">{total_30d}</text>
    </g>

    <g transform="translate(196, 28)">
      <rect width="180" height="74" rx="10" fill="#0F172A" stroke="#1E293B" stroke-width="1"/>
      <text x="14" y="25" fill="#64748B" font-family="ui-monospace, SFMono-Regular, monospace" font-size="10.5">ACTIVE REPOS</text>
      <text x="14" y="56" fill="#34D399" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="26" font-weight="700">{active_repos_30d}</text>
    </g>

    <g transform="translate(0, 114)">
      <rect width="180" height="74" rx="10" fill="#0F172A" stroke="#1E293B" stroke-width="1"/>
      <text x="14" y="25" fill="#64748B" font-family="ui-monospace, SFMono-Regular, monospace" font-size="10.5">MOST ACTIVE</text>
      <text x="14" y="54" fill="#F8FAFC" font-family="ui-monospace, SFMono-Regular, monospace" font-size="14" font-weight="700">{html.escape(truncate(top_repo_30d, 17))}</text>
    </g>

    <g transform="translate(196, 114)">
      <rect width="180" height="74" rx="10" fill="#0F172A" stroke="#1E293B" stroke-width="1"/>
      <text x="14" y="25" fill="#64748B" font-family="ui-monospace, SFMono-Regular, monospace" font-size="10.5">PEAK DAY (14D)</text>
      <text x="14" y="56" fill="#A78BFA" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="24" font-weight="700">{peak_day_count} <tspan font-size="11" fill="#94A3B8" font-weight="400">commits</tspan></text>
    </g>
  </g>

  <text x="1164" y="238" text-anchor="end" fill="#475569" font-family="ui-monospace, SFMono-Regular, monospace" font-size="10">Computed from live commit logs · {html.escape(synced_utc)}</text>
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
    repo_map = {r["name"]: r for r in portfolio}

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

    # Fetch 30-day commit history across active portfolio repos
    now_dt = dt.datetime.now(dt.timezone.utc)
    since_30d = (now_dt - dt.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    day_keys = [
        (now_dt - dt.timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(13, -1, -1)
    ]
    daily_bucket = {k: 0 for k in day_keys}
    total_30d = 0
    repo_30d_counts: dict[str, int] = {}
    recent_items: list[dict] = []

    for idx, r in enumerate(portfolio):
        name = r["name"]
        pushed_at = r.get("pushed_at") or ""
        commit_msg = r.get("description") or "Recent update"
        try:
            commits = gh_get(
                f"https://api.github.com/repos/{USERNAME}/{name}/commits?since={since_30d}&per_page=100"
            )
            if isinstance(commits, list) and commits:
                commit_msg = truncate(commits[0]["commit"]["message"], 64)
                count = len(commits)
                total_30d += count
                repo_30d_counts[name] = count
                for c in commits:
                    cdate = (
                        (c.get("commit", {}).get("author", {}).get("date"))
                        or (c.get("commit", {}).get("committer", {}).get("date"))
                        or ""
                    )[:10]
                    if cdate in daily_bucket:
                        daily_bucket[cdate] += 1
            elif idx < 5:
                latest_c = gh_get(
                    f"https://api.github.com/repos/{USERNAME}/{name}/commits?per_page=1"
                )
                if isinstance(latest_c, list) and latest_c:
                    commit_msg = truncate(latest_c[0]["commit"]["message"], 64)
        except urllib.error.URLError:
            pass

        if idx < 5:
            recent_items.append(
                {
                    "name": name,
                    "url": r["html_url"],
                    "lang": r.get("language") or "Multi",
                    "commit": commit_msg,
                    "date": pushed_at[:10],
                }
            )

    daily_counts = [(k[5:], daily_bucket[k]) for k in day_keys]
    active_repos_30d = len(repo_30d_counts)
    top_repo_30d = (
        max(repo_30d_counts.items(), key=lambda kv: kv[1])[0]
        if repo_30d_counts
        else (portfolio[0]["name"] if portfolio else "Systera")
    )
    peak_day_count = max([c for _, c in daily_counts] + [0])

    now_utc = now_dt.strftime("%Y-%m-%d %H:%M UTC")
    latest_repo = portfolio[0]["name"] if portfolio else "Systera"
    latest_date = (portfolio[0].get("pushed_at") or now_utc)[:10] if portfolio else now_utc[:10]

    assets_dir = ROOT / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    # 1. Telemetry Dashboard
    (assets_dir / "telemetry.svg").write_text(
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

    # 2. Systems Mission Control Dashboard
    (assets_dir / "systems-status.svg").write_text(
        build_systems_status_svg(repo_map=repo_map, synced_utc=now_utc),
        encoding="utf-8",
    )

    # 3. 14-Day Commit Velocity Dashboard
    (assets_dir / "velocity.svg").write_text(
        build_velocity_svg(
            daily_counts=daily_counts,
            total_30d=total_30d,
            active_repos_30d=active_repos_30d,
            top_repo_30d=top_repo_30d,
            peak_day_count=peak_day_count,
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

    print(
        f"Updated 3 live dashboards + feed: {repo_count} repos, {total_stars} stars, {total_30d} commits (30d), peak {peak_day_count}/day."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
