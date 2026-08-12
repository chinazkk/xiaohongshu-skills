#!/usr/bin/env python3
"""Create and validate bounded, Obsidian-ready Xiaohongshu research workspaces."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


EVIDENCE_HEADER = """# 证据台账

> 仅保存公开可见且与决策相关的内容。评论必须匿名概括，不保存完整评论、账号信息或访问令牌。

| ID | 类型 | 主题/主张 | 证据摘要 | 来源链接 | 采集日 | 证据等级 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
"""


def safe_slug(value: str) -> str:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,62}", value):
        raise ValueError("slug must use lowercase letters, digits, and hyphens")
    return value


def init_project(root: Path, slug: str, title: str) -> Path:
    project = root / "资料库" / "小红书调研" / safe_slug(slug)
    if project.exists():
        raise FileExistsError(f"project already exists: {project}")
    (project / "screenshots").mkdir(parents=True)
    today = date.today().isoformat()
    (project / "brief.md").write_text(
        f"# {title} - 研究简报\n\n- 决策问题：\n- 目标人群：\n- 时间与预算：\n- 必答问题：\n- 不采集范围：私信、账号数据、完整评论导出、Cookie、互动和发布。\n",
        encoding="utf-8",
    )
    (project / "evidence.md").write_text(EVIDENCE_HEADER, encoding="utf-8")
    (project / "report.md").write_text(
        f"---\ntitle: {title}\ncreated: {today}\nupdated: {today}\ntags:\n  - 小红书调研\n研究类型: 主题研究\n主题: 待填写\n市场: 不适用\n主体: 待填写\n状态: 进行中\n资料等级: 混合\n下次复核日: 待填写\n---\n\n# {title}\n\n> [!abstract] 结论\n> 待基于证据台账填写；完成后每项核心判断都应带 `【XHS-编号】`。\n\n## 研究问题与样本\n\n## 核心发现\n\n## 决策建议\n\n## 反证与风险\n\n## 来源索引\n\n- 待在完成证据采集后，按 `【XHS-编号】 [来源标题](https://...)` 列出所有来源。\n\n## 来源与证据边界\n",
        encoding="utf-8",
    )
    return project


def validate(project: Path, deep: bool) -> list[str]:
    errors = []
    required = [project / name for name in ("brief.md", "evidence.md", "report.md")]
    errors.extend(f"missing {path.name}" for path in required if not path.is_file())
    if errors:
        return errors
    evidence = (project / "evidence.md").read_text(encoding="utf-8")
    report = (project / "report.md").read_text(encoding="utf-8")
    evidence_urls = set(re.findall(r"https?://[^)\s|]+", evidence))
    evidence_ids = set(re.findall(r"^\|\s*(XHS-[A-Za-z0-9-]+)\s*\|", evidence, re.M))
    report_urls = set(re.findall(r"https?://[^)\s|]+", report))
    report_ids = set(re.findall(r"【(XHS-[A-Za-z0-9-]+)】", report))
    if "| ID |" not in evidence or not evidence_urls:
        errors.append("evidence.md needs a table and at least one source URL")
    for heading in ("## 反证与风险", "## 来源索引", "## 来源与证据边界"):
        if heading not in report:
            errors.append(f"report.md is missing {heading}")
    if evidence_ids and not report_ids:
        errors.append("report.md needs inline evidence IDs such as 【XHS-01】")
    unknown_ids = report_ids - evidence_ids
    if unknown_ids:
        errors.append(f"report.md cites IDs absent from evidence.md: {', '.join(sorted(unknown_ids))}")
    missing_urls = evidence_urls - report_urls
    if missing_urls:
        errors.append(f"report.md source index is missing {len(missing_urls)} evidence URL(s)")
    if deep:
        notes = re.findall(r"^\|\s*XHS-(?!C)[A-Za-z0-9-]+\s*\|\s*笔记\s*\|", evidence, re.M)
        comment_urls = set(re.findall(r"^\|\s*XHS-C[A-Za-z0-9-]+\s*\|\s*评论概括\s*\|.*?\]\((https?://[^)]+)\)", evidence, re.M))
        comments = re.findall(r"^\|\s*XHS-C[A-Za-z0-9-]+\s*\|\s*评论概括\s*\|", evidence, re.M)
        if len(notes) < 12:
            errors.append(f"deep validation requires 12 opened notes; found {len(notes)}")
        if len(comment_urls) < 5:
            errors.append(f"deep validation requires comments from 5 notes; found {len(comment_urls)}")
        if len(comments) < 8:
            errors.append(f"deep validation requires 8 comment themes; found {len(comments)}")
        if "精读" not in report or "评论覆盖" not in report:
            errors.append("deep report must disclose 精读 and 评论覆盖")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--root", required=True, type=Path)
    init.add_argument("--slug", required=True)
    init.add_argument("--title", required=True)
    check = commands.add_parser("validate")
    check.add_argument("--project", required=True, type=Path)
    check.add_argument("--deep", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "init":
            print(init_project(args.root.expanduser().resolve(), args.slug, args.title))
            return 0
        errors = validate(args.project.expanduser().resolve(), args.deep)
        if errors:
            print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
            return 1
        print("Research workspace validation passed")
        return 0
    except (ValueError, FileExistsError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
