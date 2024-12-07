import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_single_delimiter_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_unmatched_delimiter(self):
        node = TextNode("This is text with an unmatched `code block", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_no_delimiters_present(self):
        node = TextNode("This text has no delimiters.", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This text has no delimiters.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_bold_text_delimiters(self):
        node = TextNode("This is **bold** and **another bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

class TestExtractMarkdownImages(unittest.TestCase):
    
    def test_basic_image_extraction(self):
        text = "Here is an image ![alt text](https://example.com/image.jpg)"
        self.assertEqual(extract_markdown_images(text), [("alt text", "https://example.com/image.jpg")])
    
    def test_multiple_images(self):
        text = "Here are images ![img1](https://example.com/img1.jpg) and ![img2](https://example.com/img2.jpg)"
        self.assertEqual(extract_markdown_images(text), [
            ("img1", "https://example.com/img1.jpg"),
            ("img2", "https://example.com/img2.jpg")
        ])
    
    def test_image_with_special_characters_in_alt_text(self):
        text = "![alt (with) special characters](https://example.com/image.jpg)"
        self.assertEqual(extract_markdown_images(text), [("alt (with) special characters", "https://example.com/image.jpg")])
    
    def test_no_images(self):
        text = "This text has no images."
        self.assertEqual(extract_markdown_images(text), [])
    
    def test_non_image_markdown_links(self):
        text = "This is a [link](https://example.com) and not an image."
        self.assertEqual(extract_markdown_images(text), [])

class TestCombinedCases(unittest.TestCase):
    
    def test_text_with_both_images_and_links(self):
        text = "Here is a [link](https://example.com) and an image ![image](https://example.com/image.jpg)"
        self.assertEqual(extract_markdown_images(text), [("image", "https://example.com/image.jpg")])
        self.assertEqual(extract_markdown_links(text), [("link", "https://example.com")])

        def test_extract_markdown_images(self):
            matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
            self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )