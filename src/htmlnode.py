from functools import reduce

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return reduce(lambda a, k: a+f" {k}=\"{self.props[k]}\"", self.props, "") if self.props else ""

    def __eq__(self, other_html_node):
        return self.tag == other_html_node.tag and \
            self.value == other_html_node.value and \
            self.children == other_html_node.children and \
            self.props == other_html_node.props

    def __repr__(self, level=0):
        return f"HTMLNode('{self.tag}', '{self.value}', {str(self.children)}, {str(self.props)})"
