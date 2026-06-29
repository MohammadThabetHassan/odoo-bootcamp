import os
import json
import time
import logging
import re
from typing import Dict, List, Any
import anthropic

_logger = logging.getLogger(__name__)


class ClaudeBedrockService:
    """Service to interact with Claude via Amazon Bedrock"""
    
    def __init__(self, api_key: str = None, region: str = 'us-east-1'):
        """
        Initialize Claude Bedrock service
        
        Args:
            api_key: Anthropic API key (if None, uses AWS credentials)
            region: AWS region
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.region = region
        self.model = 'claude-3-5-sonnet-20241022'  # Using Sonnet; can switch to Opus
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
    def get_system_prompt(self) -> str:
        """Get comprehensive system prompt for Odoo code generation"""
        return """You are an expert Odoo developer with deep knowledge of:
- Odoo architecture and development patterns
- Python models, fields, API decorators (@api.model, @api.depends, etc.)
- XML view definitions (form, tree, kanban, search)
- Security rules and access control lists (ACL)
- Business logic implementation
- Best practices and conventions

When a user asks to create a model or feature, you should:

1. UNDERSTAND THE REQUIREMENTS:
   - Ask clarifying questions if needed
   - Identify all necessary components
   - Plan the data structure

2. GENERATE COMPLETE CODE:
   - Create Python models with proper fields
   - Add computed fields with @api.depends where applicable
   - Implement constraints with @api.constrains
   - Add onchange methods with @api.onchange
   - Create proper relationships (Many2one, One2many, Many2many)
   - Add security rules in CSV format
   - Create XML views (form, tree, kanban, search)

3. CODE STRUCTURE:
   Follow Odoo best practices:
   - Use proper field types (Char, Integer, Float, Selection, Many2one, etc.)
   - Add string and help attributes
   - Use compute methods for calculated fields
   - Store computed fields with store=True if needed
   - Add constraints with proper error messages
   - Use SQL constraints for database-level validation

4. OUTPUT FORMAT:
   Always structure your response as follows:
   
   FILES_START
   
   FILE: path/to/file.py
   TYPE: python
   ```python
   [code here]
   ```
   
   FILE: path/to/file.xml
   TYPE: xml
   ```xml
   [code here]
   ```
   
   FILE: security/ir.model.access.csv
   TYPE: csv
   ```csv
   [csv here]
   ```
   
   FILES_END
   
   EXPLANATION:
   [Brief explanation of what was created]

5. VALIDATION:
   - Ensure all Python code is syntactically correct
   - Ensure all XML is well-formed
   - Check that models and fields are properly defined
   - Verify relationships are correct
   - Ensure security rules grant appropriate access

6. SECURITY CONSIDERATIONS:
   - Never generate code that could be exploited
   - Always validate user input in methods
   - Use Odoo's built-in security mechanisms
   - Avoid raw SQL queries (use ORM)

EXAMPLE - Creating a simple Book model:

User: "Create a Book model with title, author, isbn, and publication date"

FILES_START

FILE: models/book.py
TYPE: python
```python
from odoo import models, fields, api

class Book(models.Model):
    _name = 'book.book'
    _description = 'Book'
    _order = 'name'

    name = fields.Char(
        string='Title',
        required=True,
        index=True
    )
    author = fields.Char(
        string='Author',
        required=True
    )
    isbn = fields.Char(
        string='ISBN',
        size=13
    )
    publication_date = fields.Date(
        string='Publication Date'
    )
    pages = fields.Integer(
        string='Pages'
    )
    
    _sql_constraints = [
        ('isbn_unique', 'UNIQUE(isbn)', 'ISBN must be unique!'),
    ]
```

