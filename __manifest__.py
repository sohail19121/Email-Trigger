# in sale_recommendations/__manifest__.py
{
    'name': 'Email Trigger (Custom)',
    'version': '18.0',
    'summary': 'Send email notification to HR when Manager approves ',
    'author': 'Cloud Science Labs',
    'category': 'Email For HR',
    'depends': ['hr_holidays','hr_attendance','remote_work','mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/email_template.xml',
       
    ],
    'installable': True,
    'application': True,
}