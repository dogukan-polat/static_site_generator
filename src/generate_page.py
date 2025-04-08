import os, shutil
from block_elements import markdown_to_html_node
from htmlnode import *

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise Exception("There is no h1 heading.")

def get_content(path):
    with open(path) as f:
        return f.read()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}:")
    md_content = get_content(from_path)
    template_content = get_content(template_path)
    converted_md = markdown_to_html_node(md_content).to_html()
    #print(converted_md)  # Print its structure to inspect nodes.
    title = extract_title(md_content)
    html_page = template_content.replace("{{ Title }}", title).replace("{{ Content }}", converted_md)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as f:
        f.write(html_page)

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):#MD files must turn to HTML.
    filelist = os.listdir(dir_path_content)
    for filename in filelist:
        src_path = os.path.join(dir_path_content, filename)
        dst_path = os.path.join(dest_dir_path,filename)
        if os.path.isfile(src_path):
            dst_path = os.path.join(os.path.dirname(dst_path), "index.html")
            generate_page(src_path, template_path, dst_path)
        else:
            os.mkdir(dst_path)
            generate_pages_recursively(src_path, template_path, dst_path)