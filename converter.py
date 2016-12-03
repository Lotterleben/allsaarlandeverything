import urllib2
import json
from bottle import route, run, template, request

'''
TODO:
    * bei Bedarf einheiten umrechnen!
    * statt Q bekommen das Q eines gegebenen Wortes rausfinden!
    * proper error handling
'''

api_base_url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=%s&format=json"
area_base_q = '''SELECT ?results
WHERE
{
  VALUES ?place { wd:%s }
  ?place %s ?results.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "de". }
}
'''
object_name_q = '''SELECT * WHERE {
  wd:%s rdfs:label ?labelDe.
  FILTER(LANG(?labelDe) = "de").
}'''

saarland_q = "Q1201"

population_p = "wdt:P1082"
area_p       = "wdt:P2046"

saarland_area = 0 # in square kilometers


'''
Get the human-readable name of a Q object (in german)
'''
def get_object_name(object_q):
    query_url = api_base_url % urllib2.quote(object_name_q % object_q)
    content = json.load(urllib2.urlopen(query_url))

    try:
        return content["results"]["bindings"][0]["labelDe"]["value"]
    except:
        print("ERROR: couldn't get name for object %s" % object_q)


def get_property(object_q, prop):
    query_url = api_base_url % urllib2.quote(area_base_q % (object_q, prop))
    content = json.load(urllib2.urlopen(query_url))
    try:
        return content["results"]["bindings"][0]["results"]["value"]
    except:
        print("ERROR: couldn't get property %s for object %s" % (prop, object))

'''
Takes a wikidata Object (Q...) and converts it to Saarland
'''
def convert_to_saarland_area(thing):
    global saarland_area

    if (saarland_area == 0):
        # get the size of saarland and cache it
        saarland_area = float(get_property(saarland_q, area_p))

    # get the size of the thing
    thing_q = thing # TODO: statt Q bekommen das Q eines gegebenen Wortes rausfinden!
    thing_area = float(get_property(thing_q, area_p))

    result = thing_area / saarland_area
    result_precision = float("%0.4f" % result)
    return result_precision

if __name__ == "__main__":
    print get_object_name("Q3012")
    print "1 Ulm sind %s Saarland" % convert_to_saarland_area("Q3012")


