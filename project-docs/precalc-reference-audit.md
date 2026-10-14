# Pre-Calculus 11 参考项目审查

审查日期：2026-10-14。源项目 `D:\Pre-Cal11` 仅作只读参考，未作修改。本记录依据实际目录、数据、脚本和审核记录；历史数据中的“已复核”是其保存的审核证据，本次没有重新逐题重算全部 Precalc 习题。

## 用户已经建立的材料与流程

| 位置 | 实際内容与用途 |
| --- | --- |
| 根目录教材 PDF | `Precalculus A Unit Circle Approach 4th Edition by J. S. Ratti.pdf`，约 116 MB。 |
| `lectures/` | 第 2.4 节 Part 1 与 Part 2 讲义 PDF，分别 28/13 PDF 页。 |
| `content/` | 第 2.4 节讲义与教材 JSON；第 2.5/2.6 节分开的正文例题和连续习题段 JSON；组装、英文整理、UI 与默认语言修订脚本。 |
| `sites/section-24/dist/` | 实际课程网站：首页和 `sections/2-4`、`2-5`、`2-6`，保留单节题目数据、脚本、样式和图像。 |
| `github-export/precal11-study/` | GitHub 静态公开包，有 README、`.nojekyll`、首页与全部 3 节；源书 PDF 不在公开包。 |
| `workflow/教材网站通用Prompt.txt` | 可填教材、章节、讲义、课程名、输出与发布目标的 reusable prompt。 |
| `workflow/textbook-study-site/` | 项目附带通用技能：SKILL、前端模板、数据合同、数学和来源审核、模型分工、标准库构建与覆盖检查脚本。 |
| `workflow/textbook-study-site.zip` | 技能打包副本。 |
| `tmp/` | 分题段原文、渲染页、题图裁剪、构建代码、数学复核、技能正常/错误样例与浏览器检查记录。 |

未发现根目录或子目录 `AGENTS.md`；唯一检索到的 README 是 GitHub 导出包的 README。技能项目副本与全局 `textbook-study-site/SKILL.md` 的 SHA-256 一致，说明已有 Precalc 工作流确实沉淀成通用技能，而非仅留网站。

## 已完成章节的实际结构

| 章节 | 主题 | 知识点 | 正文/讲义例题与练习 | 节后习题 | 来源范围 |
| --- | --- | ---: | --- | ---: | --- |
| 2.4 | 有理函数、渐近线、空洞与图像 | 7 | 18 道讲义题：11 Example、7 Practice | 137 | 教材印刷 199–219 / PDF 223–243；另有两份讲义。 |
| 2.5 | 多项式与有理不等式 | 8 | 全部 6 Example + 6 Practice Problem | 128 | 教材印刷 220–234 / PDF 244–258。 |
| 2.6 | 多项式函数的零点 | 8 | 全部 7 Example + 7 Practice Problem | 88 | 教材印刷 235–245 / PDF 259–269。 |

2.4 的数据根节点为 `lecture` 和 `textbook`；2.5/2.6 为 `lesson` 和 `textbook`。这些是历史站点格式，并非后来通用技能的新站格式。历史站点的正文审核在 `lesson.audit` 或 `lecture.audit`，习题审核保留在分题段数据或 `textbook.audit`；不能直接拿旧数据通过新合同而声称完成迁移。

新站格式需要稳定 `course.id`、`lesson.id`、独立 `coverage` 和顶层审核布尔值。Stewart 是独立新书，适合通用格式；保留旧站只读作为参考。

## 学生界面与实际行为

- 奶油色背景、深青色主色、左侧知识点目录和右侧内容。每点有摘要、统一方法步骤、容易漏掉的条件、教材例题、可先尝试的练习及节后题号链接。
- 默认英文；`?lang=zh` 指定中文，导航带语言参数。历史中文偏好不会覆盖无有效参数时的英文默认。
- 每次语言切换重新渲染内容，但保存筛选、关键词、解析开合、当前滚动锚点和本节完成进度。
- 例题解析默认展开；Practice 与 Exercise 默认收起。原图显示在解答之前，避免图题还没看图就需展开答案。
- 知识点“已掌握”勾选保存在浏览器，各节有不同进度 key。知识点、题号/范围/关键词筛选；可展开/收起全部、返回首页和打印。
- 本地文件直接打开可用：每节 HTML 内嵌 JSON，旁边 `data.json` 必须保持相同。静态 GitHub Pages 无需安装前端依赖。
- 2.5 增加符号表，区间符号和端点包含分别表示；2.6 增加逐列对齐的合成除法表；小屏图表在容器内滚动。
- 数学使用固定命令集合的本地渲染器。通用模板将不支持的数学命令显示为审核提示，因此新课程新增表示法必须检查实际页面，不能只看 JSON 正常。

## “例题对应课后习题”的实际逻辑

历史 `sections/2-6/app.js` 的 `associatedExercises(id)` 筛选 `Exercise.concept`；`topicSection` 将同知识点的 Example/Practice 放在一起，在知识点底部列前 16 个题号，并在题量较多时提供“全部 N 题”筛选入口。

这是一种**知识点 → 相关习题**结构，旧站没有逐例题对应字段，也没有同型/综合/拓展或映射理由。下面为读取第 2.6 节数据所得的实际关联，展示了现有逻辑的边界：

