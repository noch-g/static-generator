import re
import textwrap

from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(text: str) -> list[str]:
    blocks = []
    for block in text.split("\n\n"):
        block = block.removesuffix("\n")
        if block.strip() != "":
            blocks.append(block.strip())
    return blocks

def markdown_to_html_node(markdown: str) -> HTMLNode:
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(ulist_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(olist_to_html_node(block))
        else:
            children.append(paragraph_to_html_node(block))

    return ParentNode("div", children=children)

def text_to_children(text: str) -> list[LeafNode]:
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def heading_to_html_node(block: str) -> ParentNode:
    nb_tags = 0
    ix = 0
    while ix < min(6, len(block)):
        if block[ix] == "#":
            nb_tags += 1
        else:
            break
        ix += 1
    children = text_to_children(block[ix+1:])
    return ParentNode(f"h{ix}", children)

def code_to_html_node(block: str) -> ParentNode:
    text_node = TextNode(block[3:-3], TextType.CODE)
    return ParentNode("pre", [text_node_to_html_node(text_node)])

def quote_to_html_node(block: str) -> ParentNode:
    text = "\n".join([line[1:] for line in block.split("\n")])
    return ParentNode("blockquote", text_to_children(text))

def ulist_to_html_node(block: str) -> ParentNode:
    children = []
    for line in block.split("\n"):
        children.append(ParentNode("li", text_to_children(line[2:])))
    return ParentNode("ul", children)

def olist_to_html_node(block: str) -> ParentNode:
    children = []
    for line in block.split("\n"):
        children.append(ParentNode("li", text_to_children(line[3:])))
    return ParentNode("ol", children)

def paragraph_to_html_node(block: str) -> ParentNode:
    text = " ".join(block.split("\n"))
    p_children = text_to_children(text)
    return ParentNode("p", p_children)

def block_to_block_type(text: str) -> BlockType:
    lines = text.split("\n")
    if text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if text.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if text.startswith("- "):
        for line in lines:
           if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if text.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(str(i) + ". "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
