"""DeepSeek 驱动的「报告白话文翻译」与「问医生」AI 智能体.

基于 DeepSeek API (deepseek-chat / deepseek-reasoner) 实现:
  * explain_report: 把基因检测报告翻译成通俗易懂的结构化解释
  * chat_qa:        患者答疑聊天机器人，支持流式输出 (SSE)

无 API Key 时自动降级为本地模板，保证功能可用。
"""
from __future__ import annotations

import json
import re
from typing import Any, AsyncIterator, Dict, List, Optional

import httpx

from ..core.config import settings
from ..models.schema import GeneticReportQuery, ReportExplanation

SYSTEM_PROMPT = (
    "你是一名资深临床遗传咨询师与顶级基因科普专家。"
    "你的语气应当温和、客观、极其通俗，严禁使用未加解释的晦涩术语，"
    "坚决避免引发用户的基因焦虑。你只说有科学依据的内容，"
    "遇到不确定时诚实说明，并始终引导用户咨询执业医师。"
)

REPORT_JSON_INSTRUCTION = (
    "请把用户粘贴的基因检测报告翻译成大白话，并严格按如下 JSON 格式输出"
    "（只输出 JSON，不要输出多余文字），字段均为中文：\n"
    '{"what_found": "① 到底测出了什么？", '
    '"actual_impact": "② 会对我造成什么实际影响？", '
    '"next_steps": "③ 接下来我该去医院做什么？", '
    '"lifestyle": "④ 日常生活该怎么吃、怎么动？", '
    '"disclaimer": "医疗免责声明与就诊指引"}'
)

DISCLAIMER = (
    "⚠️ 免责声明：以上内容由开源社区与 AI 提供，旨在普及遗传健康常识，"
    "不能替代执业医师、临床遗传咨询师的诊断与治疗建议。涉及实际医疗、用药或检测决策，"
    "请务必前往正规医院遗传咨询科就诊。"
)

SYSTEM_PROMPT_EN = (
    "You are a senior clinical genetic counselor and a top genetics educator. "
    "Your tone should be warm, objective and extremely accessible, avoiding unexplained jargon, "
    "and firmly avoiding causing genetic anxiety. Only state scientifically grounded content, "
    "honestly admit uncertainty, and always guide users to consult a licensed physician."
)

REPORT_JSON_INSTRUCTION_EN = (
    "Translate the user's pasted genetic report into plain language, and strictly output in "
    "the following JSON format (only JSON, no extra text), with all fields in English:\n"
    '{"what_found": "What was actually found?", '
    '"actual_impact": "What does this mean for me?", '
    '"next_steps": "What should I do next (see a doctor)?", '
    '"lifestyle": "How should I eat and exercise?", '
    '"disclaimer": "Medical disclaimer and care guidance"}'
)

DISCLAIMER_EN = (
    "⚠️ Disclaimer: The content above is provided by the open-source community and AI for "
    "educational purposes only. It is not a substitute for diagnosis or treatment by a licensed "
    "physician or genetic counselor. For actual medical, medication or testing decisions, "
    "please visit a hospital genetics clinic."
)

# 常见基因符号，用于离线降级时的关键词识别
KNOWN_GENES = [
    "BRCA1", "BRCA2", "TP53", "APOE", "EGFR", "CFTR", "G6PD", "MTHFR",
    "MLH1", "MSH2", "PALB2", "CHEK2", "ATM", "TTR", "HTT",
]

# 基因 -> 通俗解读片段 (离线降级用)
GENE_PLAIN: Dict[str, str] = {
    "BRCA1": "BRCA1 就像细胞里的「DNA 汽车维修工」，它突变会让细胞修复 DNA 的能力下降，"
    "升高乳腺癌、卵巢癌的终身风险（但绝非必然发病）。",
    "BRCA2": "BRCA2 是 BRCA1 的搭档，负责递送修复 DNA 的备用零件，突变同样升高乳腺癌、卵巢癌风险。",
    "TP53": "TP53 是细胞里的「紧急制动刹车片」，突变会削弱细胞清除异常细胞的能力，升高多种早发肿瘤风险。",
    "APOE": "APOE 是大脑里的「垃圾清运卡车」，ε4 型号清运效率偏低，会增加老年痴呆（阿尔茨海默病）风险。",
    "EGFR": "EGFR 是细胞表面的「生长油门踏板」，突变会让细胞疯长；但它也是很好的精准用药靶点。",
    "CFTR": "CFTR 是细胞表面的「黏液水龙头调节器」，双份突变会导致囊性纤维化，单份则无症状。",
    "G6PD": "G6PD 是红细胞的「抗氧化防锈涂层」，缺乏者需避开蚕豆与部分氧化性药物。",
    "MTHFR": "MTHFR 是叶酸代谢的「加工流水线工人」，常见低活性版本属于体质差异，注意补充叶酸即可。",
}

