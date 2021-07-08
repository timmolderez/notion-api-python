from typing import Dict, List

from mistletoe import BaseRenderer


class NotionBlockRenderer(BaseRenderer):

    def render_paragraph(self, token) -> Dict:
        block = {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "text": self.render_inner(token)
            }
        }
        return block

    def render_raw_text(self, token) -> Dict:
        """
        Default render method for RawText. Simply return token.content.
        """
        obj = {"type": "text",
               "text": {"content": token.content}}
        return obj

    def render_inner(self, token) -> List[Dict]:
        """
        Recursively renders child tokens.
        """
        return [self.render(child) for child in token.children]
