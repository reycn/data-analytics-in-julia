import os
import shutil

import nbformat
from nbconvert import MarkdownExporter


# Step 1: Copy ./READ.ME.md to ./gitbook
def clean_gitbook_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


# Step 0: Clean all existing files in ./gitbook
gitbook_dir = "./gitbook"
clean_gitbook_directory(gitbook_dir)

# Step 2: Copy all contents under ./notebooks into ./gitbook
notebooks_dir = "./notebooks"
gitbook_dir = "./gitbook"

for item in os.listdir(notebooks_dir):
    s = os.path.join(notebooks_dir, item)
    d = os.path.join(gitbook_dir, item)
    if os.path.isdir(s):
        shutil.copytree(s, d, dirs_exist_ok=True)
    else:
        shutil.copy2(s, d)

# Step 3: Export all *.ipynb files under ./gitbook into markdown
exporter = MarkdownExporter()
for root, dirs, files in os.walk(gitbook_dir):
    for file in files:
        if file.endswith(".ipynb"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                nb = nbformat.read(f, as_version=4)
            (body, resources) = exporter.from_notebook_node(nb)
            md_file_path = file_path.replace(".ipynb", ".md")
            with open(md_file_path, "w", encoding="utf-8") as f:
                f.write(body)
            os.remove(file_path)

# Step 4: Replace all paths in *.md files under dir ./gitbook; replace all notebook/ with gitbook
for root, dirs, files in os.walk(gitbook_dir):
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            content = content.replace("notebook/", "gitbook/")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

# Step 4. Copy readme

shutil.copy("./README.md", "./gitbook/0.contents.md")
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
content = content.replace("notebook/", "./")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
