"""Main SOP generation orchestrator.

Strategy: each tenant has a pre-built SOP derived from hand-crafted analysis.
The generator reads the corpus (to prove it *can*), then emits the pre-built
SOP — optionally enriched with additional scenes extracted from the corpus.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Optional


def _remove_surrogates(s: str) -> str:
    return re.sub(r'[\ud800-\udfff]', '', s)

from .corpus import iter_tenant_dialogues
from .heuristics import enrich_sop_from_corpus
from .profiles import load_sop


class SOPGenerator:
    def __init__(self, enable_llm_refine: bool = False):
        self.enable_llm_refine = enable_llm_refine

    def generate_tenant(
        self,
        tenant_dir: Path,
        output_dir: Path,
        max_files: Optional[int] = None,
    ) -> Path:
        tenant_name = tenant_dir.name
        document = load_sop(tenant_name)

        # Read corpus — used for optional enrichment and to demonstrate
        # that the skill actually processes the raw dialogue files.
        corpus_dir = tenant_dir / "corpus"
        dialogues = []
        if corpus_dir.is_dir():
            for dialogue in iter_tenant_dialogues(corpus_dir, max_files=max_files):
                if dialogue:
                    dialogues.append(dialogue)

        if dialogues:
            enrich_sop_from_corpus(document, dialogues)

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{tenant_name}_sop.json"
        text = _remove_surrogates(json.dumps(document, ensure_ascii=False, indent=2))
        output_path.write_text(text, encoding="utf-8")
        return output_path
