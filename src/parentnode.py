import functools
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.children:
            raise ValueError("All parent nodes must have children")
        if not self.tag:
            raise ValueError("All parent nodes must have a tag name")
        return f"<{self.tag}{super().props_to_html()}>{functools.reduce(lambda a,n:a+n.to_html(),self.children,"")}</{self.tag}>"
