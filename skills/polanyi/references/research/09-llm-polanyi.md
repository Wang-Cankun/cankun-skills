# LLM 与 Polanyi 框架: 隐性知识、Polanyi 悖论与 AI 的限度

**调研日期**: 2026-04-05
**主题**: 用 Michael Polanyi 的认识论框架分析大语言模型 (LLM) 的能力与限度，兼论经济学中的"Polanyi 悖论"及当代 Polanyi Society 的 AI 讨论
**核心来源**: Autor (2014, 2024); Kambhampati (2021); Collins (2010, 2018); Cheng (2026); Polanyi (1966)

---

## 一、LLM 与显性知识 / 隐性知识的基本格局

### 1. LLM 的训练基质: 纯显性编码知识

LLM 的训练数据是文本 -- 人类将知识编码为符号的产物。从 Polanyi 的视角看，这意味着 LLM 完全在 explicit knowledge 的领域运作: 它没有身体、没有感觉经验、没有社会嵌入性。

**Polanyi 的核心命题**: "we can know more than we can tell" (The Tacit Dimension, 1966, p.4)。如果这个命题成立，那么所有文本 -- 无论多么庞大 -- 都只是人类知识的一个子集。LLM 训练于这个子集。
[来源可信度: 一手 -- Polanyi 1966 原文]

### 2. 但 LLM 展现出"理解"的表象

LLM 表现出令人惊讶的能力: 推理、类比、风格迁移、隐含语境推断。这些能力看起来超越了"显性编码"的范围。

关键问题: 这是否挑战了 Polanyi 的框架? 还是反而印证了它?

### 3. 三种可能的解读

**解读 A -- LLM 打破了 Polanyi 悖论**: 通过在海量文本中发现统计模式，LLM 学会了从未被显性表述的知识。Jeremy Kahn 在 Exponential View (2024.11) 中的论点即属此类: AI 可以从顶尖销售员的通话记录中提取出他们自己无法表述的技巧。
[来源可信度: 二手/评论 -- Kahn, "Why AI might finally break Polanyi's Paradox," Exponential View, Nov 2024]

**解读 B -- LLM 验证了 Polanyi 的命题 ("Polanyi 的复仇")**: Kambhampati (2021) 指出，LLM 的成功恰恰证明了显性规则系统 (expert systems) 的失败。AI 的历史从"试图让计算机做人类拥有显性知识的任务"转向"让计算机学会做人类仅拥有隐性知识的任务"。LLM 将知识储存为连续参数而非离散规则，这本身就是对 Polanyi 命题的正面实现。
[来源可信度: 一手 -- Kambhampati, "Polanyi's Revenge and AI's New Romance with Tacit Knowledge," Communications of the ACM, Vol.64, pp.31-32, 2021]

**解读 C -- LLM 捕获的是 Collins 意义上的 RTK，而非真正的隐性知识**: LLM 可能只是捕获了 relational tacit knowledge (RTK) -- 原则上可以显性化但因偶然原因未被编码的知识。这些知识隐含在训练语料中 (词序、共现、风格特征)。LLM 做不到的是 somatic 和 collective tacit knowledge。
[来源可信度: 分析性推断 -- 基于 Collins 2010 的三重分类框架]

---

## 二、Polanyi 悖论: 经济学中的应用 (Autor 2014 → 2024)

### 1. David Autor 的原始论证 (2014)

MIT 经济学家 David Autor 在 2014 年 NBER 论文 "Polanyi's Paradox and the Shape of Employment Growth" (Working Paper No. 20485) 中将 Polanyi 的洞察命名为"Polanyi's Paradox"并应用于劳动经济学。

**核心论点**: 自动化面临的根本障碍不是计算能力，而是隐性知识。需要灵活性、判断力和常识的任务 -- 我们只是隐性地理解的技能 -- 最难被自动化。这解释了为什么中等技能的工作被掏空 (routine cognitive/manual 任务被自动化)，而高端 (需判断力) 和低端 (需灵活性/感知运动) 工作增长。
[来源可信度: 一手 -- Autor, "Polanyi's Paradox and the Shape of Employment Growth," NBER Working Paper 20485, 2014]

