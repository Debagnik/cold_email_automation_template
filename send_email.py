import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication  # For attachments
import os
from html import escape
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")
RESUME_FILE_PATH = os.getenv("RESUME_FILE_PATH")
LINKED_IN_URL = 'https://www.linkedin.com/in/debdaru-dasgupta-a64323197/'
GITHUB_URL = 'https://github.com/Debdaru07?tab=repositories'


def send_email(sender_email, password, recipient_email, name, company):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Inquiry Regarding Mobile Application Developer Positions at {company}"

        message = f"""
            Subject: Exciting Opportunity from {company}

            Dear {name},

            I hope this email finds you well. My name is XYZ_ABC, and I am the CTO of {company}. I came across your profile and was truly impressed by your accomplishments.

            We are currently working on innovative projects at {company}, and I believe your skills and expertise could be a perfect match for our team. If you're interested in learning more, please find my resume attached for additional context.

            Feel free to reach out if you have any questions or would like to discuss this opportunity further.

            Looking forward to hearing from you!

            Best regards,
            XYZ_ABC  
            CTO, {company}
            Email: XYZ_ABC@gmail.com
            """


        msg.attach(MIMEText(message, 'html'))

        if os.path.exists(RESUME_FILE_PATH):
            with open(RESUME_FILE_PATH, 'rb') as attachment:  # Open in binary mode
                part = MIMEApplication(attachment.read(), _subtype="pdf")
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(RESUME_FILE_PATH)}"'
                msg.attach(part)
        else:
            print(f"Warning: Resume file not found at {RESUME_FILE_PATH}")


        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")


def process_csv_and_send_emails(csv_file_path, sender_email, password):
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['Name']
                email = row['Email']
                company = row['Company']
                send_email(sender_email, password, escape(email), escape(name), escape(company))
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
    except Exception as e:
        print(f"An error occurred while processing the CSV: {e}")

process_csv_and_send_emails(CSV_FILE_PATH, SENDER_EMAIL, APP_PASSWORD)
