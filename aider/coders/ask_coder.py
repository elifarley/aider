from .ask_base_coder import AskBaseCoder


class AskCoder(AskBaseCoder):
    """Ask questions about code without making any changes."""

    edit_format = "ask"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, further=False, **kwargs)
