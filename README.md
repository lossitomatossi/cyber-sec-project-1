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
`id  username   password`
9	admin	admin
10  user	user
11	fakeadmin	admin

The admin panel is open in /admin with the username admin and password admin.

Both the admin and the user have pets associated to the accounts. The relevant pages are /flaws/id/pets

FLAW : A3:2017-Sensitive Data Exposure

Source: [flaws/models.py](flaws\models.py)
The flaw is that passwords are stored in plaintext, which violates the Sensitive Data Exposure by not protecting the data at rest or in transit. Can be seen [here](https://github.com/lossitomatossi/cyber-sec-project-1/blob/main/flaws/views.py#L28)

How to fix: Instead of creating a user as a basic model, "AbstractUser" from "django.contrib.auth.models" can be used as seen on [Line 29](https://github.com/lossitomatossi/cyber-sec-project-1/blob/main/flaws/views.py#L29) or to create a hashing function ourselves. The password should be hashed before submitting it, either with a hash or with djangos "from django.contrib.auth.hashers import make_password". When comparing the submitted password to the one in the database, the hash values should be compared to each other, with for example "check_password" from the same django module. When checking the password, the password should be hashed before sending it to the server for checks.

FLAW: A2:2017-Broken Authentication
The user session is persisted as a plaintext value in the database and stored on the browser as cookie called "session_token" in their browser. If a user finds out the session_token of another user, they can impersonate that user. The user can also change this cookie value as they wish in their browser, and the cookie only expires clientside, not server side. Can be easily checked by logging in to the django admin panel, copying the cookie of another user and then changing the cookie in the dev tools.

How to fix: Use djangos authenticate and login functions to abstract session management and login functionality, [line 64](https://github.com/lossitomatossi/cyber-sec-project-1/blob/main/flaws/views.py#L64). This also makes sure that the cookie expiration is applied serverside and not only on the clients browser, which prompts the user to login later on.

FLAW A6:2017-Security Misconfiguration:

The website was created with django, which provides an admin panel that was not disabled. The admin panel can be accessed by anyone with access to the website, and since the admin uses these as their credentials:
username: admin
email: admin@example.com
password: admin

It is reasonable that a user would attempt to login as "admin; admin", in which case they would get access to everything.

How to fix: Firstly, never use a superuser account such as admin with the password admin. At minimum, the password should be a randomly generated one, and preferrably tied to some central authentication backend. Also, for a live server, the django admin backend should be disabled by removing it from [mysite/urls.py](https://github.com/lossitomatossi/cyber-sec-project-1/blob/main/mysite/urls.py#L6) or at least limit access to it behind a firewall. The admin credentials should not be documented as plaintext in the README.md either...

A5:2017-Broken Access Control

There is a functionality where an admin can see all the users registered in the website in /flaws/admin. However, the only check for access for this site is if the username contains the word admin as seen on line [103](https://github.com/lossitomatossi/cyber-sec-project-1/blob/main/flaws/views.py#L103).

How to fix: If using our custom User models, add a identifier called "is_admin" that defaults to False, and when trying to access the site, instead of checking username the value of user.is_admin should be checked. Access control could also be made easier by adding a list of forbidden words so that users can not create a user called admin2 that could cause a mixup.

A better way would be to create custom permissions using Djangos custom permissions https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#custom-permissions. Then we could evoke user.has_perm("app.view_admin") and then direct the customer to the site only if this matches.

The best way would be to use Djangos builtin authentication, since they have already implemented user.is_superuser and user.is_staff. Then the value of these variables could be referenced when checking access.

FLAW 1: A1:2017-Injection

On flaws/admin/petsearch there is a search form that lets you search for pets with user_id that is compared in the database to the owner_id of a pet. There is zero validation on the input, so any command is acceptable. For example filling the form with "1 or 1=1" without the quotation marks will print out all pets in the database. Since the implementation lets a user fill in the end of a raw SQL-query, the same implementation against a different table could leak even more sensitive information.

How to fix: At a minimum add quotes around {id} in the query would force user input to be validated as text. Also all user input should be sanitized to remove potential SQL-injection vectors, which can be achieved by letting django modules handle the query as seen on [line 134](https://github.com/lossitomatossi/cyber-sec-project-1/blob/main/flaws/views.py#L134).