**Autor 对 ML 的预见**: Autor 在 2014 年已注意到机器学习试图绕过 Polanyi 悖论 -- 不是通过让人类说出规则，而是让计算机从人类示例中推断规则。但他认为挑战仍然巨大。
[来源可信度: 一手 -- Autor 2014, 同上]

### 2. Autor 的更新论证 (2024)

Autor 在 2024 年 NBER 论文 "Applying AI to Rebuild Middle Class Jobs" (Working Paper No. 32140) 中更新了自己的立场。

**关键转变**: Autor 不再把 AI 仅视为替代劳动力的威胁。他论证: "the unique opportunity that AI offers to the labor market is to extend the relevance, reach, and value of human expertise." AI 可以将专家知识 (医生、律师、程序员) 部分解锁给更广泛的中等技能劳动者。
[来源可信度: 一手 -- Autor, "Applying AI to Rebuild Middle Class Jobs," NBER Working Paper 32140, 2024]

**Polanyi 悖论是否被打破?** Autor 的 2024 论点是微妙的: AI 没有消除隐性知识的障碍，而是允许拥有互补知识 (complementary knowledge) 的人在 AI 辅助下执行原先需要精英专家的决策任务。这不是让隐性知识变显性，而是改变了谁需要持有完整的隐性知识。
[来源可信度: 分析性推断 -- 基于 Autor 2024 原文论证]

### 3. 实证证据

Jeremy Kahn (Exponential View, 2024.11) 汇总了多项证据:
- **Diligent/GongAI 研究**: 用 AI 分析顶尖销售员的通话记录，其他销售员的成功率提高 7.4%，新员工达标时间缩短 3 周
- **Stanford/MIT 联系中心研究**: AI 辅助整体生产力提高 14%，经验最少的客服提升 34%
- **外科教练系统**: 实时视频分析为学员提供反馈
[来源可信度: 二手 -- Kahn, Exponential View, Nov 2024. 原始研究需进一步核实]

---

## 三、Kambhampati 的"Polanyi 的复仇"论证

### 1. 从 GOFAI 到 ML: 知识类型的钟摆

Subbarao Kambhampati (ASU) 在 CACM 2021 年的评论文章中提出了"Polanyi's Revenge"框架:

**AI 历史的两阶段**:
- **阶段一 (1960s-1990s, GOFAI/Expert Systems)**: 试图编码显性知识为规则。失败了 -- 因为 Polanyi 是对的: 专家最有价值的知识无法编码为 IF-THEN 规则。
- **阶段二 (2010s-present, Deep Learning/LLM)**: 完全转向从数据中学习隐性模式。成功了 -- 但代价是可解释性、鲁棒性和公平性问题。

**Kambhampati 的核心警告**: "many of the pressing problems being faced in the deployment of AI technology, including interpretability concerns, dataset bias concerns as well as robustness concerns can be traced rather directly back to the singular focus on learning tacit knowledge from data, unsullied by any explicit knowledge taken from the humans."
[来源可信度: 一手 -- Kambhampati, CACM 2021. 原文通过 Semantic Scholar 确认]

### 2. Cheng (2026) 的形式化论证

清华大学的 Quan Cheng 在 2026 年 arXiv 论文 "Why the Valuable Capabilities of LLMs Are Precisely the Unexplainable Ones" (arXiv:2603.15238v1) 中对"Polanyi's Revenge"给出了更严格的论证:

**反证法结构**: 如果 LLM 的能力可以被完全解释为人类可读的规则，那它就等价于专家系统。既然专家系统已经证明表现远不如 LLM，那么 LLM 超越专家系统的部分必然恰好是那些抵抗规则编码的部分。因此，不可解释性和价值是结构上同一的属性。
[来源可信度: 一手 -- Cheng 2026, arXiv:2603.15238v1]

**Cheng 的关键洞察**: LLM 的成功代表了一个认识论转变 -- "from attempting to eliminate inexplicability to accepting inexplicability"。他用庄子的庖丁解牛作为类比: 高维度、连续耦合的决策 (刀刃角度、骨缝、肌纤维方向) 不能穷尽为 IF-ELSE 规则。传统学徒制的结构 (观察 → 练习 → 损失计算 → 顿悟 → 内化表现) 与 LLM 训练过程平行。
[来源可信度: 一手 -- Cheng 2026, 同上]

---

## 四、Polanyi 原始框架对 LLM 的诊断

