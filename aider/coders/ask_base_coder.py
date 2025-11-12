from .folder_coder import AiderFolderCoder
from ..prompts import ask_system
from ..utils import is_image_file
import re


class AskBaseCoder(AiderFolderCoder):
    """Base for ask modes: questions about code without making any changes."""

    def __init__(self, *args, further=False, **kwargs):
        super().__init__(*args, **kwargs)

    def get_edits(self, mode="update"):
        # Always return no edits—prevent parsing
        return []

    def apply_updates(self):
        # Parse response for suggestions but don't apply
        edited = set()  # No actual edits
        try:
            # Still call base to generate/parse response, but skip apply
            edits = self.get_edits()  # Empty
            # Simulate dry-run: output suggestions if LLM provided (e.g., hypothetical diff)
            if self.partial_response_content:
                # Extract potential suggestions (e.g., look for diff-like blocks)
                suggestions = self.extract_suggestions(self.partial_response_content)
                if suggestions:
                    self.io.tool_output("Hypothetical suggestions (not applied):\n" + suggestions)
                else:
                    self.io.tool_output("Discussion complete.")
            self.add_assistant_reply_to_cur_messages()  # Log response
        except Exception as err:
            self.io.tool_error(f"Error in ask mode: {str(err)}")
            self.reflected_message = str(err)
        return edited  # Empty set—no mutations

    def auto_commit(self, edited, context=None):
        # No-op: No commits in ask mode
        if edited:
            self.io.tool_output("No commits in ask mode.")
        return None

    def lint_edited(self, fnames):
        # Skip linting—no edits
        return None

    def run_shell_commands(self):
        # Optionally allow safe shell (e.g., for info), but skip if risky
        if self.suggest_shell_commands:
            return super().run_shell_commands()
        return ""  # Safer: no shell in pure ask

    def extract_suggestions(self, content):
        # Simple parser: Look for diff/code blocks and format as suggestions
        # Customize based on edit_format (e.g., unified diff regex)
        diff_pattern = re.compile(r'---\s+\w+[\s\S]*?\+\+\+', re.MULTILINE)
        matches = diff_pattern.findall(content)
        if matches:
            return "\n".join(matches)  # Or format nicely
        # Also check for code blocks
        code_pattern = re.compile(r'```[\s\S]*?```', re.MULTILINE)
        code_matches = code_pattern.findall(content)
        if code_matches:
            return "\n".join(code_matches)
        return content  # Fallback: whole response as discussion
