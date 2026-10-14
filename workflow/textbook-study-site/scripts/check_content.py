#!/usr/bin/env python3
"""Check source coverage, bilingual structure and safe data. Not a math proof checker."""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path, PurePosixPath

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SECRET_KEYS = {
    "password", "passwd", "secret", "apikey", "api_key", "accesstoken",
    "access_token", "refreshtoken", "refresh_token", "authorization",
    "credential", "credentials", "privatekey", "private_key", "cookie", "cookies",
    "token", "authtoken", "auth_token",
}
LOCAL_PATH_RE = re.compile(
    r"(?:(?<![A-Za-z0-9])[A-Za-z]:[\\/]|\\\\[^\s\\]+\\|file://|"
    r"(?:^|\s)/(?:Users|home|tmp|mnt|etc|var|private|Volumes|workspace)/)"
)
INVISIBLE_CONTROLS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
INLINE_CONTROLS_RE = re.compile(r"[\x00-\x1f\x7f]")


def inline_math_has_controls(value):
    """Detect control collisions in paired single-dollar math, not display math.

    Unpaired dollar signs are left alone (they commonly denote prices). Adjacent
    pairs are considered independently so a preceding price does not consume a
    later actual math pair. A dollar followed by another price amount is not
    treated as a closing math delimiter. This is a narrow rendering check.
    """
    without_display = re.sub(r"(?<!\\)\$\$.*?(?<!\\)\$\$", "", value, flags=re.S)
    marks = list(re.finditer(r"(?<![\\$])\$(?!\$)", without_display))
    for opening, closing in zip(marks, marks[1:]):
        fragment = without_display[opening.end():closing.start()]
        if not INLINE_CONTROLS_RE.search(fragment):
            continue
        next_char = without_display[closing.end():closing.end() + 1]
        if (re.match(r"\s*\d", fragment) and next_char.isdigit()
                and not re.search(r"[\\=<>^{}_+*/]", fragment)):
            continue  # e.g. prices "$5 per lesson\n$10 for two".
        if fragment.strip():
            return True
    return False


class ContentError(ValueError):
    pass


def load_json(path: Path):
    if path.is_symlink():
        raise ContentError(f"Refusing symlink source: {path}")
    try:
        with path.open("r", encoding="utf-8-sig") as handle:
            return json.load(handle)
    except (OSError, ValueError) as exc:
        raise ContentError(f"Cannot read JSON {path}: {exc}") from exc


def valid_slug(value):
    return isinstance(value, str) and bool(ID_RE.fullmatch(value))


def safe_asset_path(value):
    """Only portable paths rooted in the lesson's assets directory are accepted."""
    if not isinstance(value, str) or "\\" in value or ":" in value:
        return False
    parts = value.split("/")
    return (len(parts) >= 2 and parts[0] == "assets"
            and all(part not in ("", ".", "..") for part in parts)
            and not PurePosixPath(value).is_absolute())


