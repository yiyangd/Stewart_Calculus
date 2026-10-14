#!/usr/bin/env python3
"""Build a reviewed bilingual course as static files; never deploy or change Git."""
from __future__ import annotations

import argparse
import copy
import json
import os
import stat
import sys
import tempfile
from pathlib import Path, PurePosixPath

from check_content import Checker, ContentError, check_data, load_json, valid_slug

MARKER = ".textbook-study-site.json"
GENERATOR = "textbook-study-site-v1"


def json_text(data):
    return json.dumps(data, ensure_ascii=False, allow_nan=False, indent=2) + "\n"


def inline_json(data):
    return (json.dumps(data, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
            .replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


def plain_relative(value):
    return (isinstance(value, str) and "\\" not in value and ":" not in value
            and not PurePosixPath(value).is_absolute()
            and all(p not in ("", ".", "..") for p in value.split("/")))


def reject_symlinks(path):
    """Reject symlink/junction traversal as well as the final component."""
    for parent in [path] + list(path.parents):
        reparse = False
        if parent.exists() or parent.is_symlink():
            attrs = getattr(parent.lstat(), "st_file_attributes", 0)
            reparse = bool(attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))
        if parent.is_symlink() or reparse or (hasattr(parent, "is_junction") and parent.is_junction()):
            raise ContentError(f"Symlink/junction paths are unsupported: {parent}")


def relative_source(base, relative):
    if not plain_relative(relative):
        raise ContentError(f"Unsafe relative source path: {relative!r}")
    path = base.joinpath(*relative.split("/"))
    reject_symlinks(path)
    if not path.resolve().is_relative_to(base.resolve()):
        raise ContentError(f"Source path escapes its directory: {relative!r}")
    if not path.is_file():
        raise ContentError(f"Source file is missing: {path}")
    return path


def image_references(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key in ("sourceImage", "solutionImage"):
                yield value
            else:
                yield from image_references(value)
    elif isinstance(data, list):
        for value in data:
            yield from image_references(value)


def validate_manifest(manifest):
    checker = Checker()
    manifest = checker.obj(manifest, "manifest")
    checker.scan(manifest)
    course = checker.obj(manifest.get("course"), "manifest.course")
    checker.require(valid_slug(course.get("id")), "manifest.course.id", "must be a lowercase safe ID")
    checker.text(course.get("title"), "manifest.course.title")
    checker.text(checker.obj(course.get("en"), "manifest.course.en").get("title"), "manifest.course.en.title")
    sections = checker.seq(manifest.get("sections"), "manifest.sections", nonempty=True)
    slugs = []
    for index, item in enumerate(sections):
        path = f"manifest.sections[{index}]"
        item = checker.obj(item, path)
        slug = item.get("slug")
        checker.require(valid_slug(slug), path + ".slug", "must be lowercase letters/digits/hyphens")
        if isinstance(slug, str):
            slugs.append(slug)
        for key in ("section", "title", "data"):
            checker.text(item.get(key), path + "." + key)
        checker.require(plain_relative(item.get("data")), path + ".data", "must be a safe relative JSON path")
        en = checker.obj(item.get("en"), path + ".en")
        checker.text(en.get("title"), path + ".en.title")
        if "chapter" in item:
            checker.text(item["chapter"], path + ".chapter")
            checker.text(en.get("chapter"), path + ".en.chapter")
        counts = checker.obj(item.get("counts"), path + ".counts")
        for key in ("concepts", "examples", "practice", "exercises"):
            checker.require(type(counts.get(key)) is int and counts[key] >= 0,
                            path + ".counts." + key, "must be a nonnegative integer")
    checker.require(len(slugs) == len(set(slugs)), "manifest.sections", "duplicate slugs")
    if checker.errors:
        raise ContentError("Invalid manifest:\n- " + "\n- ".join(checker.errors))


def export_section(item):
    # Input file locations belong to preparation, not public website metadata.
    result = {key: copy.deepcopy(item[key]) for key in ("slug", "section", "title", "en", "counts")}
    if "chapter" in item:
        result["chapter"] = item["chapter"]
    return result


def build(manifest_path, output):
    if not manifest_path.is_absolute() or not output.is_absolute():
        raise ContentError("--manifest and --output must be absolute paths")
    reject_symlinks(manifest_path)
    reject_symlinks(output)
    if output.exists() and not output.is_dir():
        raise ContentError("Output must be a directory")
    if not output.parent.is_dir():
        raise ContentError("Output parent directory must already exist")
    manifest = load_json(manifest_path)
    validate_manifest(manifest)
    course_id = manifest["course"]["id"]
    previous_sections = []
    owned = set()
    if output.exists() and any(output.iterdir()):
        marker_path = output / MARKER
        if not marker_path.is_file():
            raise ContentError(
                "Output contains an existing site without this builder's ownership marker. "
                "Keep its template and adapt it manually, or choose a new empty output directory. "
                "Do not directly rebuild an existing site with this generic tool.")
        marker = load_json(marker_path)
        if (not isinstance(marker, dict) or marker.get("generator") != GENERATOR
                or marker.get("courseId") != course_id):
            raise ContentError("Refusing to overwrite a site owned by another generator/course.id")
        owned_slugs = marker.get("sections")
        if not isinstance(owned_slugs, list) or not all(valid_slug(slug) for slug in owned_slugs):
            raise ContentError("Invalid ownership marker sections")
        owned = set(owned_slugs)
        previous = load_json(output / "course.json")
        if (not isinstance(previous, dict) or not isinstance(previous.get("course"), dict)
                or previous["course"].get("id") != course_id or not isinstance(previous.get("sections"), list)):
            raise ContentError("Existing public course.json does not match its ownership marker")
        for language in (None, "en"):
            old_course = previous["course"] if language is None else previous["course"].get("en", {})
            new_course = manifest["course"] if language is None else manifest["course"]["en"]
            if not isinstance(old_course, dict) or old_course.get("title") != new_course["title"]:
                raise ContentError("Course title differs from the existing site. "
                                   "A whole-course rename requires a separate reviewed adaptation.")
        previous_sections = previous["sections"]
        for item in previous_sections:
            if not isinstance(item, dict) or not valid_slug(item.get("slug")) or item["slug"] not in owned:
                raise ContentError("Existing course.json has unowned/invalid sections")
    source_root = manifest_path.parent
    frontend = Path(__file__).resolve().parent.parent / "assets" / "frontend"
    templates = {}
    for name, token in (("home.html", "__COURSE_DATA__"), ("lesson.html", "__LESSON_DATA__")):
        path = relative_source(frontend, name)
        content = path.read_text(encoding="utf-8")
        if content.count(token) != 1:
            raise ContentError(f"{name} must contain exactly one {token} placeholder")
        templates[name] = content
    static_sources = {name: relative_source(frontend, name)
                      for name in ("home.js", "home.css", "app.js", "styles.css")}
    planned = []
    for item in manifest["sections"]:
        slug = item["slug"]
        destination = output / "sections" / slug
        reject_symlinks(destination)
        if destination.exists() and slug not in owned:
            raise ContentError(f"Refusing to overwrite an unowned section directory: {slug}")
        data_path = relative_source(source_root, item["data"])
        data = load_json(data_path)
        errors = check_data(data)  # Final build has no allow-draft escape hatch.
        if errors:
            raise ContentError(f"{slug}: content check failed:\n- " + "\n- ".join(errors))
        if data["course"]["id"] != course_id or data["lesson"]["id"] != slug:
            raise ContentError(f"{slug}: course.id/lesson.id do not match manifest")
        for language in (None, "en"):
            lesson_course = data["course"] if language is None else data["course"]["en"]
            manifest_course = manifest["course"] if language is None else manifest["course"]["en"]
            if lesson_course["title"] != manifest_course["title"]:
                raise ContentError(f"{slug}: course title does not match manifest ({language or 'zh'})")
        if data["lesson"]["section"] != item["section"]:
            raise ContentError(f"{slug}: section number does not match manifest")
        for language in (None, "en"):
            record = data["lesson"] if language is None else data["lesson"]["en"]
            metadata = item if language is None else item["en"]
            if record["title"] != metadata["title"]:
                raise ContentError(f"{slug}: lesson title does not match manifest ({language or 'zh'})")
        questions = data["lesson"]["questions"]
        actual = {"concepts": len(data["lesson"]["concepts"]),
                  "examples": sum(q["type"] == "example" for q in questions),
                  "practice": sum(q["type"] == "practice" for q in questions),
                  "exercises": len(data["textbook"]["exercises"])}
        if item["counts"] != actual:
            raise ContentError(f"{slug}: manifest counts {item['counts']} differ from actual {actual}")
        images = {}
        for image in set(image_references(data)):
            source = relative_source(data_path.parent, image)
            if source.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
                raise ContentError(f"Only raster source figures are supported: {image}")
            images[image] = source
        planned.append((item, data, images))
    new_sections = {item["slug"]: export_section(item) for item in manifest["sections"]}
    public_sections = [new_sections.pop(item["slug"], copy.deepcopy(item)) for item in previous_sections]
    public_sections.extend(new_sections.values())
    public_course = {"course": copy.deepcopy(manifest["course"]), "sections": public_sections}
    # All input, ownership, template and destination checks complete before any output write.
    files = {}
    files["index.html"] = templates["home.html"].replace("__COURSE_DATA__", inline_json(public_course)).encode("utf-8")
    files["course.json"] = json_text(public_course).encode("utf-8")
    files[".nojekyll"] = b""
    files[MARKER] = json_text({"generator": GENERATOR, "courseId": course_id,
                              "sections": [item["slug"] for item in public_sections]}).encode("utf-8")
    for name in ("home.js", "home.css"):
        files[name] = static_sources[name].read_bytes()
    for item, data, images in planned:
        prefix = "sections/" + item["slug"] + "/"
        files[prefix + "index.html"] = templates["lesson.html"].replace("__LESSON_DATA__", inline_json(data)).encode("utf-8")
        files[prefix + "data.json"] = json_text(data).encode("utf-8")
        for name in ("app.js", "styles.css"):
            files[prefix + name] = static_sources[name].read_bytes()
        for relative, source in images.items():
            files[prefix + relative] = source.read_bytes()
    for relative in files:
        target = output.joinpath(*relative.split("/"))
        reject_symlinks(target)
        if target.exists() and not target.is_file():
            raise ContentError(f"Output file conflicts with directory: {target}")
        for parent in target.parents:
            if parent == output.parent:
                break
            if parent.exists() and not parent.is_dir():
                raise ContentError(f"Output directory conflicts with file: {parent}")
    # Stage complete files before atomic per-file replacement. No recursive removal is used.
    # An OS/disk failure can still interrupt replacement; backups/version control remain useful.
    with tempfile.TemporaryDirectory(prefix="study-site-build-", dir=output.parent) as temporary:
        stage = Path(temporary)
        for relative, content in files.items():
            staged = stage.joinpath(*relative.split("/"))
            staged.parent.mkdir(parents=True, exist_ok=True)
            staged.write_bytes(content)
        for relative in files:
            target = output.joinpath(*relative.split("/"))
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(stage.joinpath(*relative.split("/")), target)
    return {"courseId": course_id, "builtSections": [item["slug"] for item in manifest["sections"]],
            "totalSections": len(public_sections), "writtenFiles": len(files), "output": str(output)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        result = build(args.manifest, args.output)
    except (ContentError, OSError, ValueError) as exc:
        print("BUILD FAILED: " + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    print("Built locally. No Git changes or deployment were performed. Math review is separate from structure checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
