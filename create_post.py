#!/usr/bin/env python3
"""Create a blank post"""
import os
import requests
import sys
from datetime import date


GITHUB_REPOS = "https://api.github.com/repos/jamesrobinsonvfx"


class Post:

    POST_TYPES = ["post", "project"]

    def __init__(
        self,
        title,
        desc,
        cats=None,
        tags=None,
        post_type="post",
        has_hipfile=False
    ):
        self._post_type = post_type
        self.title = title
        self.desc = desc
        self.cats = cats
        self.tags = tags
        self.has_hipfile = has_hipfile

        # Keep it easy for now.
        self.root = os.getcwd()

    def create(self):
        if self.check_exists():
            raise Exception(
                f"A post with the name {self.shortname} already exists"
            )
        print(f"Creating {self}")
        print(f"Creating post file at {self.post_path()}")
        self._create_post()

        # if self.has_hipfile:
        #     print(f"Creating dummy hipfile {self.hipfile_path()}")

        self._create_dirs()
        print("Post created.")

    def check_exists(self):
        posts = os.listdir(os.path.join(self.root, f"_{self.post_dirname()}"))
        for post in posts:
            if self.shortname in post:
                return True
        return False

    def post_dirname(self):
        return f"{self.post_type}s"

    def post_path(self):
        post_file = f"{self.shortname}.md"
        if self.post_type == "post":
            post_file = f"{date.today().isoformat()}-{post_file}"
        return os.path.join(f"_{self.post_dirname()}", post_file)

    def assets_path(self):
        return os.path.join(*["assets", self.post_dirname(), self.shortname])

    def images_path(self):
        return os.path.join(self.assets_path(), "images")

    def thumbnail_path(self):
        return os.path.join("/", self.images_path(), "preview.png")

    def hipname(self):
        return f"jamesr_{self.shortname.replace('-', '')}.hip"

    def hipfile_path(self):
        return os.path.join("/", self.assets_path(), self.hipname())

    def _create_dirs(self):
        print(f"Creating assets directory at {self.assets_path()}")
        os.makedirs(os.path.join(self.root, self.assets_path()))
        print(f"Creating images directory at {self.images_path()}")
        os.makedirs(os.path.join(self.root, self.images_path()))

    def _create_post(self):
        with open(os.path.join(self.root, self.post_path()), "w") as post:
            post.write(self.front_matter())
            post.write(self.post_body())

    def front_matter(self):
        content = [
            "---",
            "layout: post",
            f"title: {self.title}",
            f"description: {self.desc}",
            f"thumbnail: {self.thumbnail_path()}",
        ]
        return content

    def post_body(self):
        content = ["\n"]
        if self.has_hipfile:
            content.extend([
                f"> Hipfile: [{self.hipname()}]({self.hipfile_path()})]",
                "{:style=\"border-color: #d08770\"}\n"
            ])
        content.append(
            f"![Cover Photo]({self.thumbnail_path()})\n"
        )
        return content

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = " ".join(title.split()).title()
        self.shortname = title

    @property
    def shortname(self):
        return self._shortname

    @shortname.setter
    def shortname(self, title):
        self._shortname = self._format_shortname(title)

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, desc):
        self._desc = desc.rstrip(".")

    @property
    def cats(self):
        return self._cats

    @cats.setter
    def cats(self, cats):
        if not cats:
            self._cats = ""
            return
        if not self._isiterable(cats):
            raise TypeError("cats must be a string or an iterable")
        if isinstance(cats, str):
            self._cats = cats
        else:
            self._cats = " ".join(set(cats))

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        if not tags:
            self._tags = ""
            return
        if not self._isiterable(tags):
            raise TypeError("tags must be a string or an iterable")
        if isinstance(tags, str):
            self._tags = tags
        else:
            self._tags = " ".join(set(tags))

    @property
    def post_type(self):
        return self._post_type

    @post_type.setter
    def post_type(self, post_type):
        # types = ["post", "project"]
        if not post_type in self.POST_TYPES:
            raise Exception(
                f"{post_type} is not a valid post type. "
                f"Valid options are {' '.join(self.POST_TYPES)}"
            )
        self._post_type = post_type

    def __str__(self):
        return (
            f"<{self.post_type}>: \"{self.title}\" {self.shortname} "
            f"Categories: [{self.cats}] Tags: [{self.tags}]"
        )

    @staticmethod
    def _format_shortname(title):
        return "-".join(title.lower().split())

    @staticmethod
    def _isiterable(obj):
        if isinstance(obj, (str, list, tuple, set)):
            return True
        return False


