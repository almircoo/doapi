import resend
from django.conf import settings
from django.template.loader import render_to_string


def send_email(to_email, subject, template_name, context=None):
    """
    Send an email using Resend API
    """
    if context is None:
        context = {}
    
    # Initialize Resend API
    resend.api_key = settings.RESEND_API_KEY
    
    # Render the email template
    html_content = render_to_string(template_name, context)
    
    # Send the email
    params = {
        "from": settings.DEFAULT_FROM_EMAIL,
        "to": to_email,
        "subject": subject,
        "html": html_content,
    }
    
    try:
        response = resend.Emails.send(params)
        return response
    except Exception as e:
        # Log the error
        print(f"Error sending email: {e}")
        return None
