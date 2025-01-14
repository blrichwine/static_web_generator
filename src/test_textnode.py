import unittest

from textnode import TextNode, TextType

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
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_eq4(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://docs.python.org")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://doc.rust-lang.org/book/")
        self.assertNotEqual(node, node2)

    def test_eq5(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://docs.python.org")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://docs.python.org")
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
