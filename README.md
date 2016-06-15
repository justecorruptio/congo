This is the souce code backing http://con-go.net

ConGo
-----
ConGo is a new go server for massive multiplayer consultation go. There is only one game being played at a time. Each player is automatically added to either the black or the white team. Every member on each team gets to vote on the next move. The move with the most votes is chosen.

Quick Start
-----------
This is a short (untested) guide to run a development server on Ubuntu Linux.

Clone the congo repo.

    git clone https://github.com/justecorruptio/congo.git
    cd congo

Install MySQL, redis and GnuGo.

    apt-get install mysql-server redis-server gnugo

Grant a user with read-write access to MySQL.

Next, create a file called `setting_qa.py` with our database settings:

    git clone https://github.com/justecorruptio/congo.git
    cd congo
    echo 'DATABASE = {"dbn": "mysql", "db", "user": "<USER>", "pw": "PASS"}' > setting_qa.py

Execute the database schema definitions.

    cat db/schema.sql | mysql -u"<USER>"
    cat db/change_001.sql | mysql -u"<USER>"

Install python dependencies:

    pip install -r requirements.txt

To start a new game, or to advance to the next move:

    ./scripts/progress_game.sh

To start the development server. Visit `http://localhost:8080`:

    python webapp.py

Source Code Layout
------------------

- `controllers`: Meta-game logic
- `forms.py`: POST Forms
- `db`: Database schema definitions
- `models`: ORM definitions
- `requirements.txt`: python requirements
- `scripts`: helper scripts and cronjobs
- `settings*.py`: Server configuration
- `static`: CSS and JS source
- `templates`: HTML templates
- `views`: Display view definitions
- `webapp.py`: development server and WSGI entry point
