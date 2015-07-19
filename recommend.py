import descriptions

#Importance of being different in this respect

def a (x):
    print str(x)

def give_rating(profile, lang_to_rate):
    return sum([float(sum([lang_to_rate.get(key) != other.get(key) for key, val in lang_to_rate.iteritems() if key not in ["name", "description"]])) #List of booleans corresponding to differences
                * profile["skills"][other["name"]] #Weight rating by amount of usage of each language.
                / sum([rating for name, rating in profile["skills"].iteritems()]) # sum of ratings for average
                / len(lang_to_rate.keys()) # number of elements
                for other in [descriptions.evaluated_languages[nomen] for nomen, rate in profile["skills"].iteritems() if (nomen != lang_to_rate["name"] and rate != 0)]])


# constraints is a map formatted similarly to the programming language maps, e.g.
# {"compiled" : "y", "typing" : "d"} will filter for compiled languages with dynamic typing
def give_recommendations (profile, constraints={}):
    possible_langs = [lang for name, lang in descriptions.evaluated_languages.iteritems()
                      if (name not in profile["exceptions"]
                          and False not in [lang.get(key) == val for key, val in constraints.iteritems()])]
    return {lang["name"] : give_rating(profile, lang) for lang in possible_langs}


print give_recommendations({"name" : "flerpus", "skills" : {"python": 2, "java" : 4, "clojure" : 8}, "exceptions" : ["c", "haskell"]}, {"vm": "jvm"})
