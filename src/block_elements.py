from enum import Enum, auto
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_elements import text_to_textnodes, TextType
from textnode import text_node_to_html_node, TextNode

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()

def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    splitted_markdown = markdown.split("\n\n")
    stripped_markdown = []
    for md in splitted_markdown:
        if md:
            cleaned_md = "\n".join([line.strip() for line in md.splitlines()])
            stripped_markdown.append(cleaned_md)
    return stripped_markdown

def block_to_block_type(block):

    heading_start = "#"
    while heading_start.count("#") < 7:
        if block.startswith(f"{heading_start} "):
            return BlockType.HEADING
        heading_start += "#"
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")
    if len(lines) == len(list(filter(lambda x: x.startswith(">"), lines))):
        return BlockType.QUOTE
    
    if len(lines) == len(list(filter(lambda x: x.startswith("- "), lines))):
        return BlockType.UNORDERED_LIST
    
    for i in range(0, len(lines)):
        if not lines[i].startswith(f"{i+1}."):
            return BlockType.PARAGRAPH
        
    return BlockType.ORDERED_LIST

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        if node:
            children.append(text_node_to_html_node(node))
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        if not block.strip():
            continue
        type = block_to_block_type(block)
        match(type):
            case BlockType.HEADING:
                heading_start = "#"
                while True:
                    if block.startswith(f"{heading_start} "):
                        break
                    heading_start += "#"
                count = heading_start.count("#")
                if count + 1 >= len(block):
                    raise Exception("Invalid heading!")
                text = block[count + 1:]
                nodes.append(ParentNode(f"h{count}", text_to_children(text)))
            case BlockType.CODE:
                code_content = block.strip().strip("`").strip()
                text_node = TextNode(code_content, TextType.TEXT)
                node1 = ParentNode("code", [text_node_to_html_node(text_node)])
                node2 = ParentNode("pre", [node1])
                nodes.append(node2)
            case BlockType.QUOTE:
                lines = block.split("\n")
                md_deleted_lines= list(map(lambda x: x.lstrip(">").strip(), lines))
                joined_lines = " ".join(md_deleted_lines)
                nodes.append(ParentNode("blockquote", text_to_children(joined_lines)))
            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                list_items = list(map(lambda x: x[2:], lines))
                list_nodes = []
                for item in list_items:
                    list_nodes.append(ParentNode("li", text_to_children(item)))
                html_node = ParentNode("ul", list_nodes)
                nodes.append(html_node)
            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                list_items = list(map(lambda x: x[3:], lines))
                list_nodes = []
                for item in list_items:
                    list_nodes.append(ParentNode("li", text_to_children(item)))
                html_node = ParentNode("ol", list_nodes)
                nodes.append(html_node)
            case BlockType.PARAGRAPH:
                paragraph_content = " ".join(block.splitlines())
                nodes.append(ParentNode("p", text_to_children(paragraph_content)))

    return ParentNode("div", nodes)