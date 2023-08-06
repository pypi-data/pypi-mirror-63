import smtplib
import os
import io

from datetime import datetime
from contextlib import redirect_stdout, redirect_stderr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ENVIRON_VAR = ['LOG_SENDER_EMAIL_ADDRESS',
               'LOG_SENDER_EMAIL_PASSWORD',
               'LOG_RECEIVER_EMAIL_ADDRESS']


def log_function(function):
    email, password, recipient = get_email_info()
    session = authenticate_email(email, password)
    message = create_message(email, recipient)

    def log_function(*args, **kwargs):
        arguments = get_function_arguments(args, kwargs)

        # Add subject to email
        subject = f"Function '{function.__name__}' execution log"
        message['Subject'] = subject

        # Start email body text
        text = f"Function {function.__name__}({arguments}) finished its execution.\n\n"

        start_time = datetime.now()
        text += f"Start time: {start_time:%b %d %H:%M:%S}\n"

        f = io.StringIO()
        with redirect_stdout(f):
            return_value = function(*args, **kwargs)

        text_output = f.getvalue()

        text += f'Function text output:\n{text_output}' if text_output else 'No text output\n'
        text += f'Function returned: {return_value}\n' if return_value else 'No returned value\n'

        end_time = datetime.now()
        text += f"End time: {end_time:%b %d %H:%M:%S}\n"

        total = (end_time - start_time).seconds
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        text += f'\nTotal execution time: {hours:02d}:{minutes:02d}:{seconds:02d}\n'

        # Add body to email
        message.attach(MIMEText(text, 'plain'))
        body = message.as_string()

        session.sendmail(email, recipient, body)
        session.quit()

    return log_function


def get_email_info():
    for var in ENVIRON_VAR:
        yield os.environ.get(var) if os.environ.get(var) else input(f'{var}: ')


def authenticate_email(email, password):
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(email, password)

    return session


def create_message(email, recipient):
    message = MIMEMultipart()
    message['From'] = email
    message['To'] = recipient

    return message


def get_function_arguments(args, kwargs):
    args_repr = [repr(a) for a in args]
    kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
    arguments = ", ".join(args_repr + kwargs_repr)

    return arguments
