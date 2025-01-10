import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_none(self):
        node = HTMLNode("h1","History of Kale",None,None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_one(self):
        node = HTMLNode("h1","History of Kale",None, {"class":"articleTitle"})
        self.assertEqual(node.props_to_html(), " class=\"articleTitle\"")

    def test_props_two(self):
        node = HTMLNode("h1","History of Kale",None, {"class":"articleTitle", "id":"mainTitle"})
        self.assertEqual(node.props_to_html(), " class=\"articleTitle\" id=\"mainTitle\"")

    def test_repr(self):
        node = HTMLNode("h1","History of Kale",None, {"class":"articleTitle", "id":"mainTitle"})
        self.assertEqual(node.__repr__(), "HTMLNode('h1', 'History of Kale', None, {'class': 'articleTitle', 'id': 'mainTitle'})")


if __name__ == "__main__":
    unittest.main()
