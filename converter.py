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
  ?place wdt:P2046 ?results.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "de". }
}
'''

# query that checks for all axes among which a thing could be converted to saarland
# TODO: use named placeholders!
people_base_q = '''
SELECT ?population ?max_capacity
WHERE
{
  {
    VALUES ?place { wd:%s }
    ?place wdt:P1082 ?population.
  } UNION {
    VALUES ?place { wd:%s }
    ?place wdt:P1083 ?max_capacity.
  }
}
'''

object_name_q = '''SELECT * WHERE {
  wd:%s rdfs:label ?labelDe.
  FILTER(LANG(?labelDe) = "de").
}'''

saarland_q = "Q1201"

saarland_area   = 0 # in square kilometers
saarland_people = 0

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

'''
Get area properties with which a thing could be converted to saarland.
'''
def get_properties_area(object_q):
    query_url = api_base_url % urllib2.quote(area_base_q % (object_q))
    content = json.load(urllib2.urlopen(query_url))
    result = 0.0

    try:
        result = float(content["results"]["bindings"][0]["results"]["value"])
    except:
        # no result for area
        pass

    return result

def get_properties_people(object_q):
    query_url = api_base_url % urllib2.quote(people_base_q % (object_q, object_q))
    content = json.load(urllib2.urlopen(query_url))
    result = 0.0

    # probier stumpf unterschiedliche menschenmengenproperties durch bis eine passt
    try:
        # try population
        result = float(content["results"]["bindings"][0]["population"]["value"])
    except:
        # no result for population, try max_capacity
        try:
            result = float(content["results"]["bindings"][0]["max_capacity"]["value"])
        except:
            # no result for max_capacity
            pass

    return result

'''
Takes a wikidata Object (Q...) and converts it to Saarland
'''
def convert_to_saarland_area(thing):
    global saarland_area
    result = 0.0

    if (saarland_area == 0):
        # get the size of saarland and cache it
        saarland_area = get_properties_area(saarland_q)

    # get the size of the thing
    thing_q = thing # TODO: statt Q bekommen das Q eines gegebenen Wortes rausfinden!
    thing_area = get_properties_area(thing_q)

    if (thing_area > 0):
        result = thing_area / saarland_area

    result_precision = float("%0.4f" % result)
    return result_precision

def convert_to_saarland_people(thing):
    global saarland_people
    result = 0.0

    if (saarland_people == 0):
        # get the population of saarland and cache it
        saarland_people = get_properties_people(saarland_q)

    thing_q = thing # TODO: statt Q bekommen das Q eines gegebenen Wortes rausfinden!
    thing_people = get_properties_people(thing_q)

    if (thing_people > 0):
        result = thing_people / saarland_people

    result_precision = float("%0.4f" % result)
    return result_precision

if __name__ == "__main__":
    print get_object_name("Q3012")
    print "1 Ulm sind %s Saarland bzgl Flaeche" % convert_to_saarland_area("Q3012")
    print "1 Anfield sind %s Saarland bzgl Menschen" % convert_to_saarland_people("Q45671")


