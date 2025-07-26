from odoo import models, fields, api#type: ignore
import logging

_logger = logging.getLogger(__name__)

class HrAttendence(models.Model):
    _inherit = 'request.attendence'

    def write(self, vals):
        records_to_notify = self.env['request.attendence']
        if 'state' in vals and vals['state'] == 'manager_approval':
            records_to_notify = self.filtered(lambda r: r.state == 'draft')

        result = super(HrAttendence, self).write(vals)

        if records_to_notify:
            
            all_leave_types = self.env['hr.leave.type'].search([('responsible_ids', '!=', False)])
            responsible_users = all_leave_types.mapped('responsible_ids')
            recipient_emails_list = responsible_users.mapped('employee_ids.work_email')
                
              
            valid_emails = [
                    email.strip().replace("'", "").replace('"', "")
                    for email in recipient_emails_list
                    if isinstance(email, str) and '@' in email
                ]   
            if not valid_emails:
                print("No responsible user emails found. Skipping email notification.")
                return result
            recipient_emails = ",".join(valid_emails)
            print(f"Recipients for notification: {recipient_emails}")
            print("Condition met. Preparing to send email for records: %s", records_to_notify.ids)
            
            print("Condition met. Preparing to send email for records: %s", records_to_notify.ids)
            template = self.env.ref('email_trigger.email_template_attendence_request', raise_if_not_found=False)
            
            if not template:
                print("Email template 'email_trigger.email_template_attendence_request' not found.")
                return result
            print("Template found: %s", template.name)
            email_values = {'email_to': recipient_emails}
            print("Email values prepared:", email_values)
            
            print("Template found: %s", template.name)
            for record in records_to_notify:
                try:
                    print("Attempting to send email for record ID: %s", record.id)
                    template.sudo().send_mail(record.id, force_send=True, email_values=email_values)
                    print("Successfully processed send_mail for record ID: %s. Email is in queue or sent.", record.id)
                except Exception as e:
                    print("FAILED to send email for record ID %s. ERROR: %s", record.id, e)
        
        return result