from odoo import models, fields, api#type: ignore
import logging


_logger = logging.getLogger(__name__)

class HrWorkFromHome(models.Model):
    """
    This class inherits from 'remote.work.request' to add custom logic.
    The goal is to send an email notification when a request's status is
    updated to 'approved'.
    """
    _inherit = 'remote.work.request'

    def write(self, vals):
      
       
        result = super(HrWorkFromHome, self).write(vals)

      
        if 'status' in vals and vals['status'] == 'approved':
            
            records_to_notify = self

            _logger.info("Condition met for second approval notification. Records: %s", records_to_notify.ids)
            try:
                all_leave_types = self.env['hr.leave.type'].search([('responsible_ids', '!=', False)])
                responsible_users = all_leave_types.mapped('responsible_ids')
                
                recipient_emails_list = responsible_users.mapped('employee_ids.work_email')
                
              
                valid_emails = [
                    email.strip().replace("'", "").replace('"', "")
                    for email in recipient_emails_list
                    if isinstance(email, str) and '@' in email
                ]
                
                if not valid_emails:
                    _logger.warning("Work from home notification: No valid recipient emails found for responsible users.")
                    return result

                recipient_emails_str = ",".join(valid_emails)
                _logger.info("Notification will be sent to: %s", recipient_emails_str)

            except Exception as e:
                _logger.error("Failed to gather recipient emails for WFH notification: %s", e)
                return result

            template = self.env.ref('email_trigger.email_template_work_from_home', raise_if_not_found=False)
            
            if not template:
                _logger.error("Email template 'email_trigger.email_template_work_from_home' not found. Cannot send notification.")
                return result

            _logger.info("Using email template: '%s'", template.name)
            
 
            email_values = {'email_to': recipient_emails_str}

            for record in records_to_notify:
                try:
                    template.sudo().send_mail(
                        record.id,
                        force_send=True,
                        email_values=email_values
                    )
                    _logger.info("Successfully queued email for Remote Work Request ID: %s", record.id)
                except Exception as e:
                    _logger.error("Failed to send notification email for Remote Work Request ID %s. Error: %s", record.id, e)
        
        return result
