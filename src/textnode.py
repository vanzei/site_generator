class TextNode():
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node1, node2) -> bool:
        if node1.text == node2.text and node1.text_type == node2.text_type and node1.url == node2.url:
            return True
        else:
            return False
    
    def __repr__(self) -> str:
        pass
        