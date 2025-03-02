from textnode import TextNode, TextType
import re

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, delim_text_type: TextType) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		if delimiter not in node.text:
			new_nodes.append(node)
			continue
		split_text = node.text.split(delimiter)
		if len(split_text) % 2 == 0:
			raise SyntaxError(f'check usage of delimiter "{delimiter}" in: "{node.text}"')
		for i in range(len(split_text)):
			if not split_text[i]:
				continue
			if i % 2 == 1:
				if delim_text_type == TextType.IMAGE or delim_text_type == TextType.LINK:
					data = split_text[i].split(">")
					txt, url = data[0], data[1]
					new_nodes.append(TextNode(txt, delim_text_type, url))
				else:
					new_nodes.append(TextNode(split_text[i], delim_text_type))
			else:
				new_nodes.append(TextNode(split_text[i], node.text_type))
	return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue
		matches = extract_markdown_images(node.text)
		if not matches:
			new_nodes.append(node)
			continue
		for match in matches:
			node.text = node.text.replace(f"![{match[0]}]({match[1]})", f"<img>{match[0]}>{match[1]}<img>")
		new_nodes += split_nodes_delimiter([node], "<img>", TextType.IMAGE)
	return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue
		matches = extract_markdown_links(node.text)
		if not matches:
			new_nodes.append(node)
			continue
		for match in matches:
			node.text = node.text.replace(f"[{match[0]}]({match[1]})", f"<link>{match[0]}>{match[1]}<link>")
		new_nodes += split_nodes_delimiter([node], "<link>", TextType.LINK)
	return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

if __name__ == "__main__":
	node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
	new_nodes = split_nodes_image([node])