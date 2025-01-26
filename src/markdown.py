import re
from leafnode import *
from parentnode import *
from htmlnode import *
from textnode import *

def markdown_to_blocks(markdown):
    blocks = []
    if not markdown:
        return blocks
    last_line_was_blank = False
    block = ""
    for line in markdown.split("\n"):
        line = line.strip()
        if not line:
            last_line_was_blank = True
            if block:
                blocks.append(block)
                block = ""
        else:
            block = f"{block.strip()}\n{line}" if block else line
    if block:
        blocks.append(block.strip())

    return blocks

def block_to_block_type(block):
    heading_pattern = r"^#{1,6} .+"
    codeblock_pattern = r"^```[\s\S]*```$"
    quoteblock_pattern = r"^>[^\n]*(\n>[^\n]*)*$"
    unorderedblock_pattern = r"^[*-] [^\n]*(\n[*-] [^\n]*)*$"
    orderedblock_pattern = r"^\d+. [^\n]*(\n\d+. [^\n]*)*$"

    if re.match(heading_pattern, block):
        return f"heading"
    if re.match(codeblock_pattern, block):
        return "code"
    if re.match(quoteblock_pattern, block):
        return "quote"
    if re.match(unorderedblock_pattern, block):
        return "unordered_list"
    if re.match(orderedblock_pattern, block):
        valid = True
        for i, line in enumerate(block.split("\n"), start=1):
            if not line.startswith(str(i)):
                valid = False

        if valid:
            return "ordered_list"
    return "paragraph"

def make_heading_from_block(block):
    tag_name = f"h{block.find(" ")}"
    text = block[block.find(" ")+1:]
    children = text_to_html_nodes(text)
    return ParentNode(tag_name, children, {})

def make_code_from_block(block):
    code = block[3:-3].strip()
    return ParentNode("pre", [LeafNode("code", code, {})], {})

def make_quote_from_block(block):
    children = text_to_html_nodes("\n".join([s[1:].strip() if s.startswith('>') else s.strip() for s in block.split("\n")]))
    return ParentNode("blockquote", children, {})

def make_unordered_list_from_block(block):
    items = []
    for line in block.split("\n"):
        children = text_to_html_nodes(line[1:].strip() if line.startswith('-') or line.startswith('*') else line.strip())
        items.append(ParentNode("li", children, {}))
    return ParentNode("ul", items, {})

def make_ordered_list_from_block(block):
    items = []
    for line in block.split("\n"):
        children = text_to_html_nodes(line[line.find(".")+1:].strip())
        items.append(ParentNode("li", children, {}))
    return ParentNode("ol", items, {})
                
def make_paragraph_from_block(block):
    children = text_to_html_nodes("\n".join([s[1:] if s.startswith('>') else s for s in block.split("\n")]))
    return ParentNode("p", children, {})

def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        match(block_to_block_type(block)):
            case "heading":
                html_nodes.append(make_heading_from_block(block))
            case "code":
                html_nodes.append(make_code_from_block(block))
            case "quote":
                html_nodes.append(make_quote_from_block(block))
            case "unordered_list":
                html_nodes.append(make_unordered_list_from_block(block))
            case "ordered_list":
                html_nodes.append(make_ordered_list_from_block(block))
            case "paragraph":
                html_nodes.append(make_paragraph_from_block(block))

    return ParentNode('div', html_nodes, {})

def extract_title(markdown):
    if not isinstance(markdown, str):
        raise Exception("Not a string")
    for line in markdown.split("\n"):
        line = line.strip()
        if line.startswith("# ") and len(line)>2:
            return line[2:].strip()
