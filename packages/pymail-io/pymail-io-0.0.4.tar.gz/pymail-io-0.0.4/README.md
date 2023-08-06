![PyPI](https://img.shields.io/pypi/v/pymail-io)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymail-io)
![Read the Docs (version)](https://img.shields.io/readthedocs/pymail-io/en/latest)

![PyMailIO](assets/pymail_io.png)

 An Asynchronous mail server that's built on CPython's AsyncIO library.
 
Read the docs: [Documentation](https://pymail-io.readthedocs.io/en/latest/)


```bash
pip install pymail-io

# Install & run Redis
docker run redis
```

#### Quick Start


Run PyMailIO as a complete emailing solution:

```python
from pymail_io.pymailio_task import Task

p = Task(
    password="wizard",
    receiver_email="joe@blogs.com", # Or a list of emails receiver_email=["joe@blogs.com", ...],
    sender_email="your_email@gmail.com",
    email_host="smtp.gmail.com",
)
# if you are running PyMailIO within the life time of a long running process, such as
# a web framework of rest API, then set `run_forever=True` as this will yield much
# better performances.
```
Create your email subject & body
```python
r = p.send_email(
    subject="The subject...",
    body="The email body...",
)

```

The response from calling `p.send_email`:
```python
"""

{
    "metadata": { # metadata... },
        "email": {
            "subject": subject,
            "body": body,
            "email_init": # time that PyMailIO sent your email,
    }
}
"""
```

To get the results of the email from the store, pass the metadata
to `get_email_response`. For example:
```python
# r is the return value from calling p.send_email (see above)
r = p.send_email(
    subject="The subject...",
    body="The email body...",
)

email_meta = p.get_email_response(r)

```
There are 2 datetime values that reference when PyMailIO executed the `send_email`
method & also when the email was actually sent from the background queue:
The `datetime_exec` method will give you the datetime value that PyMailIO executed
the `send_email` method.
For example:
```python
r = p.send_email(
    subject="The subject...",
    body="The email body...",
)

self.datetime_exec()

```

There are 2 datetime values that reference when PyMailIO executed the `send_email`
method & also when the email was actually sent from the background queue:
The `exec_time` method will give you the datetime value that PyMailIO's **queue** executed
the `send_email` method.
For example:

```python
r = p.send_email(
    subject="The subject...",
    body="The email body...",
)

# Some time in the future...
r = get_email_response(r)
time_email_sent = self.exec_time(r)

```


To update the task queue & store settings, you can pass in extra values as kwargs to
the `Task` class. For example:

```python

p = Task(
   password="wizard",
   receiver_email="joe@blogs.com",  # Or a list of emails receiver_email=["joe@blogs.com", ...],
   sender_email="your_email@gmail.com",
   email_host="smtp.gmail.com",

   # extra settings:
    store_port=6379,
    store_host="localhost",
    db=0,
    workers=1,
)

```
## Built With

* [PyTaskIO](https://github.com/joegasewicz/pytask_io) - Asynchronous Tasks Library using asyncio


## Authors

* **Joe Gasewicz** - *Initial work* - [JoeGasewicz](https://github.com/joegasewicz/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

This library is based on & influenced by [flask-mail](https://github.com/mattupstate/flask-mail).