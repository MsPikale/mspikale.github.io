"""Render index.html from site/content.py and site/templates/page.html.

Run it from the repository root after editing either one:

    python site/build.py

The generated index.html is committed alongside the sources. That is what
GitHub Pages publishes, so nothing on the server side has to run Python -- the
build is a convenience for whoever edits the content, not a deploy step.

It also prints which deliverables still have no link, which is a handy
checklist before a milestone is due.
"""

from __future__ import annotations

import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"

sys.path.insert(0, str(Path(__file__).resolve().parent))

import content  # noqa: E402


def render() -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=True,
        # A typo in a variable name should stop the build rather than quietly
        # render a blank where a team member's name used to be.
        undefined=StrictUndefined,
        trim_blocks=False,
        keep_trailing_newline=True,
    )
    return env.get_template("page.html").render(
        project_name=content.PROJECT_NAME,
        team=content.TEAM,
        advisor=content.ADVISOR,
        semesters=content.SEMESTERS,
        tools=content.TOOLS,
        challenges=content.CHALLENGES,
        architecture=content.ARCHITECTURE,
    )


def unpublished() -> list[str]:
    return [
        f"{row['milestone']}: {doc['label']}"
        for semester in content.SEMESTERS
        for row in semester["rows"]
        for doc in row["documents"]
        if not doc["url"]
    ]


def main() -> None:
    html = render()
    index = ROOT / "index.html"
    index.write_text(html, encoding="utf-8")
    print(f"wrote {index.relative_to(ROOT)} ({len(html):,} bytes)")

    missing = unpublished()
    if missing:
        print(f"\n{len(missing)} deliverable(s) still without a link:")
        for item in missing:
            print(f"      {item}")


if __name__ == "__main__":
    main()
