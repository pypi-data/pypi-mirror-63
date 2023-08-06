import smtplib
import os
import io

from datetime import datetime
from contextlib import redirect_stdout
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
        subject = "Function '{}' execution log".format(function.__name__)
        message['Subject'] = subject

        # Start email body text
        text = "Function {}({}) finished its execution.\n\n".format(
            function.__name__, arguments)

        start_time = datetime.now()
        text += "Start time: {0:%b %d %H:%M:%S}\n".format(start_time)

        f = io.StringIO()
        with redirect_stdout(f):
            return_value = function(*args, **kwargs)

        text_output = f.getvalue()

        text += 'Function text output:\n{}'.format(
            text_output) if text_output else 'No text output\n'
        text += 'Function returned: {}\n'.format(
            return_value) if return_value else 'No returned value\n'

        end_time = datetime.now()
        text += "End time: {0:%b %d %H:%M:%S}\n".format(end_time)

        total = (end_time - start_time).seconds
        hours, remainder = divmod(total, 3600)
        minutes, seconds = divmod(remainder, 60)
        text += '\nTotal execution time: {0:02d}:{1:02d}:{2:02d}\n'.format(
            hours, minutes, seconds)

        # Add body to email
        message.attach(MIMEText(text, 'plain'))
        body = message.as_string()

        session.sendmail(email, recipient, body)
        session.quit()

    return log_function


def get_email_info():
    for var in ENVIRON_VAR:
        yield os.environ.get(var) if os.environ.get(var) else input('{}: '.format(var))


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
    kwargs_repr = ["{0}={1!r}".format(k, v) for k, v in kwargs.items()]
    arguments = ", ".join(args_repr + kwargs_repr)

    return arguments
