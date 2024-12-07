class HTMLNode:
    def __init__(self, tag = None, value = None, children = None,props = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def __repr__(self):
        return (f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
                f"children={len(self.children)} children, props={self.props!r})")


    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def props_to_html(self):
        if not self.props:
            return  ""
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value.")
        super().__init__(tag=tag, value=value, children=[], props=props)

    def to_html(self):
        if self.tag is None:
            return self.value
        props_str = self.props_to_html()  # Get props as a string (e.g., ' href="..."')
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children=None, props=None):
        if children is None:
            raise ValueError("Parent Node must have a children.")
        super().__init__(tag=tag, children=children if children else [], props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        
        props_str = self.props_to_html()
        op_tag = f"<{self.tag}{props_str}>"
        cl_tag = f"</{self.tag}>"

        children_html = ''.join(child.to_html() for child in self.children)

        return f"{op_tag}{children_html}{cl_tag}"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    
