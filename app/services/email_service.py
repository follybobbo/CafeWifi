from dotenv import load_dotenv
import smtplib
import os
from flask import  jsonify


load_dotenv()

master_mail = os.environ.get("SERIALIZER_KEY")
password = os.environ.get("MASTER_EMAIL_PASSWORD")

def send_mail(verification_url, user_email):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(master_mail, password)
        connection.sendmail(master_mail, user_email, msg=f"Subject:Verify Your Email\n\nPlease verify your email here {verification_url}")

    return jsonify({"status": "sent"})



def check_if_user_can_resend_verification_email(user_id, redis_client):
    key = f"resend_verification:{user_id}"
    can_send = redis_client.exists(key)  #if key exist then user cannot send, if key does not exist, them user can send

    #if key does not exist, then set new key with timer/expiry equals 30 secs then return truw
    if not can_send:
        redis_client.set(key, 1, nx=True, ex=30)
        return True

    return False


