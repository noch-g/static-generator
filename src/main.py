from generate import rm_rf, copy_r, generate_pages_recursive
import sys

if __name__ == "__main__":
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    rm_rf("docs")
    copy_r("static", "docs")
    generate_pages_recursive("./content", "template.html", "./docs", basepath)
