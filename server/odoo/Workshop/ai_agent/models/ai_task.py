from odoo import models, fields, api, exceptions
from odoo.tools import format_date
import json
import logging

_logger = logging.getLogger(__name__)


class AITask(models.Model):
    """Store AI agent tasks and their results"""
    _name = 'ai.task'
    _description = 'AI Task'
    _order = 'create_date DESC'

    name = fields.Char(
        string='Task Name',
        required=True,
        help='Brief description of what to create'
    )
    
    task_description = fields.Text(
        string='Task Description',
        required=True,
        help='Detailed description of the module/feature to generate'
    )
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('error', 'Error'),
        ('archived', 'Archived'),
    ], default='draft', string='Status')
    
    task_type = fields.Selection([
        ('model', 'Create Model'),
        ('module', 'Create Module'),
        ('view', 'Create View'),
        ('controller', 'Create Controller'),
        ('feature', 'Add Feature'),
        ('fix', 'Fix Issue'),
    ], default='module', string='Task Type')
    
    claude_response = fields.Text(
        string='Claude Response',
        readonly=True,
        help='Raw response from Claude'
    )
    
    generated_code = fields.Text(
        string='Generated Code',
        readonly=True,
        help='Parsed and formatted generated code'
    )
    
    execution_log = fields.Text(
        string='Execution Log',
        readonly=True,
        help='Log of code execution and errors'
    )
    
    generated_file_ids = fields.One2many(
        'ai.generated.file',
        'task_id',
        string='Generated Files',
        readonly=True
    )
    
    module_generated = fields.Char(
        string='Generated Module Name',
        readonly=True,
        help='Name of the generated/created module'
    )
    
    created_user_id = fields.Many2one(
        'res.users',
        string='Created By',
        readonly=True,
        default=lambda self: self.env.user
    )
    
    progress = fields.Integer(
        string='Progress %',
        default=0,
        readonly=True
    )
    
    error_message = fields.Text(
        string='Error Message',
        readonly=True
    )
    
    tokens_used = fields.Integer(
        string='Tokens Used',
        readonly=True,
        help='Total tokens consumed by Claude'
    )
    
    execution_time = fields.Float(
        string='Execution Time (seconds)',
        readonly=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to log task creation"""
        for vals in vals_list:
            if 'create_uid' not in vals:
                vals['create_uid'] = self.env.user.id
        return super().create(vals_list)

    def action_execute_task(self):
        """Execute the AI task"""
        self.ensure_one()
        self.status = 'processing'
        self.progress = 10
        
        try:
            # Get Claude response
            claude_service = self.env['ai.claude.service']
            result = claude_service.generate_code(self)
            
            self.claude_response = result.get('response', '')
            self.generated_code = result.get('code', '')
            self.tokens_used = result.get('tokens', 0)
            self.execution_time = result.get('execution_time', 0)
            
            self.progress = 50
            
            # Create generated files
            if result.get('files'):
                for file_info in result['files']:
                    self.env['ai.generated.file'].create({
                        'task_id': self.id,
                        'filename': file_info.get('filename'),
                        'file_type': file_info.get('type'),
                        'content': file_info.get('content'),
                    })
            
            self.progress = 75
            
            # Log execution
            self.execution_log = result.get('log', '')
            
            self.status = 'completed'
            self.progress = 100
            
        except Exception as e:
            self.status = 'error'
            self.error_message = str(e)
            self.progress = 100
            _logger.error(f'AI Task {self.id} failed: {str(e)}')
            raise exceptions.UserError(f'Task execution failed: {str(e)}')

    def action_install_module(self):
        """Install generated module"""
        self.ensure_one()
        if not self.module_generated:
            raise exceptions.UserError('No module has been generated yet')
        
        try:
            # Install module
            module = self.env['ir.module.module'].search(
                [('name', '=', self.module_generated)]
            )
            if module:
                module.button_install()
                self.env['ir.model'].clear_caches()
                return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }
            else:
                raise exceptions.UserError(
                    f'Module {self.module_generated} not found'
                )
        except Exception as e:
            raise exceptions.UserError(f'Installation failed: {str(e)}')

    def action_view_generated_files(self):
        """View generated files"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Generated Files',
            'res_model': 'ai.generated.file',
            'domain': [('task_id', '=', self.id)],
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('ai_agent.ai_generated_file_tree_view').id, 'tree'),
                (self.env.ref('ai_agent.ai_generated_file_form_view').id, 'form'),
            ],
        }


class AIGeneratedFile(models.Model):
    """Store generated code files"""
    _name = 'ai.generated.file'
    _description = 'Generated File'
    _order = 'create_date DESC'

    task_id = fields.Many2one(
        'ai.task',
        string='Task',
        required=True,
        ondelete='cascade'
    )
    
    filename = fields.Char(
        string='Filename',
        required=True
    )
    
    file_type = fields.Selection([
        ('python', 'Python'),
        ('xml', 'XML'),
        ('csv', 'CSV'),
        ('json', 'JSON'),
        ('js', 'JavaScript'),
        ('css', 'CSS'),
        ('html', 'HTML'),
    ], string='File Type')
    
    content = fields.Text(
        string='Content',
        required=True
    )
    
    status = fields.Selection([
        ('generated', 'Generated'),
        ('validated', 'Validated'),
        ('installed', 'Installed'),
        ('error', 'Error'),
    ], default='generated', string='Status')
    
    validation_result = fields.Text(
        string='Validation Result',
        readonly=True
    )


class AIPromptTemplate(models.Model):
    """Store system prompts for different task types"""
    _name = 'ai.prompt.template'
    _description = 'Prompt Template'
    _order = 'name'

    name = fields.Char(
        string='Template Name',
        required=True,
        unique=True
    )
    
    prompt_type = fields.Selection([
        ('system', 'System Prompt'),
        ('example', 'Example'),
        ('instruction', 'Instruction'),
        ('validation', 'Validation'),
    ], string='Prompt Type')
    
    content = fields.Text(
        string='Content',
        required=True
    )
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    description = fields.Text(
        string='Description'
    )
