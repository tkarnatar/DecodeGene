"""Tests for the doctor checklist generator."""
from app.core.database import kb
from app.services.checklist import ChecklistService

svc = ChecklistService(kb)


def test_checklist_brca1():
    cl = svc.generate("BRCA1")
    assert cl is not None
    assert cl.gene_symbol == "BRCA1"
    assert len(cl.key_questions) >= 3
    assert cl.recommended_specialty


def test_checklist_unknown_gene():
    assert svc.generate("NOT_A_GENE") is None


def test_render_checklist_text():
    text = svc.render_checklist("BRCA1")
    assert "BRCA1" in text
    assert "就医提问卡" in text
