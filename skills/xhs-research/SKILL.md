---
name: xhs-research
description: Use Xiaohongshu public notes and visible comments for traceable, Obsidian-ready research. Reuse one dedicated persistent Chrome login profile, search and read notes through the local read-only Bridge, then create bounded evidence and a decision report. Trigger for research, travel/product/lifestyle investigation, Xiaohongshu article/comment collection, or sourced Obsidian reports.
version: 1.0.0
---

# Xiaohongshu Research

This is the controlling workflow for research. The Bridge is only a reader; this skill owns question decomposition, source selection, evidence quality, privacy, counterevidence, and the final Obsidian artifact.

## Scope and Safety

- Use only `scripts/launch_research_browser.sh`, which starts a dedicated persistent profile at `~/.codex/browser-profiles/xiaohongshu-research`. Never use daily Chrome.
- The user completes login, SMS, QR, CAPTCHA, or other verification personally in the visible research browser. Never request, type, store, inspect, or export credentials, cookies, QR tokens, or private messages.
- Allowed CLI calls for research: `check-login`, `search-feeds`, `get-feed-detail`. Do not use publishing, drafts, comments, replies, likes, favorites, user-profile, risk, netlog, diagnostics, or cookie commands.
- Read public content visible through normal site interaction. Do not bypass controls, bulk crawl, scrape full comment threads, or automate repeated scrolling.
- Keep comments anonymous. Store only decision-relevant themes, never nicknames, IDs, exact addresses, order data, or raw API payloads.

## Start the Research Browser

```bash
./scripts/launch_research_browser.sh
export XHS_RESEARCH_PROFILE="$HOME/.codex/browser-profiles/xiaohongshu-research"
export XHS_BRIDGE_EXTENSION_DIR="$(pwd)/extension"
uv run python scripts/cli.py check-login
```

If logged out, ask the user to log in in that same browser. Do not initiate an automated login flow.

## Workflow

1. Write the decision map into `brief.md`: scope, dates, origin, people, budget, decision modules, and what must be externally verified.
2. Create an Obsidian project:

```bash
python scripts/research_store.py init --root "/absolute/vault" --slug "topic-slug" --title "调研标题"
```

3. Search 3-5 purposeful keyword clusters: decision, logistics, cost, counterexample, and fresh signals. Use 2-4 variants per cluster.
4. Call `search-feeds`, inspect results, then open only relevant notes:

```bash
uv run python scripts/cli.py search-feeds --keyword "关键词" --sort-by "最新" --note-type "图文"
uv run python scripts/cli.py get-feed-detail --feed-id "<id>" --xsec-token "<token>" --max-comment-items 30
```

5. Work in batches of at most three detail reads, pause, and decide whether new notes add a new decision signal. Do not use `--load-all-comments` by default.
6. Record each opened note in `evidence.md`: title, direct URL, author posture, concise claim, source date, evidence grade, and limitation. Record only 2-4 anonymous comment themes for each high-signal thread.
7. Seek disconfirming evidence. External sources are mandatory for volatile facts such as price, entry rules, weather, schedules, opening status, cancellation, and safety.
8. Draft an actionable report with conclusion, alternatives, counterevidence, booking/decision rules, links, and a visible limitations section. Validate before delivery:

```bash
python scripts/research_store.py validate --project "/absolute/vault/资料库/小红书调研/topic-slug" --deep
```

Use `--deep` only when the project has 12 opened notes, comment coverage from 5 notes, and 8 comment themes. Otherwise disclose it as a targeted or initial sample.
