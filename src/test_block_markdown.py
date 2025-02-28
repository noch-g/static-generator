import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

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
        self.assertEqual(block_to_block_type("- Oeufs\n- Fromage\n- Pâtes"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(" - Bad indent"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- Oeufs\n-No Space"), BlockType.PARAGRAPH)
    
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Hello\n2. world\n3. !"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("2. wrong start"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("""1. double\n1. one"""), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. bad\n  2. indent"), BlockType.PARAGRAPH)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )