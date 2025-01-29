import smtplib
import csv
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication  # For attachments
import os
from tqdm import tqdm
from html import escape
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

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
        <html>
        <body>
        <p>Dear {name},</p>

        <p>I am writing to inquire about Mobile Application Developer positions, specifically for Flutter Developers (Android + iOS), at {company}. I have over 2 years and 6 months of experience in this domain and am highly proficient in building cross-platform mobile applications using Flutter.</p>

        <p>My expertise includes using Azure DevOps for cloud management, Git for version control, and Swagger/Postman for API interaction. I am confident I can quickly integrate into your team and contribute effectively.</p>

        <p>In parallel with my mobile development focus, I have also broadened my skillset to include:</p>
        <ul>
            <li>Frontend Web Development: Next.js, React.js, Angular, TypeScript, JavaScript</li>
            <li>Backend Development & Databases: Node.js, PostgreSQL</li>
            <li>Cloud Management: AWS (including EC2 instances and other deployment features)</li>
            <li>Containerization: Docker</li>
        </ul>

        <p>I am eager to learn and adapt to new technologies and believe my diverse skill set makes me a versatile candidate.</p>

        <p>You can find more about my professional background on <a href="{LINKED_IN_URL}">LinkedIn</a> and view my projects on <a href="{GITHUB_URL}">GitHub</a>.</p>

        <p>My resume, which provides further details about my qualifications and experience, is attached. Thank you for your time and consideration. I look forward to hearing from you soon.</p>

        <p>Sincerely,</p>

        <p>Debdaru Dasgupta</p>
        <p>Contact No :- +91 8787-588-495 </p>
        </body>
        </html>
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


def process_csv_and_send_emails(csv_file_path, sender_email, password, max_threads=10):
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = list(csv.DictReader(csvfile))
            total_emails = len(reader)
            if total_emails == 0:
                print("No email addresses found in CSV file.")
                return

            print(f"📌 Found {total_emails} email addresses. Starting email sending process...")
            start_time = time.time()

            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                futures = {
                    executor.submit(send_email, sender_email, password, escape(row['Email']), escape(row['Name']), escape(row['Company'])): row['Email']
                    for row in reader
                }
                
                for future in tqdm(as_completed(futures), total=total_emails, desc="📨 Sending Emails", unit="email"):
                    print(future.result())  # Print success/failure for each email

            end_time = time.time()
            total_time = end_time - start_time

            print(f"\n✅ All {total_emails} emails processed!")
            print(f"⏳ Total time taken: {total_time:.2f} seconds")
            print(f"📨 Average time per email: {total_time / total_emails:.2f} seconds")

    except FileNotFoundError:
        print(f"❌ Error: CSV file not found at {csv_file_path}")
    except Exception as e:
        print(f"⚠️ An error occurred while processing the CSV: {e}")

process_csv_and_send_emails(CSV_FILE_PATH, SENDER_EMAIL, APP_PASSWORD, max_threads=10)