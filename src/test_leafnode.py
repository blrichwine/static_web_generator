import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_no_value_raises_error(self):
        with self.assertRaisesRegex(ValueError, "All leaf nodes must have a value"):
            node = LeafNode("p", None, None)
            node.to_html()

    def test_no_tag_name_returns_value_string(self):
        node = LeafNode(None, "This is not the droid you are looking for.", None)
        self.assertEqual(node.to_html(), "This is not the droid you are looking for.")

    def test_tag_name_returns_html(self):
        node = LeafNode("p","I know that dude.",{"class":"quintessentialArchetype", "id":"spicoli"})
        self.assertEqual(node.to_html(), '<p class="quintessentialArchetype" id="spicoli">I know that dude.</p>')


if __name__ == "__main__":
    unittest.main()
