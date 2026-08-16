"""内置高频基因的生活比喻库 (Visual Metaphor Library).

每一条目把晦涩的分子机制翻译成 5 岁小孩都能听懂的日常生活画面，
是 DecodeGene「白话文比喻引擎」的核心数据。
"""
from __future__ import annotations

from typing import Any, Dict

# 高频基因 -> 生活比喻 (标题 + 故事)
METAPHORS: Dict[str, Dict[str, str]] = {
    "BRCA1": {
        "title": "🧬 细胞里的【DNA 汽车维修工程师】",
        "story": "我们的细胞每天都在高速运转，DNA 难免会发生小故障（磨损破裂）。"
        "BRCA1 就像一位经验丰富的随车高级维修工，发现故障就会立刻修好。"
        "如果维修工突变生病（罢工），坏掉的零件没修好就继续上路，日积月累，"
        "车子出重大事故（恶性肿瘤）的几率就会比常人高出很多。",
    },
    "BRCA2": {
        "title": "🧰 与 BRCA1 并肩的【第二维修技工】",
        "story": "BRCA2 是 BRCA1 的搭档，负责递送修补 DNA 的备用零件。"
        "当这位技工也失职时，DNA 断链无法精准修复，同样会提升乳腺癌、卵巢癌等风险。",
    },
    "TP53": {
        "title": "🚨 细胞里的【紧急制动刹车片】",
        "story": "每个细胞都像一辆车，TP53 就是负责安检的刹车片与保安。"
        "它一旦发现细胞变坏（DNA 严重受损），会立即踩下刹车、命令异常细胞自我了断。"
        "如果刹车片失灵，坏细胞便毫无阻拦地疯狂繁殖，最终演变成肿瘤。",
    },
    "APOE": {
        "title": "🧠 大脑里的【垃圾清运卡车】",
        "story": "大脑工作时会产生有害的代谢废弃物（黏糊糊的淀粉样蛋白）。"
        "APOE 就像每天在大脑巡逻清运垃圾的清洁车。它有三种型号（ε2、ε3、ε4），"
        "ε4 型号清运效率较慢，垃圾容易在脑内堆积，久了就增加老年痴呆风险。",
    },
    "EGFR": {
        "title": "🚦 细胞表面的【生长油门踏板】",
        "story": "正常细胞只有收到生长指令才会轻踩油门。若 EGFR 突变，"
        "就像油门被卡死在「踩到底」，细胞不受控制地疯长成肺癌。"
        "好消息是现代医学发明了精准的「刹车钥匙」（靶向药），可以卡住油门让癌细胞停下。",
    },
    "CFTR": {
        "title": "🚰 细胞表面的【黏液水龙头调节器】",
        "story": "CFTR 负责调节细胞表面的盐与水进出，就像控制黏液浓稠度的水龙头。"
        "若这个水龙头坏了，肺部和消化道里的黏液会变得又浓又黏，堵住气道与胰管，"
        "引发反复感染与消化障碍（囊性纤维化）。",
    },
    "G6PD": {
        "title": "🛡️ 红细胞上的【抗氧化防锈涂层】",
        "story": "红细胞每天搬运氧气，容易被氧化「生锈」。G6PD 就像给红细胞刷的一层防锈涂层。"
        "缺少这层涂层的人，一旦误吃蚕豆或某些药物，红细胞会大量破裂（溶血），"
        "这就是俗称的「蚕豆病」。",
    },
    "MTHFR": {
        "title": "🔄 体内叶酸代谢的【加工流水线工人】",
        "story": "MTHFR 是负责把叶酸加工成身体可用活性形式的流水线工人。"
        "部分人携带效率略低的版本，体内叶酸利用率下降，可能影响同型半胱氨酸水平。"
        "这属于常见「体质差异」，多数人只需注意补充富含叶酸的蔬菜即可。",
    },
    "MLH1": {
        "title": "🧩 细胞里的【DNA 拼字校对员】",
        "story": "细胞每次分裂都要抄写一整本 DNA「说明书」，难免抄错几个字母。"
        "MLH1 就像一位一丝不苟的校对员，负责找出并改正抄错的地方。"
        "若校对员失职，错误越积越多，最终容易在肠道等器官「印」出癌细胞。",
    },
    "HFE": {
        "title": "🚪 肠道里的【铁元素门卫】",
        "story": "我们的身体需要铁，但铁太多也会「生锈」伤害肝脏。"
        "HFE 就像肠道里控制铁吸收量的门卫。若门卫偷懒（突变），铁被过量放行，"
        "常年堆积在肝、心、胰腺等器官，引发「血色病」。",
    },
}


