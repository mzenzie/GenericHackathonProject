core_languages = [dict(name="java", imperative="y", typing="s", compiled="y", functional="n"),
                  dict(name="python", imperative="y", typing="d", compiled="n", functional="n"),
                  dict(name="c", imperative="y", typing="s", compiled="y", functional="n"),
                  dict(name="c++", imperative="y", typing="s", compiled="y", functional="n"),
                  dict(name="c#", imperative="y", typing="s", compiled="n", functional="n"),
                  dict(name="javascript", imperative="y", typing="d", functional="n"),
                  dict(name="clojure", imperative="y", typing="d", compiled="y", functional="y")]

def add_lanague (languages, new_lang):
    languages.append(new_lang)
