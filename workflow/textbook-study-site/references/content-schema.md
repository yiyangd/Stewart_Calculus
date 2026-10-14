# Bilingual textbook study-site data contract

This is the portable format for **new** course sites. Keep existing sites in their own
format unless an explicit migration has been reviewed. Do not point the generic
builder at an existing site: it may contain legacy lecture data and
section-specific teaching features.

The Chinese text is the base record. Every displayed narrative field also has an
English version under `en`. English terminology and questions must be checked
against the textbook, not inferred from the Chinese translation. Both languages
must explain the same steps and answer the same subparts. Math strings use `$...$`
and literal LaTeX; JSON backslashes must be doubled. No JavaScript, executable
expression strings, remote scripts, credentials or local absolute paths belong in
public data. A displayed source filename may be relative; a machine path must not
be copied into the website.

Use raw strings or correctly escaped backslashes when producing JSON with Python:
`"\\ne"`, `"\\to"` and `"\\frac"` must remain literal LaTeX commands, rather
than becoming newline, tab or form-feed characters. The checker rejects invisible
control characters such as backspace/form-feed anywhere in public strings. Normal
paragraph newlines and tabs are allowed, but raw controls inside paired `$...$`
inline math are rejected because the inline renderer cannot display those spans.
`$$...$$` display math is separate and may contain line breaks; unpaired currency
dollar signs are not rejected by this narrow check. This finds rendering risks,
not mathematical errors or every possible LaTeX syntax error.

## File layout and build commands

```text
project/
  course.json
  content/
    section-1.json
    assets/               # raster source figures used by section-1.json
      ex-1.png
  site/                   # choose a new empty output directory
```

Run `python <skill>/scripts/check_content.py <absolute lesson.json>` for each
lesson, then `python <skill>/scripts/build_course.py --manifest <absolute
course.json> --output <absolute site-dir>`. These tools use only Python's standard
library. They do not publish, modify Git or change site access permissions.

`--allow-draft` exists **only** on the checker. It permits false review flags for
preview, labels the result as draft, and still enforces all structural checks.
The final builder rejects unreviewed content. A passing result checks structure,
safe data and source-ledger coverage; **it does not prove the mathematics correct
or prove that the ledger was independently counted**. A separate source and
solution review is required before setting the review flags true.

The builder writes an ownership marker and refuses a nonempty output directory
without it, or one owned by a different `course.id`. It updates only the supplied
sections and its own root files, retaining previously built sections and home cards
that were omitted from the current manifest. It never recursively clears output.
It validates all inputs before output writes, then stages complete files and
replaces individual files atomically; a disk/OS failure is still not a whole-site
transaction. Backups or version control remain appropriate. Symlink/junction
traversal is refused, and assets must be ordinary local raster files.

## Course manifest: `course.json`

| Field | Required format |
|---|---|
| `course.id` | Stable lowercase letters/digits/hyphens; unique to the book/course. |
| `course.title`, `course.en.title` | Chinese and English course titles. |
| `sections` | Ordered array of the sections being built. |
| `sections[].slug` | Safe stable lowercase ID, also the lesson's `lesson.id`. |
| `section`, `title`, `en.title` | Section number as string; titles must match lesson data. |
| `chapter`, `en.chapter` | Optional bilingual chapter labels. |
| `counts` | Nonnegative integer `concepts`, `examples`, `practice`, `exercises`; exact actual counts. |
| `data` | Portable relative path from the manifest, e.g. `content/section-1.json`; no `..`, slash root, backslash or drive prefix. |

Input `data` preparation paths are omitted from public home metadata. The output
is a root homepage and `sections/<slug>/` lesson folders, with matching embedded
JSON and `data.json`. JSON is escaped before embedding in HTML. Each lesson gets
its own script, stylesheet and `assets/` files.

## Lesson content

