import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))
data = read('content/section23-concepts-examples.json')
exercises = read('content/section23-exercises-1-32.json') + read('content/section23-exercises-33-64.json')
assert [q['number'] for q in exercises] == list(range(1,65))
data['textbook']['exercises'] = exercises
data['lesson']['solutionReference'] = {
    'title': 'Stewart 7E Solutions',
    'printedPages': [87,97],
    'pdfPages': [97,107],
    'use': 'Cross-checking only; bilingual steps are independently rewritten.'
}
for exercise in exercises:
    exercise['relatedExamples'] = [
        q['id'] for q in data['lesson']['questions']
        if any(link['number'] == exercise['number'] for link in q.get('relatedExercises',[]))
    ]
review_file = ROOT / 'audit/review-status-2-3.json'
if review_file.exists():
    data['audit'] = read('audit/review-status-2-3.json')
(ROOT/'content/section-2-3.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest = {'course':data['course'],'sections':[{
    'slug':'2-3','section':'2.3','title':data['lesson']['title'],
    'en':{'title':data['lesson']['en']['title'],'chapter':'Chapter 2 · Limits and Derivatives'},
    'chapter':'第 2 章 · 极限与导数',
    'counts':{'concepts':8,'examples':11,'practice':0,'exercises':64},
    'data':'content/section-2-3.json'
}]}
(ROOT/'course.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rows = ['# 2.3 例题—课后习题教学对应表\n',
        '对应关系依据解题方法整理，并非教材原有的官方配套编号。所有 64 道习题均保留完整解析。\n',
        '| 正文例题 | 知识点 | 同型练习 | 综合与拓展 |',
        '| --- | --- | --- | --- |']
names = {c['id']:c['title'] for c in data['lesson']['concepts']}
for q in data['lesson']['questions']:
    groups = {key: ', '.join(str(link['number']) for link in q['relatedExercises'] if link['relation']==key)
              for key in ['same-method','extension']}
    rows.append(f"| {q['label']} | {names[q['concept']]} | {groups['same-method']} | {groups['extension'] or '—'} |")
rows += ['\n## 知识点覆盖\n','| 知识点 | 全部关联习题 |','| --- | --- |']
for cid,name in names.items():
    ns = [str(q['number']) for q in exercises if cid in ([q['concept']] if isinstance(q['concept'],str) else q['concept'])]
    rows.append(f"| {name} | {', '.join(ns)} |")
(ROOT/'project-docs/section-2-3-classification.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
print('Assembled 8 concepts, 11 examples, 64 exercises; review flags:',data['audit'])
