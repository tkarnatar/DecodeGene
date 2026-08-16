"""Tests for the family inheritance probability calculator."""
from app.models.schema import FamilyInheritanceQuery
from app.services.inheritance import InheritanceCalculator

calc = InheritanceCalculator()


def test_ad_one_affected_parent():
    q = FamilyInheritanceQuery(pattern="AD", father_status="affected", mother_status="normal")
    r = calc.calculate(q)
    assert r.child_disease_risk_pct == 50.0
    assert r.child_carrier_risk_pct == 0.0
    assert r.child_normal_pct == 50.0


def test_ad_both_affected_parents():
    q = FamilyInheritanceQuery(pattern="AD", father_status="affected", mother_status="affected")
    r = calc.calculate(q)
    assert r.child_disease_risk_pct == 75.0


def test_ar_both_carriers():
    q = FamilyInheritanceQuery(pattern="AR", father_status="carrier", mother_status="carrier")
    r = calc.calculate(q)
    assert r.child_disease_risk_pct == 25.0
    assert r.child_carrier_risk_pct == 50.0
    assert r.child_normal_pct == 25.0


def test_ar_affected_and_normal():
    q = FamilyInheritanceQuery(pattern="AR", father_status="affected", mother_status="normal")
    r = calc.calculate(q)
    assert r.child_disease_risk_pct == 0.0
    assert r.child_carrier_risk_pct == 100.0


def test_xr_mother_carrier():
    q = FamilyInheritanceQuery(pattern="XR", father_status="normal", mother_status="carrier")
    r = calc.calculate(q)
    assert r.child_disease_risk_pct == 25.0  # sons 50%, daughters 0%
    assert r.by_sex["male"].disease_risk_pct == 50.0
    assert r.by_sex["female"].carrier_risk_pct == 50.0


def test_invalid_pattern_raises():
    q = FamilyInheritanceQuery(pattern="AD", father_status="normal", mother_status="normal")
    q = q.model_copy(update={"pattern": "XX"})
    import pytest
    with pytest.raises(ValueError):
        calc.calculate(q)
