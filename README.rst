BeepBeep |travis| |coveralls|
==================

.. |travis| image:: https://travis-ci.org/MFranceschi6/BeepBeepPrimer.svg?branch=master 
    :target: https://travis-ci.org/MFranceschi6/BeepBeepPrimer 
.. |coveralls| image:: https://coveralls.io/repos/github/MFranceschi6/BeepBeepPrimer/badge.svg?branch=master
     :target: https://coveralls.io/github/MFranceschi6/BeepBeepPrimer?branch=master

How to run the app
-------------------

ATTENTION : statistics won't work on Chrome or Safari, but seriously, who still use them ?

For this application to work, you need to create a Strava API application
see https://strava.github.io/api/#access and https://www.strava.com/settings/api

Once you have an application, you will have a "Client Id" and "Client Secret".
You need to export them as environment variables::

    export STRAVA_CLIENT_ID=<ID>
    export STRAVA_CLIENT_SECRET=<SECRET>

    export WEBSITE_NAME="Butter BeepBeep"
    export GROUP_NAME="Butter Group"

    export MAIL_GMAIL_USER=<GMAIL_EMAIL>
    export MAIL_GMAIL_PASS=<GMAIL_PASSWORD>
    export MAIL_REPORT_SUBJECT="Report"
    export MAIL_MESSAGE_NO_RUN="You did not run in this period!"

Note:
Google is not allowing you to log in via smtplib because it has flagged this
sort of login as "less secure", so you have to allow the access. To do so,
click on this link: https://www.google.com/settings/security/lesssecureapps

It is a good idea to create a file (and add it to .gitignore) that contains both commands. You can 
then run it via::

    source <filename>.sh

As usual, to start the app run::

    $ pip install -r requirements.txt
    $ python setup.py develop

You can then run your application with::

    $ python monolith/app.py
    * Running on http://127.0.0.1:5000/

How to create a new user
------------------------

1. Connect to Strava with the new user's account
2. Browse http://127.0.0.1:5000/create_user and insert data.
3. Login by browsing http://127.0.0.1:5000/
4. Click on "Authorize Strava Access" -- this will perform an OAuth trip to Strava.

Once authorized, you will be able to see your last 10 runs.
But for this, we need to ask the Celery worker to fetch them.

How to run the Celery worker
----------------------------

Make sure you have a redis server running locally on port 6379 by running::

    $ redis-server
    $ redis-cli
    $ 127.0.0.1:6379> ping
        PONG

Then, open another shell and run::

    $ celery worker -A monolith.background -E -l info

This will run a celery microservice that can fetch runs.
To invoke it, visit http://127.0.0.1:5000/fetch.

Once the runs are retrieved, you should see your last ten runs
on http://127.0.0.1:5000