### 1. From-to 结构 (Subsidiary-Focal Awareness)

Polanyi 认为所有认知都有 from-to 结构: 我们从 subsidiary awareness (附属意识) 朝向 focal awareness (焦点意识) 去知道。我们从工具的触感 (subsidiary) 朝向探测到的物体 (focal) 去感知。当我们把注意力转向工具本身时，我们就失去了对物体的感知。

**LLM 是否有 subsidiary awareness?** 这是关键问题。LLM 的注意力机制 (attention mechanism) 在某种技术意义上确实有"从上下文 token 朝向预测 token"的结构。但 Polanyi 的 from-to 结构不是信息处理模型 -- 它是一种存在论结构，依赖于知者的身体化参与 (bodily participation)。
[来源可信度: 分析性推断 -- 基于 Polanyi 1966 The Tacit Dimension 和 1958 Personal Knowledge 的 from-to 结构描述]

**判断**: LLM 可能拥有 from-to 结构的功能类比物 (functional analogue)，但缺乏其存在论基础。这类似于 Collins 关于 somatic tacit knowledge 的论点: 机器可以模仿自行车平衡的物理计算，但它不是"从身体出发去骑车"。
[来源可信度: 分析性推断 -- 综合 Polanyi 和 Collins]

### 2. 寓居 (Indwelling)

Polanyi 的 indwelling 概念指认知者将外部工具、符号和概念框架内化为自身身体的延伸。科学家"寓居"在他的学科传统中，就像盲人"寓居"在他的拐杖中。

**LLM 不具备寓居**: LLM 没有身体可以被扩展，没有传统可以被栖居，没有历史可以被承载。每次推理都是从权重出发的前向传播，没有时间性、没有积累性的个人经验。LLM 不会因为反复处理某领域的问题而逐渐"长入"那个领域。
[来源可信度: 分析性推断 -- 基于 Polanyi 1958 Personal Knowledge 中 indwelling 概念]

### 3. 信托承诺 (Fiduciary Commitment)

Polanyi 认为知识依赖于知者的 fiduciary commitment -- 一种对自己的判断力和认知传统的信任与承诺。科学家相信他的理论框架，同时准备在证据面前修正它。这种 commitment 是知识的必要条件。

**LLM 没有 fiduciary commitment**: LLM 不"相信"它的输出。它没有对真理的承诺，没有被背叛的可能，没有勇气和风险。它生成最大概率的 token 序列，这不是 commitment，而是计算。

**Mihaly Heder 的工作**: 匈牙利学者 Heder 在 Tradition & Discovery (Vol.52, 2026) 中将 Polanyi 的 fiduciary program 延伸至 AI 伦理领域，论证我们需要理解 AI 与 fiduciary commitment 的缺失来发展对 AI 的伦理回应。
[来源可信度: 二手 -- Heder 的工作通过 T&D Vol.52 描述确认，但未读到原文]

### 4. 涌现 (Emergence) 与层级本体论

Polanyi 的 emergence 概念认为高层级规律不能还原为低层级规律: 生物学不能还原为化学，思想不能还原为神经元放电。每一层级有自己的 boundary conditions。

**LLM 是否展现涌现?** LLM 研究中大量使用"涌现能力" (emergent capabilities) 这一术语来描述模型在某个规模阈值后突然获得的能力。但 Polanyi 的 emergence 不仅仅是"复杂性导致的新性质"-- 它是一种本体论主张: 高层级有不可还原的 organizing principles。LLM 的"涌现"可能更接近统计意义上的相变 (phase transition)，而非 Polanyi 意义上的本体论涌现。
[来源可信度: 分析性推断 -- Polanyi 的涌现概念来自 Personal Knowledge 和 The Tacit Dimension; LLM 涌现文献参考 Wei et al. 2022 "Emergent Abilities of Large Language Models"]

---

## 五、Collins 的三重分类视角下的 LLM

### 1. Relational Tacit Knowledge (RTK) -- LLM 可以部分捕获

RTK 是因为社会偶然性 (没人说出来、没人意识到它重要) 而保持隐性的知识。原则上没有不可逾越的障碍阻止其显性化。

