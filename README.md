# 📧 Email Automation Script

This project is a simple yet powerful email automation tool that allows you to send personalized emails to multiple recipients using a `.csv` file. With minimal setup, you can send emails quickly and efficiently.

---

## 📂 Project Overview

### Files in the Repository:
1. **`emails.csv`**: Contains recipient details (Name, Email, Title, Company, etc.).
2. **`.env`**: Stores sensitive information and configuration variables.
3. **`requirements.txt`**: Lists all Python dependencies required for the project.
4. **`send_email.py`**: The main script to automate email sending.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
Use the following command to clone the repository:
```bash
git clone <repository_url>
cd <repository_directory>

python -m venv source
source source/bin/activate   # Mac/Linux
source\Scripts\activate      # Windows

pip install -r requirements.txt


SENDER_EMAIL=YOUR_EMAIL_ADDRESS
APP_PASSWORD=YOUR_APP_PASSWORD
CSV_FILE_PATH=emails.csv
RESUME_FILE_PATH=YOUR_RESUME_PATH.pdf

Ensure your emails.csv file follows this format:

Serial No.,Name,Email,Title,Company
1, Reciever Name, receiver_mail_add@xyz.com, Designation_of_reciever, Company_of_receiver

Each row represents a recipient, and columns should match the script's requirements:

Serial No.: A unique identifier for each recipient.
Name: The recipient's full name.
Email: The recipient's email address.
Title: Their job title.
Company: The organization they are associated with.


Before running the script, edit the send_email.py file to customize the message template. Below is a generic template you can use as a starting point:

message = f"""
Subject: Exciting Opportunity at {company_name}

Dear {name},

I hope this message finds you well. My name is XYZ, and I’m the CTO at {company_name}. We are working on some exciting projects, and I believe your expertise aligns perfectly with our goals.

If you are interested, please feel free to reach out for further discussions. You can find more about me and my work in the attached resume.

Looking forward to connecting!

Best regards,
XYZ
CTO, XYZ
Email: xyz@outlook.com
"""

🚀 Running the Project
Ensure the virtual environment is activated:

source source/bin/activate   # Mac/Linux
source\Scripts\activate      # Windows

Run the script:

For Python 2.x:
python send_email.py

For Python 3.x:
python3 send_email.py

Notes
App Password: Make sure to generate an app-specific password for your email account (e.g., from Google for Gmail) instead of using your account password.
Email Template: Review and test the email template to ensure it conveys the intended message.
Attachments: Add your resume or other files via the RESUME_FILE_PATH variable in the .env file.

Sample Output
The script will process each recipient in emails.csv and send an email to their respective email address. Logs or print statements (if implemented in send_email.py) will confirm successful delivery or highlight any issues.

🛠️ Troubleshooting
Environment Variables: Ensure all variables in the .env file are correct.
CSV File Format: Verify the emails.csv format matches the expected structure.
Dependencies: Use the requirements.txt to ensure all libraries are installed properly.




