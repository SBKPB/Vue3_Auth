import resend

from config import settings

resend.api_key = settings.RESEND_API_KEY

sender_email = "no-reply@liverse.com.tw"


def send_email(receiver_email: str, otp_code: str):

    params: resend.Emails.SendParams = {
        "from": f"{sender_email}",
        "to": [f"{receiver_email}"],
        "subject": "Test Auth App OTP Code",
        "html": f"<strong>你的密碼： {otp_code}</strong>",
    }

    resend.Emails.send(params)
