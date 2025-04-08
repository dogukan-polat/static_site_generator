import os, shutil
import sys
from textnode import *
from copy_statics import copy_paste
from generate_page import generate_pages_recursively


def main():
    static_dest = "static/"
    base_path = "/"
    if len(sys.argv) == 2:
        base_path = sys.argv[1]

    if os.path.exists("docs/"):
        shutil.rmtree("docs/")

    copy_paste(static_dest, "docs/")

    ##generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursively(base_path, "content/", "template.html", "docs/")

main()