FILE: views/book_views.xml
TYPE: xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- List View -->
    <record id="book_tree_view" model="ir.ui.view">
        <field name="name">Book List</field>
        <field name="model">book.book</field>
        <field name="arch" type="xml">
            <tree>
                <field name="name"/>
                <field name="author"/>
                <field name="isbn"/>
                <field name="publication_date"/>
            </tree>
        </field>
    </record>

    <!-- Form View -->
    <record id="book_form_view" model="ir.ui.view">
        <field name="name">Book</field>
        <field name="model">book.book</field>
        <field name="arch" type="xml">
            <form>
                <group>
                    <field name="name"/>
                    <field name="author"/>
                    <field name="isbn"/>
                    <field name="publication_date"/>
                    <field name="pages"/>
                </group>
            </form>
        </field>
    </record>
</odoo>
```

FILE: security/ir.model.access.csv
TYPE: csv
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_book_user,book.book user,model_book_book,base.group_user,1,1,1,1
access_book_manager,book.book manager,model_book_book,base.group_system,1,1,1,1
```

FILES_END

EXPLANATION:
Created a Book model with title, author, ISBN and publication date fields. 
Added a unique constraint on ISBN to prevent duplicates.
Created form, tree and search views for data management.
Set up proper security rules.

Remember: Generate COMPLETE, WORKING code that follows Odoo conventions."""

    def generate_code(self, task_description: str, context: Dict = None) -> Dict[str, Any]:
        """
        Generate code using Claude
        
        Args:
            task_description: The user's request
            context: Additional context (config, module name, etc.)
            
        Returns:
            Dictionary with response, files, tokens, etc.
        """
        start_time = time.time()
        
        try:
            # Prepare the message
            system_prompt = self.get_system_prompt()
            
            # Add context if provided
            if context:
                task_description += f"\n\nContext:\n{json.dumps(context, indent=2)}"
            
            # Call Claude
            _logger.info(f"Calling Claude with task: {task_description[:100]}...")
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": task_description
                    }
                ]
            )
            
            # Extract response
            claude_response = response.content[0].text
            
            # Parse files from response
            files = self._parse_files_from_response(claude_response)
            
            # Calculate execution time and tokens
            execution_time = time.time() - start_time
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            
            return {
                'response': claude_response,
                'files': files,
                'tokens': tokens_used,
                'execution_time': execution_time,
                'log': f"Successfully generated {len(files)} files using {tokens_used} tokens"
            }
            
        except Exception as e:
            _logger.error(f"Claude API error: {str(e)}")
            raise Exception(f"Claude API error: {str(e)}")
    
    def _parse_files_from_response(self, response: str) -> List[Dict[str, str]]:
        """
        Parse FILE blocks from Claude response
        
        Expected format:
        FILE: path/to/file.py
        TYPE: python
        ```python
        [content]
        ```
        """
        files = []
        
        # Extract content between FILES_START and FILES_END
        if 'FILES_START' in response and 'FILES_END' in response:
            files_section = response[
                response.find('FILES_START') + len('FILES_START'):
                response.find('FILES_END')
            ]
        else:
            files_section = response
        
        # Find all FILE blocks
        file_pattern = r'FILE:\s*([^\n]+)\n\s*TYPE:\s*([^\n]+)\n\s*```[a-z]*\n(.*?)\n\s*```'
        matches = re.finditer(file_pattern, files_section, re.DOTALL)
        
        for match in matches:
            filename = match.group(1).strip()
            file_type = match.group(2).strip()
            content = match.group(3).strip()
            
            files.append({
                'filename': filename,
                'type': file_type,
                'content': content,
            })
        
        return files


class OdooClaudeService:
    """Odoo Model Service for Claude integration"""
    
    @staticmethod
    def generate_code_for_task(task_obj) -> Dict[str, Any]:
        """
        Generate code for an Odoo AI task
        
        Args:
            task_obj: ai.task model instance
            
        Returns:
            Dictionary with response, files, tokens, execution time
        """
        # Get API key from config
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise Exception('ANTHROPIC_API_KEY environment variable not set')
        
        # Create service
        service = ClaudeBedrockService(api_key=api_key)
        
        # Prepare context
        context = {
            'module_name': task_obj.name.lower().replace(' ', '_'),
            'task_type': task_obj.task_type,
            'description': task_obj.task_description,
        }
        
        # Generate code
        result = service.generate_code(
            task_description=task_obj.task_description,
            context=context
        )
        
        return result
