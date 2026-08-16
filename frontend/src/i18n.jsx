import { createContext, useContext, useState } from 'react'

export const translations = {
  zh: {
    brand_name: 'DecodeGene 解码基因',
    mode_simple: '🌱 小白通俗模式',
    mode_pro: '🔬 专业科研模式',
    hero_title: '让复杂的基因科学，人人都看得懂',
    hero_sub: '用生活化的比喻，读懂你的基因检测报告与家族遗传风险',
    search_placeholder: '搜索基因 / 疾病，如：BRCA1、乳腺癌、老年痴呆、rxa（拼音）…',
    search_btn: '搜索',
    clear_btn: '清除',
    loading: '正在加载基因知识库…',
    search_result: '搜索「{query}」共找到 {count} 条相关结果',
    empty: '暂无数据。请先运行后端并生成数据。',
    browse_title: '📚 浏览完整基因知识库',
    browse_more: '加载更多基因',
    browse_loading: '加载中…',
    browse_done: '已显示全部批量基因',
    footer_disclaimer:
      '⚠️ 免责声明：本工具由开源社区与 AI 提供，仅供科学普及与健康常识参考，不能替代执业医师、临床遗传咨询师的诊断与治疗决策。',

    no_pro_summary: '（暂无专业摘要）',
    no_metaphor: '暂无比喻',
    bulk_no_metaphor: '🔬 此条目来自 ClinVar 批量数据，暂无比喻与通俗解释，请切换到「专业科研模式」查看证据。',
    badge_pending: '待评估',
    overall_score: '综合关联分',
    no_rating: '暂无评级',
    screening_advice: '🩺 筛查建议：',
    open_checklist: '📋 生成《门诊就医提问清单》',

    rd_title: '📄 基因检测报告「白话文翻译机」',
    rd_desc: '粘贴报告中的突变位点（如 BRCA1 c.5266dupC 杂合突变，Pathogenic），一键翻译成大白话。',
    rd_placeholder: '例如：我的报告写着 BRCA1 c.5266dupC (p.Gln1756Profs) 杂合突变，ClinVar 提示 Pathogenic…',
    rd_btn: '🔓 立即翻译',
    rd_loading: '正在翻译…',
    rd_error: '解析失败，请确认后端服务已启动。',
    rd_offline: 'ℹ️ 当前为本地离线解释（未配置 DeepSeek API Key）。',
    sec_what: '到底测出了什么？',
    sec_impact: '会对我造成什么实际影响？',
    sec_next: '接下来我该去医院做什么？',
    sec_lifestyle: '日常生活该怎么吃、怎么动？',

    cl_title: '📋 门诊就医提问清单',
    cl_loading: '加载中…',
    cl_failed: '加载失败',
    copy_btn: '📋 复制到微信',
    copied_btn: '✅ 已复制',
    print_btn: '🖨️ 打印',

    fs_title: '🧬 家族遗传风险模拟器',
    fs_desc: '选择遗传模式与父母状态，动态推算下一代的患病概率。',
    pattern_label: '遗传模式',
    father_label: '父亲状态',
    mother_label: '母亲状态',
    calc_btn: '▶ 计算',
    calc_loading: '计算中…',
    bar_affected: '患病',
    bar_carrier: '携带',
    bar_normal: '正常',
    boy_girl_hint: '👦 男孩患病 {male}% · 👧 女孩患病 {female}%、携带 {carrier}%',
    pattern_AD: '常染色体显性 (AD)',
    pattern_AR: '常染色体隐性 (AR)',
    pattern_XR: 'X 连锁隐性 (XR)',
    pattern_XD: 'X 连锁显性 (XD)',
    status_normal: '正常',
    status_carrier: '无症状携带者',
    status_affected: '患病 / 携带致病',

    myth_title: '❌ 基因健康「谣言粉碎机」',
    myth_desc: '破除常见的基因迷信，用科学还你安心。',
    myth_related: '关联：',

    ai_title: '🩺 问医生 · AI 基因健康助手',
    ai_desc: '向 AI 咨询遗传健康问题（回答仅供参考，请以执业医师意见为准）。',
    ai_welcome:
      '您好，我是 DecodeGene 的 AI 基因健康助手。您可以问我关于基因、遗传、报告解读等问题，我会尽量用大白话为您解答。',
    ai_placeholder: '例如：我测出 BRCA1 突变，一定会得乳腺癌吗？',
    send_btn: '发送',
    sending_btn: '回复中…',
    ai_error: '抱歉，暂时无法连接 AI 服务，请确认后端已启动。',
  },

  en: {
    brand_name: 'DecodeGene',
    mode_simple: '🌱 Simple Mode',
    mode_pro: '🔬 Expert Mode',
    hero_title: 'Making complex genetics understandable for everyone',
    hero_sub: 'Understand your genetic reports and family inheritance risks through everyday metaphors',
    search_placeholder: 'Search genes or diseases, e.g. BRCA1, breast cancer, Alzheimer…',
    search_btn: 'Search',
    clear_btn: 'Clear',
    loading: 'Loading gene knowledge base…',
    search_result: 'Found {count} result(s) for "{query}"',
    empty: 'No data yet. Please start the backend and generate data.',
    browse_title: '📚 Browse the full gene knowledge base',
    browse_more: 'Load more genes',
    browse_loading: 'Loading…',
    browse_done: 'All bulk genes are displayed',
    footer_disclaimer:
      '⚠️ Disclaimer: This tool is provided by the open-source community and AI for educational purposes only. It is not a substitute for diagnosis or treatment by a licensed physician or genetic counselor.',

    no_pro_summary: '(No expert summary yet)',
    no_metaphor: 'No metaphor yet',
    bulk_no_metaphor: '🔬 This entry comes from bulk ClinVar data and has no metaphor yet. Switch to Expert Mode to see the evidence.',
    badge_pending: 'Pending',
    overall_score: 'Overall score',
    no_rating: 'No rating',
    screening_advice: '🩺 Screening:',
    open_checklist: '📋 Generate doctor checklist',

    rd_title: '📄 Genetic Report Translator',
    rd_desc: 'Paste a variant from your report (e.g. BRCA1 c.5266dupC, Pathogenic) and translate it into plain language.',
    rd_placeholder: 'e.g. My report says BRCA1 c.5266dupC (p.Gln1756Profs) heterozygous, ClinVar: Pathogenic…',
    rd_btn: '🔓 Translate',
    rd_loading: 'Translating…',
    rd_error: 'Failed to parse. Please make sure the backend is running.',
    rd_offline: 'ℹ️ Running in offline mode (no DeepSeek API key configured).',
    sec_what: 'What was actually found?',
    sec_impact: 'What does this mean for me?',
    sec_next: 'What should I do next (see a doctor)?',
    sec_lifestyle: 'How should I eat and exercise?',

    cl_title: '📋 Doctor Checklist',
    cl_loading: 'Loading…',
    cl_failed: 'Failed to load',
    copy_btn: '📋 Copy',
    copied_btn: '✅ Copied',
    print_btn: '🖨️ Print',

    fs_title: '🧬 Family Inheritance Simulator',
    fs_desc: 'Pick an inheritance pattern and parental status to estimate the next generation’s risk.',
    pattern_label: 'Pattern',
    father_label: 'Father status',
    mother_label: 'Mother status',
    calc_btn: '▶ Calculate',
    calc_loading: 'Calculating…',
    bar_affected: 'Affected',
    bar_carrier: 'Carrier',
    bar_normal: 'Normal',
    boy_girl_hint: '👦 Boys affected {male}% · 👧 Girls affected {female}%, carriers {carrier}%',
    pattern_AD: 'Autosomal dominant (AD)',
    pattern_AR: 'Autosomal recessive (AR)',
    pattern_XR: 'X-linked recessive (XR)',
    pattern_XD: 'X-linked dominant (XD)',
    status_normal: 'Normal',
    status_carrier: 'Asymptomatic carrier',
    status_affected: 'Affected / carries pathogenic variant',

    myth_title: '❌ Gene Myth Buster',
    myth_desc: 'Debunk common genetic myths with science.',
    myth_related: 'Related: ',

    ai_title: '🩺 Ask the Doctor · AI Health Assistant',
    ai_desc: 'Ask the AI about genetic health (answers are informational only — always consult a physician).',
    ai_welcome:
      'Hi, I am the DecodeGene AI health assistant. Ask me about genes, inheritance, or your report — I will answer in plain language.',
    ai_placeholder: 'e.g. I have a BRCA1 mutation — will I definitely get breast cancer?',
    send_btn: 'Send',
    sending_btn: 'Replying…',
    ai_error: 'Sorry, could not reach the AI service. Please make sure the backend is running.',
  },
}

const LanguageContext = createContext(null)

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState('zh')

  const t = (key, vars) => {
    let s = translations[lang]?.[key] ?? translations.zh[key] ?? key
    if (vars) {
      for (const [k, v] of Object.entries(vars)) {
        s = s.replaceAll(`{${k}}`, v)
      }
    }
    return s
  }

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  return useContext(LanguageContext)
}
