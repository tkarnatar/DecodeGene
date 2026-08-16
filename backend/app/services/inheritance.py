"""遗传概率计算器 (InheritanceCalculator).

支持常染色体显性 (AD)、常染色体隐性 (AR)、X 连锁隐性 (XR) 与
X 连锁显性 (XD) 遗传模式，输出子女患病 / 携带百分比及白话文解析。
"""
from __future__ import annotations

from typing import Dict, List

from ..models.schema import FamilyInheritanceQuery, FamilyInheritanceResult, SexRisk


class InheritanceCalculator:
    PATTERNS = ("AD", "AR", "XR", "XD")
    VALID_STATUS = ("affected", "carrier", "normal")

    def calculate(self, query: FamilyInheritanceQuery) -> FamilyInheritanceResult:
        lang = getattr(query, "lang", "zh")
        pattern = query.pattern.upper()
        if pattern not in self.PATTERNS:
            raise ValueError(f"不支持的遗传模式: {pattern}")
        for label, status in (("father", query.father_status), ("mother", query.mother_status)):
            if status not in self.VALID_STATUS:
                raise ValueError(f"无效的{label}状态: {status}")

        if pattern == "AD":
            return self._calc_ad(query.father_status, query.mother_status, lang)
        if pattern == "AR":
            return self._calc_ar(query.father_status, query.mother_status, lang)
        return self._calc_x(query.father_status, query.mother_status, pattern, lang)

    # ---------------------------------------------------------------- helpers
    @staticmethod
    def _cross(f_alleles: List[str], m_alleles: List[str]) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for fa in f_alleles:
            for ma in m_alleles:
                genotype = "".join(sorted([fa, ma]))
                counts[genotype] = counts.get(genotype, 0) + 1
        return counts

    # ------------------------------------------------------------------- AD
    @staticmethod
    def _ad_genotype(status: str) -> List[str]:
        # 显性: D = 致病等位基因 (dominant), d = 正常等位基因
        if status in ("affected", "carrier"):
            return ["D", "d"]
        return ["d", "d"]

    def _calc_ad(self, father: str, mother: str, lang: str = "zh") -> FamilyInheritanceResult:
        counts = self._cross(self._ad_genotype(father), self._ad_genotype(mother))
        total = sum(counts.values())
        disease = sum(c for g, c in counts.items() if "D" in g) / total * 100
        normal = 100 - disease
        if lang == "en":
            explanation = (
                "Autosomal dominant: carrying one pathogenic allele may be enough to cause "
                "the disease, and there is no 'asymptomatic carrier'. Based on your selected "
                f"parental statuses, each child has about {disease:.0f}% chance of being affected "
                f"and {normal:.0f}% chance of being normal."
            )
        else:
            explanation = (
                f"常染色体显性遗传：携带一份致病基因即可能发病，没有「无症状携带者」。"
                f"根据您选择的父母状态，每个孩子患病概率约为 {disease:.0f}%，"
                f"正常概率约为 {normal:.0f}%。"
            )
        return FamilyInheritanceResult(
            pattern="AD",
            father_status=father,
            mother_status=mother,
            child_disease_risk_pct=round(disease, 1),
            child_carrier_risk_pct=0.0,
            child_normal_pct=round(normal, 1),
            plain_explanation=explanation,
            recommendations=self._recommendations(lang),
        )

    # ------------------------------------------------------------------- AR
    @staticmethod
    def _ar_genotype(status: str) -> List[str]:
        # 隐性: A = 正常等位基因, a = 致病等位基因
        if status == "affected":
            return ["a", "a"]
        if status == "carrier":
            return ["A", "a"]
        return ["A", "A"]

    def _calc_ar(self, father: str, mother: str, lang: str = "zh") -> FamilyInheritanceResult:
        counts = self._cross(self._ar_genotype(father), self._ar_genotype(mother))
        total = sum(counts.values())
        disease = counts.get("aa", 0) / total * 100
        carrier = counts.get("Aa", 0) / total * 100
        normal = counts.get("AA", 0) / total * 100
        if lang == "en":
            explanation = (
                "Autosomal recessive: a child is affected only when they inherit one pathogenic "
                "allele from each parent; carrying just one copy causes no symptoms (carrier). "
                "Based on your selected parental statuses, each child has about "
                f"{disease:.0f}% chance of being affected, {carrier:.0f}% chance of being an "
                f"asymptomatic carrier, and {normal:.0f}% chance of being normal."
            )
        else:
            explanation = (
                f"常染色体隐性遗传：需同时从父母双方各遗传一份致病基因才会发病，"
                f"只携带一份者无症状（称为携带者）。根据您选择的父母状态，"
                f"每个孩子患病概率约为 {disease:.0f}%，成为无症状携带者的概率约为 "
                f"{carrier:.0f}%，完全正常的概率约为 {normal:.0f}%。"
            )
        return FamilyInheritanceResult(
            pattern="AR",
            father_status=father,
            mother_status=mother,
            child_disease_risk_pct=round(disease, 1),
            child_carrier_risk_pct=round(carrier, 1),
            child_normal_pct=round(normal, 1),
            plain_explanation=explanation,
            recommendations=self._recommendations(lang),
        )

    # --------------------------------------------------------------- X-linked
    @staticmethod
    def _x_mother_genotype(status: str, dominant: bool = False) -> List[str]:
        # X 染色体: Xn = 正常, Xd = 致病
        if status == "affected":
            return ["Xd", "Xd"]
        if status == "carrier":
            # 隐性模式携带者 = Xn Xd；显性模式下携带一份即可能发病
            return ["Xn", "Xd"]
        return ["Xn", "Xn"]

    def _calc_x(self, father: str, mother: str, pattern: str, lang: str = "zh") -> FamilyInheritanceResult:
        dominant = pattern == "XD"
        m_alleles = self._x_mother_genotype(mother, dominant=dominant)
        f_x = "Xd" if father == "affected" else "Xn"
        n = len(m_alleles)

        # 儿子: 从母亲获得 X, 从父亲获得 Y
        son_affected = sum(1 for mx in m_alleles if mx == "Xd") / n * 100
        son_carrier = 0.0
        son_normal = 100 - son_affected

        # 女儿: 从母亲获得 X, 从父亲获得 X
        d_affected = 0
        d_carrier = 0
        for mx in m_alleles:
            xd_count = int(mx == "Xd") + int(f_x == "Xd")
            if dominant:
                if xd_count >= 1:
                    d_affected += 1
            else:
                if xd_count == 2:
                    d_affected += 1
                elif xd_count == 1:
                    d_carrier += 1
        d_affected_pct = d_affected / n * 100
        d_carrier_pct = d_carrier / n * 100
        d_normal_pct = 100 - d_affected_pct - d_carrier_pct

        # 假设男女出生比例 1:1，取平均
        disease = (son_affected + d_affected_pct) / 2
        carrier = (son_carrier + d_carrier_pct) / 2
        normal = (son_normal + d_normal_pct) / 2

        by_sex = {
            "male": SexRisk(
                disease_risk_pct=round(son_affected, 1),
                carrier_risk_pct=round(son_carrier, 1),
                normal_pct=round(son_normal, 1),
            ),
            "female": SexRisk(
                disease_risk_pct=round(d_affected_pct, 1),
                carrier_risk_pct=round(d_carrier_pct, 1),
                normal_pct=round(d_normal_pct, 1),
            ),
        }
        mode = "X 连锁显性" if dominant else "X 连锁隐性"
        if lang == "en":
            mode_en = "X-linked dominant" if dominant else "X-linked recessive"
            explanation = (
                f"{mode_en}: the pathogenic gene is on the X chromosome, so inheritance differs "
                "between boys and girls. Overall, each child has about "
                f"{disease:.0f}% chance of being affected, {carrier:.0f}% chance of being a "
                f"carrier, and {normal:.0f}% chance of being normal. Specifically: boys affected "
                f"~{son_affected:.0f}%; girls affected ~{d_affected_pct:.0f}%, carriers ~{d_carrier_pct:.0f}%."
            )
        else:
            explanation = (
                f"{mode}遗传：致病基因位于 X 染色体上，男女孩遗传规律不同。"
                f"综合来看，每个孩子患病概率约为 {disease:.0f}%，"
                f"成为无症状携带者的概率约为 {carrier:.0f}%，完全正常概率约 {normal:.0f}%。"
                f"其中：男孩患病约 {son_affected:.0f}%；"
                f"女孩患病约 {d_affected_pct:.0f}%、携带约 {d_carrier_pct:.0f}%。"
            )
        return FamilyInheritanceResult(
            pattern=pattern,
            father_status=father,
            mother_status=mother,
            child_disease_risk_pct=round(disease, 1),
            child_carrier_risk_pct=round(carrier, 1),
            child_normal_pct=round(normal, 1),
            plain_explanation=explanation,
            by_sex=by_sex,
            recommendations=self._recommendations(lang),
        )

    @staticmethod
    def _recommendations(lang: str = "zh") -> List[str]:
        if lang == "en":
            return [
                "The probabilities above are statistical estimates based on Mendelian inheritance; please consult a clinical genetic counselor for specifics.",
                "If your family has a known genetic risk, consider preimplantation genetic testing (PGT) before pregnancy.",
                "Families who already have children or are planning pregnancy are advised to seek genetic counseling and prenatal diagnosis at a hospital genetics clinic.",
            ]
        return [
            "上述概率为基于孟德尔遗传规律的统计值，具体请咨询临床遗传咨询师。",
            "若家庭中有明确的遗传病风险，备孕前可咨询三代试管婴儿 (PGT) 阻断技术。",
            "已生育或有生育计划的家庭，建议到正规医院遗传门诊进行遗传咨询与产前诊断。",
        ]


calculator = InheritanceCalculator()
