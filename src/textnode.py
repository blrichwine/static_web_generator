import re
from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_text_node):
        return self.text == other_text_node.text and \
                self.text_type == other_text_node.text_type and \
                self.url == other_text_node.url

    def __repr__(self):
        return(f"TextNode('{self.text}', '{self.text_type.value}', '{self.url}')")

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode('b', text_node.text, None)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text, None)
        case TextType.CODE:
            return LeafNode('code', text_node.text, None)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {'href':text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', '', {'src':text_node.url, 'alt':text_node.text})
        case _:
            raise Exception(f"Invalid TextNode type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not isinstance(old_nodes, list):
        raise TypeError(f"Expected lis, got {type(items).__name__}")
    new_list = []
    if old_nodes:
        for node in old_nodes:
            if node.text_type == TextType.TEXT:
                chunks = node.text.split(delimiter)
                for i, chunk in enumerate(chunks):
                    if not chunk:
                        continue
                    if i % 2 == 0:
                        new_list.append(TextNode(chunk, TextType.TEXT))
                    else:
                        new_list.append(TextNode(chunk, text_type))
            else:
                new_list.append(node)
    return new_list

def extract_markdown_images(text):
    if not text:
        return []
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    return [(alt, src) for alt, src in re.findall(pattern, text)]

def extract_markdown_links(text):
    if not text:
        return []
    pattern = r'(?<!\!)\[([^\]]*)\]\(([^)]+)\)'
    return [(anchor_text, href) for anchor_text, href in re.findall(pattern, text)]

def split_nodes_image(old_nodes):
    if not isinstance(old_nodes, list):
        raise TypeError(f"Expected list, got {type(old_nodes).__name__}")
    new_list = []
    pattern = r'!\[[^\]]*\]\([^)]+\)'
    if old_nodes:
        for node in old_nodes:
            if node.text_type == TextType.TEXT:
                chunks = re.split(pattern, node.text)
                images = extract_markdown_images(node.text)
                for i, chunk in enumerate(chunks):
                    if chunk:
                        new_list.append(TextNode(chunk, TextType.TEXT))
                    if len(images) >= i+1:
                        new_list.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
            else:
                new_list.append(node)
    return new_list

def split_nodes_link(old_nodes):
    if not isinstance(old_nodes, list):
        raise TypeError(f"Expected list, got {type(old_nodes).__name__}")
    new_list = []
    pattern = r'(?<!\!)\[[^\]]*\]\([^)]+\)'
    if old_nodes:
        for node in old_nodes:
            if node.text_type == TextType.TEXT:
                chunks = re.split(pattern, node.text)
                links = extract_markdown_links(node.text)
                for i, chunk in enumerate(chunks):
                    if chunk:
                        new_list.append(TextNode(chunk, TextType.TEXT))
                    if len(links) >= i+1:
                        new_list.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
            else:
                new_list.append(node)
    return new_list

def text_to_textnodes(text):
    if not text:
        return []
    
    return  split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter( split_nodes_delimiter( [TextNode(text,TextType.TEXT)], '**', TextType.BOLD), '*', TextType.ITALIC), '`', TextType.CODE)))

def text_to_html_nodes(text):
    HTMLNodes = []
    for node in text_to_textnodes(text):
        HTMLNodes.append(text_node_to_html_node(node))
    return HTMLNodes
