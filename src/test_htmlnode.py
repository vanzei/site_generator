import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(tag="p", value="Test paragraph")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        node = HTMLNode(tag="a", value="Link", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode(tag="p", value="Test paragraph", props={"class": "text"})
        expected_repr = "HTMLNode(tag='p', value='Test paragraph', children=0 children, props={'class': 'text'})"
        self.assertEqual(repr(node), expected_repr)

class TestLeafNode(unittest.TestCase):
    
    # Test the creation of a LeafNode with valid inputs
    def test_leaf_node_creation(self):
        leaf = LeafNode(tag="p", value="This is a paragraph.")
        self.assertEqual(leaf.tag, "p")
        self.assertEqual(leaf.value, "This is a paragraph.")
        self.assertEqual(leaf.children, [])  # LeafNode should have no children
        self.assertEqual(leaf.props, {})     # No props should be empty dictionary

    # Test rendering LeafNode with a tag and value
    def test_to_html_with_tag(self):
        leaf = LeafNode(tag="p", value="A paragraph")
        self.assertEqual(leaf.to_html(), "<p>A paragraph</p>")

    # Test rendering LeafNode with a tag and value, with HTML props (attributes)
    def test_to_html_with_props(self):
        leaf = LeafNode(tag="a", value="Google", props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(leaf.to_html(), '<a href="https://google.com" target="_blank">Google</a>')

    # Test rendering LeafNode as raw text (without a tag)
    def test_to_html_no_tag(self):
        leaf = LeafNode(tag=None, value="Just text")
        self.assertEqual(leaf.to_html(), "Just text")

    # Test that creating a LeafNode without a value raises ValueError
    def test_leaf_node_missing_value(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p", value=None)

    # Test that creating a LeafNode with empty string value still works (edge case)
    def test_leaf_node_empty_string_value(self):
        leaf = LeafNode(tag="p", value="")
        self.assertEqual(leaf.to_html(), "<p></p>")
    

if __name__ == "__main__":
    unittest.main()
