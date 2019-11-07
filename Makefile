run-movies: clark.movies
	./main.py < clark.movies

run-shows: clark.shows
	./main.py < clark.shows

clark.movies:
	ssh clark find /home/media/movies -type f -exec stat --format=\'%W %s\' {} '\;' > clark.movies

clark.shows:
	ssh clark find /home/media/shows -type f -exec stat --format=\'%W %s\' {} '\;' > clark.shows

clean:
	rm clark.{movies,shows}
