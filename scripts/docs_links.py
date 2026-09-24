"""Python-Markdown extension for the docs site: links from docs/ to repo files outside it point at GitHub.

The docs pages link to reports, scripts and data with relative paths (`../reports/eval2/summary.md`) so they work
when read on GitHub. The site only contains docs/, so those links are rewritten to the repository on GitHub.
Enabled in zensical.toml; run the site with `python -m zensical` from the repo root so this module is importable.
"""
import re

from markdown import Extension
from markdown.treeprocessors import Treeprocessor

REPO_PATH = re.compile(
    r"^(?:\.\./)+(?P<path>(?:reports|scripts|src|data|configs|calib|tests|examples|output|runs)/[^#?]*"
    r"|[A-Za-z_]+\.(?:md|toml|lock))(?P<rest>[#?].*)?$"
)


class RepoLinks(Treeprocessor):
    def __init__(self, md, repo, branch):
        super().__init__(md)
        self.blob = f"{repo}/blob/{branch}/"
        self.raw = repo.replace("https://github.com/", "https://raw.githubusercontent.com/") + f"/{branch}/"

    def run(self, root):
        for el in root.iter():
            for attr, base in (("href", self.blob), ("src", self.raw)):
                match = REPO_PATH.match(el.get(attr, ""))
                if match:
                    el.set(attr, base + match["path"] + (match["rest"] or ""))


class RepoLinksExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            "repo": ["https://github.com/Jwuthri/SelfJev", "GitHub repository URL"],
            "branch": ["master", "branch the links point at"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        processor = RepoLinks(md, self.getConfig("repo"), self.getConfig("branch"))
        md.treeprocessors.register(processor, "repo_links", 1)  # before Zensical's relative-link rewriting (0)


def makeExtension(**kwargs):
    return RepoLinksExtension(**kwargs)
