import random
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from EmailConfiguration.models import ToEmail, Setting, OTPModel
from website.models import CompanyInfo  # Import the CompanyInfo model
import smtplib

def process():
    try:
        # Fetch email settings from the Setting model
        setting = Setting.objects.get()
        sender_email = setting.email
        email_password = setting.password
        smtp_host = setting.host
        smtp_port = setting.port
    except ObjectDoesNotExist:
        print("No email settings found. Please configure the email settings.")
        return

    # Fetch the company name from the CompanyInfo model
    try:
        company_info = CompanyInfo.objects.first()  # Assuming there's only one entry
        company_name = company_info.name if company_info else "Ruban "  # Default name if not found
    except ObjectDoesNotExist:
        print("No company information found. Default name will be used.")
        company_name = "Ruban"

    # Get all active recipients from the ToEmail model
    active_recipients = ToEmail.objects.filter(active_status=True)

    if not active_recipients.exists():
        print("No active recipients found.")
        return

    # Connect to the SMTP server
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()  # Use TLS
        server.login(sender_email, email_password)

        # Loop through all active recipients to generate and send OTPs
        for recipient in active_recipients:
            receiver_email = recipient.email
            subject = f"Your One-Time Password (OTP) - {company_name}"
            
            # Generate a 4-digit OTP
            otp_code = random.randint(1000, 9999)  # 4-digit OTP
            
            # Calculate the expiration time (2 minutes from now)
            expiration_time = timezone.now() + timedelta(minutes=2)

            # Check if an OTP already exists for this email
            otp_entry, created = OTPModel.objects.update_or_create(
                email=receiver_email,
                defaults={'otp': otp_code, 'expires_at': expiration_time}
            )

           # Construct the email body with OTP and expiration info
            body_otp = f"""
            <html>
            <body style="color: black;">
                <h2 style="color: black;">{company_name}</h2>
                <p>Dear {recipient.name},</p>
                <p>Your One-Time Password (OTP) is:</p>
                <div class="otp" style="font-size: 24px; font-weight: bold; color: black; border: 2px dashed black; padding: 10px; display: inline-block; margin: 10px 0;">{otp_code}</div>
                <p>Don't share this OTP with anyone.</p>
                <p>This OTP will expire in 2 minutes, so please use it promptly.</p>
                <p>With heartfelt gratitude, we thank you!</p>
                <div class="footer" style="margin-top: 20px; font-size: 14px; color: black;">
                    Best regards,<br>{company_name} Team
                </div>
            </body>
            </html>
            """


            # Create the email message
            msg = MIMEMultipart('alternative')
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body_otp, 'html'))

            try:
                # Send the email
                text = msg.as_string()
                server.sendmail(sender_email, receiver_email, text)
                print(f"OTP email sent successfully to {receiver_email}!")

            except Exception as e:
                print(f"Error sending OTP email to {receiver_email}: {e}")

    finally:
        # Quit the server connection
        server.quit()

    print("OTP generation and email sending process completed for all active recipients.")
