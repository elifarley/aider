import re
from pathlib import Path
from typing import Dict, Any

from .base_coder import Coder
from .base_prompts import CoderPrompts

class PromptTemplate:
    """Loads and validates prompt templates from .prompt files"""
    
    def __init__(self, template_file: Path):
        self.template_file = template_file
        self.template = self._load_template()
        
    def _load_template(self) -> Dict[str, str]:
        """Load and parse the template file using XML-style tags"""
        try:
            with open(self.template_file) as f:
                content = f.read()
            
            # Remove comments (lines starting with #)
            lines = content.splitlines()
            filtered_lines = []
            for line in lines:
                stripped = line.lstrip()
                if not stripped.startswith('#'):
                    filtered_lines.append(line)
            content = '\n'.join(filtered_lines)
            
            template = {}
            pattern = r'<(\w+)>(.*?)</\1>'
            matches = re.finditer(pattern, content, re.DOTALL)
            
            for match in matches:
                key = match.group(1)
                value = match.group(2).strip()
                template[key] = value
                
            return template
                
        except Exception as e:
            raise ValueError(f"Failed to load template file {self.template_file}: {str(e)}")
            
    def create_prompts(self) -> CoderPrompts:
        """Create a CoderPrompts instance from the template"""
        prompts = CoderPrompts()
        
        # Map template fields directly to CoderPrompts attributes
        for field, value in self.template.items():
            if hasattr(prompts, field):
                setattr(prompts, field, value)
                
        return prompts

class TemplatedPromptCoder(Coder):
    """A coder that loads prompts from a JSON template file"""
    
    def __init__(self, *args, template_file: str = None, **kwargs):
        super().__init__(*args, **kwargs)

        if not template_file:
            raise ValueError("template_file is required for TemplatedPromptCoder")
            
        template = PromptTemplate(Path(template_file))
        self.gpt_prompts = template.create_prompts()