| Field | Required format |
|---|---|
| `course` | Same `id`, Chinese `title` and `en.title` as manifest. |
| `lesson.id`, `lesson.section`, `lesson.title`, `lesson.en.title` | Stable slug, section string, bilingual titles. |
| `lesson.description`, `lesson.en.description` | Optional paired descriptions. |
| `lesson.source` | `title`, `kind` (`pdf`, `text`, `html`, `epub`, `image`) and available real location metadata. PDF sources need `pdfPages`; `printedPages` is optional when no printed page labels exist. Both use positive one-based ordered page arrays. `[220,234]` means the source span, not a guarantee every intermediate page was read. |
| `lesson.concepts` | Nonempty array of `{id,title,summary,method,pitfalls,en:{title,summary,method,pitfalls}}`. |
| `method` | Nonempty ordered `{title,body}` steps; English count must equal Chinese count. |
| `pitfalls` | Array of strings, possibly empty; bilingual count must match. |
| `lesson.questions` | Textbook examples and associated practice problems, in source order within each type. |
| `textbook.exercises` | All section-end exercises in source order; not selected samples. |
| `coverage` | Independent source inventory described below. |
| `audit.sourceReviewed`, `audit.solutionsReviewed` | Actual booleans; both `true` only after the corresponding reviews. |

Course titles must match the manifest in both languages. Existing site titles
cannot be silently changed under the same `course.id`; a deliberate whole-course
rename must adapt and review every existing chapter separately.

Every example/practice has `{id,type,label,prompt,concept,steps,answer,printedPage,
pdfPage,en:{label,prompt,steps,answer}}`. Its `type` is `example` or `practice` and
`concept` is one existing concept ID. Examples remain labeled as textbook examples;
never imply lecture notes exist when they do not.

Every exercise has `{number,prompt,concept,steps,answer,printedPage,pdfPage,
en:{prompt,steps,answer}}`. `number` is a positive integer or its string form
(optionally a letter suffix such as `12a`); booleans are rejected. Exercise
`concept` may be a single ID or an array of distinct existing IDs. Related exercise
links use these associations. Every step in either language has nonempty `title`
and `body`, and the bilingual step counts must match. The answer must include all
required cases, domain restrictions, units and approximations where appropriate.

For PDF sources, `pdfPages` and every question's actual `pdfPage` are required.
`printedPages` and each `printedPage` are optional: record them when visible in the
source, and validate them when present. A PDF or lecture handout without printed
page labels is accurately located by its PDF page alone; never invent a printed
page label to satisfy a schema.

For a non-PDF source, set the explicit
`lesson.source.kind` and omit `pdfPages`/`pdfPage` unless they actually exist. Each
question must instead provide at least a real `printedPage` or a nonempty
`sourceLocator` (e.g. `"Section 1, lines 12–16"`, `"Chapter 3, Example 2"` or an
EPUB section anchor). `printedPages` may still describe actual printed page labels.
Do **not** invent PDF page 1 to satisfy a schema. Unknown/missing source kinds and
questions without a real locator fail validation. For backward compatibility,
omitting `kind` when `pdfPages` exists means PDF; providing `pdfPages` always
enables the stricter PDF page requirements.

Optional record fields: `expressionLatex`, `subpartIds`, `sourceImage`, `graph`,
`signChart`, `syntheticDivisions`, `sourceType`, `sourceName`, `en.sourceName`.
`sourceType` is `textbook` (the default) or `lecture`; any other value fails
validation. When a source name is given, both the Chinese `sourceName` and English
`en.sourceName` must be nonempty. Mixed textbook/lecture records retain clearly
distinguished labels and source names; do not label a lecture problem as a
textbook example. Give every record a distinct ID, e.g. `textbook-example-1` and
`lecture-example-1`, even when source labels both say “Example 1”. Both appear in
the independent coverage ledger just like all other examples/practice problems.

The available main `lesson.source.printedPages`/`pdfPages` arrays describe that source's span
for display. They do not replace each record's actual page/location fields and
are not universal bounds on mixed sources. A lecture record's `pdfPage` and any
available `printedPage` must refer to its own lecture PDF, even when those pages lie outside the
main textbook's span. Never relabel lecture page 3 as a textbook page to fit a
range.

Exact equations can use literal LaTeX even when
graph coordinates are decimal approximations. Other metadata may be preserved,
but every public string is scanned for local paths and common credential fields.

## Independent coverage ledger

```json
{
  "expectedExamples": ["example-1", "example-2"],
  "expectedPractice": ["practice-1", "practice-2"],
  "expectedExercises": [1, 2, 3],
  "expectedSubparts": {
    "exercise-3": ["a", "b", "c"],
    "example-2": ["a", "b"]
  }
}
```

