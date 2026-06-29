# AI Agent Module - Setup Guide

## Quick Start (5 minutes)

### Step 1: Get API Key

Choose one option:

**Option A: Using Anthropic API (Recommended)**
1. Go to https://console.anthropic.com/
2. Sign up for free account
3. Create API key
4. Copy the key

**Option B: Using AWS Bedrock (Advanced)**
1. Create AWS account
2. Enable Claude in Amazon Bedrock
3. Get AWS Access Key ID and Secret Access Key

### Step 2: Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY = "sk-your-key-here"
# Verify it's set
echo $env:ANTHROPIC_API_KEY
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-your-key-here
echo %ANTHROPIC_API_KEY%
```

**Linux/Mac:**
```bash
export ANTHROPIC_API_KEY="sk-your-key-here"
echo $ANTHROPIC_API_KEY
```

**Permanent (Add to .env or config):**
```
ANTHROPIC_API_KEY=sk-your-key-here
```

### Step 3: Install Module in Odoo

1. Copy ai_agent folder to: `server/odoo/Workshop/ai_agent`
2. Restart Odoo server
3. Go to Apps → Update Apps List (click button)
4. Search for "AI Agent"
5. Click Install

### Step 4: First Task

1. Go to **AI Agent** → **Dashboard**
2. Click **Create** button
3. Fill in:
   - **Task Name:** "Test Real Estate"
   - **Task Type:** Create Module
   - **Task Description:** Create a simple real estate module with Property model having name, price, and address fields
4. Click **Execute Task**
5. Wait for Claude to respond (30-60 seconds)
6. Review generated files
7. Click **View Generated Files** to see code

## Installation Issues?

### Issue: "Module not found"
```
Solution:
1. Make sure ai_agent folder exists in: server/odoo/Workshop/ai_agent
2. Restart Odoo server
3. Go to Apps → Update Apps List
4. Search again
```

### Issue: "API Key error"
```
Check:
1. ANTHROPIC_API_KEY environment variable is set
   echo $env:ANTHROPIC_API_KEY (PowerShell)
