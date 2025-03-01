from textnode import TextNode, TextType

import os
import shutil

def copy_r(folder_src: str, folder_dest: str) -> None:
    if not os.path.exists(folder_dest):
        os.mkdir(folder_dest)
    for item in os.listdir(folder_src):
        if os.path.isfile(os.path.join(folder_src, item)):
            shutil.copy(os.path.join(folder_src, item), os.path.join(folder_dest, item))
        else:
            copy_r(os.path.join(folder_src, item), os.path.join(folder_dest, item))

if __name__ == "__main__":
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_r("static", "public")
