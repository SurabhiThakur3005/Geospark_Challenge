# Python Challenge - Use Celery to Offload an Expensive Task

### The Challenge

1. Pull this branch
2. Create your virtual env and ```pip install``` the requirements (Flask and Celery)
3. The app let's your enter a banner URL, a comma separated list of emails and optional message.
4. The _emails_users simulates some processing time by sleeping 1 second - in real life this could be an intentional short pause so as to not hit a server or API too often. For the end users though, the page just appears slow and could result in them navigating away while the emailing is still taking place!

The challenge to add some asynchronous processing so the user can keep navigating the site.

You need to offload the emailing to a Celery task so the user does not have to wait for it to end or to prevent an impatient user from navigating away? Change the Flask app as you want, it's just some bootstrap code to get started. You could also add an option to the form to send the card at a later date

Set up a [message broker](http://docs.celeryproject.org/en/latest/getting-started/brokers/) of your choice and [start playing with Celery](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html). For a Flask + Celery basic example check [here](http://flask.pocoo.org/docs/0.12/patterns/celery/).

### Bonus

Bonus points if you can display progress of the emailing on the page. Secondly try to deploy it to a cloud service provider and make the emailing work. You could try [Heroku + Sendgrid](https://devcenter.heroku.com/articles/sendgrid) for example.
