import smtplib

import aiosmtplib
from email.message import EmailMessage
from cfg import cfg

async def send_email(recipient_email: str, subject: str, body: str):
    """

    :param sender_email:
    :param recipient_email:
    :param subject:
    :param body:
    :return:
    """
    msg = EmailMessage()
    msg['From'] = cfg.email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.set_content(body)

    try:

        await aiosmtplib.send(
            msg,
            hostname=cfg.smtp_address,
            port=cfg.smtp_port,
            username=cfg.user, ##
            password=cfg.password, ##
            use_tls=False,
            start_tls=True
        )
        return {"status": "success", "message": "Email sent!"}

    except Exception as e:
        print(str(e))
        return {"status": "failed", "message": str(e)}
