import requests
import smtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup

# ========== CONFIG ==========
URLS_TO_MONITOR = [
    "https://thetradingpit.com",
    "https://goatfundedtrader.com",
    "https://fundednext.com"
]

KEYWORDS = ["$0 challenge", "no upfront fee", "free evaluation", "no fee challenge"]
EMAIL_TO = "newspamfree.drainpipe273@passinbox.com"
EMAIL_FROM = "your_email@gmail.com"  # Replace with your Gmail
EMAIL_PASS = "your_app_password"     # See instructions below
# ============================

def check_sites():
    matched_urls = []
    for url in URLS_TO_MONITOR:
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text().lower()
            if any(keyword.lower() in text for keyword in KEYWORDS):
                matched_urls.append(url)
        except Exception as e:
            print(f"Error checking {url}: {e}")
    return matched_urls

def send_email(matches):
    msg = EmailMessage()
    msg["Subject"] = "🚨 Free Prop Firm Opportunity Found!"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content("The following sites may have a $0 challenge or no-upfront-fee funding:\n\n" + "\n".join(matches))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_FROM, EMAIL_PASS)
        smtp.send_message(msg)

if __name__ == "__main__":
    found = check_sites()
    if found:
        send_email(found)