Count these identifiers from the original textbook **before** producing solutions;
do not generate expected coverage from the finished data. A reviewer must compare
the inventory to source pages, section boundaries, graph labels and all subparts.
Expected and actual IDs are compared in order, and duplicates, unexpected IDs,
missing IDs, Boolean exercise numbers, and omitted ledger fields fail validation.
An exercise's subpart key is `exercise-<number>`; example/practice keys are their
record IDs. Each multipart record must include its `subpartIds` in the same order
as the independent inventory. Metadata presence alone does not establish that
every subpart was solved: reviewers must check the written steps and answers.

This project's checker also permits dotted nested subpart IDs, matching the
book's hierarchy: `a.i`, `a.ii`, `b.iv`. Each component contains lowercase letters
or digits, and the full ID must match the independently counted ledger in order.
Do not flatten nested source questions or change their labels solely to pass a
format check.

## Stewart project extensions

The project frontend and builder extend the portable base format without changing
the ordinary Example/Exercise IDs or coverage contract:

- `primaryConcept`: optional main display concept; otherwise the first `concept`
  association is used. Examples still display once, while exercises may have
  several topic associations.
- An Example's `relatedExercises` is an array of
  `{number, relation, reason, en:{reason}}`. The supported display relations are
  `same-method` and `extension`; the latter is labeled “Applications and
  extensions” and includes combined methods. Every number must refer to an actual
  Exercise. Reasons must describe the actual method, and the association must be
  reviewed independently against the two questions.
- An Exercise's `relatedExamples` lists actual Example IDs for reciprocal metadata.
  This does not duplicate the Exercise or replace its own complete explanation.
- `solutionImage` uses the same safe `assets/<raster-file>` paths as `sourceImage`,
  is validated and copied by this project builder, and is shown inside the
  solution. Keep `sourceImage` for a given problem figure that students must see
  before opening the solution. Keep source or construction provenance in the
  audit.
- This project's math renderer supports simple LaTeX `array` tables, `cases`,
  floor/ceiling notation and limit subscripts. These still require visual QA,
  especially fractions and long tables on narrow screens; the base renderer's
  command list is not a guarantee that every LaTeX expression is supported.

The generic structural checker does not prove the mathematical accuracy of these
links or their classification. Compare the final associations to
`project-docs/section-2-3-classification.md` and review every affected link when
changing an example or exercise.

## Optional diagrams

`sourceImage` must be `assets/<file>`, using forward slashes without empty,
`.` or `..` components. It is resolved next to the lesson JSON, not the manifest.
Allowed raster extensions: PNG, JPEG, WebP and GIF. It should be a clean figure
crop with page provenance. For graph-reading questions the given figure must be
visible before opening the solution. Avoid unnecessary reproduction of source
pages, decorative material and unrelated textbook content.

`graph` accepts finite numeric polynomial coefficients in descending-power order:

```json
{
  "numerator": [1, 1],
  "denominator": [1],
  "bounds": {"xMin": -4, "xMax": 4, "yMin": -4, "yMax": 4},
  "verticalAsymptotes": [],
  "horizontalAsymptote": null,
  "holes": [],
  "points": [{"x": -1, "y": 0}]
}
```

Supported optional keys are `label`, `obliqueAsymptote:{slope,intercept}`,
`polynomialAsymptote:[coefficients]`, and `traces:[graph-like records]`. Traces
share the outer bounds and cannot contain nested traces. `holes` and `points` use
finite numeric `{x,y}` pairs. The denominator cannot be the zero polynomial. No
functions, `eval`, code strings or symbolic coefficient evaluation are allowed.

`signChart` uses ordered numeric boundaries, exact LaTeX labels and explicitly
selected intervals:

```json
{
  "expressionLatex": "x+1",
  "boundaries": [{"value": -1, "label": "-1", "kind": "zero", "included": true}],
  "intervals": [
    {"left": null, "right": -1, "sign": "-", "selected": false, "testPoint": -2},
    {"left": -1, "right": null, "sign": "+", "selected": true, "testPoint": 0}
  ],
  "solutionLatex": "[-1,\\infty)"
}
```

