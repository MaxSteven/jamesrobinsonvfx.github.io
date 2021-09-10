#!/usr/bin/env python3
"""Gist Manifest

Output a .json file to use with my website to easily update the
snippets section.

James Robinson
30 August 2021
"""
import json
import requests
import sys


USER_NAME = "jamesrobinsonvfx"


def get_gists(username):
    response = requests.get(
        f"https://api.github.com/users/{username}/gists?per_page=100")
    if response.ok:
        return response.json()
    return []


def generate_manifest(gists, outfile):
    manifest = []
    keys = ("description", "id", "html_url", "created_at")
    for gist in gists:
        entry = {}
        for key in keys:
            entry[key] = gist.get(key)
        # Get the filename for the first file in the gist
        filename = ""
        files = gist.get("files")
        if files:
            filename = list(files.keys())[0]
        entry["filename"] = filename
        manifest.append(entry)
    return manifest


if __name__ == "__main__":
    print("Fetching....")
    try:
        outfile = sys.argv[1]
        manifest = generate_manifest(get_gists(USER_NAME), outfile)
        with open(outfile, "w") as file_:
            json.dump(manifest, file_, indent=4)
        print(f"SUCCESS: Check {outfile} for json manifest.")
    except IndexError:
        print("FAIL: Specify an output file.")
