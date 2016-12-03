import urllib2
from bottle import route, run, template, request
from converter import convert_to_saarland_area

# for debugging only! **********************************************************
#from bottle import run
#run(reloader=True)
# ******************************************************************************

population_q = ("wdt:P1082", "population")

api_base_url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=%s&format=json"

saarland_base_q = '''SELECT ?population
WHERE
{
  VALUES ?bundesland { wd:Q1201 }
  ?bundesland wdt:P1082 ?population.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "de". }
}
'''

@route('/')
@route('/new/<thing>', method='GET')
def calc_saarland(thing=""):

    if request.GET.convert:
        # input has been entered: look up ALL the things! \o,

        # get the thing we want to measure in saarlands
        compare_to = request.GET.thing.strip()

        print "received request for %s, converting to Saarland" % compare_to
        if (compare_to):
            result = convert_to_saarland_area(compare_to)
            print "received result %s, updating website..." % result
            # todo: append things to current template? geht das?

    return template('template')

run(host='0.0.0.0', port=8080, debug=False)
