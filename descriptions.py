core_languages = {"java": {imperative="y", typing="s", compiled="y", functional="n"}
                  "python": {imperative="y", typing="d", compiled="n", functional="n"}
                  "c": {imperative="y" typing="s", compiled="y", functional="n"}
                  "c++": {imperative="y" typing="s", compiled="y", functional="n"}
                  "c#": {imperative="y" typing="s" compiled="n", functional="n"}
                  "javascript": {imperative="y" typing="d", functional="n"}
                  "clojure": {imperative="y" typing="d", compiled="y", functional="y"}}

def add_lanague (languages name spec):
    languages[name] = spec
