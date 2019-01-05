# Pug or Ugh API

This is the eleventh project in the Treehouse Python tech degree.

Hosted on [Heroku](https://pug-or-ugh.herokuapp.com). To view locally clone the repo, download the requirements with `pip
install requirements.txt` and run `python manage.py`.

## Description

Paw left or right in this app to find the dog of your dreams! You can filter dogs by liked, disliked, or undecided as 
well as various attributes.

The frontend of the app is powered by React which communicates with an open api backend.

## API Routes

To communicate with the backend api, please see the following routes.

* To view a full list of available dogs

	* `/api/dog/<pk>/liked/`
	
* To view a list of dogs by status (liked/disliked/undecided)

	* `/api/dogs/liked/`
	* `/api/dogs/disliked/`
	* `/api/dogs/undecided/`

* To get the next dog by status (liked/disliked/undecided)

	* `/api/dog/<pk>/liked/next/`
	* `/api/dog/<pk>/disliked/next/`
	* `/api/dog/<pk>/undecided/next/`

* To change the dog's status

	* `/api/dog/<pk>/liked/`
	* `/api/dog/<pk>/disliked/`
	* `/api/dog/<pk>/undecided/`

* To change or set user preferences

	* `/api/user/preferences/`
