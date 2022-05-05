# Shorten-O-Matic

flask webservice that shortens urls similar to TinyURL and bit.ly

# License

MIT license

# Setup

setup and create virtual environment

	pip install virtualenv
	virtualenv shorten_o_matic

activate (unix):

	source shorten_o_matic/bin/activate

activate (windows):

	shorten_o_matic\Scripts\activate.bat

install dependencies:

	pip install -r requirements.txt

## Configuring

configure flask (unix):

	export FLASK_APP='project.app:create_app()'

configure flask (windows):

	set FLASK_APP=project.app:create_app()


## Run service

	flask run

## Run unit tests

	pytest

# Future work

no persistent storage used, so a database setup would be nice. pickle can be used as a poor man's version before setting up a proper database.
also, unit testing could be more extensive

* persistent storage
* more extensive unit testing
