# gives sorted movie recommendation by rating and name.
import json
import requests_with_caching


def get_movies_from_tastedive(mv):
    baseurl = "https://tastedive.com/api/similar"
    params_diction = {}
    params_diction["q"] = mv  # must be a comma separated string to work correctly
    params_diction["type"] = "movies"
    params_diction["limit"] = 5
    movie_resp = requests_with_caching.get(baseurl, params=params_diction)
    # Useful for debugging: print the url! Uncomment the below line to do so.
    print(movie_resp.url)  # Paste the result into the browser to check it out...
    return movie_resp.json()


def extract_movie_titles(movie):
    titles = []
    for q in movie["Similar"]["Results"]:
        titles.append(q["Name"])
    return titles


def get_related_titles(movies):
    lst = []
    for m in movies:
        results = extract_movie_titles(get_movies_from_tastedive(m))
        for name in results:
            if name not in lst:
                lst.append(name)
    return lst


def get_movie_data(title):
    baseurl = "http://www.omdbapi.com/"
    params_diction = {}
    params_diction["t"] = title  # must be a comma separated string to work correctly
    params_diction["r"] = "json"
    omdb_resp = requests_with_caching.get(baseurl, params=params_diction)
    # Useful for debugging: print the url! Uncomment the below line to do so.
    print(omdb_resp.url)  # Paste the result into the browser to check it out...
    print(omdb_resp.text)
    return omdb_resp.json()


def get_movie_data(title):
    baseurl = "http://www.omdbapi.com/"
    params_diction = {}
    params_diction["t"] = title  # must be a comma separated string to work correctly
    params_diction["r"] = "json"
    omdb_resp = requests_with_caching.get(baseurl, params=params_diction)
    # Useful for debugging: print the url! Uncomment the below line to do so.
    print(omdb_resp.url)  # Paste the result into the browser to check it out...
    return omdb_resp.json()


def get_movie_rating(t):
    score_int = 0
    for rating in t["Ratings"]:
        if rating["Source"] == "Rotten Tomatoes":
            score = rating["Value"]
            score_int = int(score.strip("%"))
            print(score_int)
    return score_int


def get_sorted_recommendations(mlist):
    suggestions = get_related_titles(mlist)
    print(suggestions)
    suggestions_sorted = sorted(
        suggestions,
        key=lambda title: (get_movie_rating(get_movie_data(title)), title),
        reverse=True,
    )
    return suggestions_sorted

#test
get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
