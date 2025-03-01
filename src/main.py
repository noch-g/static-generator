from generate import rm_rf, copy_r, generate_page


if __name__ == "__main__":
    rm_rf("public")
    copy_r("static", "public")
    generate_page("./content/index.md", "template.html", "./public")
