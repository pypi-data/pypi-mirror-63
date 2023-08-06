# Email Function Logger

A Python decorator to easily log information about a function and send it to your email.

## Installation

```bash
$ pip install email-function-logger
```

## Email setup

You can set the email information as environment variables on your machine. To do this, add the following lines to `~/.bashrc` (or `~/.bash_profile` depending on your OS).

```bash
export LOG_SENDER_EMAIL_ADDRESS="example_sender@gmail.com"
export LOG_SENDER_EMAIL_PASSWORD="password"
export LOG_RECEIVER_EMAIL_ADDRESS="example_receiver@gmail.com"
```

This step is optional since you can input the information during the function runtime.

## Example of use

```python
from email_function_logger import log_function

@log_function
def mult(x, y):
    # Function text output
    print(x)
    print(y)

    # Value returned by function
    return x * y

mult(9, 7)
```

The log sent by email will look like this:

```
Subject:
Function 'mult' execution log

Body:
Function mult(9, 7) finished its execution.

Start time: Mar 16 18:32:16
Function text output:
9
7
Function returned: 63
End time: Mar 16 18:32:16

Total execution time: 00:00:00
```

## Supported versions

- Python 3.6 and above

## Lincense

- MIT License

## Links

- PyPI: https://pypi.org/project/email-function-logger/
- GitHub: https://github.com/arthurcerveira/Email-Function-Logger
