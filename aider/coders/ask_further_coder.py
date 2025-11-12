from .ask_base_coder import AskBaseCoder


class AskFurtherCoder(AskBaseCoder):
    """Ask deeper questions about code without making any changes."""

    edit_format = "ask-further"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, further=True, **kwargs)
