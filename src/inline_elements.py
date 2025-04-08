from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or node.text.find(delimiter) == -1:
            new_nodes.append(node)
            continue
        node_list = node.text.split(delimiter)
        if len(node_list) % 2 == 0:
            raise Exception("Markdown symbol not closed!")
        if len(node_list) > 1:
            for i in range(0, len(node_list)):
                if node_list[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(node_list[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(node_list[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if len(extract_markdown_images(node.text)) == 0 or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        images = extract_markdown_images(node_text)
        for i in range(0,len(images)):
            nodelist = node_text.split(f"![{images[i][0]}]({images[i][1]})", 1)
            if len(nodelist) != 2:
                raise Exception(f"Image markdown not closed. Length: {len(nodelist)}")
            new_nodes.append(TextNode(nodelist[0], TextType.TEXT))
            new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
            node_text = nodelist[1]
            if node_text != "" and i == len(images) - 1:
                new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if len(extract_markdown_links(node.text)) == 0 or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        links = extract_markdown_links(node_text)
        for i in range(0, len(links)):
            nodelist = node_text.split(f"[{links[i][0]}]({links[i][1]})", 1)
            if len(nodelist) != 2:
                raise Exception(f"Link markdown not closed. Length: {len(nodelist)}")
            new_nodes.append(TextNode(nodelist[0], TextType.TEXT))
            new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
            node_text = nodelist[1]
            if node_text != "" and i == len(links) - 1:
                new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    bolded_nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    italicized_nodes = split_nodes_delimiter(bolded_nodes, "_", TextType.ITALIC)
    coded_nodes = split_nodes_delimiter(italicized_nodes, "`", TextType.CODE)
    linked_nodes = split_nodes_link(coded_nodes)
    return split_nodes_image(linked_nodes)
    
##Tests are in test_textnode.py