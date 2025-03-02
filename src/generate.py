import os
import shutil

from block_markdown import markdown_to_html_node

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    generate_page(dir_path_content, template_path, dest_dir_path, basepath)
    for dir in os.listdir(dir_path_content):
        if not os.path.isfile(os.path.join(dir_path_content, dir)):
            if not os.path.exists(os.path.join(dest_dir_path, dir)):
                os.mkdir(os.path.join(dest_dir_path, dir))
            generate_pages_recursive(os.path.join(dir_path_content, dir), template_path, os.path.join(dest_dir_path, dir), basepath)
        

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    md_file = os.path.join(from_path, "index.md")
    if not os.path.exists(md_file):
        print(f"no index.md found in {md_file}")
        return
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(md_file) as f:
        md = f.read()
    with open(template_path) as f:
        template = f.read()
    doc = markdown_to_html_node(md)
    doc_str = doc.to_html()
    title = extract_title(md)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", doc_str)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    with open(os.path.join(dest_path, "index.html"), "w") as f:
        f.write(template)


def extract_title(markdown: str)-> str:
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