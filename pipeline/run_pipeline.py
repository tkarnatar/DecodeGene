"""一键数据摄取与通俗化标注管道.

    用法::

    python pipeline/run_pipeline.py            # 生成离线样本知识库
    python pipeline/run_pipeline.py --live     # 额外调用 Open Targets / ClinVar 实时 API
    python pipeline/run_pipeline.py --bulk     # 从 ClinVar 全量 dump 批量导入 1000+ 基因
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from rich.console import Console

from .apis.clinvar import fetch_many_genes
from .apis.clinvar_bulk import download_variant_summary, parse_variant_summary
from .apis.opentargets import fetch_many_targets
from .parsers.metaphors import EXTRA_ASSOCIATIONS

# 确保 Windows 控制台以 UTF-8 输出中文/emoji，避免 cp950 编码错误
for _stream in (sys.stdout, sys.stderr):
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

console = Console()

# Ensembl gene ids used for live Open Targets enrichment
ENSEMBL_IDS = {
    "BRCA1": "ENSG00000012048",
    "BRCA2": "ENSG00000139618",
    "TP53": "ENSG00000141510",
    "APOE": "ENSG00000130203",
    "EGFR": "ENSG00000146648",
    "CFTR": "ENSG00000001626",
    "G6PD": "ENSG00000160211",
    "MLH1": "ENSG00000076242",
    "MTHFR": "ENSG00000177000",
    "HFE": "ENSG00000010704",
    "ALDH2": "ENSG00000111275",
    "LDLR": "ENSG00000130164",
    "HBB": "ENSG00000244734",
    "APC": "ENSG00000134982",
    "RET": "ENSG00000165731",
    "PALB2": "ENSG00000083093",
    "SMN1": "ENSG00000172062",
    "DMD": "ENSG00000198947",
    "PAH": "ENSG00000171759",
    "CYP2C19": "ENSG00000165841",
}

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "data" / "sample" / "demo_associations.json"
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUT_PATH = PROCESSED_DIR / "sample_associations.json"
BULK_OUTPUT_PATH = PROCESSED_DIR / "bulk_associations.json"
CLINVAR_CACHE = ROOT / "data" / "cache" / "variant_summary.txt.gz"


def curated_symbols() -> set:
    """Collect gene symbols that already have curated (metaphor) entries."""
    symbols = set()
    for item in load_sample() + EXTRA_ASSOCIATIONS:
        sym = (item.get("gene") or {}).get("symbol")
        if sym:
            symbols.add(sym)
    return symbols


def load_sample() -> list:
    if not SAMPLE_PATH.exists():
        console.print(f"[red]未找到样本数据: {SAMPLE_PATH}[/red]")
        return []
    return json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))


def merge_associations(base: list, extra: list) -> list:
    seen = {item.get("association_id") for item in base}
    merged = list(base)
    for item in extra:
        if item.get("association_id") not in seen:
            seen.add(item.get("association_id"))
            merged.append(item)
    return merged


async def enrich_live(associations: list) -> None:
    """用实时 API 补充科研证据评分 (离线失败不影响主流程)."""
    symbols = [a["gene"]["symbol"] for a in associations if a["gene"]["symbol"] in ENSEMBL_IDS]
    console.print(f"[cyan]→ 实时查询 Open Targets / ClinVar ({len(symbols)} 个基因)...[/cyan]")

    ot_results, cv_results = await asyncio.gather(
        fetch_many_targets([ENSEMBL_IDS[s] for s in symbols]),
        fetch_many_genes(symbols, max_records=10),
        return_exceptions=True,
    )
    if isinstance(ot_results, Exception):
        console.print("[yellow]Open Targets 查询失败，跳过实时证据补充[/yellow]")
        ot_results = {}
    if isinstance(cv_results, Exception):
        console.print("[yellow]ClinVar 查询失败，跳过实时证据补充[/yellow]")
        cv_results = {}

    for assoc in associations:
        symbol = assoc["gene"]["symbol"]
        ensembl = ENSEMBL_IDS.get(symbol)
        if ensembl and ensembl in ot_results and ot_results[ensembl]:
            top = max(ot_results[ensembl], key=lambda r: r["score"])
            assoc.setdefault("evidence", {})["opentargets_score"] = top["score"]
            assoc["evidence"]["opentargets_disease"] = top["disease_name"]
        if symbol in cv_results and cv_results[symbol]:
            pathogenic = [
                v for v in cv_results[symbol] if "风险变异" in v["significance_chinese"]
            ]
            assoc.setdefault("evidence", {})["clinvar_pathogenic_count"] = len(pathogenic)


def run(live: bool = False) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    console.rule("[bold green]DecodeGene 数据摄取管道[/bold green]")
    base = load_sample()
    console.print(f"✔ 载入样本数据 {len(base)} 条关联")

    merged = merge_associations(base, EXTRA_ASSOCIATIONS)
    console.print(f"✔ 合并通俗比喻库后共 {len(merged)} 条关联")

    if live:
        asyncio.run(enrich_live(merged))

    OUTPUT_PATH.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    console.print(f"[bold green]✔ 已生成: {OUTPUT_PATH}[/bold green]")


def run_bulk(max_genes: int = 3000) -> None:
    """从 ClinVar 全量 dump 批量导入基因-疾病关联（无通俗比喻，供专业模式）。"""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    console.rule("[bold green]DecodeGene 批量导入 (ClinVar)[/bold green]")

    exclude = curated_symbols()
    console.print(f"✔ 已排除 {len(exclude)} 个已收录的精选基因")

    cache = download_variant_summary(CLINVAR_CACHE)
    associations = parse_variant_summary(cache, exclude_symbols=exclude, max_genes=max_genes)

    BULK_OUTPUT_PATH.write_text(
        json.dumps(associations, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    console.print(f"[bold green]✔ 已生成 {len(associations)} 条批量关联: {BULK_OUTPUT_PATH}[/bold green]")


def main() -> None:
    parser = argparse.ArgumentParser(description="DecodeGene 数据摄取管道")
    parser.add_argument(
        "--live",
        action="store_true",
        help="额外调用 Open Targets / ClinVar 实时 API 补充证据评分",
    )
    parser.add_argument(
        "--bulk",
        action="store_true",
        help="从 ClinVar 全量 dump 批量导入基因-疾病关联",
    )
    parser.add_argument(
        "--max-genes",
        type=int,
        default=3000,
        help="批量导入的基因数量上限 (默认 3000)",
    )
    args = parser.parse_args()
    if args.bulk:
        run_bulk(max_genes=args.max_genes)
    else:
        run(live=args.live)


if __name__ == "__main__":
    main()
