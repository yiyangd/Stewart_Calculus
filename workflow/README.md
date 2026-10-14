# Stewart Calculus 制作流程

本目录继承 `D:\Pre-Cal11\workflow` 的通用技能与 prompt，供本项目后续章节继续使用。项目内技能位于 [textbook-study-site/SKILL.md](textbook-study-site/SKILL.md)，无需修改全局技能。Precalc 实际参考审查见 [precalc-reference-audit.md](../project-docs/precalc-reference-audit.md)。

## 从哪里开始

- 新章节使用 [教材网站通用Prompt.txt](prompts/教材网站通用Prompt.txt)，填写范围。
- 当前优先章节使用 [Stewart-2.3-Prompt.txt](prompts/Stewart-2.3-Prompt.txt)。
- 数学与来源复审使用 [章节独立复审Prompt.txt](prompts/章节独立复审Prompt.txt)。
- 中断后继续使用 [恢复制作Prompt.txt](prompts/恢复制作Prompt.txt)。

## 项目约定

```text
Stewart-Calculus/
  course.json                     课程 ID、章节与实际题量
  content/                        已完成的双语课次 JSON 与题目原图
  site/                           学生可打开的静态学习网站
  project-docs/                   原书清单、例题对应、数学与网页审核记录
  workflow/
    textbook-study-site/          项目内技能、数据合同、前端与构建工具
    prompts/                     可直接复用的制作和复审请求
  tmp/                            原文抽取、整页渲染与临时题段
```

教材与参考答案保留在本地根目录，网站公开包只含必要题目数据与题目原图。网站不依赖本机 PDF 路径。课程 ID 在 `course.json` 中确定后保持稳定，章节用 `sections/<slug>/`；后续新增章节保留旧地址与学习进度。

## 一节的制作顺序

1. **独立清点。** 对照教材页面确定节的边界、实际 PDF/印刷页、全部 Example/Exercise 与小问、原图；记录清单再写答案。
2. **分类与对应。** 按解题方法压缩知识点，建立每道正文例题到节后习题的具体对应，注明同型、综合或拓展及理由。
3. **逐题解答。** 保留原题形式和条件，写出具体的“动作 → 运算 → 结果”。参考答案用于核对，省略的过程自行补足。原书无 Practice 时其数量记 0。
4. **来源和数学复核。** 复核者重新读教材与答案页，独立检验重要运算、定义域、左右极限、所有小问及映射理由；处理差异并保存记录。
5. **静态构建。** 数据审核确实完成后设置审核标志，运行结构覆盖检查与构建工具。生成独立 `data.json` 与相同的内嵌数据。
6. **学生体验验收。** 检查英文默认、中文切换、例题默认展开、习题默认收起、筛选、每例题对应链接、独立进度、返回首页、手机及打印。
7. **按会话授权交付。** 本地入口与线上发布分开记录；发布后检查实际部署及关键资源，未确认的环节不能称已完成。

## 检查与构建

在项目根目录，使用本机可用的 Python 运行：

```text
python workflow/textbook-study-site/scripts/check_content.py content/section-2-3.json
python workflow/textbook-study-site/scripts/build_course.py --manifest D:/Stewart-Calculus/course.json --output D:/Stewart-Calculus/site
```

文件名以实际 `course.json` 为准。checker 的 `--allow-draft` 仅用于预览结构；最终 builder 要求真实审核完成。工具通过只证明数据格式与清单匹配，数学正确性需独立复核。

前端和工具以已在 Precalc 工作流验证的通用技能为起点。本项目增加逐例题对应链接、解析内图像、嵌套小问 ID 与极限/取整/分段/数值表表示法；具体扩展写在 [数据合同](textbook-study-site/references/content-schema.md)。项目专项约定在 [stewart-project.md](textbook-study-site/references/stewart-project.md)；后续只更新受影响题目、例题映射和对应审核，不重新制作已核章节。