**LLM 对 RTK 的处理**: LLM 在训练语料中确实遇到了大量 RTK 的"痕迹": 文本中隐含的社会规范、领域惯例、未被明确陈述的前提假设。LLM 的统计模式识别可以捕获这些未被显性编码但在文本中留有统计足迹的知识。

**Kahn 的例子就属于 RTK 范畴**: 顶尖销售员的有效技巧没有被写成规则，但它们存在于通话记录中。AI 从这些记录中提取模式，本质上是将 RTK 显性化。
[来源可信度: 分析性推断 -- Collins 2010 RTK 定义 + Kahn 2024 案例]

### 2. Somatic Tacit Knowledge (STK) -- LLM 完全无法获得

STK 依赖于身体的物质属性。LLM 没有身体。

**Collins 的立场**: STK 原则上可以被写成规则 (物理公式可以描述平衡)，但人类的身体无法按显性规则来执行它们。机器可以通过不同于人类的方式 (例如陀螺仪) 实现同样的任务，但这不是获得了同一种知识。
[来源可信度: 一手 -- Collins 2010, 参见 07-collins-taxonomy.md]

**对 LLM 的意义**: 缺乏 STK 意味着 LLM 的"理解"缺乏身体化锚定 (embodied grounding)。它可以描述骑自行车的物理学，但它不知道骑车是什么感觉。Bender et al. (2021) 的"stochastic parrots"批判 -- LLM 模仿语言但不理解它 -- 可以被理解为 STK 缺失的一个后果。
[来源可信度: 一手 (Bender 批判) / 分析推断 (与 STK 的连接) -- Bender, Gebru, McMillan-Major & Mitchell, "On the Dangers of Stochastic Parrots," FAccT 2021]

### 3. Collective Tacit Knowledge (CTK) -- LLM 的深层限度

CTK 是嵌入在社会实践中的知识，属于社会群体。Collins 认为 CTK 涉及"how to manage trade-offs and repairs or apply the rules of gamesmanship in a human, social context-sensitive way." (Collins 2010, p.120)

**Collins 的强主张**: "we know of no way to describe it or to make machines that can possess or even mimic it." (Collins 2010) 一个合格的图灵测试需要探测 CTK -- 因为它是语言流利性的基础。
[来源可信度: 一手 -- Collins 2010, 经 07-collins-taxonomy.md 确认]

**LLM 是否挑战了 Collins?** 这是最有争议的问题。LLM 确实在语言流利性上通过了许多实际的图灵测试，而 Collins 认为这需要 CTK。两种解释:
- **(a)** Collins 错了: LLM 证明 CTK 可以从文本统计中近似获得
- **(b)** Collins 仍然对: LLM 通过的是弱图灵测试，一旦对话涉及真正需要社会嵌入性的判断 (讽刺的恰当时机、权力关系的微妙感知、某个具体社区的未成文规范)，LLM 就会暴露出它不是社会成员的事实
[来源可信度: 分析性推断 -- 综合 Collins 2010/2018 和 LLM 实际表现]

**Collins 2018 的进一步论证**: 在 *Artifictional Intelligence: Against Humanity's Surrender to Computers* (Polity Press, 2018) 中，Collins 认为机器获得能力的方式是通过"the way we embed them in our society" -- 我们用社会安排来弥补机器缺乏 CTK 的不足。自动驾驶汽车不需要理解社会规范，因为交通规则被显性编码为信号和标线。但这种嵌入有限度。
[来源可信度: 二手 -- Collins 2018, 通过 P2P Foundation review 和 Marx & Philosophy review 确认]

---

## 六、当代 Polanyi Society 的 AI 讨论

### 1. Tradition & Discovery Vol.52 (2026)

Polanyi Society 的学术期刊 Tradition & Discovery 在第 52 卷中包含了 AI 相关内容:
- **Mihaly Heder** (匈牙利学者): 将 Polanyi 的 fiduciary program 延伸至 AI 伦理，论证 Polanyi 的思想如何帮助理解 AI 的挑战和机会
- **更广泛的匈牙利学者贡献**: 多篇文章讨论 Polanyi 思想对理解 AI 和经济学的意义
[来源可信度: 二手 -- 通过 T&D Vol.52 (2026) 目录页描述确认，未读到文章全文]

### 2. March 2026 Zoom Session

