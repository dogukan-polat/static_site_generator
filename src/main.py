import os, shutil
from textnode import *
from copy_statics import copy_paste
from generate_page import generate_pages_recursively


def main():
    static_dest = "static/"
    public_dest = "public/"
    

    if os.path.exists(public_dest):
        shutil.rmtree(public_dest)

    copy_paste(static_dest, public_dest)

    ##generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursively("content/", "template.html", "public/")

main()