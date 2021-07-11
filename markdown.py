import logging
from typing import Dict, List

from mistletoe import BaseRenderer


class NotionBlockRenderer(BaseRenderer):

    def __init__(self):
        self.block_type = None
        super().__init__()

    def render_paragraph(self, token) -> Dict:
        return _create_block('paragraph', {"text": self.render_inner(token)})

    def render_heading(self, token) -> Dict:
        level = token.level
        if level > 3:
            level = 3
            logging.warning("Heading levels > 3 are not supported by "
                            "Notion; falling back to level 3.")

        return _create_block(f'heading_{level}',
                             {'text': self.render_inner(token)})

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
        logging.warning('Image links are not yet supported by the Notion API;'
                        'falling back to a plain link.')
        return {'type': 'url', 'url': token.src}

    def render_link(self, token) -> List[Dict]:
        inner_objs = self.render_inner(token)
        for inner_obj in inner_objs:
            inner_obj['href'] = token.target
        return inner_objs

    def render_auto_link(self, token) -> Dict:
        return {'type': 'url', 'url': token.src}

    def render_list(self, token) -> Dict:
        current_block_type = self.block_type
        self.block_type = ('numbered_list_item' if token.start
                           else 'bulleted_list_item')
        rendered = self.render_inner(token)
        self.block_type = current_block_type
        return rendered

    def render_list_item(self, token) -> Dict:
        inner = self.render_inner(token)
        nested_items = [x for x in inner if x['type'] != 'paragraph']
        paragraphs = [x for x in inner if x['type'] == 'paragraph']
        text_items = []
        for paragraph in paragraphs:
            for text_obj in paragraph['paragraph']['text']:
                text_items.append(text_obj)

        return _create_block(self.block_type,
                             {'text': text_items, 'children': nested_items})

    def render_quote(self, token) -> List[Dict]:
        logging.warning('Quotes are not yet supported by the Notion API;'
                        'falling back to a paragraph block.')
        return self.render_paragraph(token)

    def render_block_code(self, token) -> Dict:
        logging.warning('Code blocks are not yet supported by the Notion API;'
                        'falling back to a paragraph block.')
        return self.render_paragraph(token)

    def render_thematic_break(self, token) -> List[Dict]:
        logging.warning('Thematic breaks are not yet supported by the Notion '
                        'API; ignorning.')
        return []

    def render_line_break(self, token) -> Dict:
        return self.render_paragraph(token)

    def render_table(self, token) -> List[Dict]:
        logging.warning('Tables are not yet supported by the Notion API; '
                        'ignoring.')
        return []

    def render_table_row(self, token) -> List[Dict]:
        return []

    def render_table_cell(self, token) -> List[Dict]:
        return []

    def render_document(self, token) -> List[Dict]:
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


def _add_annotation(objs: List[Dict], annotation_key: str) -> List[Dict]:
    """
    Adds an annotation to a list of rich text objects
    (https://developers.notion.com/reference/rich-text)
    """
    for obj in objs:
        if 'annotations' in obj:
            obj['annotations'][annotation_key] = True
        else:
            obj['annotations'] = {annotation_key: True}
    return objs


def _create_block(block_type: str, body: Dict) -> Dict:
    return {
        "object": "block",
        "type": block_type,
        block_type: body
    }