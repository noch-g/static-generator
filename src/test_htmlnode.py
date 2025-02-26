import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "www.example.com", "style": "centred", "color":"red"})
        props_string = node.props_to_html()
        self.assertEqual(props_string, " href=\"www.example.com\" style=\"centred\" color=\"red\"")
    
    def test_empty_props(self):
        node = HTMLNode()
        props_string = node.props_to_html()
        self.assertEqual(props_string, "")

    def test_values(self):
        node = HTMLNode("div", "I wish I could read")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

class TestLeafNode(unittest.TestCase):
    def test_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    
    def test_no_value(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()