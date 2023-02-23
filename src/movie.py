"""
movie.py

Implements a dataclasses to represent a movie, a function to create a dictionary of movie objects, and
a few query and helper functions specific to movie dataclasses
"""

from dataclasses import dataclass

# Totals
current_count = 0

@dataclass
class Movie:
    titleType: str
    primaryTitle: str
    originalTitle: str
    startYear: int
    endYear: int
    runtimeMinutes: int
    genres: [str]

_VALUE_NONE  = "\\N"

def get_movies_from_file(movies_filename):
    """Returns a list of movies read from movies_filename"""
    global current_count
    
    # Initialize dict and file object
    movies = {}
    movies_file = open(movies_filename, "r", encoding = "utf-8")

    for line in movies_file.readlines()[1:]:
        values = line[:-1].split("\t") # Use [:-1] to ignore newline
        current_count += 1
        
        # Check isAdult first, ignore
        if int(values[4]) == 1:
            continue # Keep things R-rated here
        
        # Set sane defaults if values are absent
        # startYear
        if values[5] == _VALUE_NONE: 
            values[5] = "0"      

        # endYear
        if values[6] == _VALUE_NONE: 
            values[6] = "0"      
        
        # runtimeMinutes
        if values[7] == _VALUE_NONE: 
            values[7] = "0"
        
        # genres
        if values[8] == _VALUE_NONE: 
            values[8] = "None"
 
        tconst = int(values[0][2:])
        
        # Template: Movie(titleType, primaryTitle, originalTitle, \
        #   startYear, endYear, runtimeMinutes, \
        #   genres)
        movies[tconst] = Movie(values[1], values[2], values[3], \
            int(values[5]), int(values[6]), int(values[7]), \
            values[8].split(","))
                    
    movies_file.close()
    return movies

def contains(movies, titleType, words):
    """Returns a dictionary of movies that contain given *words* in their title"""
    ret = {}

    for tconst, movie in movies.items():
        for word in words:
            if movie.titleType == titleType and \
                word.lower() in movie.primaryTitle.lower():

                ret[tconst] = movie

    return ret

def in_year_and_genre(movies, titleType, year, genre):
    """Returns a dictionary of movies within a given year and genre"""
    ret = {}
    for tconst, movie in movies.items():
        if movie.titleType == titleType and \
            movie.startYear == year and \
            genre in movie.genres:

            ret[tconst] = movie

    return ret

def print_info(tconst, movie):
    """Neatly print information about a specific movie"""
    print("Identifier: tt{}, Title: {}, Type: {}, Year: {}, Runtime: {}, Genres: {}".format(str(tconst).zfill(6), movie.primaryTitle, movie.titleType, movie.endYear, movie.runtimeMinutes, ", ".join(movie.genres)))

def runtime(movies, titleType, minlen, maxlen):
    """Returns a dictionary of movies of titleType that fall between two given runtimes"""
    ret = {}

    for tconst, movie in movies.items():
        if movie.titleType == titleType and movie.runtimeMinutes > minlen \
            and movie.runtimeMinutes < maxlen:

            ret[tconst] = movie

    return ret
