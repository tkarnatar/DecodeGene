"""Tests for fuzzy search (symbol / Chinese / pinyin initials)."""
from app.core.database import kb


def _symbols(results):
    return [a.gene.symbol for a in results]


def test_search_by_symbol_case_insensitive():
    results = kb.search("brca1")
    assert "BRCA1" in _symbols(results)


def test_search_by_chinese_disease():
    results = kb.search("乳腺癌")
    assert "BRCA1" in _symbols(results)


def test_search_by_chinese_gene_name():
    results = kb.search("老年痴呆")
    assert "APOE" in _symbols(results)


def test_search_by_pinyin_initials():
    results = kb.search("rxa")
    assert "BRCA1" in _symbols(results)


def test_search_lung_cancer():
    results = kb.search("肺癌")
    assert "EGFR" in _symbols(results)


def test_search_empty_query():
    assert kb.search("") == []
