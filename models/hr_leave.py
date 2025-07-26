from odoo import models, api#type: ignore

class HrLeave(models.Model):
    """
    This class inherits from hr.leave to add a custom email trigger
    for the second level of approval.
    """
    _inherit = 'hr.leave'

    def write(self, vals):
        records_to_notify = self.env['hr.leave']
        if 'state' in vals and vals['state'] == 'validate1':
            records_to_notify = self.filtered(lambda r: r.state == 'confirm')
        result = super(HrLeave, self).write(vals)
        if records_to_notify:
            print("Sending email notification for second level approval")
            template = self.env.ref('email_trigger.email_template_time_off', raise_if_not_found=False)
            print("Template found:", template)
            if template:
                print("Sending email to HR for records:", records_to_notify)
                for record in records_to_notify:
                    print("Sending email for record ID:", record.id)
                    template.sudo().send_mail(record.id, force_send=True)
                    print("Email sent for record ID:", record.id)
        return result
    

