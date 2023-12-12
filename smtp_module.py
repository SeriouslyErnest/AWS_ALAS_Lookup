#SMTP modules here
#reads from config.json for email details
#note: update to ensure the path of config.json is correct or remove placeholders
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(email_content):
    # Load configuration from JSON file
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # Email configuration
    
    sender_email = config["gmail_username"]
    #temporary in case config.json path fails
    # sender_email = "e.projects.temp@gmail.com"
    receiver_email = config["gmail_username"]
    # receiver_email = "e.projects.temp@gmail.com"
    subject = "Updated ALAS"
    message = email_content

    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach message
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        # Login to your Gmail account
        server.login(sender_email, config["gmail_password"])
        #alternative in case config.json fails: 
        # server.login(sender_email, "lfnf gzfi xdhd sqcc")

        # Send email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Quit the server
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def main():
    send_email("hello")
    

if __name__ == "__main__":
    main()
