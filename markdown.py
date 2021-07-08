from typing import Dict, List
from pprint import pprint

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

    def render_strong(self, token):
        inner_objs = self.render_inner(token)
        return _add_annotation(inner_objs, 'bold')

    def render_emphasis(self, token):
        inner_objs = self.render_inner(token)
        return _add_annotation(inner_objs, 'italic')

    def render_strikethrough(self, token):
        inner_objs = self.render_inner(token)
        return _add_annotation(inner_objs, 'strikethrough')

    def render_inline_code(self, token):
        inner_objs = self.render_inner(token)
        return _add_annotation(inner_objs, 'code')

    def render_raw_text(self, token) -> Dict:
        """
        Default render method for RawText. Simply return token.content.
        """
        obj = {"type": "text",
               "text": {"content": token.content}}
        return obj

    def render_inner(self, token) -> List[Dict]:
        rendered_list = []
        for child in token.children:
            obj = self.render(child)
            if isinstance(obj, List):
                # Flatten when there's recursive render_inner() calls..
                for subobj in obj:
                    rendered_list.append(subobj)
            else:
                rendered_list.append(obj)
        return rendered_list


def _add_annotation(objs: List[Dict], annotation_key:str) -> List[Dict]:
    for obj in objs:
        if 'annotations' in obj:
            obj['annotations'][annotation_key] = True
        else:
            obj['annotations'] = {annotation_key: True}
    return objs