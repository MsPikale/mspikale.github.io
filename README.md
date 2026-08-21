# RootView - project page

The public course page for **RootView**, a KVM-based eBPF malware detection
engine (Florida Tech senior design, 2026-2027): project identity, the
deliverables index, the project summary, the two architecture diagrams, tools,
technical challenges and milestones.

Plain HTML and CSS. No server, no JavaScript, no backend, so it can be hosted
anywhere and stays reachable whether or not anyone is running the tool. The
diagrams are interactive without any script: hovering or tab-focusing a shape
reveals its description through CSS alone, and a screen that cannot hover gets
every description listed under the diagram instead.

This repository is self-contained. The RootView application itself - the
dashboard, the introspection view, the JSON API - lives in the separate
`rootview` repository and needs Python running on the KVM host next to the
guest VMs, so it cannot be published as a public link.

## What is in here

```
index.html            the page, generated (see below) and committed
assets/css/site.css   the only stylesheet
docs/                 deliverables published as files in this repo
site/content.py       everything the page says: team, milestones, tools, ...
site/templates/       the page's markup
site/build.py         renders content.py + template -> index.html
.nojekyll             stops GitHub Pages running the output through Jekyll
```

## Publishing a deliverable

Every document in `site/content.py` has a `url` that starts empty. An empty url
renders as inert grey text marked "not published yet" rather than a dead link;
fill the url in and it becomes a working hyperlink.

1. Edit `site/content.py`:

   ```python
   {"label": "Plan", "url": "https://docs.google.com/document/d/..."}   # external
   {"label": "Plan", "url": "docs/plan.pdf"}                            # in this repo
   ```

   For a file in this repo, drop it in `docs/` first. Keep the path relative -
   a leading `/` breaks on GitHub Pages, which serves this from
   `/<repo-name>/` rather than from the domain root.

2. Rebuild and commit both files:

   ```sh
   pip install -r site/requirements.txt   # once
   python site/build.py
   ```

The build prints which deliverables are still without a link, which is a handy
checklist before a milestone is due.

Everything else the page says - team members, milestone tasks, tools,
challenges, the diagram descriptions - lives in `site/content.py` too, and
changes the same way. The template only holds the shapes the words go into.

You can also hand-edit `index.html` directly; it is ordinary readable markup.
Just know the next build overwrites it.

## Publishing to GitHub Pages

`.github/workflows/pages.yml` rebuilds the page and deploys it on every push to
`main`, so a `content.py` edit goes live without your having to remember to run
the build first.

**One-time setup** on a fresh repository: Settings -> Pages -> Source ->
**GitHub Actions**. The site is then at
`https://<user>.github.io/<repo-name>/`.

To publish from a branch before merging, go to Actions -> Pages -> Run workflow
and pick the branch.

If you would rather not use Actions at all, the committed `index.html` is
already a complete site: Settings -> Pages -> Source -> **Deploy from a
branch**, `main` / root works too. Then it is on you to run `python
site/build.py` and commit the result after editing `content.py`.

## Local preview

Open `index.html` in a browser. Nothing needs to be served.
