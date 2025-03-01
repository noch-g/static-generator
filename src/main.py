from generate import rm_rf, copy_r, generate_pages_recursive


if __name__ == "__main__":
    rm_rf("public")
    copy_r("static", "public")
    generate_pages_recursive("./content", "template.html", "./public")
