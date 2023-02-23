import sys, time
import rating, movie

def print_movie_results(movies):
    for tconst, m in movies.items():
        print("\t", end="")
        movie.print_info(tconst, m)

def query_contains(movies, titleType, words):
    timer_start()
    contains = movie.contains(movies, titleType, words)

    if len(contains) < 1:
        print("\tNo match found!")

    else:
        print_movie_results(contains)
        
    timer_finish()

def query_lookup(movies, ratings, tconst):
    tconst = int(tconst[2:])

    if not tconst in movies.keys() and tconst not in ratings.keys():
        print("\tNo match found!")

    else:
        print("\tMOVIE:", end=" ")
        movie.print_info(tconst, movies[tconst])
        print("\tRATING:", end=" ")
        rating.print_info(tconst, ratings[tconst])

def query_runtime(movies, titleType, minlen, maxlen):
    timer_start()
    timely = movie.runtime(movies, titleType, int(minlen), int(maxlen))
    
    if len(timely) < 1:
        print("\tNo match found!")

    else:
        print_movie_results(timely)

    timer_finish()

def query_year_and_genre(movies, titleType, year, genre):
    timer_start()
    relevant = movie.in_year_and_genre(movies, titleType, int(year), genre)
    
    if len(relevant) < 1:
        print("\tNo match found!")

    else:
        print_movie_results(relevant)

    timer_finish()



global_timer = 0

def timer_start():
    global global_timer

    global_timer = time.time()

def timer_finish():
    global global_timer

    print("elapsed time (s):", time.time() - global_timer)
    global_timer = 0

SMALL_MOVIES_FILE = "data/small.basics.tsv"
LARGE_MOVIES_FILE = "data/title.basics.tsv"

SMALL_RATINGS_FILE = "data/small.ratings.tsv"
LARGE_RATINGS_FILE = "data/title.ratings.tsv"

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "small":
        movies_file = SMALL_MOVIES_FILE
        ratings_file = SMALL_RATINGS_FILE
    
    else:
        movies_file = LARGE_MOVIES_FILE
        ratings_file = LARGE_RATINGS_FILE
 
    timer_start()
    
    print("reading {}...".format(movies_file))
    movies = movie.get_movies_from_file(movies_file)

    timer_finish()
    timer_start()

    print("reading {}...".format(ratings_file))
    ratings = rating.get_ratings_from_file(ratings_file)
    
    timer_finish()

    for line in sys.stdin:
        print("Processing:", line.strip("\n"))
        tokens = line.strip("\n").split(" ")

        if tokens[0] == "CONTAINS":
            query_contains(movies, tokens[1], tokens[2:])

        elif tokens[0] == "LOOKUP":
            query_lookup(movies, ratings, tokens[1])

        elif tokens[0] == "RUNTIME":
            query_runtime(movies, tokens[1], tokens[2], tokens[3])

        elif tokens[0] == "YEAR_AND_GENRE":
            query_year_and_genre(movies, tokens[1], tokens[2], tokens[3])

        print()
            
if __name__ == '__main__':
    main()
