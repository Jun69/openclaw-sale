from __future__ import annotations

import argparse
from pathlib import Path

from .generator import SOPGenerator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate SOP JSON files from tenant dialogue corpora.")
    parser.add_argument("--data-dir", required=True, help="Path to competition_data directory")
    parser.add_argument("--output-dir", required=True, help="Where generated SOP JSON files are written")
    parser.add_argument("--tenant", help="Generate one tenant only, e.g. tenant_A")
    parser.add_argument("--max-files", type=int, help="Only process the first N dialogue files per tenant")
    parser.add_argument("--enable-llm-refine", action="store_true", help="Use OpenAI-compatible API to rewrite labels/descriptions")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    data_dir = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    generator = SOPGenerator(enable_llm_refine=args.enable_llm_refine)

    if args.tenant:
        tenants = [data_dir / args.tenant]
    else:
        tenants = sorted(path for path in data_dir.iterdir() if path.is_dir())

    for tenant_dir in tenants:
        output_path = generator.generate_tenant(tenant_dir, output_dir, max_files=args.max_files)
        print(f"generated {output_path}")
    return 0