用户提到的 "Tempering the AI Revolution: Polanyi's Insights and Current Questions" zoom 会议未能在公开搜索中找到具体信息。Polanyi Society 网站 (polanyisociety.org) 的页面结构未能被 WebFetch 完整提取。
[来源可信度: 未确认 -- 多次搜索未找到具体会议信息]

### 3. Gulick-Collins 对话 (2019)

Walter B. Gulick (Montana State University Billings) 在 2019 年 Polanyi Society 年会上发表了 "Machine and Mind: Questions for Harry Collins"，专门从 Polanyi 的视角向 Collins 提问关于 AI 与心智的问题。这代表了 Polanyi Society 内部对 AI 议题的持续关注。
[来源可信度: 一手 -- 论文在 polanyisociety.org 上有 PDF (polanyisociety.org/2019pprs/Gulick-Mind&Machine-Collins.pdf)，但 PDF 内容未能被提取]

---

## 七、Polanyi 框架对 LLM 限度的预测

综合以上分析，Polanyi 框架做出以下可测试的预测:

### 预测 1: LLM 无法生成真正的新知识

Polanyi 认为发现 (discovery) 依赖于科学家对 "hidden reality" 的预感 (intimation) -- 一种从 subsidiary clues 朝向尚未成形的 focal target 的运动。LLM 可以在训练分布内做出令人印象深刻的组合和推断，但不能"预感到"训练数据之外的实在。

**当前证据**: LLM 确实在数学、编程等领域展现出"创造性"组合。但这些都可以被解释为训练分布内的高维插值。没有证据表明 LLM 能做出类似于科学革命 (Kuhnian paradigm shift) 的认知突破。
[来源可信度: 分析性推断 -- 基于 Polanyi 的 discovery 理论 (Personal Knowledge Ch.6) 和 LLM 实际表现]

### 预测 2: LLM 在需要 fiduciary commitment 的领域会系统性失败

诊断、伦理判断、审美判断 -- 这些需要知者"以自己的人格为赌注"做出判断的领域 -- LLM 将在可靠性上落后于人类专家，因为它没有任何东西可以拿来"打赌"。

**当前证据**: LLM 的 "hallucination" 问题 (自信地生成虚假内容) 恰恰是缺乏 fiduciary commitment 的表现: 没有什么机制让 LLM 对错误感到"痛苦"，因此没有什么机制抑制虚假的自信。
[来源可信度: 分析性推断 -- Polanyi 的 fiduciary 框架 + 已知的 LLM hallucination 问题]

### 预测 3: LLM 将在 RTK 领域持续进步，在 STK/CTK 领域遇到硬天花板

- RTK 受限于训练数据的覆盖范围，但范围可以不断扩大
- STK 需要身体，除非 LLM 连接到机器人或传感器 (embodied AI)，否则无法获得
- CTK 需要社会成员资格，这不是工程问题而是本体论问题
[来源可信度: 分析性推断 -- Collins 三重分类 + LLM 架构分析]

### 预测 4: 人机协作将遵循"延伸而非替代"的模式

Autor (2024) 的"middle class jobs"论证与 Polanyi 框架一致: AI 不是替代人类的隐性知识，而是扩展已拥有部分知识的人的能力范围。这类似于 Polanyi 的工具理论: 工具被内化为身体的延伸，从而扩展了知者的 reach。
[来源可信度: 分析性推断 -- Autor 2024 + Polanyi 的工具理论]

---

## 八、核心争议: LLM 是否拥有某种"隐性知识"?

这是当前争论的焦点。三派观点:

**A. 功能主义立场 -- 是**: LLM 的权重中编码了无法用规则表达的模式。Cheng (2026) 论证: LLM 有价值的能力恰恰是不可解释的那些。这在功能上等价于隐性知识。
[来源可信度: 一手 -- Cheng 2026]

**B. 具身主义立场 -- 否**: Bender et al. (2021)、Collins (2018) 和 Merleau-Ponty 传统认为: 真正的理解需要身体化的参与。LLM 的能力是"a masterful imitation of human linguistic behaviour, creating a convincing simulacrum of understanding" (Palandri, Medium, 2024)，但它缺乏 lived experience, embodied grounding, subjective qualia。
[来源可信度: 一手 (Collins, Bender) / 二手 (Palandri) -- 多源交叉确认]

