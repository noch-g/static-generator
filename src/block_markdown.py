import re

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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


def markdown_to_blocks(text: str) -> list[str]:
    blocks = []
    for block in text.split("\n\n"):
        block = block.removesuffix("\n")
        if block.strip() != "":
            blocks.append(block.strip())
    return blocks

if __name__ == "__main__":
    ordered_list = """1. Hello
2. world
3. !"""
    print(block_to_block_type(ordered_list))