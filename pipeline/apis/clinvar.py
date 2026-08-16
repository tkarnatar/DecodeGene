"""Async adapter for NCBI ClinVar E-utilities.

Queries variant clinical significance and maps raw classifications to
consumer-friendly Chinese labels defined in docs/PROJECT_PLAN.md.
"""
from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

import httpx

EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
USER_AGENT = "DecodeGene-Bot/1.0 (open-source gene education project)"

# Raw ClinVar significance -> 大众通俗中文标签
CLINVAR_SIGNIFICANCE_MAP: Dict[str, str] = {
    "Pathogenic": "⚠️ 明确风险变异 (需关注)",
    "Likely pathogenic": "⚠️ 可能风险变异 (建议关注)",
    "Pathogenic/Likely pathogenic": "⚠️ 明确/可能风险变异 (需关注)",
    "Uncertain significance": "❓ 意义未明变异 (持续研究中)",
    "Variant of uncertain significance": "❓ 意义未明变异 (持续研究中)",
    "Conflicting interpretations of pathogenicity": "❓ 临床意义存争议 (需专业复核)",
    "Likely benign": "✅ 可能良性变异 (基本无需担心)",
    "Benign": "✅ 良性变异 (无需担心)",
    "Benign/Likely benign": "✅ 良性/可能良性变异 (无需担心)",
}


def map_significance(raw: str) -> str:
    """Translate a raw ClinVar significance string to a Chinese plain label."""
    return CLINVAR_SIGNIFICANCE_MAP.get(
        raw, f"❓ 未明确分类变异 ({raw or '未知'})"
    )


async def _esearch_terms(
    term: str, client: httpx.AsyncClient
) -> List[str]:
    """Search ClinVar and return a list of variation UIDs."""
    params = {
        "db": "clinvar",
        "term": term,
        "retmode": "json",
        "retmax": 50,
        "tool": "DecodeGene",
    }
    resp = await client.get(f"{EUTILS_BASE}/esearch.fcgi", params=params)
    resp.raise_for_status()
    data = resp.json()
    return data.get("esearchresult", {}).get("idlist", [])


async def _esummary(uids: List[str], client: httpx.AsyncClient) -> Dict[str, Any]:
    """Fetch JSON summaries for a list of variation UIDs."""
    params = {
        "db": "clinvar",
        "id": ",".join(uids),
        "retmode": "json",
        "tool": "DecodeGene",
    }
    resp = await client.get(f"{EUTILS_BASE}/esummary.fcgi", params=params)
    resp.raise_for_status()
    return resp.json()


async def fetch_clinvar_variants(
    gene_symbol: str,
    max_records: int = 10,
    client: Optional[httpx.AsyncClient] = None,
) -> List[Dict[str, Any]]:
    """Fetch ClinVar variants for a gene, annotated with Chinese labels.

    Returns a list of dictionaries::

        {
            "variation_id": "12345",
            "gene_symbol": "BRCA1",
            "significance": "Pathogenic",
            "significance_chinese": "⚠️ 明确风险变异 (需关注)",
            "phenotypes": "Breast-ovarian cancer, familial 1",
        }
    """
    owns_client = client is None
    if client is None:
        client = httpx.AsyncClient(timeout=30.0, headers={"User-Agent": USER_AGENT})

    try:
        uids = await _esearch_terms(f"{gene_symbol}[gene]", client)
        if not uids:
            return []
        uids = uids[:max_records]
        summary = await _esummary(uids, client)
        result = summary.get("result", {})
        records: List[Dict[str, Any]] = []
        for uid in uids:
            node = result.get(uid)
            if not node:
                continue
            sig = node.get("clinical_significance", {})
            raw_sig = ""
            if isinstance(sig, dict):
                raw_sig = sig.get("description", "")
            elif isinstance(sig, str):
                raw_sig = sig
            records.append(
                {
                    "variation_id": uid,
                    "gene_symbol": gene_symbol,
                    "significance": raw_sig,
                    "significance_chinese": map_significance(raw_sig),
                    "phenotypes": node.get("title", ""),
                }
            )
        return records
    except (httpx.HTTPError, ValueError, KeyError):
        return []
    finally:
        if owns_client:
            await client.aclose()


async def fetch_many_genes(
    gene_symbols: List[str], max_records: int = 10
) -> Dict[str, List[Dict[str, Any]]]:
    """Fetch ClinVar variants for several genes with rate limiting."""
    sem = asyncio.Semaphore(3)

    async def _one(symbol: str) -> tuple[str, List[Dict[str, Any]]]:
        async with sem:
            await asyncio.sleep(0.4)  # polite rate limit per data_sources.md
            rows = await fetch_clinvar_variants(symbol, max_records=max_records)
            return symbol, rows

    async with httpx.AsyncClient(timeout=30.0, headers={"User-Agent": USER_AGENT}) as c:
        tasks = [_one(s) for s in gene_symbols]
        outcomes = await asyncio.gather(*tasks)

    return {s: rows for s, rows in outcomes}