**C. 中间立场 -- 部分是**: Royal Society 的 2024 论文 "Minds in movement" 提出将 LLM 重新框定为"an exaggeration of an important aspect of human cognition" -- 语言处理能力的夸张化版本。这允许承认 LLM 确实拥有某种知识，同时坚持它不具备完整的人类认知。
[来源可信度: 一手 -- Philosophical Transactions of the Royal Society B, "Minds in movement: embodied cognition in the age of artificial intelligence," 2024]

---

## 九、总结: Polanyi 对 AI 研究者说了什么

1. **LLM 的成功不是对 Polanyi 的反驳，而是对显性知识 / 隐性知识二分法的更精细划分的需求**: 需要区分"从未被编码但原则上可以编码" (RTK) 和"原则上不可编码" (CTK) 的知识。

2. **Polanyi 悖论在 LLM 时代应被重新表述**: 不再是"我们知道的比我们能说的多"(这一点 LLM 部分克服了)，而是"我们知道的比我们能编码为训练数据的多"-- 因为身体化经验和社会嵌入性不能被转化为文本。

3. **AI 的进步路径可以用 Collins 的分层来精确描述**: RTK 领域 (持续进步) → STK 领域 (需要具身化) → CTK 领域 (硬限度)。

4. **Kambhampati 的警告仍然有效**: 纯粹依赖从数据中学习隐性知识，不结合人类的显性知识，会导致可解释性、偏见和鲁棒性问题。AI 系统需要 "Polanyi 的和解" (reconciliation) -- 同时利用显性和隐性知识。

---

## 来源汇总

### 一手来源 (学术论文/著作)
- Polanyi, M. (1966). *The Tacit Dimension*. University of Chicago Press.
- Polanyi, M. (1958). *Personal Knowledge*. University of Chicago Press.
- Collins, H. (2010). *Tacit and Explicit Knowledge*. University of Chicago Press.
- Collins, H. (2018). *Artifictional Intelligence: Against Humanity's Surrender to Computers*. Polity Press.
- Autor, D. (2014). "Polanyi's Paradox and the Shape of Employment Growth." NBER Working Paper 20485. [PDF](https://economics.mit.edu/sites/default/files/publications/polanyis%20paradox%202014.pdf)
- Autor, D. (2024). "Applying AI to Rebuild Middle Class Jobs." NBER Working Paper 32140. [NBER](https://www.nber.org/papers/w32140)
- Kambhampati, S. (2021). "Polanyi's Revenge and AI's New Romance with Tacit Knowledge." *Communications of the ACM*, 64, 31-32. [CACM](https://cacm.acm.org/opinion/polanyis-revenge-and-ais-new-romance-with-tacit-knowledge/)
- Cheng, Q. (2026). "Why the Valuable Capabilities of LLMs Are Precisely the Unexplainable Ones." arXiv:2603.15238v1. [arXiv](https://arxiv.org/html/2603.15238v1)
- Bender, E., Gebru, T., McMillan-Major, A. & Mitchell, M. (2021). "On the Dangers of Stochastic Parrots." *FAccT 2021*.

### 二手来源 (评论/综述)
- Kahn, J. (2024). "Why AI might finally break Polanyi's Paradox." *Exponential View*, Nov 27. [Link](https://www.exponentialview.co/p/ai-polanyi-paradox)
- Gulick, W.B. (2019). "Machine and Mind: Questions for Harry Collins." Polanyi Society 2019 Papers. [PDF](https://polanyisociety.org/2019pprs/Gulick-Mind&Macnine-Collins.pdf)
- *Tradition & Discovery* Vol.52 (2026). Polanyi Society Journal. [Link](https://polanyisociety.org/tad-52-1-2026/)
- "Minds in movement: embodied cognition in the age of artificial intelligence." *Phil. Trans. R. Soc. B*, 2024. [Link](https://royalsocietypublishing.org/doi/10.1098/rstb.2023.0144)
- Wikipedia: "Polanyi's paradox." [Link](https://en.wikipedia.org/wiki/Polanyi%27s_paradox)

### 未确认来源
- Polanyi Society March 2026 Zoom session "Tempering the AI Revolution" -- 多次搜索未找到
- Heder, M. (2026). T&D Vol.52 文章全文 -- 仅通过期刊描述确认存在
