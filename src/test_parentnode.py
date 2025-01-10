import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_no_tag_value_raises_error(self):
        with self.assertRaisesRegex(ValueError, "All parent nodes must have a tag name"):
            node = ParentNode(None, [LeafNode("p", "Just a paragraph", None)],None)
            node.to_html()

    def test_no_children__raises_error(self):
        with self.assertRaisesRegex(ValueError, "All parent nodes must have children"):
            node = ParentNode("p", None, None)
            node.to_html()
    
    def test_single_child_html__string(self):
        node = ParentNode("div", [LeafNode("p", "Just a paragraph", None)], {"class":"container"})
        self.assertEqual(node.to_html(), "<div class=\"container\"><p>Just a paragraph</p></div>")



if __name__ == "__main__":
    unittest.main()
