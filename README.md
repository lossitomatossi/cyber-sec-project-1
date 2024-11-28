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
9	admin	admin	admin
10  user	user	user
11	fakeadmin	admin	23b6d73505d5f2937caa4ff367cf194a1ed45137079b4aef5610d701bf57db95

The admin panel is open in /admin with the username admin and password admin.

Both the admin and the user have pets associated to the accounts. The relevant pages are /flaws/id/pets

FLAW : A3:2017-Sensitive Data Exposure

Source: [flaws/models.py](flaws\models.py)
The flaw is that passwords are stored in plaintext, which violates the Sensitive Data Exposure by not protecting the data at rest or in transit.

How to fix: Instead of creating a user as a basic model, we can use "AbstractUser" from "django.contrib.auth.models" as seen on [line XXX](github.com) or to create a hashing function ourselves as seen on [line YYY](github.com). We should also hash the password before submitting it either manually or with djangos "from django.contrib.auth.hashers import make_password". When comparing the submitted password to the one in the database, we should compare the hash values to each other, with for example "check_password" from the same django module.

FLAW: A2:2017-Broken Authentication
We are persisting user session as a plaintext value in the database and storing it for the user as cookie called "session_token" in their browser. If a user finds out the session_token of another user, they can impersonate that user. The user can also change this cookie value as they wish in their browser, and the cookie only expires clientside, not server side.

How to fix: Use djangos authenticate and login functions to abstract session management and login functionality. This also makes sure that the cookie expiration is applied serverside and not only on the clients browser, which prompts the user to login later on.


FLAW A6:2017-Security Misconfiguration:

Since the website was created with django, there is an admin panel that was not disabled. The admin panel can be accessed by anyone with access to the website, and since the admin uses these as their credentials:
username: admin
email: admin@example.com
password: admin

It is reasonable that a user would attempt to login as "admin; admin", in which case they would get access to everything.

How to fix: Firstly, never use a superuser account such as admin with the password admin. At minimum, the password should be a randomly generated one, and preferrably tied to some central authentication backend. Also, for a live server, we would disable the django admin backend from (mysite\urls.py) or at least limit access to it behind a firewall. We should not document the admin credentials in plaintext in the README.md either...

A5:2017-Broken Access Control

We have created a functionality where an admin can see all the users registered in the website in /flaws/admin. However, the only check for access for this site is if the username contains the word admin as seen on line [](github.com).

How to fix: If using our custom User models, add a identifier called "is_admin" that defaults to False, and when trying to access the site, instead of checking username the value of user.is_admin should be checked. Access control could also be made easier by adding a list of forbidden words so that users can not create a user called admin2 that could cause a mixup.

A better way would be to create custom permissions using Djangos custom permissions https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#custom-permissions. Then we could evoke user.has_perm("app.view_admin") and then direct the customer to the site only if this matches.

The best way would be to use Djangos builtin authentication, since they have already implemented user.is_superuser and user.is_staff. Then the value of these variables could be referenced when checking access.

FLAW 1: A1:2017-Injection

On flaws/admin/petsearch there is a search form that lets you search for pets with user_id that is compared in the database to the owner_id of a pet. There is zero validation on the input, so any command is acceptable. For example filling the form with "1 or 1=1" without the quotation marks will print out all pets in the database. Since the implementation lets a user fill in the end of a raw SQL-query, the same implementation against a different table could leak even more sensitive information.

How to fix: At a minimum add quotes around {id} in the query would force user input to be validated as text. Also all user input should be sanitized to remove potential SQL-injection vectors, which can be achieved by letting django modules handle the query as seen on line 138.