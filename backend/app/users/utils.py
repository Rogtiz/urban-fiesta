import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from app.config import settings

SMTP_SERVER = settings.SMTP_SERVER
SMTP_PORT = settings.SMTP_PORT
SMTP_USER = settings.SMTP_USER
SMTP_PASSWORD = settings.SMTP_PASSWORD

SENDER_NAME = settings.SENDER_NAME


def send_verification_email(to_email: str, token: str):
    msg = EmailMessage()
    msg["Subject"] = "Подтверждение Email адреса"
    msg["From"] = formataddr((SENDER_NAME, SMTP_USER))
    msg["To"] = to_email

    verification_link = f"http://localhost:5173/verify-email?token={token}"
    msg.set_content(f"Пожалуйста, подтвердите ваш Email, перейдя по ссылке: {verification_link}")
    msg.add_alternative(f"""
    <html>
      <head>
        <style>
          body {{
            font-family: Arial, sans-serif;
            background-color: #f6f9fc;
            padding: 20px;
            color: #333;
          }}
          .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
          }}
          .button {{
            display: inline-block;
            padding: 12px 24px;
            margin-top: 20px;
            background-color: #a2a2a8;
            color: #ffffff;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
          }}
          .footer {{
            margin-top: 30px;
            font-size: 12px;
            color: #888;
            text-align: center;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h2>Подтверждение Email</h2>
          <p>Здравствуйте!</p>
          <p>Вы зарегистрировались в <strong>SyncDevs</strong>. Чтобы подтвердить свой адрес электронной почты, нажмите на кнопку ниже:</p>
          <a href="{verification_link}" class="button">Подтвердить Email</a>
          <p>Если вы не создавали аккаунт, просто проигнорируйте это письмо.</p>
          <div class="footer">
            &copy; 2025 YourAppName. Все права защищены.
          </div>
        </div>
      </body>
    </html>
    """, subtype="html")


    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)


# send_verification_email("carterthe1337@gmail.com", "shfueohfsfoihes545sef488s4ef")