| 知识点 ID | Example | Practice | 关联 Exercises |
| --- | --- | --- | --- |
| `descartes` | 1 | 1 | 1, 2, 9–22, 71–74 |
| `bounds` | 2 | 2 | 23–30 |
| `real-zeros` | 3 | 3 | 无直接标签匹配，因此显示浏览本节题库。 |
| `complex-zeros` | 无 | 无 | 3, 5, 7, 8, 31–40 |
| `conjugates` | 5, 6 | 5, 6 | 4, 6, 41–46 |
| `construct` | 4 | 4 | 47–50, 65–68, 75–78 |
| `all-zeros` | 7 | 7 | 51–64, 79–82 |
| `extensions` | 无 | 无 | 69, 70, 83–88 |

Stewart 当前请求更细：每道原例题连接具体课后题。建议保留知识点层全类入口，同时独立建立逐例题映射；逐条说明共同运算或推理，区别同型、综合与拓展，明确是教学整理。多个例题可链接同一 Exercise，但 Exercise 只有一个完整条目和稳定 ID。教材无配套 Practice 的章节应记 0，不能套用 Precalc 的 6 或 7 道。

## 已有数学与来源审核证据

第 2.4 节讲义 audit 保存逐页覆盖和勘误：将笼统的 oblique 限定为分子次数只高 1 的直线情况，区分相对于 x 轴与相对于水平渐近线的符号，并重写原讲义循环引用步骤。README 同时明确教材 Exercise 137 的原 GeoGebra 内容/准确公式尚未核实，网页中的公式只是补充模型。这个限制必须保留，不能以“137 题”计数隐去。

第 2.5 节正文 audit 保存 6+6 题覆盖、PDF 245–254 的目视核对、精确区间符号/端点和 SymPy 解集复核，以及 Example 5 严格不等式在教材解释中被误印为非严格的修正。习题数据按 1–76 与 77–128 分段，保留符号表、原图、应用域、定义域、构造题等核验。`tmp/section25-exercises-b/audit_math.py` 独立用原式和情境有效域交集核对应用题、定义域、构造题和复合区间。

第 2.6 节正文 audit 保存全部 7+7 题与例题 4/练习 4 小问、12 个精确因式分解/重数、21 合成除法行、笛卡尔计数及长除法审核。它修正教材下界法遗漏负测试值条件的问题，保存正值测试的具体反例。41–88 题段记录目视核对 PDF 268/269、原图 65–68、右栏 83(c)，并保留复系数不应用共轭配对、尺度不唯一、Cardano 实立方根分支与 Vieta 重数等说明。`tmp/section26-examples/audit_exercises_b.py` 与 `tmp/section26-exercises-a/audit_b.py` 从独立转录系数核对根、每列合成除法及商余关系。

## 通用技能已经测试的边界

`tmp/study-skill-evaluation/run/source-inventory.json` 是先建立的独立清单。`verification-report.json` 记录：

- 删除 Exercise 3 的小问后，checker 与 builder 均失败，输出目录未生成。
- 删除英文答案后，两者均失败，输出目录未生成。
- 初始 Python 字符串将 `\\ne` 和 `\\frac` 变成换行与 form-feed，浏览器目视发现后用 raw strings 修复，增加控制字符和原始 LaTeX 检查，双语重看通过。
- 正常样例通过内嵌/独立数据一致、英文默认、来源是真实非 PDF 定位、数学样例及浏览器检查。
- 语言切换保留筛选/展开/进度；两门课程进度独立；无参数返回英文；浏览器无控制台错误。

这些说明工具能拦截真实覆盖和显示错误，但不等于原教材每题数学正确，也不替代当前 Stewart 的独立清点与复审。

## 迁移到 Stewart 的落实

已复制通用技能的 `SKILL.md`、`references/`、`scripts/`、`assets/frontend/`、`agents/` 至本项目 `workflow/textbook-study-site/`，排除 `__pycache__`。复制时 9 个脚本/前端/UI 元数据文件的哈希与源副本一致；随后主任务在项目副本增加逐例题链接、解析图、嵌套小问及极限/取整/分段/数值表显示支持。本地 SKILL 增加 Stewart 专项 reference，未修改全局技能或源 Precalc 项目。实际新字段与支持范围已补入项目的数据合同。

新增 `references/stewart-project.md` 处理教材/答案双来源、正文 Example 到 Exercise 的逐条映射、原书无 Practice 的准确计数和第 2.3 节极限专项核验。新增 4 个 prompts：通用新章节、当前 2.3、独立复审和恢复制作；流程入口为 `workflow/README.md`。

本项目约定由主任务确定：`course.id=stewart-calculus-7e`、`content/section-2-3.json`、`site/sections/2-3/`。第 2.3 节由教材来源清点任务报告：教材 PDF 131–140 / 印刷 99–108，正文 Example 1–11、无独立 Practice、Exercise 1–64；答案书 PDF 97–106 / 印刷 87–96。此处记录的是任务输入，实际逐题覆盖审核以本项目的原书清单与复审为准。

后续章节继续复用相同流程和独立课程；已完成内容按题段保存，修订仅重核受影响条目。网页交付和 GitHub 部署分别记录，最终以实际已确认入口及覆盖数量报告。
