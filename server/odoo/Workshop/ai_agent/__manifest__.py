{
    'name': 'AI Agent - Odoo Module Generator',
    'version': '1.0.0',
    'category': 'Tools',
    'summary': 'AI-powered module and code generator using Claude 3 Opus',
    'description': '''
        An intelligent AI agent that can generate, create, and manage Odoo modules
        based on natural language descriptions. Uses Claude 3 Opus via Amazon Bedrock.
        
        Features:
        - Natural language task processing
        - Automatic Odoo model generation
        - View and security configuration
        - Code validation and execution
        - Real-time streaming responses
        - Generated module installation
    ''',
    'author': 'Mohammad Thabet',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/prompt_templates.xml',
        'views/ai_task_views.xml',
        'views/ai_menu.xml',
    ],
    'static': {
        'description': 'Static assets'
    },
    'installable': True,
    'application': True,
    'external_dependencies': {
        'python': [
            'anthropic',
            'boto3',
        ],
    },
}