2. API key is valid (starts with sk-)
3. Try restarting Odoo server
```

### Issue: "Permission denied"
```
Solution:
1. Log in as admin user
2. Go to Settings → Users to verify admin role
3. Try again
```

### Issue: "anthropic module not found"
```
Solution: Install Python dependencies
pip install anthropic boto3
Then restart Odoo server
```

## Using the AI Agent

### Create Your First Module

1. Go to **AI Agent** → **Dashboard**
2. Click **+ Create**
3. Fill form:

```
Task Name: My First Module
Task Type: Create Module
Description: Create a Book module with:
- Book model: title, author, isbn, pages, publication_date
- BookCategory model: name, description
- Book to Category relationship (Many2one)
- Add form and tree views
- Setup access control for users and managers
```

4. Click **Execute Task**
5. Watch the progress bar
6. Claude will generate complete code

### Review Generated Files

After execution:
1. Scroll down to **Generated Files** tab
2. Click on each file to view code
3. Check for any errors in **Execution Log** tab
4. Review the **Claude Response** to see all details

### Install Generated Module

If code looks good:
1. Click **Action** button → **Install Module**
2. Wait for installation to complete
3. New module will appear in Apps list
4. Go to that module and start using it!

## Tips for Better Results

### 1. Be Specific
❌ "Create a model"
✅ "Create a Customer model with name, email, phone, address fields and form/tree views"

### 2. Include Relationships
❌ "Create products and categories"
✅ "Create Product model with Many2one to Category. Add form, tree, and search views."

### 3. Mention Security
✅ "Users can view all. Only managers can edit. Only admins can delete."

### 4. Describe Business Logic
✅ "Add validation: price must be > 0, email must be valid"

### 5. Ask for Specific Views
✅ "Add kanban view grouped by status and search filters for date range"

## Example Tasks

### Example 1: Simple Model
```
Task Name: Customer Module
Task Type: Create Module
Description:
Create a Customer management module with:
- Customer model: name (required), email, phone, address, city, country
- Add form view with all fields
- Add tree view with name, email, phone, city
- Add search view to filter by city and country
- Setup ACL: users can view and edit, managers can delete
```

### Example 2: With Relationships
```
Task Name: Order System
Task Type: Create Module
Description:
Create an Order management module with:
- Customer model (link to built-in res.partner)
- Order model: name, customer, order_date, total_amount
- OrderLine model: order, product, quantity, unit_price (Many2one to sale.product)
- Implement order status workflow: draft → confirmed → delivered
- Add notifications when status changes
- Include form and tree views
- Setup manager-only permissions for deletion
```

### Example 3: Advanced Feature
```
Task Name: Inventory Tracking
Task Type: Add Feature
Description:
Add inventory management to product module:
- Track stock quantities per warehouse
- Add reorder level alerts
- Implement stock history (log all movements)
- Create reports showing low stock items
- Add automated email when stock < reorder level
- Include dashboard showing inventory summary
```

## Common Claude Responses

### If Claude asks questions:
Reply with clarifications:
- "Yes, use Many2one for customer relationship"
- "Include all three view types"
- "Make email field required and unique"

### If Claude provides partial code:
Click "Execute Task" again or ask for:
- "Complete the missing field definitions"
- "Add the XML views for this model"
- "Include security configuration"

### If generated code has errors:
Ask Claude to fix it:
- "Fix the Python syntax errors"
- "The XML has invalid tags, please correct"
- "Add the missing imports"

## Next Steps

After first successful module:

1. **Explore other task types:**
   - Create Model
   - Create View
   - Create Controller
   - Add Feature
   - Fix Issue

2. **Try complex modules:**
   - CRM system
   - E-commerce
   - Project management
   - Inventory

3. **Customize generated code:**
   - Add custom business logic
   - Enhance security
   - Optimize performance

4. **Share your modules:**
   - Commit to git
   - Document your code
   - Create pull requests

## Troubleshooting Detailed

### Claude takes too long
- Normal: 30-90 seconds for complex modules
- Very long (>3 min): May timeout, try simpler task

### Generated code won't install
- Check **Execution Log** tab for error details
- Review **Claude Response** to understand the code
- Ask Claude to fix specific issues

### Module installed but doesn't work
- Check Odoo server logs: `tail -f logs/odoo.log`
- Verify dependencies are installed
- Try clicking "Update Apps List" again

### Out of API quota
- Check Anthropic dashboard: console.anthropic.com
- May need to upgrade to paid account
- Try with smaller tasks to reduce token usage

## Advanced Configuration

### Adjust Claude Model (in claude_service.py)

```python
# Change line ~30 in services/claude_service.py
self.model = 'claude-3-opus-20240229'  # Faster
# or
self.model = 'claude-3-sonnet-20240229'  # Cheaper
```

### Increase max tokens

```python
# In services/claude_service.py line ~150
response = self.client.messages.create(
    model=self.model,
    max_tokens=8000,  # Increased from 4096
    ...
)
```

### Custom system prompt

Edit **prompts/odoo_system.txt** to customize Claude's behavior.

## Prompt Engineering Guide

The system prompt teaches Claude about Odoo. It includes:

1. **Knowledge sections:**
   - Odoo architecture
   - Model field types
   - API decorators
   - View types
   - Security rules

2. **Examples:**
   - Complete model example
   - View definitions
   - Security rules
   - Best practices

3. **Format instructions:**
   - How to structure responses
   - File format expectations
   - Code style guidelines

## Real-world Workflows

### Workflow 1: MVP Development
1. Create core module with AI Agent
2. Test and review generated code
3. Customize and enhance
4. Add business logic
5. Deploy to production

### Workflow 2: Feature Addition
1. Ask AI Agent to add feature
2. Merge generated code with existing
3. Test integration
4. Deploy

### Workflow 3: Rapid Prototyping
1. Generate multiple module versions
2. Compare different approaches
3. Pick best implementation
4. Polish and optimize

## What's Generated

### Python Files (models/)
- Model classes with fields
- Relationships (Many2one, One2many, Many2many)
- Computed fields with @api.depends
- Methods and constraints
- Business logic

### XML Files (views/)
- Form views (detailed entry screens)
- Tree views (list views)
- Kanban views (visual boards)
- Search views (filters)

### Security Files (security/)
- ir.model.access.csv (ACL)
- ir.rule.xml (record rules)
- Access control policies

## Support & Help

If stuck:
1. Check README.md in module folder
2. Review troubleshooting section above
3. Check Claude response for clues
4. Try simpler task first
5. Check Odoo logs

## Success Indicators

✅ Module installs without errors
✅ Models appear in database
✅ Views render correctly
✅ Can create and edit records
✅ Search and filtering work
✅ Security rules enforce access
✅ No error messages in logs

## Next Advanced Topics

After mastering basics:
- Custom widgets
- Server actions and automations
- Wizards and workflows
- Reports and PDFs
- Email templates
- External API integration

Ready to start? Go to AI Agent → Dashboard and create your first task!
