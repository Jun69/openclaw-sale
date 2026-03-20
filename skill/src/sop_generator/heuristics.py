"""Corpus-based enrichment for pre-built SOP documents.

The pre-built SOPs already contain high-quality scenes from hand-crafted
analysis.  This module optionally scans the corpus to add supplementary
话术模板 (script templates) where they are missing.
"""
from __future__ import annotations

from collections import Counter
from typing import Dict, List

from .corpus import ROLE_CUSTOMER, ROLE_SALES, Utterance


def enrich_sop_from_corpus(
    document: Dict, dialogues: List[List[Utterance]]
) -> None:
    """Add representative 话术模板 to subtasks that lack them."""
    tasks = document.get("任务树", [])
    # Build a keyword-to-task index from task names
    for task in tasks:
        for subtask in task.get("子任务", []):
            templates = subtask.get("话术模板")
            if templates:
                continue
            # Try to find matching sales utterances from corpus
            subtask_name = subtask.get("子任务主题", "")
            task_name = task.get("任务主题", "")
            keywords = _extract_keywords(task_name, subtask_name)
            if not keywords:
                continue
            matched = _find_matching_templates(dialogues, keywords)
            if matched:
                subtask["话术模板"] = matched[:4]


def _extract_keywords(task_name: str, subtask_name: str) -> List[str]:
    """Extract a few keywords from task/subtask names for fuzzy matching."""
    combined = task_name + subtask_name
    # Simple: use 2-char substrings that are likely meaningful
    keywords = []
    for word in (task_name, subtask_name):
        clean = word.replace(".", "").replace("（", "").replace("）", "")
        if len(clean) >= 2:
            keywords.append(clean[:4])
    return keywords


def _find_matching_templates(
    dialogues: List[List[Utterance]], keywords: List[str], limit: int = 4
) -> List[str]:
    """Find frequent sales utterances matching any keyword."""
    counter: Counter = Counter()
    for dialogue in dialogues:
        for utt in dialogue:
            if utt.role != ROLE_SALES:
                continue
            text = utt.text.strip()
            if len(text) < 6:
                continue
            if any(kw in text for kw in keywords):
                counter[text] += 1
    return [text for text, _ in counter.most_common(limit)]
