from enum import Enum, auto
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_elements import text_to_textnodes
from textnode import text_node_to_html_node

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
        if md.strip():
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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        match(type):
            case BlockType.HEADING:
                heading_start = "#"
                while True:
                    if block.startswith(f"{heading_start} "):
                        break
                    heading_start += "#"
                count = heading_start.count("#")
                if len(text_to_textnodes(block)) != 0:
                    html_node = ParentNode(f"h{count}", text_node_to_html_node(text_to_textnodes(block)))
                    nodes.append(html_node)
                else:
                    html_node = LeafNode(f"h{count}", block[count+1:])
            case BlockType.CODE:
                code_content = block.strip("`").strip()
                code_content += "\n"
                node1 = LeafNode("code", code_content)
                node2 = ParentNode("pre", [node1])
                nodes.append(node2)
            case BlockType.QUOTE:
                lines = block.split("\n")
                md_deleted_lines= list(map(lambda x: x[1:], lines))
                joined_lines = "\n".join(md_deleted_lines)
                if len(text_to_textnodes(block)) != 0:
                    html_node = ParentNode("blockquote", text_node_to_html_node(text_to_textnodes(block)))
                    nodes.append(html_node)
                else:
                    html_node = LeafNode("blockquote", joined_lines)
                    nodes.append(html_node)
            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                list_items = list(map(lambda x: x[2:], lines))
                list_nodes = []
                for item in list_items:
                    if len(text_to_textnodes(item)) != 0:
                        list_nodes.append(ParentNode("li", text_node_to_html_node(text_to_textnodes(item))))
                    else:
                        list_nodes.append(LeafNode("li", item))
                html_node = ParentNode("ul", list_nodes)
                nodes.append(html_node)
            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                list_items = list(map(lambda x: x[2:], lines))
                list_nodes = []
                for item in list_items:
                    if len(text_to_textnodes(item)) != 0:
                        list_nodes.append(ParentNode("li", text_node_to_html_node(text_to_textnodes(item))))
                    else:
                        list_nodes.append(LeafNode("li", item))
                html_node = ParentNode("ol", list_nodes)
                nodes.append(html_node)
            case BlockType.PARAGRAPH:
                paragraph_content = " ".join(block.splitlines()).strip()
                if len(text_to_textnodes(block)) != 0:
                    nodes.append(ParentNode("p", text_node_to_html_node(text_to_textnodes(paragraph_content))))
                else:
                    nodes.append(LeafNode("p", paragraph_content))

    return ParentNode("div", nodes)