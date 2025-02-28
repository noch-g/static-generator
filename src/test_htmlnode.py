import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode

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

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
    def test_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")])
        self.assertRaises(ValueError, node.to_html)
    
    def test_no_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_siblings_with_kids(self):
        grandchild1 = LeafNode("b", "Image 1")
        grandchild2 = LeafNode("i", "image link")
        grandchild3 = LeafNode(None, "Hello, world!")
        child_node1 = ParentNode("span", [grandchild1, grandchild2])
        child_node2 = ParentNode("p", [grandchild3])
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>Image 1</b><i>image link</i></span><p>Hello, world!</p></div>",
        )

if __name__ == "__main__":
    unittest.main()