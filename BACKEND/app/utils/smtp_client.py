import aiosmtplib
from email.message import EmailMessage

async def send_email(sender_email: str, recipient_email: str, subject: str, body: str):
    """

    :param sender_email:
    :param recipient_email:
    :param subject:
    :param body:
    :return:
    """
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        await aiosmtplib.send(
            msg,
            hostname='smtp.mrtexpert.ru',
            port=587,
            username="<EMAIL>", ##
            password="<PASSWORD>", ##
            use_tls=False,
            start_tls=True
        )
        return {"status": "success", "message": "Email sent!"}

    except Exception as e:
        return {"status": "failed", "message": str(e)}