# 额外新增的完整基因-疾病关联条目 (补充 demo 数据，丰富后端知识库)
EXTRA_ASSOCIATIONS: list = [
    {
        "association_id": "GDA_TP53_LI_FRAUMENI",
        "gene": {
            "symbol": "TP53",
            "name": "Tumor Protein P53",
            "chinese_name": "肿瘤抑制蛋白 P53",
            "chromosome": "17 号染色体",
            "metaphor": {
                "title": METAPHORS["TP53"]["title"],
                "story": METAPHORS["TP53"]["story"],
            },
            "plain_summary": "TP53 被称为「基因组守护者」，负责识别并清除变坏的细胞。"
            "携带其致病突变的人患多种早发性肿瘤的风险升高，需进行规律的全套肿瘤筛查。",
            "academic_summary": "TP53 编码转录因子 p53，介导 DNA 损伤后的细胞周期阻滞、"
            "DNA 修复与凋亡。生殖系致病变异导致 Li-Fraumeni 综合征，"
            "显著提升肉瘤、乳腺癌、脑肿瘤、肾上腺皮质癌等早发风险。",
        },
        "disease": {
            "id": "MONDO:0018875",
            "name": "Li-Fraumeni syndrome",
            "chinese_name": "李-佛美尼综合征 (遗传性多发性肿瘤综合征)",
            "categories": ["遗传性肿瘤综合征", "恶性肿瘤"],
            "severity_badge": "⚠️ 需高度关注 (需系统筛查)",
        },
        "evidence": {
            "overall_score": 0.95,
            "plain_rating": "⭐️⭐️⭐️⭐️⭐️ 国际医学界最高级别确证 (Definitive)",
            "clinvar_pathogenic_count": 640,
            "clinvar_summary_chinese": "已收录 600+ 明确致病变异位点",
            "opentargets_score": 0.93,
        },
        "lifestyle_prevention": {
            "screening_advice": "建议自幼年/青年起进入 Li-Fraumeni 专项筛查方案："
            "每年全身体检、腹部超声、乳腺磁共振 (女性) 等，由遗传门诊制定个体化计划。",
            "lifestyle_tips": [
                "避免不必要的放射性检查（如反复 CT），减少辐射暴露",
                "严格防晒、戒烟限酒，维持健康体重",
                "保持规律运动与充足睡眠，提升整体免疫力"
            ],
        },
        "doctor_checklist": {
            "specialty": "肿瘤科 / 临床遗传门诊 / 遗传咨询师",
            "questions": [
                "医生，我确诊携带 TP53 致病突变，应从几岁开始、每隔多久做一次肿瘤筛查？",
                "平时出现哪些症状（如不明原因肿块、持续骨痛）需要立即就医？",
                "我的子女是否需要尽早做基因检测与遗传咨询？"
            ],
        },
        "myth_buster": {
            "myth": "“TP53 突变就是「癌症开关」，携带者注定会得很多种癌症吗？”",
            "truth": "不是！TP53 突变升高的是多种肿瘤的「风险」，"
            "通过规范筛查实现早发现早治疗，绝大多数携带者都能获得良好预后。",
        },
    },
    {
        "association_id": "GDA_CFTR_CYSTIC_FIBROSIS",
        "gene": {
            "symbol": "CFTR",
            "name": "CF Transmembrane Conductance Regulator",
            "chinese_name": "囊性纤维化跨膜传导调节因子",
            "chromosome": "7 号染色体",
            "metaphor": {
                "title": METAPHORS["CFTR"]["title"],
                "story": METAPHORS["CFTR"]["story"],
            },
            "plain_summary": "CFTR 突变导致的囊性纤维化是一种常染色体隐性遗传病。"
            "只有从父母双方各遗传到一份致病拷贝才会发病；只携带一份者无症状，"
            "属于「携带者」。",
            "academic_summary": "CFTR 编码 cAMP 依赖的氯离子通道，调节上皮表面液体平衡。"
            "双等位基因致病变异导致呼吸道、胰腺、肠道黏液异常黏稠，引发慢性感染与营养不良。",
        },
        "disease": {
            "id": "MONDO:0009061",
            "name": "Cystic fibrosis",
            "chinese_name": "囊性纤维化",
            "categories": ["单基因遗传病", "常染色体隐性遗传"],
            "severity_badge": "⚠️ 需系统管理 (现代治疗已大幅改善预后)",
        },
        "evidence": {
            "overall_score": 0.97,
            "plain_rating": "⭐️⭐️⭐️⭐️⭐️ 明确致病基因 (Definitive)",
            "clinvar_pathogenic_count": 2100,
            "clinvar_summary_chinese": "已收录 2000+ 明确致病与功能变异位点",
            "opentargets_score": 0.98,
        },
        "lifestyle_prevention": {
            "screening_advice": "新生儿出生后会进行足跟血筛查；确诊后由呼吸科与营养科"
            "联合长期管理，配合每日气道廓清与靶向调节剂（如 CFTR 调节剂）。",
            "lifestyle_tips": [
                "规律进行肺部物理治疗，保持气道通畅",
                "高热量高营养饮食，补充脂溶性维生素与胰酶",
                "按时接种疫苗，避免交叉感染"
            ],
        },
        "doctor_checklist": {
            "specialty": "呼吸内科 / 儿科 / 遗传门诊",
            "questions": [
                "医生，我的孩子确诊囊性纤维化，是否需要做 CFTR 调节剂基因匹配检测？",
                "日常气道廓清和用药的频率应如何安排？",
                "我们夫妇若再生育，通过产前诊断或三代试管 (PGT) 如何避免遗传？"
            ],
        },
        "myth_buster": {
            "myth": "“囊性纤维化是绝症，孩子活不长了吗？”",
            "truth": "并非如此！随着 CFTR 调节剂等精准治疗问世，"
            "患者预期寿命和生活质量已得到极大改善，早诊断早干预非常关键。",
        },
    },
    {
        "association_id": "GDA_G6PD_DEFICIENCY",
        "gene": {
            "symbol": "G6PD",
            "name": "Glucose-6-Phosphate Dehydrogenase",
            "chinese_name": "葡萄糖-6-磷酸脱氢酶",
            "chromosome": "X 染色体",
            "metaphor": {
                "title": METAPHORS["G6PD"]["title"],
                "story": METAPHORS["G6PD"]["story"],
            },
            "plain_summary": "G6PD 缺乏症（蚕豆病）是 X 连锁隐性遗传。"
            "只要远离蚕豆和特定药物（如磺胺类、阿司匹林），绝大多数携带者一生健康无虞。",
            "academic_summary": "G6PD 是磷酸戊糖途径的限速酶，维持红细胞 NADPH 水平以对抗氧化应激。"
            "缺乏时，接触氧化性食物/药物会诱发急性溶血性贫血。",
        },
        "disease": {
            "id": "MONDO:0005778",
            "name": "Glucose-6-phosphate dehydrogenase deficiency",
            "chinese_name": "葡萄糖-6-磷酸脱氢酶缺乏症 (蚕豆病)",
            "categories": ["单基因遗传病", "X 连锁隐性遗传"],
            "severity_badge": "✅ 可防可控 (避开诱因即可)",
        },
        "evidence": {
            "overall_score": 0.96,
            "plain_rating": "⭐️⭐️⭐️⭐️⭐️ 明确致病基因 (Definitive)",
            "clinvar_pathogenic_count": 300,
            "clinvar_summary_chinese": "已收录多种酶活性分级变异",
            "opentargets_score": 0.95,
        },
        "lifestyle_prevention": {
            "screening_advice": "新生儿出生后部分地区会做 G6PD 筛查；确诊后终身随身携带"
            "「禁食/禁药清单」卡片，就诊时主动告知医生。",
            "lifestyle_tips": [
                "绝对禁食蚕豆及其制品（如蚕豆粉丝、豆瓣酱）",
                "禁用磺胺类、阿司匹林、维生素 K 等氧化性药物（用药前咨询医生/药师）",
                "避免接触樟脑丸（萘）等强氧化物质"
            ],
        },
        "doctor_checklist": {
            "specialty": "儿科 / 血液科 / 遗传门诊",
            "questions": [
                "医生，我确诊 G6PD 缺乏，平时开药时有哪些药物需要特别避开？",
                "出现哪些症状（如尿色变深、乏力、黄疸）提示可能发生溶血，需要立即就医？",
                "我的家族里其他人需要一起做 G6PD 检测吗？"
            ],
        },
        "myth_buster": {
            "myth": "“得了蚕豆病，这辈子什么药都不能吃了吗？”",
            "truth": "不是！只要避开明确的氧化性诱因，绝大多数药物仍可安全使用，"
            "关键是就诊时主动告知医生自己携带 G6PD 缺乏。",
        },
    },
    {
        "association_id": "GDA_BRCA2_HBOC",
        "gene": {
            "symbol": "BRCA2",
            "name": "Breast Cancer Susceptibility Gene 2",
            "chinese_name": "乳腺癌易感基因 2 号",
            "chromosome": "13 号染色体",
            "metaphor": {
                "title": METAPHORS["BRCA2"]["title"],
                "story": METAPHORS["BRCA2"]["story"],
            },
            "plain_summary": "BRCA2 与 BRCA1 并肩作战，负责递送修复 DNA 的备用零件。"
            "携带致病突变会升高乳腺癌、卵巢癌、胰腺癌及男性乳腺癌的风险，"
            "但绝非必然发病，早期筛查可有效预防。",
            "academic_summary": "BRCA2 与 RAD51 直接结合，介导同源重组中 RAD51 纤丝装配，"
            "维护 DNA 双链断裂的无差错修复。生殖系致病变异导致遗传性乳腺癌-卵巢癌综合征，"
            "亦与范可尼贫血 D1 型及前列腺/胰腺癌易感相关。",
        },
        "disease": {
            "id": "MONDO:0011200",
            "name": "Hereditary breast-ovarian cancer syndrome",
            "chinese_name": "遗传性乳腺癌-卵巢癌综合征",
            "categories": ["恶性肿瘤", "遗传性肿瘤综合征"],
            "severity_badge": "⚠️ 需高度关注 (科学可防可治)",
        },
        "evidence": {
            "overall_score": 0.95,
            "plain_rating": "⭐️⭐️⭐️⭐️⭐️ 国际医学界最高级别确证 (Definitive)",
            "clinvar_pathogenic_count": 4100,
            "clinvar_summary_chinese": "已收录 4000+ 明确致病变异位点",
            "opentargets_score": 0.93,
        },
        "lifestyle_prevention": {
            "screening_advice": "建议女性从 25 岁起每 6-12 个月乳腺专科体检，30 岁起每年"
            "乳腺增强磁共振 (MRI) 联合钼靶；男性携带者关注乳腺癌、前列腺癌与胰腺癌筛查。",
            "lifestyle_tips": [
                "保持健康体重，规律作息，戒烟限酒",
                "女性在医生指导下可考虑口服避孕药降低卵巢癌风险（需权衡利弊）",
                "有生育计划者可咨询三代试管 (PGT) 阻断技术"
            ],
        },
        "doctor_checklist": {
            "specialty": "乳腺外科 / 肿瘤科 / 临床遗传门诊",
            "questions": [
                "医生，我的 BRCA2 突变报告提示前列腺癌/胰腺癌风险，男性亲属需要筛查吗？",
                "从几岁开始、间隔多久做乳腺增强磁共振与卵巢相关检查？",
                "是否建议预防性手术（如乳腺/卵巢切除）？风险和收益如何权衡？"
            ],
        },
        "myth_buster": {
            "myth": "“BRCA2 突变是不是也像 BRCA1 一样，一定会得乳腺癌？”",
            "truth": "不是！BRCA2 突变同样只是升高风险（终身乳腺癌风险约 50%~70%），"
            "通过规律筛查和干预，绝大多数携带者都能健康生活。",
        },
    },
    {
        "association_id": "GDA_MLH1_LYNCH",
        "gene": {
            "symbol": "MLH1",
            "name": "MutL Homolog 1",
            "chinese_name": "错配修复蛋白 MLH1",
            "chromosome": "3 号染色体",
            "metaphor": {
                "title": METAPHORS["MLH1"]["title"],
                "story": METAPHORS["MLH1"]["story"],
            },
            "plain_summary": "MLH1 突变是林奇综合征最常见的原因之一，"
            "显著升高结直肠癌、子宫内膜癌、胃癌等风险。规律肠镜筛查可大大降低死亡率。",
            "academic_summary": "MLH1 参与 DNA 错配修复 (MMR)，与 PMS2 形成异源二聚体，"
            "识别并切除复制过程中的碱基错配。生殖系致病变异导致微卫星不稳定，"
            "诱发林奇综合征相关的多器官肿瘤。",
        },
        "disease": {
            "id": "MONDO:0007356",
            "name": "Lynch syndrome",
            "chinese_name": "林奇综合征 (遗传性非息肉病性结直肠癌)",
            "categories": ["遗传性肿瘤综合征", "消化系统肿瘤"],
            "severity_badge": "⚠️ 需规律肠镜筛查 (可防可治)",
        },
        "evidence": {
            "overall_score": 0.96,
            "plain_rating": "⭐️⭐️⭐️⭐️⭐️ 国际医学界最高级别确证 (Definitive)",
            "clinvar_pathogenic_count": 1500,
            "clinvar_summary_chinese": "已收录 1500+ 明确致病/疑似致病变异",
            "opentargets_score": 0.94,
        },
        "lifestyle_prevention": {
            "screening_advice": "建议从 20-25 岁起每 1-2 年做一次结肠镜检查；女性关注子宫内膜癌"
            "相关筛查（如经阴道超声），由遗传门诊制定个体化随访方案。",
            "lifestyle_tips": [
                "多吃膳食纤维与新鲜蔬果，少吃红肉与加工肉制品",
                "戒烟限酒，保持健康体重与规律运动",
                "出现便血、排便习惯改变、不明原因消瘦时尽早就医"
            ],
        },
        "doctor_checklist": {
            "specialty": "消化内科 / 结直肠外科 / 临床遗传门诊",
            "questions": [
                "医生，我确诊林奇综合征，从几岁开始、每隔多久做一次肠镜？",
                "除结直肠外，胃、子宫内膜等部位需要额外筛查吗？",
                "我的兄弟姐妹和子女是否都需要做基因检测？"
            ],
        },
        "myth_buster": {
            "myth": "“林奇综合征一定会得肠癌，只能等着发病吗？”",
            "truth": "完全错误！通过从青年期开始的规律肠镜筛查，"
            "可在息肉阶段直接切除，显著降低肠癌发生率和死亡率。",
        },
    },
    {
        "association_id": "GDA_MTHFR_HOMOCYSTEINE",
        "gene": {
            "symbol": "MTHFR",
            "name": "Methylenetetrahydrofolate Reductase",
            "chinese_name": "亚甲基四氢叶酸还原酶",
            "chromosome": "1 号染色体",
            "metaphor": {
                "title": METAPHORS["MTHFR"]["title"],
                "story": METAPHORS["MTHFR"]["story"],
            },
            "plain_summary": "MTHFR 参与叶酸代谢，常见低活性版本（如 C677T 纯合）"
            "会让叶酸利用率略降，可能使同型半胱氨酸轻度升高。多数人补充富含叶酸的食物即可，"
            "不必过度焦虑。",
            "academic_summary": "MTHFR 催化 5,10-亚甲基四氢叶酸还原为 5-甲基四氢叶酸，"
            "是叶酸循环与同型半胱氨酸再甲基化的关键酶。C677T 纯合变异使酶活性下降约 70%，"
            "属于常见良性体质差异。",
        },
        "disease": {
            "id": "MONDO:0009634",
            "name": "Hyperhomocysteinemia",
            "chinese_name": "同型半胱氨酸血症 (叶酸代谢障碍)",
            "categories": ["代谢相关体质差异", "营养代谢"],
            "severity_badge": "💡 常见体质差异 (多数无需特殊处理)",
        },
        "evidence": {
            "overall_score": 0.6,
            "plain_rating": "⭐️⭐️⭐️ 有科学关联但需个体化解读",
            "clinvar_pathogenic_count": 40,
            "clinvar_summary_chinese": "常见多态性，多为良性/低风险",
            "opentargets_score": 0.55,
        },
        "lifestyle_prevention": {
            "screening_advice": "若血检发现同型半胱氨酸升高，建议在医生指导下补充叶酸/维生素 B 族，"
            "并定期复查；常规健康人群无需专项筛查。",
            "lifestyle_tips": [
                "多吃深绿色叶菜（菠菜、西兰花）、豆类与全谷物",
                "必要时在医生指导下补充叶酸、维生素 B6 与 B12",
                "戒烟限酒，保持均衡饮食即可"
            ],
        },
        "doctor_checklist": {
            "specialty": "全科 / 营养科 / 心内科",
            "questions": [
                "医生，我的 MTHFR 检测显示 C677T 纯合，需要治疗吗？",
                "我的同型半胱氨酸偏高，需要补充叶酸吗？剂量多少？",
                "备孕期间是否需要额外补充叶酸或特殊类型的叶酸？"
            ],
        },
        "myth_buster": {
            "myth": "“MTHFR 变异就是「叶酸代谢障碍」，会导致流产、自闭、各种病吗？”",
            "truth": "夸大其词！MTHFR 多态性极其常见（约一半人群携带），"
            "绝大多数人毫无症状，只需均衡饮食、必要时补叶酸即可，"
            "不应被商业检测恐吓营销。",
        },
    },
    {
        "association_id": "GDA_HFE_HEMOCHROMATOSIS",
        "gene": {
            "symbol": "HFE",
            "name": "Homeostatic Iron Regulator",
            "chinese_name": "遗传性血色病基因 HFE",
            "chromosome": "6 号染色体",
            "metaphor": {
                "title": METAPHORS["HFE"]["title"],
                "story": METAPHORS["HFE"]["story"],
            },
            "plain_summary": "HFE 突变（如 C282Y 纯合）会导致肠道过量吸收铁，"
            "长期堆积损伤肝脏、心脏与胰腺。早发现后通过定期放血即可轻松控制，预后良好。",
            "academic_summary": "HFE 与转铁蛋白受体相互作用，负调控肠上皮对铁的摄取。"
            "C282Y 纯合变异破坏该负反馈，导致铁超载，即遗传性血色病 (HFE 型)。",
        },
        "disease": {
            "id": "MONDO:0006507",
            "name": "Hereditary hemochromatosis",
            "chinese_name": "遗传性血色病 (铁过载)",
            "categories": ["代谢性遗传病", "常染色体隐性遗传"],
            "severity_badge": "✅ 可防可控 (定期放血即可)",
        },
        "evidence": {
            "overall_score": 0.93,
            "plain_rating": "⭐️⭐️⭐️⭐️⭐️ 明确致病基因 (Definitive)",
            "clinvar_pathogenic_count": 25,
            "clinvar_summary_chinese": "C282Y/H63D 为经典致病变异",
            "opentargets_score": 0.9,
        },
        "lifestyle_prevention": {
            "screening_advice": "确诊后每 3-6 个月抽血监测血清铁蛋白与转铁蛋白饱和度，"
            "根据医生建议定期放血（治疗性静脉切开放血）。",
            "lifestyle_tips": [
                "避免额外补充铁剂和维生素 C（会促进铁吸收）",
                "限制红肉与动物肝脏等高铁食物",
                "避免饮酒，减轻肝脏负担"
            ],
        },
        "doctor_checklist": {
            "specialty": "血液科 / 肝病科 / 遗传门诊",
            "questions": [
                "医生，我的铁蛋白和转铁蛋白饱和度升高，需要做 HFE 基因检测吗？",
                "放血治疗的频率和疗程应该怎么安排？",
                "我的亲属需要一起做铁代谢相关的筛查吗？"
            ],
        },
        "myth_buster": {
            "myth": "“血色病没得治，肝脏迟早会硬化吗？”",
            "truth": "错！血色病是少数「治疗极其简单」的遗传病之一，"
            "定期放血即可有效清除多余铁，只要早发现早干预，预后通常很好。",
        },
    },
]


def build_association_templates() -> Dict[str, Any]:
    """Return a dict {gene_symbol: association_template} for enrichment."""
    templates: Dict[str, Any] = {}
    for item in EXTRA_ASSOCIATIONS:
        templates[item["gene"]["symbol"]] = item
    return templates
