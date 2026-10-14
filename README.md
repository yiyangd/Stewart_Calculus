# Stewart Calculus · 双语学习网站

按照 Precalc 11 的学习流程制作：知识点 → 解题方法 → 教材例题 → 对应节后习题。默认英语，可切换中文。

- 第 2.3 节 **Calculating Limits Using the Limit Laws / 用极限定律计算极限**。
- 8 个知识点、全部 11 道正文例题、全部 64 道节后习题及其小问。
- 每题有独立分步解析，包含图像、数值表、分段函数图、取整函数图和证明。
- 每道例题提供同型练习与综合拓展链接。这些对应关系按方法整理，并非出版社的官方配套编号。
- 例题解析默认展开，课后习题解析默认收起。支持题号范围、关键词、知识点筛选、进度保存及打印。
- 本节没有独立 Practice Problems，网站按教材实际内容展示。

## 入口

[课程首页](https://yiyangd.github.io/Stewart_Calculus/) · [2.3 英文](https://yiyangd.github.io/Stewart_Calculus/sections/2-3/?lang=en) · [2.3 中文](https://yiyangd.github.io/Stewart_Calculus/sections/2-3/?lang=zh)

本地直接打开 `site/index.html`，无需安装。公式、数据和图像随网站提供，支持离线阅读。

## 项目结构

```text
content/                  双语内容、独立覆盖清单、给定原图和解析图
course.json               独立课程标识与章节清单
site/                     可直接打开或发布的静态网站
scripts/                  来源定位、内容装配与核验
audit/                    各段数学审核及最终审核状态
project-docs/             Precalc 工作复盘、例题对应表、独立复审
workflow/                 项目内 skill 和后续章节 prompts
gh-pages 分支             仅发布 site/ 中的静态网站
```

## 后续章节

使用 `workflow/prompts/` 内的通用与独立复审 prompts，并遵循 `workflow/textbook-study-site/SKILL.md`。先清点原书，再按知识点分类，完成双语逐步解析、来源核对、独立数学复审与网页检查。

修改内容后重新装配与构建；最终构建要求真实的来源和解答审核记录，不能仅为了通过检查而设置完成标志。

```powershell
python scripts/build_section23_examples.py
python scripts/assemble_section23.py
python workflow/textbook-study-site/scripts/check_content.py D:/Stewart-Calculus/content/section-2-3.json
python workflow/textbook-study-site/scripts/build_course.py --manifest D:/Stewart-Calculus/course.json --output D:/Stewart-Calculus/site
```

## 来源与核对

教材：James Stewart, *Calculus: Early Transcendentals*, 7th Edition；2.3 位于印刷页 99–108、PDF 页 131–140。最后一页以第 64 题结束，随后进入 2.4。

答案核对：*Stewart 7E Solutions*，印刷页 87–97、PDF 页 97–107。答案书用于校核，网站的双语步骤独立改写。

原书 PDF 保留在本地项目，未纳入仓库或发布网站。题目与图像保留逐题来源位置。审核证据见 `audit/` 与 `project-docs/independent-review-2-3.md`。

GitHub Pages 从 `gh-pages` 分支的根目录发布。主分支保留课程源数据、网站、技能、prompts 和审核记录；后续更新网站时，将 `site/` 的内容同步到发布分支。
