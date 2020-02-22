import time

from celery import Celery
from flask import render_template, request, Flask

DEFAULT_BANNER = 'https://pbs.twimg.com/media/DZsKAs9W4AAEdpO.jpg:large'
DEFAULT_GREETING = 'I wish your a Happy Easter'
MSG = '''<p>Hey {name}, {greeting}!</p>
<p>Enjoy and keep calm and code in Python!</p>
<img width="400px;" src="{banner}" alt="nice Easter banner">
'''
TIMEOUT = 1

app = Flask(__name__)
# Added by Surbhi
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

# Added by Surbhi
# The function creates a new Celery object, configures it with the broker from the application config,
# updates the rest of the Celery config from the Flask config and then creates a subclass of the task
# that wraps the task execution in an application context.o
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    #celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
celery = make_celery(app)

# Added by Surbhi
# Created a separate function to send emails.
@celery.task(name="tasks.send_email")
def send_email():
    time.sleep(TIMEOUT)

def _emails_users(emails, banner, message):
    emails_done = {}
    for email in emails:
        # just printing message, bonus challenge: make it work with Sendgrid
        name = email.split('@')[0]  # for demo purposes
        mail_body = MSG.format(name=name,
                               greeting=message or DEFAULT_GREETING,
                               banner=banner,
                               message=message)

        emails_done[email] = mail_body

        # simulate some heavy processing
        #time.sleep(TIMEOUT)
        # Added by Surbhi
        # Moved this part to send_email function
        send_emails = send_email.delay()

    return emails_done


@app.route('/', methods=['GET', 'POST'])
def login():
    banner = emails = message = emails_done = None

    if request.method == 'POST':
        banner = request.form.get('url') or DEFAULT_BANNER
        emails = [email.strip() for email in
                  request.form.get('emails').split(',')]
        message = request.form.get('message')

        emails_done = _emails_users(emails, banner, message).items()

    return render_template("index.html",
                           default_banner=DEFAULT_BANNER,
                           banner=banner or '',
                           emails=emails and ', '.join(emails) or '',
                           message=message or '',
                           emails_done=emails_done)



if __name__ == "__main__":
    app.run(debug=True)
