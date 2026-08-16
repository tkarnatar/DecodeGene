"""Bulk ingestion from the ClinVar variant_summary dump.

Downloads the full ClinVar ``variant_summary.txt.gz`` (tab-delimited) once,
stream-parses it, and aggregates one gene-disease association per gene with
pathogenic / likely-pathogenic variant counts and a primary disease name.
"""
from __future__ import annotations

import gzip
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set

import httpx

CLINVAR_SUMMARY_URL = (
    "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz"
)

# Significance values counted as "risk" for bulk ranking
RISK_SIGNIFICANCE = {
    "Pathogenic",
    "Likely pathogenic",
    "Pathogenic/Likely pathogenic",
}

SKIP_SYMBOLS = {"-", "", "Multiple"}
# ClinVar 的 GeneSymbol 欄位偶爾是 CNV 片段描述而非真實基因符號
_JUNK_GENE = re.compile(
    r"[\s:]|covers|subset|genes|deletion|duplication|region|entire|none of which",
    re.IGNORECASE,
)
IGNORED_CONDITIONS = {
    "not provided",
    "not specified",
    "not applicable",
    "see cases",
    "none",
}


def download_variant_summary(cache_path: Path) -> Path:
    """Download the ClinVar variant_summary gz if not already cached."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    if cache_path.exists() and cache_path.stat().st_size > 0:
        return cache_path

    tmp = cache_path.with_suffix(".part")
    print(f"  下载 ClinVar variant_summary (约 441MB) ...", flush=True)
    with httpx.stream(
        "GET", CLINVAR_SUMMARY_URL, timeout=120.0, follow_redirects=True
    ) as resp:
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        done = 0
        last_pct = -1
        with open(tmp, "wb") as fh:
            for chunk in resp.iter_bytes(1024 * 256):
                fh.write(chunk)
                done += len(chunk)
                if total:
                    pct = done * 100 // total
                    if pct >= last_pct + 10:
                        last_pct = pct
                        print(
                            f"  下载中... {pct}% ({done // (1024 * 1024)} MB)",
                            flush=True,
                        )
    tmp.rename(cache_path)
    print(f"  下载完成: {cache_path}", flush=True)
    return cache_path


def _split_genes(raw: str) -> List[str]:
    out = []
    for g in (raw or "").replace(",", ";").split(";"):
        g = g.strip()
        if not g or g in SKIP_SYMBOLS:
            continue
        if _JUNK_GENE.search(g):
            continue
        out.append(g)
    return out


def _best_condition(phenotypes: str) -> str:
    if not phenotypes:
        return ""
    for sep in ("|", ";"):
        for part in (phenotypes or "").split(sep):
            p = part.strip().split("(")[0].strip()
            if p and p.lower() not in IGNORED_CONDITIONS:
                return p
    return ""


def _rating_and_badge(count: int) -> tuple:
    if count >= 100:
        return (
            5,
            0.9,
            "⭐️⭐️⭐️⭐️⭐️ ClinVar 明确致病证据（≥100 个致病变异）",
            "🟢 明确致病基因",
        )
    if count >= 20:
        return (
            4,
            0.75,
            "⭐️⭐️⭐️⭐️ ClinVar 强致病证据（≥20 个致病变异）",
            "🔵 强证据基因",
        )
    if count >= 5:
        return (
            3,
            0.6,
            "⭐️⭐️⭐️ ClinVar 中等证据（≥5 个致病变异）",
            "🟡 中等证据基因",
        )
    return (
        2,
        0.4,
        "⭐️⭐️ ClinVar 初步证据（1-4 个致病变异）",
        "⚪ 初步证据基因",
    )


def parse_variant_summary(
    path: Path, exclude_symbols: Set[str], max_genes: int = 3000
) -> List[Dict]:
    """Stream-parse the gz and return one association dict per gene."""
    gene_risk: Dict[str, int] = defaultdict(int)
    gene_disease: Dict[str, str] = {}

    with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as fh:
        header = None
        col: Dict[str, int] = {}
        for line in fh:
            if header is None:
                header = line.rstrip("\n").split("\t")
                col = {name: i for i, name in enumerate(header)}
                continue
            fields = line.rstrip("\n").split("\t")

            def get(name: str) -> str:
                i = col.get(name)
                return fields[i] if i is not None and i < len(fields) else ""

            sig = get("ClinicalSignificance")
            if sig not in RISK_SIGNIFICANCE:
                continue
            symbols = _split_genes(get("GeneSymbol"))
            if not symbols:
                continue
            cond = _best_condition(get("PhenotypeList"))
            for sym in symbols:
                if sym in exclude_symbols:
                    continue
                gene_risk[sym] += 1
                if sym not in gene_disease and cond:
                    gene_disease[sym] = cond

    ranked = sorted(gene_risk.items(), key=lambda kv: kv[1], reverse=True)[:max_genes]

    associations: List[Dict] = []
    for sym, count in ranked:
        disease_name = gene_disease.get(sym, "")
        stars, score, rating, badge = _rating_and_badge(count)
        associations.append(
            {
                "association_id": f"BULK_{sym}",
                "gene": {
                    "symbol": sym,
                    "name": sym,
                    "chinese_name": "",
                    "chromosome": "",
                    "metaphor": {},
                    "plain_summary": "",
                    "academic_summary": "",
                },
                "disease": {
                    "id": "",
                    "name": disease_name,
                    "chinese_name": "",
                    "categories": [],
                    "severity_badge": badge,
                },
                "evidence": {
                    "overall_score": score,
                    "plain_rating": rating,
                    "professional_rating": f"ClinVar pathogenic/likely-pathogenic variants: {count}",
                    "star_rating": stars,
                    "clinvar_pathogenic_count": count,
                    "clinvar_summary_chinese": f"ClinVar 收录 {count} 个明确/可能致病变异",
                    "opentargets_score": 0.0,
                },
                "lifestyle_prevention": {"screening_advice": "", "lifestyle_tips": []},
                "doctor_checklist": {},
                "myth_buster": None,
            }
        )
    return associations