GENE_PLAIN_EN: Dict[str, str] = {
    "BRCA1": "BRCA1 is like a 'DNA car mechanic' inside cells; its mutation weakens the cell's "
    "ability to repair DNA, raising the lifetime risk of breast and ovarian cancer (though it is by no means inevitable).",
    "BRCA2": "BRCA2 is BRCA1's partner, delivering spare parts for DNA repair; its mutation also raises breast and ovarian cancer risk.",
    "TP53": "TP53 is the cell's 'emergency brake pad'; its mutation weakens the cell's ability to remove abnormal cells, raising the risk of several early-onset tumors.",
    "APOE": "APOE is the 'trash truck' in the brain; the ε4 form clears waste less efficiently and raises the risk of Alzheimer's disease in old age.",
    "EGFR": "EGFR is the 'growth gas pedal' on the cell surface; its mutation makes cells grow out of control, but it is also a great precision-drug target.",
    "CFTR": "CFTR is the 'mucus faucet regulator' on the cell surface; inheriting two mutated copies causes cystic fibrosis, while one copy causes no symptoms.",
    "G6PD": "G6PD is the 'anti-rust coating' of red blood cells; deficient individuals must avoid fava beans and certain oxidizing drugs.",
    "MTHFR": "MTHFR is the 'processing line worker' in folate metabolism; common low-activity variants are a constitutional difference — just ensure adequate folate intake.",
}

ZYGOSITY_PLAIN: Dict[str, str] = {
    "杂合": "「杂合」指两份基因拷贝中只有一份发生变异，另一份正常。",
    "杂合突变": "「杂合突变」指两份拷贝中只有一份变异，另一份正常。",
    "纯合": "「纯合」指两份基因拷贝都发生了变异。",
    "纯合突变": "「纯合突变」指两份拷贝都发生了变异。",
    "heterozygous": "「杂合 (heterozygous)」指两份拷贝中只有一份变异。",
    "homozygous": "「纯合 (homozygous)」指两份拷贝都发生了变异。",
}

ZYGOSITY_PLAIN_EN: Dict[str, str] = {
    "杂合": "'Heterozygous' means only one of your two gene copies has the variant; the other is normal.",
    "杂合突变": "'Heterozygous' means only one of your two gene copies has the variant; the other is normal.",
    "纯合": "'Homozygous' means both of your gene copies have the variant.",
    "纯合突变": "'Homozygous' means both of your gene copies have the variant.",
    "heterozygous": "'Heterozygous' means only one of your two gene copies has the variant.",
    "homozygous": "'Homozygous' means both of your gene copies have the variant.",
}

VARIANT_TERM_PLAIN: Dict[str, str] = {
    "pathogenic": "「致病性变异 (Pathogenic)」指该变异已被医学界证实与疾病风险升高明确相关。",
    "likely pathogenic": "「可能致病性变异 (Likely pathogenic)」指该变异与疾病风险高度相关。",
    "benign": "「良性变异 (Benign)」指该变异通常不会致病，无需担心。",
    "vus": "「意义未明变异 (VUS)」指该变异目前医学界尚无定论，暂时无需恐慌，持续研究中。",
    "uncertain": "「意义未明变异」指该变异目前尚无定论，暂时无需恐慌，持续研究中。",
}

VARIANT_TERM_PLAIN_EN: Dict[str, str] = {
    "pathogenic": "'Pathogenic' means this variant has been clearly linked to an increased disease risk.",
    "likely pathogenic": "'Likely pathogenic' means this variant is highly associated with increased risk.",
    "benign": "'Benign' means this variant usually does not cause disease — no need to worry.",
    "vus": "'Variant of uncertain significance (VUS)' means the medical community has no conclusion yet; no need to panic.",
    "uncertain": "'Variant of uncertain significance' — no conclusion yet; no need to panic.",
}


