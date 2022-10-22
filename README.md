# HIVE OS API 2.1 Intregration for Reporting

This code will run an Flask app to fetch worker stats via HIVE OS API, instead of manually trying to download this information through the intreface per farm per worker, which is not fun and is a waste of a precious human lifetime.

This is setup to fetch a two factor authenication (2FA) code from the user's registered email with HIVE OS.  This currently only works with Gmail account, but I have not tested it with other email providers.  You will also need to setup an app password through gmail and enable two-factor authenication (2FA) on your email account as well.  Go to Security > App Passwords for more info. 2FA must be enabled first.

How to install on a local computer:

install flask and requests, if not installed.
`install flask`
`pip install flask flask_caching requests`
 
move to the virtual enivorment folder:
`cd satlee_rpts`

declare virtual environment:
 `pip install virtualenv`

activate virtual environment:
 `python -m venv saltee_rpts`




