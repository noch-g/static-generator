from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, delim_text_type: TextType) -> list[TextNode]:
	new_nodes = []
	for node in old_nodes:
		split_text = node.text.split(delimiter)
		if len(split_text) % 2 == 0:
			raise SyntaxError(f'check usage of delimiter "{delimiter}" in: "{node.text}"')
		for i in range(len(split_text)):
			if not split_text[i]:
				continue
			if i % 2 == 1:
				new_nodes.append(TextNode(split_text[i], delim_text_type))
			else:
				new_nodes.append(TextNode(split_text[i], node.text_type))
	return new_nodes
