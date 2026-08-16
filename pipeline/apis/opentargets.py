"""Async adapter for the Open Targets Platform GraphQL API.

Fetches target (gene) -> disease association scores used to populate the
"专业科研模式" evidence view of DecodeGene.
"""
from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

import httpx

OPEN_TARGETS_ENDPOINT = "https://api.platform.opentargets.org/api/v4/graphql"
USER_AGENT = "DecodeGene-Bot/1.0 (open-source gene education project)"

TARGET_DISEASES_QUERY = """
query TargetDiseases($ensemblId: String!, $size: Int!) {
  target(ensemblId: $ensemblId) {
    id
    approvedSymbol
    approvedName
    associatedDiseases(page: { size: $size, index: 0 }) {
      count
      rows {
        disease { id name }
        score
      }
    }
  }
}
"""


def _build_headers() -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
    }


async def fetch_target_diseases(
    ensembl_id: str,
    size: int = 10,
    client: Optional[httpx.AsyncClient] = None,
) -> List[Dict[str, Any]]:
    """Fetch the top associated diseases for a single Ensembl gene id.

    Returns a list of dictionaries::

        {
            "gene_symbol": "BRCA1",
            "ensembl_id": "ENSG00000012048",
            "disease_id": "MONDO:0007254",
            "disease_name": "breast carcinoma",
            "score": 0.94,
        }
    """
    owns_client = client is None
    if client is None:
        client = httpx.AsyncClient(timeout=30.0)

    try:
        payload = {
            "query": TARGET_DISEASES_QUERY,
            "variables": {"ensemblId": ensembl_id, "size": size},
        }
        resp = await client.post(
            OPEN_TARGETS_ENDPOINT, json=payload, headers=_build_headers()
        )
        resp.raise_for_status()
        data = resp.json()
        target = data.get("data", {}).get("target")
        if not target:
            return []

        symbol = target.get("approvedSymbol", ensembl_id)
        rows = target.get("associatedDiseases", {}).get("rows", [])
        results: List[Dict[str, Any]] = []
        for row in rows:
            disease = row.get("disease") or {}
            results.append(
                {
                    "gene_symbol": symbol,
                    "ensembl_id": ensembl_id,
                    "disease_id": disease.get("id", ""),
                    "disease_name": disease.get("name", ""),
                    "score": float(row.get("score", 0.0)),
                }
            )
        return results
    except (httpx.HTTPError, ValueError, KeyError):
        return []
    finally:
        if owns_client:
            await client.aclose()


async def fetch_many_targets(
    ensembl_ids: List[str], size: int = 10
) -> Dict[str, List[Dict[str, Any]]]:
    """Fetch association scores for several genes concurrently."""
    sem = asyncio.Semaphore(3)  # gentle rate limiting per data_sources.md

    async def _one(eid: str) -> tuple[str, List[Dict[str, Any]]]:
        async with sem:
            rows = await fetch_target_diseases(eid, size=size)
            return eid, rows

    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = [_one(eid) for eid in ensembl_ids]
        outcomes = await asyncio.gather(*tasks)

    return {eid: rows for eid, rows in outcomes}
