# Odoo AI Agent Module

A powerful AI-powered code generator for Odoo that leverages Claude 3 to automatically create Odoo modules, models, views, and complete features from natural language descriptions.

## Features

- **Natural Language Processing**: Describe what you want in plain English
- **Complete Code Generation**: Models, Views, Security Rules, Controllers
- **Claude 3 Integration**: Uses Claude 3 Sonnet/Opus via Amazon Bedrock
- **Real-time Streaming**: Watch responses stream in real-time
- **File Management**: Generated files tracked and stored
- **Module Installation**: Direct installation from the interface
- **Validation**: Automatic syntax and logic validation
- **History**: Keep track of all generated code and tasks

## Installation

### Prerequisites

```bash
# Install required Python packages
pip install anthropic boto3
```

### Setup

1. **Get AWS Credentials** (for Amazon Bedrock Claude access):
   - Visit: https://aws.amazon.com/bedrock/
   - Create AWS account if needed
   - Generate Access Key ID and Secret Access Key

2. **Get Anthropic API Key** (Alternative to Bedrock):
   - Visit: https://console.anthropic.com/
   - Create account and get API key

3. **Set Environment Variables**:
   ```bash
   # Windows (PowerShell)
   $env:ANTHROPIC_API_KEY = "your-api-key-here"
   
   # Linux/Mac
   export ANTHROPIC_API_KEY="your-api-key-here"
   
   # Or use .env file in Odoo config directory
   ```

4. **Install Module in Odoo**:
   - Go to Apps → Update Apps List
   - Search for "AI Agent"
   - Click Install

## Usage

### Basic Workflow

1. **Navigate to AI Agent** → Dashboard
2. **Click Create** to add new task
3. **Fill in details**:
   - Task Name: Brief description (e.g., "Real Estate Management")
   - Task Type: What to create (Model, Module, Feature, etc.)
   - Task Description: Detailed requirements
4. **Click Execute Task** button
5. **Monitor Progress** - Watch real-time generation
6. **Review Generated Files** - Check what was created
7. **Install Module** - Deploy to Odoo

### Example Tasks

#### 1. Create a Real Estate Model
```
Task Type: Create Module
Description: 
"Create a complete real estate module with:
- Property model with fields: name, description, address, price, bedrooms, bathrooms
- Property Type model (apartment, house, land)
- Agent model to assign to properties
- Add form, tree, kanban, and search views
- Set up security rules for users and managers"
```

#### 2. Add a Feature to Existing Module
```
Task Type: Add Feature
Description:
"Add a 'Favorites' feature to the real estate module where users can:
- Mark properties as favorites
- See favorite count on property list
- Filter properties by favorite status
- Add a favorites model to track user preferences"
```

#### 3. Create an API Controller
```
Task Type: Create Controller
Description:
"Create a REST API controller for the real estate module with endpoints:
- GET /api/properties - List all properties
- GET /api/properties/{id} - Get single property
- POST /api/properties - Create new property
- PUT /api/properties/{id} - Update property
- DELETE /api/properties/{id} - Delete property"
```

## Architecture

### Models

**ai.task**
- Stores task descriptions and results
- Tracks execution status and progress
- Links to generated files
- Records token usage and execution time

**ai.generated.file**
- Stores individual generated code files
- File type tracking (Python, XML, CSV, etc.)
- Validation status
- Links back to source task

**ai.prompt.template**
- Reusable prompt templates
- System prompts for different task types
- Few-shot examples
- Validation rules

### Services

**claude_service.py**
- Handles Claude API calls
- Prompt engineering
- Response parsing
- File extraction from responses

### Views

- **List View (Tree)**: Browse all tasks
- **Kanban View**: Visual task status board
- **Form View**: Detailed task management
- **Search View**: Filter and find tasks

## Prompt Engineering

The module includes a sophisticated system prompt that:

1. **Teaches Claude about Odoo**:
   - Model architecture and field types
   - API decorators (@api.depends, @api.onchange, etc.)
   - Security and access control
   - View types (form, tree, kanban, search)

2. **Enforces Best Practices**:
   - Proper naming conventions
   - Security validation
   - Code quality standards
   - Error handling

3. **Provides Examples**:
   - Sample models with relationships
   - Complete view definitions
   - Security rule examples
   - Common patterns and tricks

## File Format

Claude responses should follow this format:

```
FILES_START

FILE: models/book.py
TYPE: python
```python
# Python code here
```

FILE: views/book_views.xml
TYPE: xml
```xml
<!-- XML code here -->
```

FILE: security/ir.model.access.csv
TYPE: csv
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
```

FILES_END

EXPLANATION:
Brief explanation of what was generated.
```

## Advanced Features

### Token Tracking
- Monitor token usage per task
- Track costs and optimize queries
- Historical token usage analytics

### Code Validation
- Syntax validation for Python files
- XML well-formedness checks
- Field reference validation
- Security rule verification

### Streaming Responses
- Real-time response viewing
- Partial file rendering
- Progress tracking

### History & Logs
- Complete audit trail
- Error logs and debugging
- Execution timings
- User activity tracking

## Configuration

### Environment Variables

```bash
# Anthropic API Key
ANTHROPIC_API_KEY=sk-...

# AWS Credentials (if using Bedrock)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1

