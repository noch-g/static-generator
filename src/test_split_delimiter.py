import unittest

from textnode import TextNode, TextType
from split_delimeter import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_simple_split(self):
        node = TextNode("Command: `hello` world", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
             new_nodes,
             [TextNode("Command: ", TextType.TEXT), TextNode("hello", TextType.CODE), TextNode(" world", TextType.TEXT)]
        )

    def test_split_start_of_line(self):
        node = TextNode("**Now** is the time", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [TextNode("Now", TextType.BOLD), TextNode(" is the time", TextType.TEXT)]
        )
    
    def test_split_end_of_line(self):
        node = TextNode("Good morning _Italy_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [TextNode("Good morning ", TextType.TEXT), TextNode("Italy", TextType.ITALIC)]
        )

    def test_more_splits(self):
        node = TextNode("**Now** is **the** time for **action**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
            TextNode("Now", TextType.BOLD), 
            TextNode(" is ", TextType.TEXT),
            TextNode("the", TextType.BOLD),
            TextNode(" time for ", TextType.TEXT),
            TextNode("action", TextType.BOLD),
            ]
        )

    def test_several_nodes(self):
        node = TextNode("**Now** is the time", TextType.TEXT)
        node2 = TextNode("for **action**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
            TextNode("Now", TextType.BOLD),
            TextNode(" is the time", TextType.TEXT),
            TextNode("for ", TextType.TEXT),
            TextNode("action", TextType.BOLD),
            ]
        )