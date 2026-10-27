#!/usr/bin/env python3
"""Generate the animated SVG cards used in the profile README.

Edit the data below, then run:  python3 assets/generate.py
"""
import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
ICONS = ROOT / "icons"
OUT = ROOT / "cards"

ROLES = [
    "Oracle APEX Engineering",
    "PL/SQL & Database Architecture",
    "Multi-Tenant SaaS Architecture",
    "Cloud & DevOps Automation",
    "AI Vector Search & RAG",
]

# (icon, value, suffix, label lines)
HIGHLIGHTS = [
    ("calendar-clock", 3, "+", ["YEARS OF ORACLE", "ENTERPRISE DELIVERY"]),
    ("badge-check", 7, "", ["ORACLE", "CERTIFICATIONS"]),
    ("monitor-smartphone", 180, "+", ["APEX SCREENS", "IN ONE PLATFORM"]),
    ("gauge", 40, "%", ["EFFICIENCY GAIN FROM", "SQL & PL/SQL TUNING"]),
]

PROJECT = [
    ("monitor", 180, "+", ["APEX", "SCREENS"]),
    ("table", 171, "+", ["TABLES"]),
    ("eye", 91, "", ["VIEWS"]),
    ("package", 100, "+", ["PL/SQL", "PACKAGES"]),
    ("zap", 174, "", ["TRIGGERS"]),
    ("search", 413, "", ["INDEXES"]),
    ("webhook", 20, "+", ["ORDS", "REST APIS"]),
]

ACCENT = "#C74634"
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Noto Sans', Helvetica, Arial, sans-serif"
THEMES = {
    "light": {"tile": "#F6F8FA", "border": "#D0D7DE", "value": "#1F2328", "label": "#59636E"},
    "dark": {"tile": "#161B22", "border": "#30363D", "value": "#F0F6FC", "label": "#9198A1"},
}


def icon_body(name):
    svg = (ICONS / f"{name}.svg").read_text()
    return re.search(r">\s*(<(?:path|circle|rect|line|polyline|polygon|ellipse).*)</svg>", svg, re.S).group(1)


def count_frames(target, start, duration, steps=18):
    """Ease-out count-up frames as (value, begin, length) tuples, excluding the final value."""
    frames, last = [], None
    for k in range(steps):
        value = round(target * (1 - (1 - k / steps) ** 3))
        if value != last and value != target:
            frames.append([value, start + duration * k / steps])
            last = value
    return [(v, t, (frames[i + 1][1] if i + 1 < len(frames) else start + duration) - t)
            for i, (v, t) in enumerate(frames)]


def stat_card(items, theme, width=880, gap=16, height=160, value_size=30):
    c = THEMES[theme]
    n = len(items)
    tile_w = (width - gap * (n - 1)) / n
    parts = []
    for i, (icon, value, suffix, label) in enumerate(items):
        x = i * (tile_w + gap)
        cx = x + tile_w / 2
        delay = 0.15 + i * 0.12
        count_start, count_len = delay + 0.25, 1.1
        frames = count_frames(value, count_start, count_len)
        numbers = "".join(
            f'<text class="v f" x="{cx:.1f}" y="92" style="animation-delay:{t:.3f}s;animation-duration:{d:.3f}s">{v}{escape(suffix)}</text>'
            for v, t, d in frames
        )
        final = f'<text class="v" x="{cx:.1f}" y="92" style="animation:hide {count_start + count_len:.3f}s steps(1)">{value}{escape(suffix)}</text>'
        labels = "".join(
            f'<text class="l" x="{cx:.1f}" y="{124 + j * 15}">{escape(line)}</text>' for j, line in enumerate(label)
        )
        parts.append(
            f'<g class="tile" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{x + 0.5:.1f}" y="8.5" width="{tile_w - 1:.1f}" height="{height - 17}" rx="10" fill="{c["tile"]}" stroke="{c["border"]}"/>'
            f'<g transform="translate({cx - 12:.1f} 24)" fill="none" stroke="{ACCENT}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icon_body(icon)}</g>'
            f"{numbers}{final}"
            f'<rect class="bar" x="{cx - 14:.1f}" y="103" width="28" height="2.5" rx="1.25" fill="{ACCENT}" style="animation-delay:{count_start + count_len - 0.2:.2f}s"/>'
            f"{labels}</g>"
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
text {{ font-family: {FONT}; text-anchor: middle; }}
.v {{ font-size: {value_size}px; font-weight: 700; fill: {c["value"]}; }}
.l {{ font-size: 10.5px; font-weight: 600; letter-spacing: 1px; fill: {c["label"]}; }}
.f {{ opacity: 0; animation-name: show; animation-timing-function: steps(1); }}
.tile {{ animation: rise .7s cubic-bezier(.2,.7,.2,1) both; }}
.bar {{ transform-box: fill-box; transform-origin: center; animation: grow .6s ease-out both; }}
@keyframes show {{ from, to {{ opacity: 1; }} }}
@keyframes hide {{ from, to {{ opacity: 0; }} }}
@keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
{"".join(parts)}
</svg>
"""


def roles_card(width=880, height=64, slot=2.6):
    n = len(ROLES)
    cycle = slot * n
    p = 100 / n
    words = "".join(
        f'<text class="r" x="{width / 2}" y="32" style="animation-delay:{i * slot:.1f}s;{"opacity:1" if i == 0 else ""}">{escape(r)}</text>'
        for i, r in enumerate(ROLES)
    )
    dots_x0 = width / 2 - (n - 1) * 7
    dots = "".join(f'<circle cx="{dots_x0 + i * 14}" cy="54" r="3" fill="#8B949E" opacity=".45"/>' for i in range(n))
    active = "".join(
        f'<circle class="d" cx="{dots_x0 + i * 14}" cy="54" r="3" fill="{ACCENT}" style="animation-delay:{i * slot:.1f}s;{"opacity:1" if i == 0 else ""}"/>'
        for i in range(n)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
.r {{ font-family: {FONT}; font-size: 21px; font-weight: 600; letter-spacing: .3px; fill: {ACCENT}; text-anchor: middle; opacity: 0;
      animation: role {cycle:.1f}s cubic-bezier(.2,.7,.2,1) infinite backwards; }}
.d {{ opacity: 0; animation: dot {cycle:.1f}s linear infinite; }}
@keyframes role {{
  0% {{ opacity: 0; transform: translateY(12px); }}
  {p * 0.15:.2f}% {{ opacity: 1; transform: none; }}
  {p * 0.85:.2f}% {{ opacity: 1; transform: none; }}
  {p:.2f}% {{ opacity: 0; transform: translateY(-12px); }}
  100% {{ opacity: 0; transform: translateY(-12px); }}
}}
@keyframes dot {{ 0%, {p:.2f}% {{ opacity: 1; }} {p + 0.01:.2f}%, 100% {{ opacity: 0; }} }}
@media (prefers-reduced-motion: reduce) {{ .r, .d {{ animation: none; }} }}
</style>
{words}{dots}{active}
</svg>
"""


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "roles.svg").write_text(roles_card())
    for theme in THEMES:
        (OUT / f"highlights-{theme}.svg").write_text(stat_card(HIGHLIGHTS, theme))
        (OUT / f"project-{theme}.svg").write_text(stat_card(PROJECT, theme, gap=12, height=160, value_size=26))
    print("wrote", ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
