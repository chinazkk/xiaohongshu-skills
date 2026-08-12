---
name: xiaohongshu-research-bridge
description: Use a dedicated persistent Chrome login profile to perform bounded, public Xiaohongshu research. Read normal search results and visible note/comments through a local bridge, then create anonymous, traceable Obsidian evidence and reports. Trigger for Xiaohongshu research, travel/product/lifestyle investigation, comment synthesis, or Obsidian-ready sourced reports.
version: 1.0.0
---

# Xiaohongshu Research Bridge

This repository is configured for **read-only research**. The controlling workflow is [`skills/xhs-research/SKILL.md`](skills/xhs-research/SKILL.md).

## Allowed workflow

1. Start `scripts/launch_research_browser.sh` to reuse the dedicated persistent profile.
2. The user completes any login or verification in that visible browser.
3. Use only `check-login`, `search-feeds`, and `get-feed-detail` to read normally visible public content.
4. Use `scripts/research_store.py` to create and validate an Obsidian evidence workspace.
5. Build a bounded, anonymous evidence set with counterexamples and external checks for volatile facts.

## Never use for research

- Posting, drafts, comments, replies, likes, favorites, or account operations.
- Cookie export, private-message access, user-profile collection, full comment exports, or bulk crawling.
- Risk-control analysis, NetLog, diagnostics, platform-control bypasses, or evasion of detection.

The user controls login. The research agent controls problem decomposition, source quality, evidence storage, anonymization, and the final decision report.
