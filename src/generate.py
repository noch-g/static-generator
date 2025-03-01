import os
import shutil

from block_markdown import markdown_to_html_node

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md = f.read()
    with open(template_path) as f:
        template = f.read()
    doc = markdown_to_html_node(md)
    doc_str = doc.to_html()
    title = extract_title(md)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", doc_str)
    
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    with open(os.path.join(dest_path, "index.html"), "w") as f:
        f.write(template)


def extract_title(markdown: str)-> None:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no title found in markdown")

def rm_rf(folder: str) -> None:
    if os.path.exists(folder):
        shutil.rmtree(folder)

def copy_r(folder_src: str, folder_dest: str) -> None:
    if not os.path.exists(folder_dest):
        os.mkdir(folder_dest)
    for item in os.listdir(folder_src):
        if os.path.isfile(os.path.join(folder_src, item)):
            shutil.copy(os.path.join(folder_src, item), os.path.join(folder_dest, item))
        else:
            copy_r(os.path.join(folder_src, item), os.path.join(folder_dest, item))