# HIVE OS API 2.1 Intregration for Farm and Worker Statistics Reporting

This will run an Flask app to fetch worker stats via HIVE OS API v2.1, instead of manually trying to download this information through the intreface per farm per worker, which is not fun and is a waste of a precious human time.

This is setup to fetch a two factor authenication (2FA) code from the user's registered email with HIVE OS.  This currently only works with Gmail account, but I have not tested it with other email providers.  You will also need to setup an app password through gmail and enable two-factor authenication (2FA) on your email account as well.  Go to Security > App Passwords for more info. 2FA must be enabled first.

<b>How to install on a local computer:</b>

 Install Flask and requests package:

 `install flask`

 `pip install flask flask_caching requests`

 Move to the Virtual Environment Folder:

 `cd saltee_rpts`

 Declare virtual environment:

  `pip install virtualenv`

 Activate virtual environment:

  `python -m venv saltee_rpts`




