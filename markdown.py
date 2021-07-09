import logging
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

    def render_heading(self, token) -> Dict:
        level = token.level
        if level > 3:
            level = 3
            logging.warning("Heading levels > 3 are not supported by the "
                            "Notion API; falling back to level 3.")

        block = {
            "object": "block",
            "type": f'heading_{level}',
            f'heading_{level}': {
                'text': self.render_inner(token)
            }
        }
        return block

    def render_strong(self, token) -> List[Dict]:
        inner_objs = self.render_inner(token)
        return _add_annotation(inner_objs, 'bold')

    def render_emphasis(self, token):
        inner_objs = self.render_inner(token)
        return _add_annotation(inner_objs, 'italic')

    def render_strikethrough(self, token) -> List[Dict]:
        inner_objs = self.render_inner(token)
        return _add_annotation(inner_objs, 'strikethrough')

    def render_inline_code(self, token) -> List[Dict]:
        inner_objs = self.render_inner(token)
        return _add_annotation(inner_objs, 'code')

    def render_image(self, token) -> Dict:
        logging.warning(f'Found an image link in Markdown text. ({token.src})\n'
                        'These are currently not supported by the Notion API;'
                        'replacing with a plain link.')
        return {'type': 'url', 'url': token.src}

    def render_link(self, token) -> List[Dict]:
        inner_objs = self.render_inner(token)
        for inner_obj in inner_objs:
            inner_obj['href'] = token.target
        return inner_objs

    def render_auto_link(self, token) -> Dict:
        return {'type': 'url', 'url': token.src}

    def render_list_item(self, token) -> Dict:
        return self.render_paragraph(token)

    def render_quote(self, token):
        logging.warning('Quotes are not yet supported by the Notion API.')
        return self.render_inner(token)


    def render_raw_text(self, token) -> Dict:
        """
        Default render method for RawText. Simply return token.content.
        """
        obj = {"type": "text",
               "text": {"content": token.content}}
        return obj

    def render_escape_sequence(self, token):
        return self.render_inner(token)

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