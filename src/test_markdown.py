import unittest

from markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title
from htmlnode import HTMLNode

class TestMarkDown(unittest.TestCase):


    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        new_nodes = markdown_to_blocks(markdown)
        expected_nodes = ["# This is a heading",
                          "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                          "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
                          ]
        self.assertEqual(expected_nodes, new_nodes)

    def test_block_to_block_type(self):
        self.assertEqual("heading", block_to_block_type("# main heading"))

    def test_block_to_block_type2(self):
        self.assertEqual("heading", block_to_block_type("## sub heading"))

    def test_block_to_block_type3(self):
        self.assertEqual("heading", block_to_block_type("###### last valid heading"))

    def test_block_to_block_type4(self):
        self.assertEqual("paragraph", block_to_block_type("####### not a valid heading"))

    def test_block_to_block_type5(self):
        self.assertEqual("paragraph", block_to_block_type(""))

    def test_block_to_block_type6(self):
        self.assertEqual("code", block_to_block_type("``` just some wild stuff\nin here\wow```"))

    def test_block_to_block_type7(self):
        self.assertEqual("quote", block_to_block_type("> to be or not to\n>be"))

    def test_block_to_block_type8(self):
        self.assertEqual("unordered_list", block_to_block_type("- test\n* list"))

    def test_block_to_block_type9(self):
        self.assertEqual("ordered_list", block_to_block_type("1. first\n2. second\n3. third"))

    def test_block_to_block_type10(self):
        self.assertEqual("paragraph", block_to_block_type("1. first\n2. second\n7. third"))

    def test_markdown_to_html_node(self):
        new_nodes = markdown_to_html_node("")
        expected_nodes = HTMLNode("div", None, [], {})
        self.assertEqual(new_nodes, expected_nodes)

    def test_extract_title(self):
        markdown = "\n\n# Just a test\n\nWe are just testing"
        self.assertEqual("Just a test", extract_title(markdown))

if __name__ == "__main__":
    unittest.main()