class BlogPost(Post):

    def __init__(
        self,
        title,
        desc,
        cats=None,
        tags=None,
        post_type="post",
        has_hipfile=False
    ):
        super().__init__(
            title,
            desc,
            cats=cats,
            tags=tags,
            post_type=post_type,
            has_hipfile=has_hipfile
        )

    def front_matter(self):
        content = super().front_matter()
        content.extend([
            f"categories: {self.cats}",
            f"tags: {self.tags}",
            "---"
        ])
        return "\n".join(content)

    def post_body(self):
        content = super().post_body()

        return "\n".join(content)


class ProjectPost(Post):
    def __init__(
        self,
        title,
        desc,
        cats=None,
        tags=None,
        post_type="project",
        has_hipfile=False,
        repo=""
    ):
        super().__init__(
            title,
            desc,
            cats=cats,
            tags=tags,
            post_type=post_type,
            has_hipfile=has_hipfile
        )
        # self.repo = repo

    @property
    def repo(self):
        return self._repo

    @repo.setter
    def repo(self, repo_name):
        if not requests.get(f"{GITHUB_REPOS}/{repo_name}").ok:
            print("Warning: Github repo does not yet exist.")
        self._repo = repo_name

    def front_matter(self):
        content = super().front_matter()
        content.extend([
            f"repo: {self.repo}",
            "---"
        ])
        return "\n".join(content)

    def post_body(self):
        content = super().post_body()
        content.extend([
            "> Get it [here]({{ site.socials.github }}/{{ page.repo }}) "
            "<a class=\"fab fa-gtihub\" href=\"{{site.socials.github}}"
            "/{{page.repo}}\"</a>"
        ])
        return "\n".join(content)


def check_location():
    """Make sure the script is running from the proper root dir."""
    cwd = os.getcwd()
    assets = os.path.join(cwd, "assets")
    posts = os.path.join(cwd, "_posts")
    projects = os.path.join(cwd, "_projects")
    req = [assets, posts, projects]
    ok = True
    for dir_ in req:
        if not os.path.exists(dir_):
            ok = False
            break
    return ok


def cli_input(prompt):
    return str(input(f"{prompt}: ")).rstrip()


def cli_input_bool(prompt):
    valid_input = False
    result = None
    while (not valid_input):
        user_input = input(f"{prompt} (y/n): ")
        try:
            result = {"y": True, "n": False}[user_input]
            valid_input = True
        except KeyError:
            print("Please enter 'y' or 'n' (without the quotes)")
    return result


def post_generator(post_type):
    if not post_type in Post.POST_TYPES:
        raise RuntimeError(
            f"{post_type} unknown. "
            f"Options are {' '.join(Post.POST_TYPES)}"
        )
    type_map = {
        "post": BlogPost,
        "project": ProjectPost
    }
    return type_map[post_type]


def wizard(post_obj):
    post = post_obj("", "")
    exists = True
    while (exists):
        post.title = cli_input("Title")
        if post.check_exists():
            print(
                f"A post with the title {post.title} ({post.shortname}) "
                "already exists. Please try a new title."
            )
        else:
            exists = False

    post.desc = cli_input("Description")

    if isinstance(post, BlogPost):
        post.cats = cli_input("Categories")
        post.tags = cli_input("Tags")
        post.has_hipfile = cli_input_bool("Has a hipfile?")

    elif isinstance(post, ProjectPost):
        post.repo = cli_input("GitHub Repo Name")

    return post


def main():
    """Execute the script."""
    if not check_location():
        raise RuntimeError("Run this script from the site's root.")

    # If there are arguments, skip the wizard...someday
    try:
        post_type = sys.argv[1]
    except IndexError:
        raise Exception(
            "Unknown or missing command. "
            "Specify post type like:\n./create_post post"
        )
    post = wizard(post_generator(post_type))

    post.create()


if __name__ == "__main__":
    main()

# ./create_post post
