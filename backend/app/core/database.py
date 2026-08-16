"""Knowledge base backed by DuckDB (fallback: SQLite) with Chinese + pinyin fuzzy search."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from ..models.schema import GeneDiseaseAssociation, MythBuster, association_from_dict
from .config import settings
from .pinyin import pinyin_initials

# 常见基因别名 -> 标准 symbol (用于模糊检索)
GENE_ALIASES: Dict[str, str] = {
    "p53": "TP53",
    "乳腺癌": "BRCA1",
    "乳癌": "BRCA1",
    "卵巢癌基因": "BRCA1",
    "肺癌": "EGFR",
    "老年痴呆": "APOE",
    "阿兹海默": "APOE",
    "阿尔茨海默": "APOE",
    "蚕豆病": "G6PD",
    "囊性纤维化": "CFTR",
}


class KnowledgeBase:
    """In-memory search index over the offline association JSON, with an
    optional DuckDB/SQLite backing store for direct SQL retrieval."""

    def __init__(self, data_paths: Optional[List[Path]] = None) -> None:
        self.associations: List[GeneDiseaseAssociation] = []
        self.by_symbol: Dict[str, GeneDiseaseAssociation] = {}
        self._token_index: Dict[str, List[GeneDiseaseAssociation]] = {}
        self._load(data_paths)
        self._load_narratives()
        self._build_index()
        self._conn = None  # backing store is created lazily on first query_db

    # ------------------------------------------------------------------ load
    def _load(self, data_paths: Optional[List[Path]]) -> None:
        paths = data_paths or [
            settings.SAMPLE_DATA_PATH,
            settings.PROCESSED_DATA_PATH,
            settings.BULK_DATA_PATH,
        ]
        seen = set()
        for path in paths:
            if not path or not Path(path).exists():
                continue
            try:
                data = json.loads(Path(path).read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if isinstance(data, dict):
                data = data.get("associations", data.get("data", []))
            for item in data or []:
                assoc = association_from_dict(item)
                if assoc.association_id in seen:
                    continue
                seen.add(assoc.association_id)
                self.associations.append(assoc)

    def _load_narratives(self) -> None:
        """Merge AI-generated plain-language narratives into bulk associations."""
        path = settings.BULK_NARRATIVES_PATH
        if not path or not path.exists():
            return
        try:
            narratives = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        if not isinstance(narratives, dict):
            return
        for assoc in self.associations:
            n = narratives.get(assoc.gene.symbol)
            if not n:
                continue
            if not assoc.gene.chinese_name and n.get("chinese_name"):
                assoc.gene.chinese_name = n["chinese_name"]
            if not assoc.gene.metaphor_title and n.get("metaphor_title"):
                assoc.gene.metaphor_title = n["metaphor_title"]
                assoc.gene.metaphor_story = n.get("metaphor_story", "")
            if not assoc.gene.plain_summary and n.get("plain_summary"):
                assoc.gene.plain_summary = n["plain_summary"]
            if n.get("screening_advice"):
                assoc.lifestyle_prevention.screening_advice = n["screening_advice"]
            if n.get("lifestyle_tips"):
                assoc.lifestyle_prevention.lifestyle_tips = n["lifestyle_tips"]
            if n.get("key_questions"):
                assoc.doctor_checklist.key_questions = n["key_questions"]
            if n.get("myth") and n.get("truth"):
                assoc.myth_buster = MythBuster(myth=n["myth"], truth=n["truth"])

    # ----------------------------------------------------------------- index
    def _add_token(self, token: str, assoc: GeneDiseaseAssociation) -> None:
        token = (token or "").strip().lower()
        if len(token) < 2:
            return
        self._token_index.setdefault(token, [])
        if not any(a.association_id == assoc.association_id for a in self._token_index[token]):
            self._token_index[token].append(assoc)

    def _build_index(self) -> None:
        for assoc in self.associations:
            self.by_symbol[assoc.gene.symbol.upper()] = assoc
            tokens = {
                assoc.gene.symbol,
                assoc.gene.name,
                assoc.gene.chinese_name,
                assoc.disease.name,
                assoc.disease.chinese_name,
                pinyin_initials(assoc.gene.chinese_name),
                pinyin_initials(assoc.disease.chinese_name),
            }
            for cat in assoc.disease.categories:
                tokens.add(cat)
                tokens.add(pinyin_initials(cat))
            for token in tokens:
                self._add_token(token, assoc)

        for alias, symbol in GENE_ALIASES.items():
            target = self.by_symbol.get(symbol.upper())
            if target is not None:
                self._add_token(alias, target)
                self._add_token(pinyin_initials(alias), target)

    # ---------------------------------------------------------------- search
    def get_by_symbol(self, symbol: str) -> Optional[GeneDiseaseAssociation]:
        return self.by_symbol.get((symbol or "").strip().upper())

    def _score(self, query: str, assoc: GeneDiseaseAssociation) -> float:
        q = query.lower()
        symbol = assoc.gene.symbol.lower()
        gene_zh = assoc.gene.chinese_name
        disease_zh = assoc.disease.chinese_name
        gene_ini = pinyin_initials(gene_zh)
        disease_ini = pinyin_initials(disease_zh)

        score = 0.0
        if symbol == q:
            score += 100
        elif symbol.startswith(q):
            score += 60
        elif q in symbol:
            score += 40
        if gene_zh and q == gene_zh:
            score += 90
        elif gene_zh and q in gene_zh:
            score += 50
        if disease_zh and q == disease_zh:
            score += 90
        elif disease_zh and q in disease_zh:
            score += 50
        gene_en = assoc.gene.name.lower()
        disease_en = assoc.disease.name.lower()
        if gene_en and q == gene_en:
            score += 80
        elif gene_en and q in gene_en:
            score += 45
        if disease_en and q == disease_en:
            score += 90
        elif disease_en and q in disease_en:
            score += 50
        if gene_ini and q == gene_ini:
            score += 70
        elif gene_ini and q in gene_ini:
            score += 40
        if disease_ini and q == disease_ini:
            score += 70
        elif disease_ini and q in disease_ini:
            score += 40
        for cat in assoc.disease.categories:
            if q == cat.lower():
                score += 60
            elif q in cat.lower():
                score += 30
        return score

    def search(self, query: str, limit: int = 10) -> List[GeneDiseaseAssociation]:
        q = (query or "").strip().lower()
        if not q:
            return []
        alias_target = self.by_symbol.get(GENE_ALIASES.get(q, "").upper())
        scored: Dict[str, float] = {}
        if alias_target is not None:
            scored[alias_target.association_id] = 200.0
        for token, assocs in self._token_index.items():
            if q == token or q in token or (len(token) >= 2 and token in q):
                for assoc in assocs:
                    s = self._score(q, assoc) or 10.0
                    scored[assoc.association_id] = max(scored.get(assoc.association_id, 0.0), s)
        ranked = sorted(
            scored.items(), key=lambda kv: kv[1], reverse=True
        )
        result = [self._by_id(aid) for aid, _ in ranked[:limit]]
        return [a for a in result if a is not None]

    def _by_id(self, association_id: str) -> Optional[GeneDiseaseAssociation]:
        for assoc in self.associations:
            if assoc.association_id == association_id:
                return assoc
        return None

    # -------------------------------------------------------- backing store
    def _init_backing_store(self):
        """Create an in-memory SQLite store for direct SQL retrieval.

        SQLite (stdlib) is used because DuckDB's ``executemany`` is orders of
        magnitude slower for bulk inserts; the store is created lazily so app
        startup stays fast.
        """
        import sqlite3

        rows = [
            (
                a.association_id,
                a.gene.symbol,
                a.gene.chinese_name,
                a.disease.chinese_name,
                a.evidence.overall_score,
            )
            for a in self.associations
        ]
        conn = sqlite3.connect(":memory:")
        conn.execute(
            "CREATE TABLE associations ("
            "association_id TEXT PRIMARY KEY, symbol TEXT, "
            "chinese_name TEXT, disease TEXT, score REAL)"
        )
        conn.executemany(
            "INSERT OR REPLACE INTO associations VALUES (?, ?, ?, ?, ?)", rows
        )
        conn.commit()
        return conn

    def query_db(self, sql: str, params: tuple = ()) -> List[tuple]:
        """Run a raw SQL query against the backing store (SQLite)."""
        if self._conn is None:
            self._conn = self._init_backing_store()
        cur = self._conn.execute(sql, params)
        if cur.description is None:
            return []
        return list(cur.fetchall())


kb = KnowledgeBase()
