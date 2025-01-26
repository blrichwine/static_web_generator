import os
import shutil
from textnode import TextNode, TextType
from leafnode import LeafNode
from markdown import markdown_to_html_node, extract_title

def clean_directory(dir_path):
    if not os.path.exists(dir_path):
        raise Exception("Path to clean does not exist: {dir_path}")
    if not os.path.isdir(dir_path):
        raise Exception("Path to clean is not a directory: {dir_path}")
    abs_path = os.path.abspath(dir_path)
    if abs_path.find("static_web_generator/public")<5:
        raise Exception("BAD PATH: {abs_path")
    shutil.rmtree(dir_path)
    os.mkdir(dir_path)


def copy_folder(src_path, dest_path):
    if not os.path.exists(src_path):
        raise Exception(f"Source path does not exist: {src_path}") 
    abs_path = os.path.abspath(src_path)
    if abs_path.find("static_web_generator/static")<5:
        raise Exception("BAD src_path: {abs_path")
    abs_path = os.path.abspath(dest_path)
    if abs_path.find("static_web_generator/public")<5:
        raise Exception("BAD dest_path: {abs_path")

    if os.path.exists(dest_path):
        clean_directory(dest_path)
    else:
        os.mkdir(dest_path)

    for f in os.listdir(src_path):
        ff_src = os.path.join(src_path, f)
        ff_dest = os.path.join(dest_path, f)
        if os.path.isfile(ff_src):
            shutil.copy(ff_src, ff_dest)
        else:
            copy_folder(ff_src, ff_dest)

def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise Exception(f"From path does not exist: {from_path}")
    if not os.path.exists(template_path):
        raise Exception(f"Template path does not exist: {template_path}")
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, encoding="utf-8") as f:
        md = f.read()
    with open(template_path, encoding="utf-8") as f:
        t = f.read()
    hn = markdown_to_html_node(md)
    title = extract_title(md)
    t = t.replace("{{ Title }}", title)
    t = t.replace("{{ Content }}", hn.to_html())
    with open(dest_path, "w") as f:
        f.write(t)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception("Content path does not exist: {dir_path_content}")
    if not os.path.exists(template_path):
        raise Exception("Template path does not exist: {template_path}")
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    
    for f in os.listdir(dir_path_content):
        ff = os.path.join(dir_path_content,f)
        if os.path.isfile(ff):
            if(ff.endswith('.md')):
                generate_page(ff, template_path, os.path.join(dest_dir_path, f[:-2]+'html'))
        else:
            generate_pages_recursive(ff, template_path, os.path.join(dest_dir_path, f))

def main():
    copy_folder("/Users/brichwin/workspace/github.com/blrichwine/static_web_generator/static/",
                "/Users/brichwin/workspace/github.com/blrichwine/static_web_generator/public/")
    generate_pages_recursive("./content/", "./template.html", "./public/")

if __name__ == "__main__":
    main()
