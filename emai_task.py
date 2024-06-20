from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from fastapi import HTTPException, status
from settings import *


def send_email_reminder(recipient_email, name):
    """sendgrid free trial expired"""
    
    subject = f"Birthday Reminder for {name}"
    body = f"Today is {name}'s birthday. Don't forget to wish them a happy birthday!"

    """Create a Mail object"""
    message = Mail(
        from_email='yhamid2828@gmail.com',
        to_emails=recipient_email,
        subject=subject,
        plain_text_content=body)

    try:
        sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)

        response = sg.send(message)

        """Check if email was successfully sent (status code 2xx)"""
        if not response.status_code >= 200 and response.status_code < 300:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email."
                )
        print("Email sent successfully")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Email sending failed: {e}")

