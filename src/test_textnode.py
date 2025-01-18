import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq4(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://docs.python.org")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://doc.rust-lang.org/book/")
        self.assertNotEqual(node, node2)

    def test_eq5(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://docs.python.org")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://docs.python.org")
        self.assertEqual(node, node2)

    def test_to_html_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        lnode = text_node_to_html_node(node)
        self.assertEqual(str(lnode),"HTMLNode('None', 'This is a text node', None, None)")
        self.assertEqual(lnode.to_html(), "This is a text node")

    def test_to_html_node2(self):
        node = TextNode("This is a text node that for some reason is an image", TextType.IMAGE, "/images/fancy.gif")
        lnode = text_node_to_html_node(node)
        self.assertEqual(str(lnode),"HTMLNode('img', '', None, {'src': '/images/fancy.gif', 'alt': 'This is a text node that for some reason is an image'})")
        self.assertEqual(lnode.to_html(), '<img src="/images/fancy.gif" alt="This is a text node that for some reason is an image"></img>')

    def test_split_nodes_delimiter(self):
        nodes = []
        self.assertEqual(nodes, split_nodes_delimiter(nodes, "`", TextType.CODE))

    def test_split_nodes_delimiter2(self):
        nodes = [TextNode("The `aria-hidden` attribute can hide content from screen readers.", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), [
            TextNode("The ", TextType.TEXT), TextNode("aria-hidden", TextType.CODE), TextNode(" attribute can hide content from screen readers.", TextType.TEXT)
            ])

    def test_split_nodes_delimiter3(self):
        nodes = [TextNode("This is *just* some **simple** text.", TextType.TEXT)]
        new_nodes1 = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        new_nodes2 = split_nodes_delimiter(new_nodes1, "*", TextType.ITALIC)
        self.assertEqual(new_nodes2, [TextNode("This is ", TextType.TEXT), TextNode("just", TextType.ITALIC), TextNode(" some ", TextType.TEXT), 
                                               TextNode("simple", TextType.BOLD), TextNode(" text.", TextType.TEXT)])

    def test_extract_markdown_images(self):
        self.assertEqual([], extract_markdown_images(None))

    def test_extract_markdown_images2(self):
        self.assertEqual([], extract_markdown_images(''))

    def test_extract_markdown_images3(self):
        self.assertEqual([], extract_markdown_images('I don\'t contain any images or links'))

    def test_extract_markdown_images4(self):
        self.assertEqual([], extract_markdown_images('I don\'t contain any images but I do have a link [Google](https://www.google.com)'))

    def test_extract_markdown_images5(self):
        self.assertEqual([('', 'cool.gif'), ('alt text goes here', 'morecool.gif')], extract_markdown_images('I contain two images ![](cool.gif) and ![alt text goes here](morecool.gif)'))

    def test_extract_markdown_links(self):
        self.assertEqual([], extract_markdown_links(None))

    def test_extract_markdown_links2(self):
        self.assertEqual([], extract_markdown_links(''))

    def test_extract_markdown_links3(self):
        self.assertEqual([], extract_markdown_links('I don\'t contain any images or links'))

    def test_extract_markdown_links4(self):
        self.assertEqual([], extract_markdown_links('I don\'t contain any links but I do have an image ![Google](https://www.google.com/googlelogo.gif)'))

    def test_extract_markdown_links5(self):
        self.assertEqual([('Best place', 'https://www.boot.dev'), ('Bing', 'https://www.bing.com')], extract_markdown_links('I contain two links [Best place](https://www.boot.dev) and [Bing](https://www.bing.com)'))


if __name__ == "__main__":
    unittest.main()
