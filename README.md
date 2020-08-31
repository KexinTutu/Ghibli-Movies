Ghibli Movie List
=================
Show plain list of all movies of Studio Ghibli.

Dependencies
-------
First, make sure docker and docker-compose are available on your local machine.

Docker >= 17.05

Docker-Compose >= 1.13

Installation
------------
Quick setup, run from the `GhibliMovies` directory:

```sh
docker-compose build
docker-compose up -d
```
localhost:8000/movies

Usage
-----

Test

```sh
docker-compose run web python manage.py test
```

Comment
-------
I created a field called 'new_people' for each movie to include all the people appeared in a movie, in this way we don't lose the original 'people' field information on movie.