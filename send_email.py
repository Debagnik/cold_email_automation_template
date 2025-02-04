import smtplib
import csv
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from chat import generateMessage
from html import escape
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")
RESUME_FILE_PATH = os.getenv("RESUME_FILE_PATH")
LINKED_IN_URL = os.getenv("LINKED_IN_URL", 'https://www.linkedin.com/in/debdaru-dasgupta-a64323197/')
GITHUB_URL = os.getenv("GITHUB_URL", 'https://github.com/Debdaru07?tab=repositories')


def send_email(sender_email, password, recipient_email, name, company, role, specificRole):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Inquiry Regarding Positions at {company}"

        ai_data = {
            'recutersName': name,
            'role': role,
            'specificRole': specificRole,
            'company': company,
            'yoe': os.getenv("YOE"),
            'domain': os.getenv("DOMAIN"),
            'myExpertise': os.getenv("EXPERTISE"),
            'skillset1': os.getenv("SKILL_1"),
            'describeSkillSet1': os.getenv("DESC_SKILL_1"),
            'skillset2': os.getenv("SKILL_2"),
            'describeSkillSet2': os.getenv("DESC_SKILL_2"),
            'skillset3': os.getenv("SKILL_3"),
            'describeSkillSet3': os.getenv("DESC_SKILL_3"),
            'LINKED_IN_URL': LINKED_IN_URL,
            'GITHUB_URL': GITHUB_URL,
            'myName': os.getenv("MY_NAME"),
            'myEmail': os.getenv("MY_EMAIL"),
            'myWebsiteLink': os.getenv("MY_WEBSITE"),
            'host': os.getenv("OLLAMA_URI"),
            'model': os.getenv("AI_MODEL_NAME")
        }

        ai_prompt = '<body><p>Dear {recutersName},</p><p>I am writing to inquire about the {role} positions, specifically for {specificRole}, at {company}. I have over {yoe} of experience in this domain and I am highly proficient in {domain}.</p><p>My expertise includes {myExpertise}. I am confident I can quickly integrate into your team and contribute effectively.</p><p>In parallel with {myExpertise} focus, I have also broadened my skillset to include:</p><ul><li>{skillset1}: {describeSkillSet1}</li><li>{skillset2}: {describeSkillSet2}</li><li>{skillset3}: {describeSkillSet3}</li></ul><p>I am eager to learn and adapt to new technologies and believe my diverse skill set makes me a versatile candidate.</p><p>You may find more about my professional background on <a href=\"{LINKED_IN_URL}\">LinkedIn</a> and view my projects on <a href=\"{GITHUB_URL}\">GitHub</a>.</p><p>My resume, which provides further details about my qualifications and experience, is attached. Thank you for your time and consideration. I look forward to hearing from you soon.</p><p>Sincerely,</p><p>{myName}</p><p>Email:{myEmail}</p>Website: <a href=\"{myWebsiteLink}\">{myWebsiteLink}</a></body>'

        message = generateMessage(ai_data, ai_prompt)

        msg.attach(MIMEText(message, 'html'))

        if os.path.exists(RESUME_FILE_PATH):
            with open(RESUME_FILE_PATH, 'rb') as attachment:  # Open in binary mode
                part = MIMEApplication(attachment.read(), _subtype="pdf")
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(RESUME_FILE_PATH)}"'
                msg.attach(part)
        else:
            print(f"Warning: Resume file not found at {RESUME_FILE_PATH}")

        # Send the email
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
            tasks = []
            for row in reader:
                name = row['Name']
                email = row['Email']
                company = row['Company']
                role = row['Role']
                specific_role = row['SpecificRole']

                # Schedule sending emails asynchronously
                send_email(sender_email, password, escape(email), escape(name), escape(company), escape(role), escape(specific_role))

    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
    except Exception as e:
        print(f"An error occurred while processing the CSV: {e}")


def main():
    process_csv_and_send_emails(CSV_FILE_PATH, SENDER_EMAIL, APP_PASSWORD)


if __name__ == "__main__":
    main()