# Claude Model Selection
CLAUDE_MODEL=claude-3-5-sonnet-20241022
# Options: claude-3-sonnet, claude-3-opus
```

### Odoo Configuration

Add to your Odoo config file:

```ini
[ai_agent]
# API key for Claude
anthropic_api_key = your-api-key
# Model to use (sonnet or opus)
claude_model = claude-3-5-sonnet-20241022
# Max tokens per request
max_tokens = 4096
# Temperature (0-1, lower = more deterministic)
temperature = 0.7
# Enable sandbox execution
sandbox_mode = True
```

## Security Considerations

⚠️ **Important Security Notes**:

1. **Code Validation**: Always review generated code before installation
2. **Sandbox Mode**: Enable sandbox execution for untrusted code
3. **API Keys**: Never commit API keys to version control
4. **Permissions**: Only admin users should access AI Agent
5. **Code Review**: Implement code review workflow before deployment
6. **SQL Injection**: Generated code must use ORM, not raw SQL
7. **Access Control**: Validate all database access in generated code

## Troubleshooting

### "API Key not found"
```
Solution: Set ANTHROPIC_API_KEY environment variable
export ANTHROPIC_API_KEY="your-key-here"
```

### "Module not found after generation"
```
Solution: Refresh module list in Odoo
Settings → Technical → Modules → Update Apps List
```

### "Generated code has syntax errors"
```
Solution: Re-run task with better description or request fixes
Example: "Fix the Python syntax errors in the previous model"
```

### "Claude response incomplete"
```
Solution: Increase max_tokens in configuration
Generated code may have been truncated
```

### "Permission denied when installing"
```
Solution: Ensure you're logged in as admin user
AI Agent requires system permissions to install modules
```

## Workflow Tips & Tricks

### 1. Clear, Detailed Descriptions
❌ Bad: "Create a model"
✅ Good: "Create a Book model with title, author, ISBN, publication date, and genre. Include form and tree views."

### 2. Specify Relationships
❌ Bad: "Create products"
✅ Good: "Create Product model with Many2one relationship to Category, One2many to ProductVariant"

### 3. Security Requirements
Always mention who should access what:
- "Users can view all products"
- "Only managers can delete"
- "Admins have full access"

### 4. Business Logic
Describe validation rules:
- "Price must be positive"
- "Stock quantity must be integer"
- "Title is required"

### 5. UI Requirements
Specify views needed:
- "Add kanban view grouped by status"
- "Create search filters for date range"
- "Show progress bar for completion"

## Examples

### Example 1: E-commerce Module
```
Name: E-Commerce System
Type: Create Module
Description:
Create a complete e-commerce module with:
- Product model: name, description, price, sku, quantity, category
- Category model: name, icon
- Order model: customer, products, total, status
- OrderLine model: product, quantity, price
- Include workflows: draft → confirmed → shipped → delivered
- Add notifications on status change
- Implement discount system for bulk orders
```

### Example 2: CRM Feature
```
Name: Add CRM Notes Feature
Type: Add Feature
Description:
Add a note-taking system to CRM module:
- Notes model linked to customers
- Rich text editor for content
- Attachments support
- Sharing with team members
- Auto-save every 30 seconds
- Version history of notes
```

### Example 3: REST API
```
Name: Product API
Type: Create Controller
Description:
Create REST API for product management:
- GET /api/v1/products - list with pagination
- GET /api/v1/products/{id} - single product
- POST /api/v1/products - create
- PUT /api/v1/products/{id} - update
- DELETE /api/v1/products/{id} - delete
- Authentication via API tokens
- Rate limiting: 100 requests/minute
```

## Best Practices

1. **Start Simple**: Begin with basic models, add complexity gradually
2. **Review First**: Always review generated code before installing
3. **Test Locally**: Test in development before production
4. **Version Control**: Commit generated modules to git
5. **Documentation**: Add comments to customize generated code
6. **Iterative Refinement**: Ask Claude to improve code incrementally

## Common Pitfalls

❌ **Don't**:
- Request overly complex functionality in one task
- Use vague descriptions
- Skip code review before installation
- Ignore security warnings
- Assume generated code is production-ready

✅ **Do**:
- Break complex tasks into smaller ones
- Be specific and detailed
- Review and test code
- Add error handling
- Test on development first

## API Reference

### Task Model

```python
# Create a new task
task = env['ai.task'].create({
    'name': 'Real Estate Module',
    'task_type': 'module',
    'task_description': 'Create a complete real estate management system...',
})

# Execute task
task.action_execute_task()

# Get results
print(task.claude_response)
print(task.generated_code)
print(task.execution_log)

# View generated files
for file in task.generated_file_ids:
    print(f"{file.filename}: {file.content}")
```

### Claude Service

```python
from odoo.addons.ai_agent.services.claude_service import ClaudeBedrockService

service = ClaudeBedrockService(api_key='sk-...')
result = service.generate_code(
    task_description='Create a Book model',
    context={'module_name': 'book_module'}
)

print(result['response'])  # Full Claude response
print(result['files'])     # Extracted files
print(result['tokens'])    # Token count
print(result['execution_time'])  # Time taken
```

## Support

For issues or feature requests:
1. Check this documentation
2. Review troubleshooting section
3. Check Odoo logs for detailed errors
4. Contact module developer

## License

This module is part of the Odoo Bootcamp Project.
Author: Mohammad Thabet

## Changelog

### v1.0.0 (2026-06-29)
- Initial release
- Claude 3 integration via Amazon Bedrock
- Complete model, view, controller generation
- Real-time streaming responses
- File management and installation
- Security configuration
- Comprehensive documentation