class DeepSeekPublicAgent:
    def __init__(self, config=None) -> None:
        self.config = config or settings

    # ------------------------------------------------------------ availability
    @property
    def available(self) -> bool:
        return bool(self.config.DEEPSEEK_API_KEY)

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }

    def _endpoint(self) -> str:
        return f"{self.config.DEEPSEEK_BASE_URL}/chat/completions"

    # ---------------------------------------------------------------- helpers
    async def _chat_json(self, messages: List[Dict[str, str]], model: str) -> Optional[str]:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.3,
            "stream": False,
            "response_format": {"type": "json_object"},
        }
        async with httpx.AsyncClient(timeout=self.config.DEEPSEEK_TIMEOUT) as client:
            resp = await client.post(self._endpoint(), json=payload, headers=self._headers())
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    # ---------------------------------------------------------- explain report
    async def explain_report(self, query: GeneticReportQuery) -> ReportExplanation:
        lang = getattr(query, "lang", "zh")
        raw = (query.raw_text or "").strip()
        disclaimer = DISCLAIMER if lang == "zh" else DISCLAIMER_EN
        if not raw:
            return ReportExplanation(
                what_found=(
                    "请先在上方粘贴您的基因检测报告内容，我们再为您逐条翻译。"
                    if lang == "zh"
                    else "Please paste your genetic report above first, and we will translate it for you."
                ),
                actual_impact="",
                next_steps="",
                lifestyle="",
                disclaimer=disclaimer,
            )

        if not self.available:
            return self._fallback_explain(raw, query)

        system_prompt = SYSTEM_PROMPT if lang == "zh" else SYSTEM_PROMPT_EN
        instruction = REPORT_JSON_INSTRUCTION if lang == "zh" else REPORT_JSON_INSTRUCTION_EN
        report_prefix = (
            f"{instruction}\n\n以下是用户的基因检测报告内容：\n{raw}"
            if lang == "zh"
            else f"{instruction}\n\nHere is the user's genetic report:\n{raw}"
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": report_prefix},
        ]
        try:
            content = await self._chat_json(messages, self.config.DEEPSEEK_MODEL)
            parsed = json.loads(content or "{}")
            return ReportExplanation(
                what_found=parsed.get("what_found", ""),
                actual_impact=parsed.get("actual_impact", ""),
                next_steps=parsed.get("next_steps", ""),
                lifestyle=parsed.get("lifestyle", ""),
                disclaimer=parsed.get("disclaimer", disclaimer),
                model=self.config.DEEPSEEK_MODEL,
            )
        except Exception:
            return self._fallback_explain(raw, query)

    def _fallback_explain(self, raw: str, query: GeneticReportQuery) -> ReportExplanation:
        """无 API Key 时的本地模板解释器，保证功能可用。"""
        lang = getattr(query, "lang", "zh")
        text = raw.lower()
        found_genes = [g for g in KNOWN_GENES if g.lower() in text]
        detected_gene = (query.detected_gene or "").strip().upper()
        if detected_gene and detected_gene not in found_genes:
            found_genes.insert(0, detected_gene)

        if lang == "en":
            zygosity_line = ""
            zygosity = (query.zygosity or "").strip() or raw
            for key, desc in ZYGOSITY_PLAIN_EN.items():
                if key.lower() in zygosity.lower():
                    zygosity_line = desc
                    break

            variant_line = ""
            for key, desc in VARIANT_TERM_PLAIN_EN.items():
                if key in text:
                    variant_line = desc
                    break

            gene_desc = ", ".join(
                f"{g} ({GENE_PLAIN_EN.get(g, 'No detailed explanation available yet')})"
                for g in found_genes
            ) or "Could not automatically identify the gene; please check the report content."

            what_found = (
                f"① What was actually found? {gene_desc}"
                + (f" {zygosity_line}" if zygosity_line else "")
                + (f" {variant_line}" if variant_line else "")
            )
            actual_impact = (
                "② What does this mean for me? First, stay calm: carrying a mutation does NOT "
                "mean you are already ill. It represents an 'increased risk (susceptibility)', "
                "and in most cases it can be effectively prevented and managed through early "
                "screening, lifestyle changes and standard treatment."
            )
            next_steps = (
                "③ What should I do next? Bring your report to a 'clinical genetics clinic' or "
                "the relevant specialty at a hospital, where a doctor will assess and design an "
                "individualized screening plan (e.g. breast MRI, colonoscopy, tumor markers), and "
                "decide whether first-degree relatives should be tested."
            )
            lifestyle = (
                "④ How should I eat and exercise? Maintain a healthy weight, eat a balanced diet "
                "(more dark vegetables and whole grains), quit smoking and limit alcohol, exercise "
                "regularly, get enough sleep, and have regular check-ups as advised by your doctor."
            )
            return ReportExplanation(
                what_found=what_found,
                actual_impact=actual_impact,
                next_steps=next_steps,
                lifestyle=lifestyle,
                disclaimer=DISCLAIMER_EN,
                offline_fallback=True,
            )

        zygosity_line = ""
        zygosity = (query.zygosity or "").strip() or raw
        for key, desc in ZYGOSITY_PLAIN.items():
            if key.lower() in zygosity.lower():
                zygosity_line = desc
                break

        variant_line = ""
        for key, desc in VARIANT_TERM_PLAIN.items():
            if key in text:
                variant_line = desc
                break

        gene_desc = "、".join(
            f"{g}（{GENE_PLAIN.get(g, '暂未收录详细解释')}）" for g in found_genes
        ) or "未能自动识别具体基因，请确认报告内容或切换到专业模式查看。"

        what_found = (
            f"① 到底测出了什么？{gene_desc}"
            + (f" {zygosity_line}" if zygosity_line else "")
            + (f" {variant_line}" if variant_line else "")
        )
        actual_impact = (
            "② 会对我造成什么实际影响？首先请保持冷静：携带基因突变并不等于已经患病，"
            "它代表的是一种「患病风险升高（易感性）」，绝大多数情况都可以通过早期筛查、"
            "生活方式干预和规范治疗来有效预防与管理。"
        )
        next_steps = (
            "③ 接下来我该去医院做什么？建议携带检测报告到正规医院的「临床遗传咨询门诊」"
            "或相应专科就诊，由医生评估后制定个体化筛查方案（如乳腺增强磁共振、"
            "肠镜、肿瘤标志物等），并决定是否需要对直系亲属做位点检测。"
        )
        lifestyle = (
            "④ 日常生活该怎么吃、怎么动？保持健康体重、均衡饮食（多吃深色蔬菜与全谷物）、"
            "戒烟限酒、规律运动、保证睡眠，并按医生建议定期体检。"
        )
        return ReportExplanation(
            what_found=what_found,
            actual_impact=actual_impact,
            next_steps=next_steps,
            lifestyle=lifestyle,
            disclaimer=DISCLAIMER,
            offline_fallback=True,
        )

    # ------------------------------------------------------------------- chat
    async def chat_qa_stream(self, message: str, history: Optional[List[Dict[str, str]]] = None, lang: str = "zh") -> AsyncIterator[str]:
        """SSE 流式问答。生成 data: {...} 事件块，以 data: [DONE] 结束。"""
        if not self.available:
            answer = self._fallback_chat(message, lang)
            for piece in answer:
                yield self._sse({"content": piece})
            yield self._sse({"done": True})
            return

        system_prompt = SYSTEM_PROMPT if lang == "zh" else SYSTEM_PROMPT_EN
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": message})

        payload = {
            "model": self.config.DEEPSEEK_MODEL,
            "messages": messages,
            "temperature": 0.4,
            "stream": True,
        }
        try:
            async with httpx.AsyncClient(timeout=self.config.DEEPSEEK_TIMEOUT) as client:
                async with client.stream(
                    "POST", self._endpoint(), json=payload, headers=self._headers()
                ) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if not line or not line.startswith("data:"):
                            continue
                        data_str = line[len("data:"):].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data_str)
                            delta = chunk["choices"][0]["delta"].get("content", "")
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue
                        if delta:
                            yield self._sse({"content": delta})
        except httpx.HTTPError:
            for piece in self._fallback_chat(message, lang):
                yield self._sse({"content": piece})
        yield self._sse({"done": True})

    @staticmethod
    def _sse(payload: Dict[str, Any]) -> str:
        return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"

    def _fallback_chat(self, message: str, lang: str = "zh") -> List[str]:
        text = message.lower()
        if lang == "en":
            for gene in KNOWN_GENES:
                if gene.lower() in text:
                    return [
                        f"About {gene}: {GENE_PLAIN_EN.get(gene, '')}",
                        "I recommend bringing your report to a hospital clinical genetics clinic for individualized advice.",
                        DISCLAIMER_EN,
                    ]
            return [
                "I currently don't have the DeepSeek API connected, so I can only provide basic local answers.",
                "I recommend consulting a genetic counselor at a hospital.",
                DISCLAIMER_EN,
            ]
        for gene in KNOWN_GENES:
            if gene.lower() in text:
                return [
                    f"关于 {gene}：{GENE_PLAIN.get(gene, '')}",
                    "建议您携带检测报告前往医院临床遗传咨询门诊，由医生给出个体化建议。",
                    DISCLAIMER,
                ]
        return [
            "我目前没有接入 DeepSeek API，暂时只能提供本地基础回答。",
            "建议您携带检测报告咨询正规医院的临床遗传咨询师。",
            DISCLAIMER,
        ]
