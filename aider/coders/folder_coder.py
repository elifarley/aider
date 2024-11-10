from pathlib import Path
from typing import Type

from pylibtypes import create_named_subclass, load_class_attrs_from_folder, FolderBasedAttrsError
from cedarscript_integration_aider import prompt_folder_path
import re
from .base_prompts import CoderPrompts
from .base_coder import Coder


class FolderCoder(Coder):
    """A coder that loads prompts from a folder"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gpt_prompts = self._create_coder_prompts_subclass(self.edit_format)

    @staticmethod
    def _create_coder_prompts_subclass(coder_name: str) -> Type[CoderPrompts]:
        """Creates a folder-based subclass of CoderPrompts"""
        coder_prompts_subclass: Type[CoderPrompts] = create_named_subclass(CoderPrompts, coder_name)
        coder_path: Path = prompt_folder_path(coder_name)
        load_class_attrs_from_folder(coder_path, coder_prompts_subclass, FolderCoder.parse_banterml_pairs)
        return coder_prompts_subclass

    @staticmethod
    def parse_banterml_pairs(content: str) -> list[dict[str, str]]:
        messages = []
        user_pattern = r'<banterml:role.user>(.*?)</banterml:role.user>'
        assistant_pattern = r'<banterml:role.assistant>(.*?)</banterml:role.assistant>'

        users = re.findall(user_pattern, content, re.DOTALL)
        assistants = re.findall(assistant_pattern, content, re.DOTALL)

        if len(users) != len(assistants):
            raise ValueError(
                f"Mismatched number of user {len(users)} and assistant {len(assistants)} messages"
            )

        for user, assistant in zip(users, assistants):
            messages.append({"role": "user", "content": user.strip()})
            messages.append({"role": "assistant", "content": assistant.strip()})

        return messages
