# dashboard
Django App for Whittier Scholars Program

# about
The [Whittier Scholars Program](https://www.whittier.edu/academics/whittierscholars/about) offers students an alternative curricular path for a liberal arts education at Whittier College.
Each student designs their own course of study at [Whittier College](https://www.whittier.edu).
This app is designed to help students manage their curricular path, and to help the Whittier Scholars Council to advise students in the program.

The app was previously branded as Poetfolio (Poets + Portfolio; the nickname for Whittier College students is "The Poets" and the mascot is Johnny Poet).
While perhaps a clever name, it proved too confusing in practice and so the app has been rebranded as Dashboard.
However, the codebase is filled with references to the old branding and those references are likely to persist.

The app is in active development.

# setup
The `requirements.txt` file was created with `pip freeze`, so any new deployment can use `pip install -r requirements.txt` to install the dependencies to the appropriate virtual environment.
In addition, a number of environment variables will need to be set. They are as follows:
  * `POETFOLIO_SECRET_KEY` - a randomly generated value for the `SECRET_KEY` used in `poetfolio/settings.py`
  * `POETFOLIO_PRODUCTION` - set to any truthy value to set `DEBUG` to `False`; if the variable does not exist, `DEBUG` is set to `True`
  * `POETFOLIO_DB_NAME` - Django MySQL database name; defaults to `'poetfolio_dev'`
  * `POETFOLIO_DB_USER` - Django MySQL database user; defaults to `'poetfolio'`
  * `POETFOLIO_DB_PASSWORD` - Django MySQL database password; defaults to `'devdevdev'` so don't use that
  * `POETFOLIO_STATIC` - full path for `STATIC_ROOT`; defaults to `'/home/{yourusername}/static'`
  * `POETFOLIO_MEDIA` - full path for `MEDIA_ROOT`; defaults to `'/home/{yourusername}/media'`
  * `POETFOLIO_EMAIL_HOST` - URL string for SMTP email server; port hard coded to `587`
  * `POETFOLIO_EMAIL_USER` - login for SMTP email server
  * `POETFOLIO_EMAIL_PASSWORD` - password for SMTP email server; it's suggested to use a unique app password if possible

Other variables in `poetfolio/settings.py` are hardcoded with values that make sense for Whittier College (like `LANGUAGE_CODE = 'en-us'` and `TIME_ZONE = 'America/Los_Angeles'`, etc.).

Otherwise, see [https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/](https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/)

# credits
A great deal of work on this project was done by two Whittier Scholars Program students: Aaron Dodds ('19) and [Noah Wilson ('21)](https://noahwilson.tech/).
