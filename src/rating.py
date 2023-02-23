"""
rating.py

Implements a dataclasses to represent a rating for a movie, a function to create a 
dictionary of rating objects, and a few query and helper functions specific to rating dataclasses
"""

from dataclasses import dataclass

# Totals
current_count = 0

@dataclass
class Rating:
    averageRating: float
    numVotes: int

def get_ratings_from_file(ratings_filename):
    """Create a dictionary of ratings from ratings_filename"""
    global current_count
    
    current_count = 0

    # Initialize dict and file object
    ratings = {}
    ratings_file = open(ratings_filename, "r", encoding = "utf-8")

    for line in ratings_file.readlines()[1:]:
        values = line[:-1].split("\t") # Use [:-1] to ignore newline
        current_count += 1
        
        tconst = int(values[0][2:])
        
        # Template: Rating()
        ratings[tconst] = Rating(float(values[1]), int(values[2]))
                    
    ratings_file.close()
    return ratings

def print_info(tconst, rating):
    """Neatly print information about a given rating for a movie"""
    print("Identifier: tt{}, Rating: {}, Votes: {}".format(str(tconst).zfill(6), rating.averageRating, rating.numVotes))

def _ratings_partition_avg(ratings, pivot):
    """Partition ratings based on averageRating, used for quick_select_avg"""
    less, equal, greater = {}, {}, {}
    for tconst, rating in ratings.items():
        if rating.averageRating < pivot.averageRating:
            less[tconst] = rating
        elif rating.averageRating > pivot.averageRating:
            greater[tconst] = rating
        else:
            equal[tconst] = rating
    return less, equal, greater

def quick_select_avg(ratings, k):
    """Select nth rating by average"""
    pivot = list(ratings.values())[0]
    pivot_tconst = list(ratings.keys())[0]
    less, equal, greater = _ratings_partition_avg(ratings, pivot)
    
    l_size = len(less)
    e_size = len(equal)

    if l_size <= k and l_size + e_size > k:
        return pivot_tconst, pivot

    elif l_size > k:
        return quick_select_avg(less, k)

    else:
        return quick_select_avg(greater, k - l_size - e_size)


def _ratings_partition_votes(ratings, pivot):
    """Partition ratings based on numVotes, used for quick_select_votes"""
    less, equal, greater = {}, {}, {}
    for tconst, rating in ratings.items():
        if rating.numVotes < pivot.numVotes:
            less[tconst] = rating
        elif rating.numVotes > pivot.numVotes:
            greater[tconst] = rating
        else:
            equal[tconst] = rating
    return less, equal, greater

def quick_select_votes(ratings, k):
    """Select nth rating by number of votes"""
    pivot = list(ratings.values())[0]
    pivot_tconst = list(ratings.keys())[0]
    less, equal, greater = _ratings_partition_votes(ratings, pivot)
    
    l_size = len(less)
    e_size = len(equal)

    if l_size <= k and l_size + e_size > k:
        return pivot_tconst, pivot

    elif l_size > k:
        return quick_select_votes(less, k)

    else:
        return quick_select_votes(greater, k - l_size - e_size)

