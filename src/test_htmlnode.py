import unittest
from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    """def test_eq(self):
        node = HTMLNode("header", "Backend", [HTMLNode("div")])
        node2 = HTMLNode("nav", "Backend", [HTMLNode("div")])
        self.assertNotEqual(node, node2)
    
    def test2_eq(self):
        node = HTMLNode("section","Python is good.", [HTMLNode("div")])
        node2 = HTMLNode("section", "Java is also good.", [HTMLNode("div")])
        self.assertNotEqual(node, node2)
    
    def test3_eq(self):
        node = HTMLNode("section","Backend", [HTMLNode("nav")])
        node2 = HTMLNode("section", "Backend", [HTMLNode("div")])
        self.assertNotEqual(node, node2)
    
    def test4_eq(self):
        node = HTMLNode("section","Backend", [HTMLNode("div")], {"href":"https://boot.dev/"})
        node2 = HTMLNode("section", "Backend", [HTMLNode("div")], {"style": "color:red;"})
        self.assertNotEqual(node, node2)
    
    def test5_eq(self):
        node = HTMLNode("section","Backend", [HTMLNode("div")], {"href":"https://boot.dev/", "style":"color:red;"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev/" style="color:red;"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )"""

if __name__ == "__main__":
    unittest.main()