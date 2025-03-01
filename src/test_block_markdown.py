import unittest
import textwrap

from htmlnode import ParentNode, LeafNode
from block_markdown import (
BlockType,
markdown_to_blocks, 
block_to_block_type,
heading_to_html_node, 
code_to_html_node,
quote_to_html_node,
ulist_to_html_node,
olist_to_html_node,
paragraph_to_html_node,
markdown_to_html_node
)

class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = textwrap.dedent("""\
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here
        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = textwrap.dedent("""\
            ```This is text that _should_ remain
            the **same** even with inline stuff
            ```
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_inline_in_list_blocks(self):
        md = textwrap.dedent("""\
            - Hello **bold**
            - and _italic_
        """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Hello <b>bold</b></li><li>and <i>italic</i></li></ul></div>",
        )

class TestBlockToHTML(unittest.TestCase):
    def test_heading_block_html(self):
        self.assertEqual(heading_to_html_node("# Title"), ParentNode("h1", [LeafNode(None, "Title")]))
        self.assertEqual(heading_to_html_node("### Title"), ParentNode("h3", [LeafNode(None, "Title")]))
        self.assertEqual(heading_to_html_node("#### Title"), ParentNode("h4", [LeafNode(None, "Title")]))
    
    def test_code_block_html(self):
        self.assertEqual(code_to_html_node("```code block\nmore code```"), ParentNode("pre", [LeafNode("code", "code block\nmore code")]))

    def test_quote_block_html(self):
        children = [LeafNode(None, "quote\nsecond "), LeafNode("b", "line")]
        self.assertEqual(quote_to_html_node(">quote\n>second **line**"), ParentNode("blockquote", children))

    def test_unordered_list_html(self):
        unordered_list = "- Eggs\n- Cheese\n- **Whole** Pasta"
        children = [
            ParentNode("li", [LeafNode(None, "Eggs")]), 
            ParentNode("li", [LeafNode(None, "Cheese")]), 
            ParentNode("li", [LeafNode("b", "Whole"), LeafNode(None, " Pasta")]),
        ]
        self.assertEqual(ulist_to_html_node(unordered_list), ParentNode("ul", children))

    def test_ordered_list_html(self):
        ordered_list = "1. Hello\n2. _world_\n3. !"
        children = [
            ParentNode("li", [LeafNode(None, "Hello")]), 
            ParentNode("li", [LeafNode("i", "world")]), 
            ParentNode("li", [LeafNode(None, "!")])
        ]
        self.assertEqual(olist_to_html_node(ordered_list), ParentNode("ol", children))

    def test_paragraph_html(self):
        paragraph = "Hello world **in bold**"
        self.assertEqual(paragraph_to_html_node(paragraph), ParentNode("p", [LeafNode(None, "Hello world "), LeafNode("b", "in bold")]))

class TestBlockMarkdown(unittest.TestCase):
    def test_headings(self):
        self.assertEqual(block_to_block_type("# Title"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Title"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Title"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Title"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Title"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Title"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### Title"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("##Title"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(" # Title"), BlockType.PARAGRAPH)

    def test_code(self):
        self.assertEqual(block_to_block_type("```block of code```"), BlockType.CODE)
        self.assertEqual(block_to_block_type(" ```space at start```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```space at end``` "), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```\nprint('several lines')\nprint('hello world')\n```"), BlockType.CODE)

    def tets_quote(self):
        self.assertEqual(block_to_block_type(">Title"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(" >Title"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("> bla bla\n> bla bla\n>bla bla bla"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> bla bla\nmissing symbol\n> bla bla bla"""), BlockType.PARAGRAPH)
    
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Eggs\n- Cheese\n- Pasta"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(" - Bad indent"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- Eggs\n-No Space"), BlockType.PARAGRAPH)
    
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Hello\n2. world\n3. !"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("2. wrong start"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("""1. double\n1. one"""), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. bad\n  2. indent"), BlockType.PARAGRAPH)

    def test_markdown_to_blocks(self):
        md = textwrap.dedent("""\
            This is **bolded** paragraph


            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
        """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )