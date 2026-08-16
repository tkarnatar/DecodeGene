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
    "ALDH2": {
        "title": "🍺 体内的【解酒酶清洁工】",
        "story": "喝酒后，酒精先在体内变成一种有毒的中间产物「乙醛」。ALDH2 就像负责把乙醛"
        "清理掉的清洁工。东亚约有三分之一的人天生清洁工效率偏低，乙醛排不出去就会"
        "脸红、心跳加快——这是身体在「报警」，提醒你少喝酒。",
    },
    "LDLR": {
        "title": "🧹 血管里的【坏胆固醇清道夫】",
        "story": "血液里的「坏胆固醇」(LDL) 多了会堵血管。LDLR 就像血管壁上的清道夫，"
        "专门把坏胆固醇回收进肝脏处理掉。清道夫太少（突变），坏胆固醇越积越多，"
        "年纪轻轻就可能心梗、中风。",
    },
    "HBB": {
        "title": "🧱 血红蛋白里的【运氧砖块】",
        "story": "血红蛋白是红细胞里负责运氧的「货车车厢」，HBB 就是造车厢的关键砖块。"
        "砖块有缺陷，车厢（红细胞）就脆弱易碎，导致地中海贫血；在镰刀型贫血里，"
        "砖块还会让红细胞变硬卡住血管。",
    },
    "APC": {
        "title": "🚧 肠道细胞的【刹车闸门】",
        "story": "APC 像肠道细胞生长的刹车闸门，防止细胞无序增生。闸门失灵（突变）后，"
        "肠道会长出成百上千个息肉，几乎必然会演变成肠癌，因此需要早期手术与随访。",
    },
    "RET": {
        "title": "🔘 甲状腺细胞上的【生长开关按钮】",
        "story": "RET 就像甲状腺 C 细胞上的生长开关按钮。突变会让开关卡在「常开」位置，"
        "细胞持续增生，可能导致甲状腺髓样癌，并可能合并其他内分泌肿瘤（多发性内分泌"
        "肿瘤 2 型）。",
    },
    "PALB2": {
        "title": "🤝 BRCA2 的【最佳搭档】",
        "story": "修复 DNA 断裂需要一支团队。PALB2 就是 BRCA2 的最佳搭档，负责把 BRCA2"
        "准确送到 DNA 断裂处修补。搭档失职，修复团队效率下降，乳腺癌、胰腺癌风险随之升高。",
    },
    "SMN1": {
        "title": "⚡ 运动神经元的【供电线路维护员】",
        "story": "支配肌肉的「运动神经元」就像一条条供电线路，SMN1 负责制造维护这些线路"
        "所需的蛋白。缺少它，线路逐渐报废，肌肉接不到指令就萎缩无力（脊髓性肌萎缩症）。"
        "好消息是现代已有基因治疗。",
    },
    "DMD": {
        "title": "🪢 肌肉细胞的【减震绳索】",
        "story": "肌肉每次收缩都像用力拉扯。DMD 编码的抗肌萎缩蛋白就像肌肉细胞里的减震"
        "绳索，吸收拉扯的冲击。绳索缺失，肌肉细胞反复受损坏死，导致杜氏肌营养不良。",
    },
    "PAH": {
        "title": "♻️ 体内的【苯丙氨酸回收站】",
        "story": "食物里的苯丙氨酸需要被 PAH 这个「回收站」分解掉。回收站坏了，苯丙氨酸"
        "越堆越多，会损伤大脑（苯丙酮尿症）。只要新生儿期发现、坚持低苯丙氨酸饮食，"
        "孩子完全可以正常发育。",
    },
    "CYP2C19": {
        "title": "💊 肝脏里的【药物加工机床】",
        "story": "很多药物吃进去是「原料」，要经过肝脏的 CYP2C19「加工机床」才能变成有效"
        "成分。每个人的机床效率天生不同，所以同一种药对不同人的疗效和副作用也不一样。",
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
    {
        "association_id": "GDA_ALDH2_ALCOHOL_FLUSH",
        "gene": {
            "symbol": "ALDH2",
            "name": "Aldehyde Dehydrogenase 2",
            "chinese_name": "乙醛脱氢酶 2",
            "chromosome": "12 号染色体",
            "metaphor": {
                "title": METAPHORS["ALDH2"]["title"],
                "story": METAPHORS["ALDH2"]["story"],
            },
            "plain_summary": "ALDH2 是把饮酒产生的乙醛进一步分解的「解酒酶」。"
            "东亚约三分之一人群携带活性降低的 ALDH2*2 变异，喝酒容易脸红、心悸，"
            "长期大量饮酒者食管癌风险升高。",
            "academic_summary": "ALDH2 编码线粒体乙醛脱氢酶，将乙醇代谢中间产物乙醛"
            "氧化为乙酸。E487K (rs671) 变异使酶活性大幅下降，导致乙醛蓄积与"
            "「酒精潮红」反应，并与酒精相关食管癌风险相关。",
        },
        "disease": {
            "id": "MONDO:0011895",
            "name": "Alcohol flush reaction",
            "chinese_name": "酒精潮红反应 (ALDH2 缺乏)",
            "categories": ["代谢体质差异", "药物/代谢个体差异"],
            "severity_badge": "💡 常见体质差异 (少喝酒即可)",
        },
        "evidence": {
            "overall_score": 0.85,
            "plain_rating": "⭐️⭐️⭐️⭐️ 明确的体质差异与风险关联",
            "clinvar_pathogenic_count": 1,
            "clinvar_summary_chinese": "rs671 (E487K) 为高频东亚变异",
            "opentargets_score": 0.8,
        },
        "lifestyle_prevention": {
            "screening_advice": "无需特殊筛查；建议有潮红反应者尽量少饮酒或不饮酒，"
            "长期饮酒者关注食管/上消化道健康。",
            "lifestyle_tips": [
                "减少或避免饮酒，尤其避免空腹、大量饮酒",
                "喝酒易脸红者更应严格限量",
                "戒烟，避免烟酒叠加进一步损伤上消化道"
            ],
        },
        "doctor_checklist": {
            "specialty": "消化内科 / 全科",
            "questions": [
                "医生，我喝酒容易脸红，是不是应该完全戒酒？",
                "长期少量饮酒对我的食管癌风险影响有多大？",
                "我的直系亲属是否也有必要了解这一体质差异？"
            ],
        },
        "myth_buster": {
            "myth": "“喝酒脸红说明能喝、酒量大吗？”",
            "truth": "恰恰相反！脸红说明体内乙醛堆积、解酒酶效率低，"
            "是身体在「报警」，这类人反而更应该少喝酒。",
        },
    },
    {
        "association_id": "GDA_LDLR_FAMILIAL_HYPERCHOLESTEROLEMIA",
        "gene": {
            "symbol": "LDLR",
            "name": "Low Density Lipoprotein Receptor",
            "chinese_name": "低密度脂蛋白受体",
            "chromosome": "19 号染色体",
            "metaphor": {
                "title": METAPHORS["LDLR"]["title"],
                "story": METAPHORS["LDLR"]["story"],
            },
            "plain_summary": "LDLR 像血管里的「坏胆固醇清道夫」，把血液里的 LDL 回收进肝脏。"
            "突变导致清道夫减少，坏胆固醇长期堆积，早发心肌梗死风险大增。"
            "越早降脂治疗，获益越大。",
            "academic_summary": "LDLR 介导肝细胞对循环 LDL 颗粒的受体介导内吞，"
            "是血浆 LDL-C 清除的主要途径。致病变异导致家族性高胆固醇血症 (FH)，"
            "显著升高早发动脉粥样硬化性心血管病风险。",
        },
        "disease": {
            "id": "MONDO:0007750",
            "name": "Familial hypercholesterolemia",
            "chinese_name": "家族性高胆固醇血症",
            "categories": ["遗传性代谢病", "心血管疾病"],
            "severity_badge": "⚠️ 需积极降脂治疗 (可有效控制)",
        },
        "evidence": {
            "overall_score": 0.95,
            "plain_rating": "⭐️⭐️⭐️⭐️⭐️ 明确致病基因 (Definitive)",
            "clinvar_pathogenic_count": 1800,
            "clinvar_summary_chinese": "已收录 1800+ 明确致病变异位点",
            "opentargets_score": 0.96,
        },
        "lifestyle_prevention": {
            "screening_advice": "建议从儿童/青少年期开始监测血脂；确诊后尽早启动他汀等降脂治疗，"
            "定期复查 LDL-C 达标情况与心血管风险。",
            "lifestyle_tips": [
                "低饱和脂肪、低胆固醇饮食，多吃蔬果与全谷物",
                "规律有氧运动，控制体重，戒烟",
                "遵医嘱坚持服用他汀/依折麦布等降脂药，勿自行停药"
            ],
        },
        "doctor_checklist": {
            "specialty": "心内科 / 血脂专科门诊",
            "questions": [
                "医生，我确诊家族性高胆固醇血症，LDL-C 应降到多少才达标？",
                "他汀类药物需要吃一辈子吗？有哪些副作用要留意？",
                "我的孩子和兄弟姐妹是否需要尽早查血脂或做基因检测？"
            ],
        },
        "myth_buster": {
            "myth": "“我还年轻，血脂高点没关系，等老了再说吗？”",
            "truth": "对 FH 患者，坏胆固醇从出生起就在持续损伤血管，"
            "越早降脂获益越大，年轻绝不是「豁免」。",
        },
    },
    {
        "association_id": "GDA_HBB_THALASSEMIA",
        "gene": {
            "symbol": "HBB",
            "name": "Hemoglobin Subunit Beta",
            "chinese_name": "血红蛋白 β 亚基",
            "chromosome": "11 号染色体",
            "metaphor": {
                "title": METAPHORS["HBB"]["title"],
                "story": METAPHORS["HBB"]["story"],
            },
            "plain_summary": "HBB 是制造血红蛋白（红细胞里运氧的「车厢」）的关键零件。"
            "零件缺陷会导致红细胞脆弱易破（地中海贫血）或变形卡血管（镰刀型贫血）。"
            "华南地区人群中携带率较高，婚育前筛查很重要。",
            "academic_summary": "HBB 编码血红蛋白 β-珠蛋白链。β-珠蛋白基因致病变异导致"
            "β-地中海贫血（链合成减少）或镰刀型细胞贫血（结构异常），"
            "均属常见单基因血红蛋白病。",
        },
        "disease": {
            "id": "MONDO:0009169",
            "name": "Beta-thalassemia",
            "chinese_name": "β-地中海贫血 / 镰刀型细胞贫血",
            "categories": ["单基因遗传病", "血液系统疾病"],
            "severity_badge": "⚠️ 需血液科长期管理",
        },
        "evidence": {
            "overall_score": 0.97,
            "plain_rating": "⭐️⭐️⭐️⭐️⭐️ 明确致病基因 (Definitive)",
            "clinvar_pathogenic_count": 900,
            "clinvar_summary_chinese": "已收录多种地贫/镰贫致病变异",
            "opentargets_score": 0.95,
        },
        "lifestyle_prevention": {
            "screening_advice": "建议婚育前进行地中海贫血筛查（尤其华南高发区）；"
            "确诊者定期输血、去铁治疗，重型患者可评估造血干细胞移植。",
            "lifestyle_tips": [
                "地贫患者不要盲目补铁，须遵医嘱避免铁过载",
                "均衡营养，规律随访血常规与铁蛋白",
                "备孕夫妇双方均筛查，评估胎儿遗传风险"
            ],
        },
        "doctor_checklist": {
            "specialty": "血液科 / 儿科 / 遗传门诊",
            "questions": [
                "我是地中海贫血基因携带者，我的伴侣也需要筛查吗？",
                "怀孕期间需要做产前诊断吗？",
                "轻型携带者平时需要注意什么？"
            ],
        },
        "myth_buster": {
            "myth": "“地贫就是缺铁性贫血，多吃补铁药就行吗？”",
            "truth": "错！地贫是遗传性血红蛋白合成障碍，盲目补铁反而可能加重铁过载，"
            "必须在血液科指导下规范管理。",
        },
    },
    {
        "association_id": "GDA_APC_FAP",
        "gene": {
            "symbol": "APC",
            "name": "Adenomatous Polyposis Coli",
            "chinese_name": "腺瘤性结肠息肉病蛋白",
            "chromosome": "5 号染色体",
            "metaphor": {
                "title": METAPHORS["APC"]["title"],
                "story": METAPHORS["APC"]["story"],
            },
            "plain_summary": "APC 像肠道细胞的「刹车闸门」，防止细胞无序增生。闸门失灵，"
            "肠道会长出成百上千个息肉，几乎必然演变成肠癌，需要早期内镜随访乃至预防性手术。",
            "academic_summary": "APC 是 Wnt/β-catenin 信号通路的负调控因子，"
            "抑制结直肠上皮过度增殖。生殖系功能丧失突变导致家族性腺瘤性息肉病 (FAP)。",
        },
        "disease": {
            "id": "MONDO:0007435",
            "name": "Familial adenomatous polyposis",
            "chinese_name": "家族性腺瘤性息肉病 (FAP)",
            "categories": ["遗传性肿瘤综合征", "消化系统肿瘤"],
            "severity_badge": "⚠️ 需早期手术干预",
        },
        "evidence": {
            "overall_score": 0.96,
            "plain_rating": "⭐️⭐️⭐️⭐️⭐️ 明确致病基因 (Definitive)",
            "clinvar_pathogenic_count": 1600,
            "clinvar_summary_chinese": "已收录 1600+ 明确致病变异",
            "opentargets_score": 0.94,
        },
        "lifestyle_prevention": {
            "screening_advice": "建议从青少年期开始定期结肠镜监测；适时行预防性结肠切除术；"
            "关注十二指肠、甲状腺等肠外表现。",
            "lifestyle_tips": [
                "规律内镜随访，勿因无症状而中断",
                "健康饮食，出现便血、腹痛及时就医",
                "直系亲属尽早进行基因检测与筛查"
            ],
        },
        "doctor_checklist": {
            "specialty": "消化内科 / 结直肠外科 / 遗传门诊",
            "questions": [
                "医生，我确诊 FAP，应该从几岁开始做肠镜？",
                "什么情况下需要考虑预防性结肠切除？",
                "我的子女应从几岁开始基因检测与筛查？"
            ],
        },
        "myth_buster": {
            "myth": "“有息肉很正常，切掉就没事了吗？”",
            "truth": "对 FAP 患者，息肉会成百上千地不断长出，单纯切除远远不够，"
            "必须规范内镜随访，必要时预防性手术。",
        },
    },
    {
        "association_id": "GDA_RET_MEN2",
        "gene": {
            "symbol": "RET",
            "name": "Ret Proto-Oncogene",
            "chinese_name": "原癌基因 RET",
            "chromosome": "10 号染色体",
            "metaphor": {
                "title": METAPHORS["RET"]["title"],
                "story": METAPHORS["RET"]["story"],
            },
            "plain_summary": "RET 像甲状腺 C 细胞上的「生长开关按钮」，突变让开关常开，"
            "细胞持续增生，可导致甲状腺髓样癌，并可能合并嗜铬细胞瘤（多发性内分泌肿瘤 2 型）。"
            "预防性甲状腺切除可彻底避免。",
            "academic_summary": "RET 编码受体酪氨酸激酶，参与神经嵴衍生细胞的分化。"
            "激活性生殖系突变导致 MEN2A/MEN2B 及家族性甲状腺髓样癌。",
        },
        "disease": {
            "id": "MONDO:0019950",
            "name": "Multiple endocrine neoplasia type 2",
            "chinese_name": "多发性内分泌肿瘤 2 型",
            "categories": ["遗传性肿瘤综合征", "内分泌肿瘤"],
            "severity_badge": "⚠️ 建议预防性甲状腺切除",
        },
        "evidence": {
            "overall_score": 0.95,
            "plain_rating": "⭐️⭐️⭐️⭐️⭐️ 明确致病基因 (Definitive)",
            "clinvar_pathogenic_count": 300,
            "clinvar_summary_chinese": "按基因型分层指导手术时机",
            "opentargets_score": 0.92,
        },
        "lifestyle_prevention": {
            "screening_advice": "确诊后按基因型分层，高危者儿童期行预防性甲状腺切除；"
            "定期监测血降钙素与儿茶酚胺。",
            "lifestyle_tips": [
                "规律随访内分泌指标",
                "控制血压，出现心悸、多汗、头痛及时就医",
                "子女尽早做基因检测与遗传咨询"
            ],
        },
        "doctor_checklist": {
            "specialty": "内分泌科 / 甲状腺外科 / 遗传门诊",
            "questions": [
                "医生，我携带 RET 突变，应该在哪一阶段做预防性甲状腺切除？",
                "平时需要监测哪些激素指标、多久一次？",
                "我的子女何时需要做基因检测？"
            ],
        },
        "myth_buster": {
            "myth": "“甲状腺髓样癌很罕见，跟我没关系吗？”",
            "truth": "若家族中有 MEN2 病史，携带 RET 突变者几乎 100% 会发生甲状腺髓样癌，"
            "预防性切除可彻底避免，关键在于早发现。",
        },
    },
    {
        "association_id": "GDA_PALB2_BREAST_PANCREATIC",
        "gene": {
            "symbol": "PALB2",
            "name": "Partner and Localizer of BRCA2",
            "chinese_name": "BRCA2 搭档蛋白 PALB2",
            "chromosome": "16 号染色体",
            "metaphor": {
                "title": METAPHORS["PALB2"]["title"],
                "story": METAPHORS["PALB2"]["story"],
            },
            "plain_summary": "PALB2 是 BRCA2 的最佳搭档，负责把 BRCA2 送到 DNA 断裂处修补。"
            "搭档失职会升高乳腺癌（终身风险约 35%~58%）与胰腺癌风险，但绝非必然发病。",
            "academic_summary": "PALB2 与 BRCA1/BRCA2 协同参与同源重组修复。"
            "致病变异升高乳腺癌与胰腺癌风险，并罕见地与范可尼贫血相关。",
        },
        "disease": {
            "id": "MONDO:0016419",
            "name": "Hereditary breast and pancreatic cancer",
            "chinese_name": "遗传性乳腺癌/胰腺癌易感 (PALB2 相关)",
            "categories": ["恶性肿瘤", "遗传性肿瘤综合征"],
            "severity_badge": "⚠️ 需关注 (可防可治)",
        },
        "evidence": {
            "overall_score": 0.93,
            "plain_rating": "⭐️⭐️⭐️⭐️⭐️ 强科学共识",
            "clinvar_pathogenic_count": 620,
            "clinvar_summary_chinese": "已收录 600+ 明确致病变异",
            "opentargets_score": 0.9,
        },
        "lifestyle_prevention": {
            "screening_advice": "建议参照 BRCA1/2 携带者进行乳腺增强磁共振筛查；"
            "有胰腺癌家族史者咨询相关筛查方案。",
            "lifestyle_tips": [
                "保持健康体重，戒烟限酒",
                "女性在医生指导下合理母乳喂养",
                "有生育计划者咨询遗传咨询与 PGT"
            ],
        },
        "doctor_checklist": {
            "specialty": "乳腺外科 / 肿瘤科 / 临床遗传门诊",
            "questions": [
                "医生，我的 PALB2 突变对乳腺癌筛查方案有什么影响？",
                "家族里有胰腺癌病史，我需要做相关筛查吗？",
                "我的亲属需要做同位点基因检测吗？"
            ],
        },
        "myth_buster": {
            "myth": "“只有 BRCA1/BRCA2 才算「乳腺癌基因」吗？”",
            "truth": "不只！PALB2、CHEK2、ATM 等基因同样影响乳腺癌风险，"
            "遗传咨询应综合评估，不能只看一两个基因。",
        },
    },
    {
        "association_id": "GDA_SMN1_SMA",
        "gene": {
            "symbol": "SMN1",
            "name": "Survival of Motor Neuron 1",
            "chinese_name": "运动神经元存活蛋白 1",
            "chromosome": "5 号染色体",
            "metaphor": {
                "title": METAPHORS["SMN1"]["title"],
                "story": METAPHORS["SMN1"]["story"],
            },
            "plain_summary": "SMN1 制造维护「运动神经元」（支配肌肉的神经）所需的蛋白。"
            "缺少它，运动神经元逐渐死亡，肌肉萎缩无力，即脊髓性肌萎缩症 (SMA)。"
            "近年已有基因治疗与疾病修饰药物，越早治疗预后越好。",
            "academic_summary": "SMN1 编码运动神经元存活蛋白 (SMN)，缺失导致脊髓前角"
            "运动神经元进行性变性。SMN2 拷贝数可部分代偿，是 SMA 的重要修饰因子。"
            "nusinersen、onasemnogene 等治疗已获批。",
        },
        "disease": {
            "id": "MONDO:0001516",
            "name": "Spinal muscular atrophy",
            "chinese_name": "脊髓性肌萎缩症 (SMA)",
            "categories": ["单基因遗传病", "神经肌肉疾病"],
            "severity_badge": "⚠️ 需专科治疗 (已有基因治疗)",
        },
        "evidence": {
            "overall_score": 0.94,
            "plain_rating": "⭐️⭐️⭐️⭐️⭐️ 明确致病基因 (Definitive)",
            "clinvar_pathogenic_count": 60,
            "clinvar_summary_chinese": "SMN1 外显子 7 纯合缺失为主要病因",
            "opentargets_score": 0.93,
        },
        "lifestyle_prevention": {
            "screening_advice": "备孕人群可做 SMA 携带者筛查；确诊者尽早启动疾病修饰治疗，"
            "配合呼吸支持与康复。",
            "lifestyle_tips": [
                "早期多学科康复训练",
                "关注呼吸功能，遵医嘱使用呼吸支持",
                "定期神经科随访评估运动功能"
            ],
        },
        "doctor_checklist": {
            "specialty": "神经内科 / 儿科 / 遗传门诊",
            "questions": [
                "医生，我的孩子确诊 SMA，目前有哪些治疗药物可选择？",
                "SMA 携带者筛查适合我们夫妇吗？",
                "若再生育，如何通过产前诊断或 PGT 避免遗传？"
            ],
        },
        "myth_buster": {
            "myth": "“SMA 无药可治吗？”",
            "truth": "时代变了！近年的基因治疗与鞘内注射药物已能显著改善病程，"
            "越早诊断、越早治疗，预后越好。",
        },
    },
    {
        "association_id": "GDA_DMD_DUCHENNE",
        "gene": {
            "symbol": "DMD",
            "name": "Dystrophin",
            "chinese_name": "抗肌萎缩蛋白 (DMD)",
            "chromosome": "X 染色体",
            "metaphor": {
                "title": METAPHORS["DMD"]["title"],
                "story": METAPHORS["DMD"]["story"],
            },
            "plain_summary": "DMD 编码抗肌萎缩蛋白，像肌肉细胞收缩时的「减震绳索」。"
            "缺了它，肌肉细胞不断受损坏死，导致杜氏肌营养不良，男孩多见（X 连锁隐性）。",
            "academic_summary": "DMD 编码 dystrophin，连接肌膜下细胞骨架与细胞外基质。"
            "移码突变导致蛋白完全缺失，引起进行性杜氏肌营养不良。",
        },
        "disease": {
            "id": "MONDO:0010679",
            "name": "Duchenne muscular dystrophy",
            "chinese_name": "杜氏肌营养不良",
            "categories": ["单基因遗传病", "X 连锁隐性遗传"],
            "severity_badge": "⚠️ 需专科长期管理",
        },
        "evidence": {
            "overall_score": 0.97,
            "plain_rating": "⭐️⭐️⭐️⭐️⭐️ 明确致病基因 (Definitive)",
            "clinvar_pathogenic_count": 4200,
            "clinvar_summary_chinese": "已收录大量缺失/重复/点突变",
            "opentargets_score": 0.96,
        },
        "lifestyle_prevention": {
            "screening_advice": "有家族史者进行遗传咨询与携带者筛查；确诊者规律康复训练、"
            "糖皮质激素治疗并监测心功能与呼吸功能。",
            "lifestyle_tips": [
                "规律物理治疗，维持关节活动度",
                "避免剧烈离心运动造成肌肉损伤",
                "定期心功能、肺功能随访"
            ],
        },
        "doctor_checklist": {
            "specialty": "神经内科 / 儿科 / 康复科",
            "questions": [
                "医生，孩子肌酶显著升高，需要做 DMD 基因检测吗？",
                "目前有哪些延缓病情的药物？",
                "我的家族其他人需要做携带者检测吗？"
            ],
        },
        "myth_buster": {
            "myth": "“男孩走路晚、爱摔跤只是发育慢吗？”",
            "truth": "若同时血肌酸激酶显著升高，需警惕杜氏肌营养不良，"
            "尽早就医排查，不要简单归因于「发育慢」。",
        },
    },
    {
        "association_id": "GDA_PAH_PKU",
        "gene": {
            "symbol": "PAH",
            "name": "Phenylalanine Hydroxylase",
            "chinese_name": "苯丙氨酸羟化酶",
            "chromosome": "12 号染色体",
            "metaphor": {
                "title": METAPHORS["PAH"]["title"],
                "story": METAPHORS["PAH"]["story"],
            },
            "plain_summary": "PAH 负责分解食物里的苯丙氨酸，就像「苯丙氨酸回收站」。"
            "回收站坏了，苯丙氨酸堆积损伤大脑（苯丙酮尿症）。新生儿筛查可早发现，"
            "坚持低苯丙氨酸饮食即可正常生活。",
            "academic_summary": "PAH 编码苯丙氨酸羟化酶，催化苯丙氨酸转化为酪氨酸。"
            "双等位基因突变导致苯丙酮尿症，未治疗可致严重智力障碍；"
            "新生儿筛查加饮食治疗可完全避免。",
        },
        "disease": {
            "id": "MONDO:0009861",
            "name": "Phenylketonuria",
            "chinese_name": "苯丙酮尿症 (PKU)",
            "categories": ["单基因遗传病", "代谢性疾病"],
            "severity_badge": "✅ 可防可控 (低苯丙氨酸饮食)",
        },
        "evidence": {
            "overall_score": 0.96,
            "plain_rating": "⭐️⭐️⭐️⭐️⭐️ 明确致病基因 (Definitive)",
            "clinvar_pathogenic_count": 700,
            "clinvar_summary_chinese": "已收录多种酶活性相关变异",
            "opentargets_score": 0.94,
        },
        "lifestyle_prevention": {
            "screening_advice": "新生儿出生后进行足跟血筛查；确诊者终身低苯丙氨酸饮食；"
            "备孕女性需严格控制血苯丙氨酸浓度。",
            "lifestyle_tips": [
                "使用特殊配方奶粉与低蛋白饮食",
                "定期监测血苯丙氨酸浓度",
                "成年后仍需坚持饮食控制"
            ],
        },
        "doctor_checklist": {
            "specialty": "儿科 / 遗传代谢科",
            "questions": [
                "医生，孩子的 PKU 需要哪种特殊饮食方案？",
                "血苯丙氨酸应控制在什么范围？",
                "长大以后还需要继续控制饮食吗？"
            ],
        },
        "myth_buster": {
            "myth": "“PKU 的孩子智力一定会受影响吗？”",
            "truth": "不会！只要新生儿期确诊并坚持低苯丙氨酸饮食，"
            "绝大多数孩子的智力发育完全正常。",
        },
    },
    {
        "association_id": "GDA_CYP2C19_PHARMACOGENOMICS",
        "gene": {
            "symbol": "CYP2C19",
            "name": "Cytochrome P450 2C19",
            "chinese_name": "细胞色素 P450 2C19",
            "chromosome": "10 号染色体",
            "metaphor": {
                "title": METAPHORS["CYP2C19"]["title"],
                "story": METAPHORS["CYP2C19"]["story"],
            },
            "plain_summary": "CYP2C19 是把某些药物「激活」成有效形式的「加工机床」，"
            "如抗血小板药氯吡格雷需经它活化才起效。机床效率因人而异，影响药效与副作用。",
            "academic_summary": "CYP2C19 编码药物代谢酶，参与氯吡格雷、奥美拉唑等多种药物的"
            "生物转化。功能缺失等位基因（*2、*3）导致氯吡格雷活化不足；"
            "快代谢型（*17）则增加出血风险。",
        },
        "disease": {
            "id": "PHARMACOGENOMICS:2C19",
            "name": "CYP2C19 pharmacogenomic variability",
            "chinese_name": "CYP2C19 药效个体差异 (药物基因组学)",
            "categories": ["药物基因组学", "个体化用药"],
            "severity_badge": "💡 用药个体差异 (可指导精准用药)",
        },
        "evidence": {
            "overall_score": 0.9,
            "plain_rating": "⭐️⭐️⭐️⭐️ 有临床指南支持 (CPIC)",
            "clinvar_pathogenic_count": 0,
            "clinvar_summary_chinese": "功能变异 *2/*3/*17 为高频多态性",
            "opentargets_score": 0.7,
        },
        "lifestyle_prevention": {
            "screening_advice": "服用氯吡格雷前可做基因检测指导用药，"
            "功能缺失者必要时在医生指导下换用替格瑞洛等。",
            "lifestyle_tips": [
                "遵医嘱用药，勿自行换药、停药",
                "服药期间注意观察有无出血或血栓相关症状",
                "就诊时告知医生自己的用药与检测情况"
            ],
        },
        "doctor_checklist": {
            "specialty": "心内科 / 临床药学门诊",
            "questions": [
                "医生，我植入支架后吃氯吡格雷，需要做 CYP2C19 基因检测吗？",
                "如果检测显示我是慢代谢型，是否需要换药？",
                "还有哪些常用药会受 CYP2C19 影响？"
            ],
        },
        "myth_buster": {
            "myth": "“一样的药对每个人都一样有效吗？”",
            "truth": "不是！基因差异会导致同一药物的疗效与副作用因人而异，"
            "药物基因检测正用于指导精准用药。",
        },
    },
]


def build_association_templates() -> Dict[str, Any]:
    """Return a dict {gene_symbol: association_template} for enrichment."""
    templates: Dict[str, Any] = {}
    for item in EXTRA_ASSOCIATIONS:
        templates[item["gene"]["symbol"]] = item
    return templates
