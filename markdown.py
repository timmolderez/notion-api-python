from mistletoe import BaseRenderer


class NotionPyRenderer(BaseRenderer):
    def render(self, token):
        """
        Takes a single Markdown token and renders it down to
        NotionPy classes. Note that all the recursion is handled in the delegated
        methods.
        Overrides super().render but still uses render_map and then just
        does special parsing for stuff
        """
        return self.render_map[token.__class__.__name__](token)