class Checker:
    def __init__(self):
        self.errors = []

    def require(self, condition, path, message):
        if not condition:
            self.errors.append(f"{path}: {message}")
        return condition

    def obj(self, value, path):
        self.require(isinstance(value, dict), path, "must be an object")
        return value if isinstance(value, dict) else {}

    def text(self, value, path):
        return self.require(isinstance(value, str) and bool(value.strip()), path,
                            "must be a nonempty string")

    def seq(self, value, path, nonempty=False):
        self.require(isinstance(value, list), path, "must be an array")
        result = value if isinstance(value, list) else []
        if nonempty:
            self.require(bool(result), path, "must not be empty")
        return result

    def number(self, value, path):
        try:
            valid = type(value) in (int, float) and math.isfinite(value)
        except OverflowError:
            valid = False
        return self.require(valid,
                            path, "must be a finite JSON number (not boolean)")

    def page(self, value, path):
        return self.require(type(value) is int and value > 0, path,
                            "must be a positive, one-based page number")

    def scan(self, value, path="$"):
        if isinstance(value, dict):
            for key, child in value.items():
                self.require(key.casefold() not in SECRET_KEYS, f"{path}.{key}",
                             "credential fields must not appear in public data")
                self.scan(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                self.scan(child, f"{path}[{index}]")
        elif isinstance(value, str):
            self.require(not INVISIBLE_CONTROLS_RE.search(value), path,
                         "contains an invisible control character; check literal LaTeX escaping")
            self.require(not inline_math_has_controls(value), path,
                         "inline $math$ contains raw newline/tab/control characters; use literal LaTeX escapes")
            self.require(not LOCAL_PATH_RE.search(value), path,
                         "must not contain a local absolute path")
            self.require(not re.search(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,})\b", value),
                         path, "possible credential found")
        elif type(value) is float:
            self.require(math.isfinite(value), path, "NaN/Infinity are not JSON data")

    def steps(self, value, path):
        result = self.seq(value, path, nonempty=True)
        for index, step in enumerate(result):
            step = self.obj(step, f"{path}[{index}]")
            for key in ("title", "body"):
                self.text(step.get(key), f"{path}[{index}].{key}")
        return result

    def concepts(self, value):
        concepts = self.seq(value, "lesson.concepts", nonempty=True)
        ids = []
        for index, concept in enumerate(concepts):
            path = f"lesson.concepts[{index}]"
            concept = self.obj(concept, path)
            ident = concept.get("id")
            self.require(valid_slug(ident), path + ".id", "must be a lowercase safe ID")
            if isinstance(ident, str):
                ids.append(ident)
            for key in ("title", "summary"):
                self.text(concept.get(key), path + "." + key)
            method = self.steps(concept.get("method"), path + ".method")
            pitfalls = self.seq(concept.get("pitfalls"), path + ".pitfalls")
            for i, item in enumerate(pitfalls):
                self.text(item, f"{path}.pitfalls[{i}]")
            en = self.obj(concept.get("en"), path + ".en")
            for key in ("title", "summary"):
                self.text(en.get(key), path + ".en." + key)
            en_method = self.steps(en.get("method"), path + ".en.method")
            en_pitfalls = self.seq(en.get("pitfalls"), path + ".en.pitfalls")
            for i, item in enumerate(en_pitfalls):
                self.text(item, f"{path}.en.pitfalls[{i}]")
            self.require(len(method) == len(en_method), path, "English method count differs")
            self.require(len(pitfalls) == len(en_pitfalls), path, "English pitfalls count differs")
        self.require(len(ids) == len(set(ids)), "lesson.concepts", "duplicate concept IDs")
        return set(ids)

    def numeric_array(self, value, path):
        values = self.seq(value, path, nonempty=True)
        for index, item in enumerate(values):
            self.number(item, f"{path}[{index}]")
        return values

    def graph(self, value, path, trace=False):
        value = self.obj(value, path)
        allowed = {"numerator", "denominator", "verticalAsymptotes", "horizontalAsymptote",
                   "obliqueAsymptote", "polynomialAsymptote", "holes", "points", "bounds",
                   "traces", "label"}
        for key in value:
            self.require(key in allowed, path + "." + key, "unsupported graph field")
        numerator = self.numeric_array(value.get("numerator"), path + ".numerator")
        denominator = self.numeric_array(value.get("denominator"), path + ".denominator")
        self.require(any(type(n) in (int, float) and n != 0 for n in denominator), path,
                     "graph denominator must not be the zero polynomial")
        if "label" in value:
            self.text(value["label"], path + ".label")
        for key in ("verticalAsymptotes", "polynomialAsymptote"):
            if key in value and value[key] is not None:
                if key == "polynomialAsymptote":
                    self.numeric_array(value[key], path + "." + key)
                else:
                    for i, n in enumerate(self.seq(value[key], path + "." + key)):
                        self.number(n, f"{path}.{key}[{i}]")
        if value.get("horizontalAsymptote") is not None:
            self.number(value["horizontalAsymptote"], path + ".horizontalAsymptote")
        if value.get("obliqueAsymptote") is not None:
            oblique = self.obj(value["obliqueAsymptote"], path + ".obliqueAsymptote")
            for key in ("slope", "intercept"):
                self.number(oblique.get(key), path + ".obliqueAsymptote." + key)
        for key in ("points", "holes"):
            if key in value:
                for i, point in enumerate(self.seq(value[key], path + "." + key)):
                    point = self.obj(point, f"{path}.{key}[{i}]")
                    for axis in ("x", "y"):
                        self.number(point.get(axis), f"{path}.{key}[{i}].{axis}")
        if not trace or "bounds" in value:
            bounds = self.obj(value.get("bounds"), path + ".bounds")
            for key in ("xMin", "xMax", "yMin", "yMax"):
                self.number(bounds.get(key), path + ".bounds." + key)
            for axis in ("x", "y"):
                low, high = bounds.get(axis + "Min"), bounds.get(axis + "Max")
                if type(low) in (int, float) and type(high) in (int, float):
                    self.require(low < high, path + ".bounds", "minimum must be below maximum")
        if "traces" in value:
            self.require(not trace, path, "nested traces are unsupported")
            for i, item in enumerate(self.seq(value["traces"], path + ".traces")):
                if not trace:
                    self.graph(item, f"{path}.traces[{i}]", trace=True)

    def sign_chart(self, value, path):
        value = self.obj(value, path)
        self.text(value.get("solutionLatex"), path + ".solutionLatex")
        boundaries = self.seq(value.get("boundaries"), path + ".boundaries")
        numeric = []
        for i, boundary in enumerate(boundaries):
            p = f"{path}.boundaries[{i}]"
            boundary = self.obj(boundary, p)
            if self.number(boundary.get("value"), p + ".value"):
                numeric.append(boundary["value"])
            self.text(boundary.get("label"), p + ".label")
            self.require(boundary.get("kind") in ("zero", "excluded"), p + ".kind",
                         "must be zero or excluded")
            self.require(type(boundary.get("included")) is bool, p + ".included", "must be boolean")
            if boundary.get("kind") == "excluded":
                self.require(boundary.get("included") is False, p,
                             "an excluded domain point cannot be included")
        self.require(all(a < b for a, b in zip(numeric, numeric[1:])), path,
                     "boundaries must be unique and increasing")
        intervals = self.seq(value.get("intervals"), path + ".intervals", nonempty=True)
        self.require(len(intervals) == len(boundaries) + 1, path, "one interval per boundary gap required")
        edges = [None] + numeric + [None]
        for i, interval in enumerate(intervals):
            p = f"{path}.intervals[{i}]"
            interval = self.obj(interval, p)
            self.require(interval.get("sign") in ("+", "-"), p + ".sign", "must be + or -")
            self.require(type(interval.get("selected")) is bool, p + ".selected", "must be boolean")
            for side, offset in (("left", 0), ("right", 1)):
                v = interval.get(side)
                if v is not None:
                    self.number(v, p + "." + side)
                self.require(side in interval, p + "." + side, "use null for infinity")
                if len(numeric) == len(boundaries) and i + offset < len(edges):
                    expected = edges[i + offset]
                    equal = v is expected if expected is None else (
                        type(v) in (int, float) and math.isclose(v, expected, rel_tol=1e-10, abs_tol=1e-10))
                    self.require(equal, p + "." + side, "interval must align with ordered boundaries")
            if "testPoint" in interval:
                v = interval["testPoint"]
                if isinstance(v, str):
                    self.text(v, p + ".testPoint")
                else:
                    self.number(v, p + ".testPoint")

    def synthetic(self, values, path):
        for i, table in enumerate(self.seq(values, path, nonempty=True)):
            p = f"{path}[{i}]"
            table = self.obj(table, p)
            for key in ("rootLatex", "remainderLatex", "quotientLatex"):
                self.text(table.get(key), p + "." + key)
            rows = []
            for key in ("coefficientsLatex", "productsLatex", "bottomLatex"):
                row = self.seq(table.get(key), p + "." + key, nonempty=True)
                rows.append(row)
                for j, item in enumerate(row):
                    if key == "productsLatex" and j == 0 and item is None:
                        continue
                    self.text(item, f"{p}.{key}[{j}]")
            self.require(len(rows[0]) >= 2 and len({len(row) for row in rows}) == 1,
                         p, "synthetic-division rows must have the same length, at least two")
            if rows[2] and isinstance(table.get("remainderLatex"), str):
                self.require(rows[2][-1] == table["remainderLatex"], p,
                             "bottom row's final cell must equal remainderLatex")

    def question(self, value, path, concept_ids, exercise=False, pdf_source=True):
        value = self.obj(value, path)
        for key in ("prompt", "answer"):
            self.text(value.get(key), path + "." + key)
        steps = self.steps(value.get("steps"), path + ".steps")
        en = self.obj(value.get("en"), path + ".en")
        if "sourceType" in value:
            self.require(value["sourceType"] in ("textbook", "lecture"), path + ".sourceType",
                         "must be textbook or lecture")
        if "sourceName" in value or "sourceName" in en:
            self.text(value.get("sourceName"), path + ".sourceName")
            self.text(en.get("sourceName"), path + ".en.sourceName")
        for key in ("prompt", "answer"):
            self.text(en.get(key), path + ".en." + key)
        en_steps = self.steps(en.get("steps"), path + ".en.steps")
        self.require(len(steps) == len(en_steps), path, "English step count differs")
        if pdf_source:
            self.page(value.get("pdfPage"), path + ".pdfPage")
            if "printedPage" in value:
                self.page(value["printedPage"], path + ".printedPage")
        else:
            self.require("printedPage" in value or "sourceLocator" in value, path,
                         "non-PDF questions need a real printedPage or sourceLocator")
            for key in ("printedPage", "pdfPage"):
                if key in value:
                    self.page(value[key], path + "." + key)
        if "sourceLocator" in value:
            self.text(value["sourceLocator"], path + ".sourceLocator")
        concepts = value.get("concept")
        if exercise and isinstance(concepts, list):
            concepts = self.seq(concepts, path + ".concept", nonempty=True)
            self.require(len(concepts) == len(set(str(c) for c in concepts)), path, "duplicate concept links")
        else:
            concepts = [concepts]
        for ident in concepts:
            self.require(isinstance(ident, str) and ident in concept_ids, path + ".concept",
                         "must reference an existing concept ID")
        if not exercise:
            self.require(valid_slug(value.get("id")), path + ".id", "must be a lowercase safe ID")
            self.require(value.get("type") in ("example", "practice"), path + ".type",
                         "must be example or practice")
            self.text(value.get("label"), path + ".label")
            self.text(en.get("label"), path + ".en.label")
        if "sourceImage" in value:
            self.require(safe_asset_path(value["sourceImage"]), path + ".sourceImage",
                         "must be a safe relative assets/ path")
        if "solutionImage" in value:
            self.require(safe_asset_path(value["solutionImage"]), path + ".solutionImage",
                         "must be a safe relative assets/ path")
        if "graph" in value:
            self.graph(value["graph"], path + ".graph")
        if "signChart" in value:
            self.sign_chart(value["signChart"], path + ".signChart")
        if "syntheticDivisions" in value:
            self.synthetic(value["syntheticDivisions"], path + ".syntheticDivisions")
        if "subpartIds" in value:
            self.subparts(value["subpartIds"], path + ".subpartIds")

    def subparts(self, value, path):
        values = self.seq(value, path, nonempty=True)
        for part in values:
            self.require(isinstance(part, str) and bool(re.fullmatch(r"[a-z0-9]+(?:\.[a-z0-9]+)*", part)),
                         path, "subpart IDs must be lowercase letters/digits with optional dotted nesting")
        self.require(len(values) == len(set(str(v) for v in values)), path, "duplicate subpart IDs")
        return values

    def identifiers(self, values, path, exercise=False):
        result = []
        for v in self.seq(values, path):
            valid = (type(v) is int and v > 0) or (isinstance(v, str) and
                    bool(re.fullmatch(r"[1-9][0-9]*(?:[a-z])?", v))) if exercise else valid_slug(v)
            self.require(valid, path, "invalid coverage identifier (boolean is not a number)")
            if valid:
                result.append(str(v))
        self.require(len(result) == len(set(result)), path, "duplicate coverage identifiers")
        return result

    def check(self, data, allow_draft=False):
        data = self.obj(data, "$")
        self.scan(data)
        course = self.obj(data.get("course"), "course")
        self.require(valid_slug(course.get("id")), "course.id", "must be a lowercase safe ID")
        self.text(course.get("title"), "course.title")
        self.text(self.obj(course.get("en"), "course.en").get("title"), "course.en.title")
        lesson = self.obj(data.get("lesson"), "lesson")
        self.require(valid_slug(lesson.get("id")), "lesson.id", "must be a lowercase safe ID")
        for key in ("section", "title"):
            self.text(lesson.get(key), "lesson." + key)
        lesson_en = self.obj(lesson.get("en"), "lesson.en")
        self.text(lesson_en.get("title"), "lesson.en.title")
        if "description" in lesson:
            self.text(lesson["description"], "lesson.description")
            self.text(lesson_en.get("description"), "lesson.en.description")
        source = self.obj(lesson.get("source"), "lesson.source")
        self.text(source.get("title"), "lesson.source.title")
        source_kind = source.get("kind", "pdf" if "pdfPages" in source else None)
        self.require(source_kind in ("pdf", "text", "html", "epub", "image"), "lesson.source.kind",
                     "must identify pdf, text, html, epub or image source")
        pdf_source = source_kind == "pdf" or "pdfPages" in source
        for key in ("printedPages", "pdfPages"):
            if key not in source and (key == "printedPages" or not pdf_source):
                continue
            pages = self.seq(source.get(key), "lesson.source." + key, nonempty=True)
            for i, page in enumerate(pages):
                self.page(page, f"lesson.source.{key}[{i}]")
            self.require(all(type(a) is int and type(b) is int and a <= b for a, b in zip(pages, pages[1:])),
                         "lesson.source." + key, "page list must be increasing")
        concept_ids = self.concepts(lesson.get("concepts"))
        questions = self.seq(lesson.get("questions"), "lesson.questions")
        questions = [self.obj(q, f"lesson.questions[{i}]") for i, q in enumerate(questions)]
        for i, question in enumerate(questions):
            self.question(question, f"lesson.questions[{i}]", concept_ids, pdf_source=pdf_source)
        question_ids = [q.get("id") for q in questions]
        self.require(len(question_ids) == len(set(str(q) for q in question_ids)),
                     "lesson.questions", "duplicate question IDs")
        textbook = self.obj(data.get("textbook"), "textbook")
        exercises = self.seq(textbook.get("exercises"), "textbook.exercises")
        exercises = [self.obj(q, f"textbook.exercises[{i}]") for i, q in enumerate(exercises)]
        for i, exercise in enumerate(exercises):
            self.question(exercise, f"textbook.exercises[{i}]", concept_ids, exercise=True, pdf_source=pdf_source)
        actual_exercises = self.identifiers([e.get("number") for e in exercises], "textbook.exercise numbers", exercise=True)
        coverage = self.obj(data.get("coverage"), "coverage")
        for key, actual in (
            ("expectedExamples", [q.get("id") for q in questions if q.get("type") == "example"]),
            ("expectedPractice", [q.get("id") for q in questions if q.get("type") == "practice"]),
            ("expectedExercises", actual_exercises),
        ):
            expected = self.identifiers(coverage.get(key), "coverage." + key, exercise=key == "expectedExercises")
            actual = [str(v) for v in actual]
            self.require(expected == actual, "coverage." + key,
                         f"source-ledger order/coverage mismatch; missing={sorted(set(expected)-set(actual))}, "
                         f"unexpected={sorted(set(actual)-set(expected))}")
        expected_subparts = self.obj(coverage.get("expectedSubparts"), "coverage.expectedSubparts")
        records = {q.get("id"): q for q in questions if isinstance(q.get("id"), str)}
        records.update({"exercise-" + str(e.get("number")): e for e in exercises})
        for ident, parts in expected_subparts.items():
            self.subparts(parts, "coverage.expectedSubparts." + ident)
            self.require(ident in records, "coverage.expectedSubparts." + ident, "unknown question")
            if ident in records:
                self.require(records[ident].get("subpartIds") == parts, ident,
                             "actual subpart IDs/order differ from independent source ledger")
        for ident, record in records.items():
            if "subpartIds" in record:
                self.require(ident in expected_subparts, ident,
                             "subparts need an independently counted coverage entry")
        audit = self.obj(data.get("audit"), "audit")
        for key in ("sourceReviewed", "solutionsReviewed"):
            if allow_draft:
                self.require(type(audit.get(key)) is bool, "audit." + key, "must be boolean even for draft")
            else:
                self.require(audit.get(key) is True, "audit." + key,
                             "must be true after source/math review; draft preview is not publishable")
        return self.errors


def check_data(data, allow_draft=False):
    return Checker().check(data, allow_draft=allow_draft)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson", type=Path)
    parser.add_argument("--allow-draft", action="store_true",
                        help="preview only: allow unreviewed audit flags; all structural checks still apply")
    args = parser.parse_args(argv)
    try:
        errors = check_data(load_json(args.lesson), args.allow_draft)
    except ContentError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if errors:
        print("CONTENT CHECK FAILED", file=sys.stderr)
        for error in errors:
            print("- " + error, file=sys.stderr)
        return 1
    mode = "DRAFT PREVIEW ONLY" if args.allow_draft else "STRUCTURE/COVERAGE CHECK PASSED"
    print(mode + ". Mathematical correctness still requires independent source and solution review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
