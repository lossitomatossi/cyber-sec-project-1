LINK: https://github.com/lossitomatossi/cyber-sec-project-1
Installed according to [MOOC instructions](https://cybersecuritybase.mooc.fi/installation-guide)
Dependencies can be installed with the command

```bash
python3 -m pip install django "selenium<4" "urllib3<2" beautifulsoup4 requests
```

and then you can run the program with the command

```bash
python manage.py runserver
```

For testing, the following users already exist in the app
`id  username   password    session_token`
10  user	user	user
9	admin	admin	admin

The admin panel is open in /admin with the username admin and password admin.

Both the admin and the user have pets associated to the accounts. The relevant pages are /flaws/id/pets

FLAW : A3:2017-Sensitive Data Exposure

Source: [flaws/models.py](flaws\models.py)
The flaw is that passwords are stored in plaintext, which violates the Sensitive Data Exposure by not protecting the data at rest or in transit.

How to fix: Instead of creating a user as a basic model, we can use "AbstractUser" from "django.contrib.auth.models" as seen on [line XXX](github.com) or to create a hashing function ourselves as seen on [line YYY](github.com). We should also hash the password before submitting it either manually or with djangos "from django.contrib.auth.hashers import make_password". When comparing the submitted password to the one in the database, we should compare the hash values to each other, with for example "check_password" from the same django module.

FLAW: A2:2017-Broken Authentication
We are persisting user session as a plaintext value in the database and storing it for the user as cookie called "session_token" in their browser. If a user finds out the session_token of another user, they can impersonate that user. The user can also change this cookie value as they wish in their browser, and the cookie only expires clientside, not server side.

How to fix: Use djangos authenticate and login functions to abstract session management and login functionality.


FLAW A6:2017-Security Misconfiguration:

Since the website was created with django, there is an admin panel that was not disabled. The admin panel can be accessed by anyone with access to the website, and since the admin uses these as their identifiers:
username: admin
email: admin@example.com
password: admin

It is reasonable that a user would attempt to login as "admin; admin", in which case they would get access to everything.

How to fix: Firstly, never use a superuser account such as admin with the password admin. At minimum, the password should be a randomly generated one, and preferrably tied to some central authentication backend. Also, for a live server, we would disable the django admin backend from (mysite\urls.py) or at least limit access to it behind a firewall. We should not document the admin credentials in plaintext in the README.md either...

FLAW 1: A1:2017-Injection
[exact source link pinpointing flaw 1...](https://owasp.org/www-project-top-ten/2017/A1_2017-Injection)

how to fix it...

FLAW 2:
exact source link pinpointing flaw 2...
description of flaw 2...
how to fix it...

...

FLAW 5:
exact source link pinpointing flaw 5...
description of flaw 5...
how to fix it...