`null` denotes infinity at an outer endpoint. There must be exactly one interval
per boundary gap, in order. Boundary `kind` is `zero` or `excluded`; excluded
domain points always have `included:false`. An included isolated point is allowed
even if both neighboring intervals are unselected. `testPoint` and `valueLatex`
are optional. Sign and endpoint consistency still need mathematical review.

`syntheticDivisions` is an array of tables:

```json
{
  "rootLatex": "-1",
  "coefficientsLatex": ["1", "1"],
  "productsLatex": [null, "-1"],
  "bottomLatex": ["1", "0"],
  "remainderLatex": "0",
  "quotientLatex": "1"
}
```

All three rows must have identical lengths of at least two; every entry is a
literal math string, except the first products cell may be null. The last bottom
cell must equal `remainderLatex`. A checker verifies format and matching cells,
not the arithmetic of a division using symbolic/complex coefficients.

## Minimal schema-only example

The following equations are invented solely to illustrate the format. They are
**not a source inventory or replacement for any book's original problems**. In a
real course, count all original questions/subparts and review the full solutions.

Manifest:

```json
{
  "course": {"id":"schema-demo","title":"格式示例","en":{"title":"Schema demonstration"}},
  "sections": [{
    "slug":"section-1","section":"1","title":"一次方程","en":{"title":"Linear equations"},
    "counts":{"concepts":1,"examples":1,"practice":1,"exercises":1},
    "data":"content/section-1.json"
  }]
}
```

Lesson `content/section-1.json`:

```json
{
  "course":{"id":"schema-demo","title":"格式示例","en":{"title":"Schema demonstration"}},
  "lesson":{
    "id":"section-1","section":"1","title":"一次方程","en":{"title":"Linear equations"},
    "source":{"title":"Invented schema fixture, not a textbook","printedPages":[1],"pdfPages":[1]},
    "concepts":[{
      "id":"linear","title":"解一次方程","summary":"两边进行相同运算。",
      "method":[{"title":"隔离未知数","body":"先去常数，再除以系数。"}],"pitfalls":[],
      "en":{"title":"Solve a linear equation","summary":"Apply the same operation to both sides.",
        "method":[{"title":"Isolate the variable","body":"Remove the constant, then divide by the coefficient."}],"pitfalls":[]}
    }],
    "questions":[
      {"id":"example-1","type":"example","label":"例题 1","prompt":"解 $x+1=0$。","concept":"linear",
       "steps":[{"title":"减去 1","body":"两边减去 $1$，得 $x=-1$。"}],"answer":"$x=-1$","printedPage":1,"pdfPage":1,
       "en":{"label":"Example 1","prompt":"Solve $x+1=0$.","steps":[{"title":"Subtract 1","body":"Subtract $1$ from both sides to obtain $x=-1$."}],"answer":"$x=-1$"}},
      {"id":"practice-1","type":"practice","label":"练习 1","prompt":"解 $x-2=0$。","concept":"linear",
       "steps":[{"title":"加上 2","body":"两边加上 $2$，得 $x=2$。"}],"answer":"$x=2$","printedPage":1,"pdfPage":1,
       "en":{"label":"Practice Problem 1","prompt":"Solve $x-2=0$.","steps":[{"title":"Add 2","body":"Add $2$ to both sides to obtain $x=2$."}],"answer":"$x=2$"}}
    ]
  },
  "textbook":{"exercises":[
    {"number":1,"prompt":"解 $2x=4$。","concept":"linear",
     "steps":[{"title":"除以 2","body":"两边除以 $2$，得 $x=2$。"}],"answer":"$x=2$","printedPage":1,"pdfPage":1,
     "en":{"prompt":"Solve $2x=4$.","steps":[{"title":"Divide by 2","body":"Divide both sides by $2$ to obtain $x=2$."}],"answer":"$x=2$"}}
  ]},
  "coverage":{"expectedExamples":["example-1"],"expectedPractice":["practice-1"],"expectedExercises":[1],"expectedSubparts":{}},
  "audit":{"sourceReviewed":true,"solutionsReviewed":true,"note":"Schema fixture only; not real-book coverage."}
}
```
